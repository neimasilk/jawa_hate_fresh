"""Pilot #6 — smoke test model lokal (Ollama) sbg pengganti Grok.

Uji cepat di ~12 teks yang SUDAH punya label cloud (Grok filter + deepseek/grok
hate v2), untuk 2 tugas:
  1. FILTER bahasa (jawa/campuran/indonesia/lainnya) — vs label Grok Pilot #2
  2. KLASIFIKASI hate prompt v2 — vs label deepseek+grok Pilot #3

Metrik per model: JSON valid %, latency, agreement filter, agreement hate,
contoh output (cek kualitas Jawa kualitatif).

Pemakaian:
  $env:SMOKE_MODELS="aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m,qwen3:14b"
  .venv\Scripts\python experiments\pilot06_local_models\smoke_test.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.cultural_prompt import (  # noqa: E402
    load_prompt_template,
    parse_llm_output,
    render_user_prompt,
)
from src.llm_clients import call_ollama  # noqa: E402

HOT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
V2_PATH = ROOT / "experiments" / "pilot03_cultural_prompt" / "outputs" / "responses_v2.jsonl"
FILTER_PROMPT = ROOT / "prompts" / "jawa_filter_v0.md"
CLASSIFY_PROMPT = ROOT / "prompts" / "cultural_classification_v2.md"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

N_SMOKE = 12
MODELS = os.environ.get(
    "SMOKE_MODELS",
    "aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m,qwen3:14b",
).split(",")
# Qwen3 / SEA-LION-R = reasoning model (thinking ON default → lambat).
# "/no_think" = soft switch Qwen3 untuk matikan thinking (cocok utk filter
# high-volume yang tak butuh reasoning). Set SMOKE_NO_THINK=1.
NO_THINK = os.environ.get("SMOKE_NO_THINK") == "1"
THINK_TAG = "\n\n/no_think" if NO_THINK else ""


def load_cloud_labels() -> list[dict]:
    """Ambil N_SMOKE teks dgn label cloud: filter bahasa (Grok) + hate (ds/grok)."""
    # filter bahasa + orig dari hot subset
    hot = {}
    with HOT_PATH.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            hot[r["source_id"]] = {
                "source_id": r["source_id"],
                "text": r["text"],
                "orig_label": r.get("orig_label"),
                "grok_bahasa": (r.get("parsed") or {}).get("bahasa"),
            }
    # hate label v2 per vendor
    hate = {}
    with V2_PATH.open(encoding="utf-8-sig") as f:
        for line in f:
            r = json.loads(line)
            p = r.get("parsed") or {}
            if "_parse_error" in p or r.get("error"):
                continue
            hate.setdefault(r["source_id"], {})[r["vendor"]] = bool(p.get("hate"))
    rows = []
    for sid, h in hate.items():
        if sid in hot and "deepseek" in h and "grok" in h:
            row = dict(hot[sid])
            row["ds_hate"] = h["deepseek"]
            row["grok_hate"] = h["grok"]
            rows.append(row)
    rows.sort(key=lambda r: r["source_id"])
    # ambil campuran hate & non-hate untuk variasi
    return rows[:N_SMOKE]


def run_model(model: str, rows: list[dict]) -> dict:
    f_sys, f_tpl = load_prompt_template(FILTER_PROMPT)
    c_sys, c_tpl = load_prompt_template(CLASSIFY_PROMPT)
    log_path = OUT_DIR / f"smoke_{model.replace('/', '_').replace(':', '_')}.jsonl"

    n_filter_valid = n_filter_agree = 0
    n_hate_valid = n_hate_agree_ds = n_hate_agree_grok = 0
    latencies = []
    samples = []

    with log_path.open("w", encoding="utf-8") as lf:
        for row in rows:
            # --- FILTER ---
            fr = call_ollama(f_sys + THINK_TAG, render_user_prompt(f_tpl, row["text"]), model=model)
            fp = parse_llm_output(fr.raw_text)
            f_valid = "_parse_error" not in fp and not fr.error
            if f_valid:
                n_filter_valid += 1
                # strict: bahasa sama persis; practical: sama-sama keep (jawa/campuran)
                keep = {"jawa", "campuran"}
                if fp.get("bahasa") == row["grok_bahasa"] or (
                    fp.get("bahasa") in keep and row["grok_bahasa"] in keep
                ):
                    n_filter_agree += 1
            # --- CLASSIFY hate v2 ---
            cr = call_ollama(c_sys + THINK_TAG, render_user_prompt(c_tpl, row["text"]), model=model)
            cp = parse_llm_output(cr.raw_text)
            c_valid = "_parse_error" not in cp and not cr.error
            local_hate = None
            if c_valid:
                n_hate_valid += 1
                local_hate = bool(cp.get("hate"))
                if local_hate == row["ds_hate"]:
                    n_hate_agree_ds += 1
                if local_hate == row["grok_hate"]:
                    n_hate_agree_grok += 1
            latencies.append((fr.latency_ms + cr.latency_ms) / 2)
            rec = {
                "source_id": row["source_id"], "text": row["text"],
                "grok_bahasa": row["grok_bahasa"], "local_bahasa": fp.get("bahasa") if f_valid else None,
                "ds_hate": row["ds_hate"], "grok_hate": row["grok_hate"], "local_hate": local_hate,
                "local_severity": cp.get("severity") if c_valid else None,
                "local_target": cp.get("target_group") if c_valid else None,
                "filter_raw": fr.raw_text[:300], "classify_raw": cr.raw_text[:400],
                "filter_err": fr.error, "classify_err": cr.error,
            }
            lf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            samples.append(rec)

    n = len(rows)
    return {
        "model": model, "n": n,
        "filter_valid_pct": n_filter_valid / n * 100,
        "filter_agree_pct": (n_filter_agree / n_filter_valid * 100) if n_filter_valid else 0,
        "hate_valid_pct": n_hate_valid / n * 100,
        "hate_agree_ds_pct": (n_hate_agree_ds / n_hate_valid * 100) if n_hate_valid else 0,
        "hate_agree_grok_pct": (n_hate_agree_grok / n_hate_valid * 100) if n_hate_valid else 0,
        "latency_mean_ms": sum(latencies) / len(latencies) if latencies else 0,
        "samples": samples,
    }


def main() -> None:
    rows = load_cloud_labels()
    print(f"Smoke test {len(rows)} teks | models: {', '.join(MODELS)}\n", flush=True)
    results = []
    for model in MODELS:
        print(f"=== {model} ===", flush=True)
        res = run_model(model.strip(), rows)
        results.append(res)
        print(f"  filter valid {res['filter_valid_pct']:.0f}% | agree vs Grok {res['filter_agree_pct']:.0f}%", flush=True)
        print(f"  hate valid {res['hate_valid_pct']:.0f}% | agree vs ds {res['hate_agree_ds_pct']:.0f}% | vs grok {res['hate_agree_grok_pct']:.0f}%", flush=True)
        print(f"  latency mean {res['latency_mean_ms']:.0f}ms\n", flush=True)

    # tulis ringkasan
    summary = OUT_DIR / "smoke_summary.md"
    L = ["# Pilot #6 — Smoke Test Model Lokal", "",
         f"Pool: {len(rows)} teks (label cloud: Grok filter + deepseek/grok hate v2).", "",
         "| Model | Filter valid | Filter agree vs Grok | Hate valid | Hate agree vs ds | vs grok | Latency |",
         "|---|---|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['model']} | {r['filter_valid_pct']:.0f}% | {r['filter_agree_pct']:.0f}% | "
                 f"{r['hate_valid_pct']:.0f}% | {r['hate_agree_ds_pct']:.0f}% | {r['hate_agree_grok_pct']:.0f}% | "
                 f"{r['latency_mean_ms']:.0f}ms |")
    L += ["", "## Contoh output (kualitatif — cek kualitas Jawa)", ""]
    for r in results:
        L.append(f"### {r['model']}")
        for s in r["samples"][:4]:
            L.append(f"- `{s['source_id']}` bahasa: Grok={s['grok_bahasa']} / lokal={s['local_bahasa']} | "
                     f"hate: ds={s['ds_hate']} grok={s['grok_hate']} lokal={s['local_hate']} (sev={s['local_severity']})")
            L.append(f"  > {s['text'][:120]}")
            if s["classify_err"]:
                L.append(f"  ERR: {s['classify_err'][:120]}")
        L.append("")
    summary.write_text("\n".join(L), encoding="utf-8")
    print(f"Ringkasan: {summary}", flush=True)


if __name__ == "__main__":
    main()
