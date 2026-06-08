"""Pilot #1b — C3 re-test: 3-LLM characterization pada subset Jawa-panas.

Konteks: Pilot #1 menghasilkan alpha=1.000 DEGENERATE (semua sampel FineWeb2
dilabeli BUK karena sumber nyaris tanpa hate). C3 (apakah multi-LLM agreement
bekerja pada hate Jawa ASLI?) belum terjawab.

Input: hot_jawa_subset.jsonl dari Pilot #2 (24 teks Jawa/code-mixed dari dump
hate Indonesia haipradana; 9 di antaranya berlabel asli "hate").
Ada variasi label -> alpha tidak lagi degenerate.

Pipeline:
  1. Load 24 teks dari pilot02 outputs.
  2. Tiap teks x tiap vendor (DeepSeek, Grok, Kimi): render cultural prompt
     v0, call API, log raw + parsed + metadata.
  3. Append ke outputs/c3_responses.jsonl (resumable, sama seperti Pilot #1).

~72 call total. Estimasi runtime ~40-50 menit (Kimi lambat), cost ~$0.2-0.3.
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

from src.cultural_prompt import (  # noqa: E402
    load_prompt_template,
    parse_llm_output,
    render_user_prompt,
)
from src.llm_clients import call_deepseek, call_grok, call_kimi  # noqa: E402

INPUT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUTPUT_DIR / "c3_responses.jsonl"

# Vendor mix C3. Default 3-LLM (klaim paper "cross-LLM consistency", D8).
# Override via env C3_VENDORS="deepseek,grok" untuk run cepat tanpa Kimi
# (Kimi K2.6 ~115s/call + validity 62.5% -> bottleneck untuk pool besar;
# sensitivitas drop-Kimi dilaporkan di analyze.py, jadi 2-LLM = pelengkap sah).
# Resume-aware: run_c3 append, dedup keep-last di analyze. Menjalankan ulang
# dengan input lebih besar (hot_jawa_subset di-scale Pilot #2) akan otomatis
# memproses source_id baru saja.
_ALL_VENDORS = {
    "deepseek": call_deepseek,
    "grok": call_grok,
    "kimi": call_kimi,
}


def load_hot_subset() -> list[dict]:
    """Load subset Jawa-panas dari Pilot #2 (unik per source_id)."""
    samples: dict[str, dict] = {}
    with INPUT_PATH.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            samples[rec["source_id"]] = {
                "source_id": rec["source_id"],
                "text": rec["text"],
                "orig_label": rec.get("orig_label"),  # label asli haipradana (referensi, bukan gold)
                "filter_bahasa": (rec.get("parsed") or {}).get("bahasa"),
            }
    return list(samples.values())


def already_processed(out_path: Path) -> set[tuple[str, str]]:
    """Return set (source_id, vendor) yang sudah sukses di-log, untuk resume."""
    done: set[tuple[str, str]] = set()
    if not out_path.exists():
        return done
    with out_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                raw_text = (rec.get("raw_text") or "").strip()
                if rec.get("error") or raw_text:
                    done.add((rec["source_id"], rec["vendor"]))
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    samples = load_hot_subset()
    print(f"Loaded {len(samples)} hot-Jawa samples from pilot #2", flush=True)

    system_prompt, user_template = load_prompt_template()
    done = already_processed(OUT_PATH)
    if done:
        print(f"Resume mode: {len(done)} (sample, vendor) pairs already logged", flush=True)

    sel = os.environ.get("C3_VENDORS")
    names = [s.strip() for s in sel.split(",")] if sel else list(_ALL_VENDORS)
    vendors = [(n, _ALL_VENDORS[n]) for n in names if n in _ALL_VENDORS]
    print(f"Vendors C3: {', '.join(n for n, _ in vendors)}", flush=True)

    total_calls = len(samples) * len(vendors)
    pbar = tqdm(total=total_calls, desc="LLM calls")

    with OUT_PATH.open("a", encoding="utf-8") as f:
        for sample in samples:
            user_prompt = render_user_prompt(user_template, sample["text"])
            for vendor_name, call_fn in vendors:
                key = (sample["source_id"], vendor_name)
                if key in done:
                    pbar.update(1)
                    continue

                resp = call_fn(system_prompt, user_prompt)
                parsed = parse_llm_output(resp.raw_text)

                record = {
                    "source_id": sample["source_id"],
                    "text": sample["text"],
                    "orig_label": sample["orig_label"],
                    "filter_bahasa": sample["filter_bahasa"],
                    "vendor": resp.vendor,
                    "model": resp.model,
                    "raw_text": resp.raw_text,
                    "parsed": parsed,
                    "latency_ms": resp.latency_ms,
                    "input_tokens": resp.input_tokens,
                    "output_tokens": resp.output_tokens,
                    "error": resp.error,
                    "extra": resp.extra,
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "run_id": timestamp,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                f.flush()
                pbar.update(1)
                time.sleep(0.3)  # gentle rate limit

    pbar.close()
    print(f"\nDone. Responses logged to {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
