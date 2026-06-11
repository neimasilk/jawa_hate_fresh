"""Pilot #6b — validasi model LOKAL untuk tugas FILTER (sebelum commit run ~8K).

Smoke test filter cuma n=12 (keep-agree 67-75%) — terlalu tipis untuk memutuskan
run 8.352 teks (~satu malam GPU). Validasi di sampel stratified dari teks yang
SUDAH difilter Grok (Pilot #2/#5): 150 keep (jawa/campuran) + 150 drop
(indonesia/lainnya), seed tetap.

Metrik kunci per model lokal (vs label Grok sebagai referensi):
  - keep-recall: dari grok-keep, berapa % lokal juga keep (false negative = pool hilang)
  - drop-agreement: dari grok-drop, berapa % lokal juga drop (false positive = pool kotor;
    mitigasi: semua keep lokal nanti diverifikasi Grok murah)
  - JSON valid %, latency

Pemakaian:
  $env:VALIDATE_MODELS="aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m,qwen3:14b"
  .venv\Scripts\python experiments\pilot06_local_models\run_filter_validation.py
"""
from __future__ import annotations

import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt  # noqa: E402
from src.llm_clients import call_ollama  # noqa: E402

MODELS = [
    m.strip()
    for m in os.environ.get(
        "VALIDATE_MODELS", "aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m,qwen3:14b"
    ).split(",")
    if m.strip()
]
NO_THINK = os.environ.get("LOCAL_NO_THINK", "1") == "1"
THINK_TAG = "\n\n/no_think" if NO_THINK else ""
N_KEEP = 150
N_DROP = 150
SEED = 42
KEEP_CATS = {"jawa", "campuran"}

FILTER_LOG = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "pilot02_responses.jsonl"
PROMPT_PATH = ROOT / "prompts" / "jawa_filter_v0.md"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
SUMMARY_PATH = OUT_DIR / "filter_validation_summary.md"


def load_grok_labeled() -> list[dict]:
    latest: dict[str, dict] = {}
    with FILTER_LOG.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            latest[rec["source_id"]] = rec
    out = []
    for rec in latest.values():
        p = rec.get("parsed") or {}
        if "_parse_error" in p or rec.get("error") or p.get("bahasa") is None:
            continue
        out.append({"source_id": rec["source_id"], "text": rec["text"], "grok_bahasa": p["bahasa"]})
    return out


def stratified_sample(rows: list[dict]) -> list[dict]:
    keeps = sorted((r for r in rows if r["grok_bahasa"] in KEEP_CATS), key=lambda r: r["source_id"])
    drops = sorted((r for r in rows if r["grok_bahasa"] not in KEEP_CATS), key=lambda r: r["source_id"])
    rng = random.Random(SEED)
    sample = rng.sample(keeps, min(N_KEEP, len(keeps))) + rng.sample(drops, min(N_DROP, len(drops)))
    rng.shuffle(sample)
    return sample


def already_done(path: Path) -> set[str]:
    done = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    if (r.get("raw_text") or "").strip() and not r.get("error"):
                        done.add(r["source_id"])
                except json.JSONDecodeError:
                    continue
    return done


def run_model(model: str, sample: list[dict], system: str, user_tpl: str) -> Path:
    out_path = OUT_DIR / f"filter_val_{model.replace('/', '_').replace(':', '_')}.jsonl"
    done = already_done(out_path)
    with out_path.open("a", encoding="utf-8") as f:
        for row in tqdm(sample, desc=f"filter-val {model}"):
            if row["source_id"] in done:
                continue
            resp = call_ollama(system + THINK_TAG, render_user_prompt(user_tpl, row["text"]), model=model)
            parsed = parse_llm_output(resp.raw_text)
            rec = {
                "source_id": row["source_id"], "text": row["text"], "grok_bahasa": row["grok_bahasa"],
                "vendor": resp.vendor, "model": resp.model, "raw_text": resp.raw_text, "parsed": parsed,
                "latency_ms": resp.latency_ms, "error": resp.error,
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
    return out_path


def score(out_path: Path) -> dict:
    recs = {}
    with out_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            recs[r["source_id"]] = r
    n = len(recs)
    valid = [r for r in recs.values() if not r.get("error") and "_parse_error" not in (r.get("parsed") or {})
             and (r.get("parsed") or {}).get("bahasa") is not None]
    keep_hit = keep_tot = drop_hit = drop_tot = 0
    for r in valid:
        grok_keep = r["grok_bahasa"] in KEEP_CATS
        local_keep = r["parsed"]["bahasa"] in KEEP_CATS
        if grok_keep:
            keep_tot += 1
            keep_hit += local_keep
        else:
            drop_tot += 1
            drop_hit += not local_keep
    lat = sorted(r["latency_ms"] for r in valid)
    return {
        "n": n, "valid": len(valid),
        "keep_recall": keep_hit / keep_tot if keep_tot else float("nan"), "keep_tot": keep_tot,
        "drop_agree": drop_hit / drop_tot if drop_tot else float("nan"), "drop_tot": drop_tot,
        "latency_med_s": (lat[len(lat) // 2] / 1000) if lat else float("nan"),
    }


def main() -> None:
    rows = load_grok_labeled()
    sample = stratified_sample(rows)
    n_keep = sum(1 for r in sample if r["grok_bahasa"] in KEEP_CATS)
    print(f"Sampel validasi: {len(sample)} ({n_keep} keep + {len(sample) - n_keep} drop) dari {len(rows)} grok-labeled", flush=True)
    system, user_tpl = load_prompt_template(PROMPT_PATH)

    L = ["# Pilot #6b — Validasi filter lokal vs Grok", "",
         f"Sampel stratified n={len(sample)} ({n_keep} keep / {len(sample) - n_keep} drop), seed {SEED}. no_think={NO_THINK}.", "",
         "| Model | JSON valid | keep-recall | drop-agree | latency med |",
         "|---|---|---|---|---|"]
    for model in MODELS:
        out_path = run_model(model, sample, system, user_tpl)
        s = score(out_path)
        line = (f"| {model} | {s['valid']}/{s['n']} | {s['keep_recall']*100:.0f}% (n={s['keep_tot']}) "
                f"| {s['drop_agree']*100:.0f}% (n={s['drop_tot']}) | {s['latency_med_s']:.1f}s |")
        L.append(line)
        print(line, flush=True)

    L += ["", "**Interpretasi:** keep-recall rendah = pool hilang (false negative, tidak terpulihkan); "
          "drop-agree rendah = pool kotor (false positive, termitigasi verifikasi Grok murah di tahap keep). "
          "Pilih model dengan keep-recall tertinggi; latency tie-breaker."]
    SUMMARY_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nSummary -> {SUMMARY_PATH}", flush=True)


if __name__ == "__main__":
    main()
