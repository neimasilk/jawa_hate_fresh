"""Pilot #6 — validasi: bisakah model LOKAL gantikan Grok di consensus?

Jalankan model lokal (Ollama) dengan prompt v2 di 149 pool yang SAMA dengan
Pilot #3, lalu hitung Krippendorff alpha(deepseek, lokal) — pakai ulang label
deepseek v2 yang sudah ada. Target: alpha mendekati 0.763 (deepseek+grok) →
deepseek(cloud murah)+lokal(gratis) = consensus tanpa ketergantungan xAI.

Pemakaian:
  $env:LOCAL_MODEL="qwen3:14b"; $env:LOCAL_NO_THINK="1"
  .venv\Scripts\python experiments\pilot06_local_models\run_local_consensus.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.agreement import bootstrap_alpha_ci, is_refusal, is_valid_json, krippendorff_alpha_nominal  # noqa: E402
from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt  # noqa: E402
from src.llm_clients import call_ollama  # noqa: E402

MODEL = os.environ.get("LOCAL_MODEL", "qwen3:14b")
NO_THINK = os.environ.get("LOCAL_NO_THINK") == "1"
THINK_TAG = "\n\n/no_think" if NO_THINK else ""

V2_PROMPT = ROOT / "prompts" / "cultural_classification_v2.md"
DS_LABELS = ROOT / "experiments" / "pilot03_cultural_prompt" / "outputs" / "responses_v2.jsonl"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / f"local_v2_{MODEL.replace('/', '_').replace(':', '_')}.jsonl"


def load_deepseek_v2() -> dict[str, bool]:
    """source_id -> deepseek hate label (v2, valid only)."""
    out = {}
    with DS_LABELS.open(encoding="utf-8-sig") as f:
        for line in f:
            r = json.loads(line)
            if r["vendor"] != "deepseek":
                continue
            p = r.get("parsed") or {}
            if "_parse_error" in p or r.get("error"):
                continue
            out[r["source_id"]] = {"hate": bool(p.get("hate")), "text": r["text"], "orig": r.get("orig_label")}
    return out


def already_done() -> set[str]:
    done = set()
    if OUT_PATH.exists():
        with OUT_PATH.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    if r.get("raw_text", "").strip() and not r.get("error"):
                        done.add(r["source_id"])
                except json.JSONDecodeError:
                    continue
    return done


def main() -> None:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    ds = load_deepseek_v2()
    sys_p, tpl = load_prompt_template(V2_PROMPT)
    done = already_done()
    print(f"Local consensus: {MODEL} (no_think={NO_THINK}) | {len(ds)} teks | {len(done)} sudah ada", flush=True)

    with OUT_PATH.open("a", encoding="utf-8") as f:
        for sid, info in tqdm(ds.items(), total=len(ds), desc=MODEL):
            if sid in done:
                continue
            r = call_ollama(sys_p + THINK_TAG, render_user_prompt(tpl, info["text"]), model=MODEL)
            p = parse_llm_output(r.raw_text)
            rec = {
                "source_id": sid, "text": info["text"], "orig_label": info["orig"],
                "vendor": r.vendor, "model": r.model, "raw_text": r.raw_text, "parsed": p,
                "latency_ms": r.latency_ms, "output_tokens": r.output_tokens, "error": r.error,
                "ts": datetime.now(timezone.utc).isoformat(), "run_id": ts,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()

    # ── alpha(deepseek, lokal) ──────────────────────────────────────────
    local = {}
    with OUT_PATH.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if is_valid_json(r) and not is_refusal(r):
                local[r["source_id"]] = bool(r["parsed"].get("hate"))

    units = []
    agree = total = 0
    for sid, info in ds.items():
        if sid in local:
            units.append([info["hate"], local[sid]])
            total += 1
            if info["hate"] == local[sid]:
                agree += 1
    a = krippendorff_alpha_nominal(units)
    ci = bootstrap_alpha_ci(units)
    n_valid = len(local)
    print("\n=== HASIL ===", flush=True)
    print(f"Model: {MODEL} (no_think={NO_THINK})", flush=True)
    print(f"JSON valid: {n_valid}/{len(ds)} ({n_valid/len(ds)*100:.0f}%)", flush=True)
    print(f"Pairwise agreement deepseek-lokal: {agree}/{total} ({agree/total*100:.0f}%)", flush=True)
    print(f"Krippendorff alpha(deepseek, {MODEL}): {a:.3f} (CI [{ci[0]:.3f}, {ci[1]:.3f}])", flush=True)
    print(f"Pembanding: alpha(deepseek, grok) v2 = 0.763", flush=True)


if __name__ == "__main__":
    main()
