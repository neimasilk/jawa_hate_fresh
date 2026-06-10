"""Pilot #5 — Bulk labeling pool hot-Jawa dengan prompt v2 × deepseek+grok (D15).

Pipeline produksi pertama:
  hot_jawa_subset.jsonl (Pilot #2 full-filter, ~950 teks)
    -> label prompt v2 (pemenang Pilot #3) × 2 vendor
    -> outputs/bulk_responses.jsonl

Teks yang sudah dilabel v2 di Pilot #3 (149 pool prompt-iteration,
responses_v2.jsonl) TIDAK diulang — analyze.py menggabungkan keduanya.
Held-out = semua sid di luar 149 itu (snapshot prompt_iter_sids.json).

Resume-aware + 429-aware (error kuota di-retry saat rerun).
"""
from __future__ import annotations

import json
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
from src.llm_clients import call_deepseek, call_grok  # noqa: E402

PROMPT_VERSION = "v2"  # pemenang Pilot #3 (alpha ds+grok 0.763)
PROMPT_PATH = ROOT / "prompts" / f"cultural_classification_{PROMPT_VERSION}.md"

INPUT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
PILOT03_PATH = ROOT / "experiments" / "pilot03_cultural_prompt" / "outputs" / f"responses_{PROMPT_VERSION}.jsonl"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUTPUT_DIR / "bulk_responses.jsonl"

VENDORS = [("deepseek", call_deepseek), ("grok", call_grok)]  # D15: Kimi dropped


def load_hot_subset() -> list[dict]:
    samples: dict[str, dict] = {}
    with INPUT_PATH.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            samples[rec["source_id"]] = {
                "source_id": rec["source_id"],
                "text": rec["text"],
                "orig_label": rec.get("orig_label"),
                "filter_bahasa": (rec.get("parsed") or {}).get("bahasa"),
            }
    return list(samples.values())


def already_processed(*paths: Path) -> set[tuple[str, str]]:
    """(source_id, vendor) selesai — termasuk yang sudah dilabel di Pilot #3.

    Error kuota/saldo (429) tidak dihitung done (lesson insiden Kimi)."""
    done: set[tuple[str, str]] = set()
    for path in paths:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    raw_text = (rec.get("raw_text") or "").strip()
                    err = rec.get("error") or ""
                    if "429" in err or "insufficient balance" in err.lower():
                        continue
                    if err or raw_text:
                        done.add((rec["source_id"], rec["vendor"]))
                except (json.JSONDecodeError, KeyError):
                    continue
    return done


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    samples = load_hot_subset()
    print(f"Bulk labeling prompt {PROMPT_VERSION} | pool {len(samples)} teks hot-Jawa", flush=True)

    system_prompt, user_template = load_prompt_template(PROMPT_PATH)
    done = already_processed(OUT_PATH, PILOT03_PATH)
    if done:
        print(f"Resume/merge mode: {len(done)} (sample, vendor) pairs sudah ada", flush=True)

    total_calls = len(samples) * len(VENDORS)
    pbar = tqdm(total=total_calls, desc="Bulk label v2")

    with OUT_PATH.open("a", encoding="utf-8") as f:
        for sample in samples:
            user_prompt = render_user_prompt(user_template, sample["text"])
            for vendor_name, call_fn in VENDORS:
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
                    "prompt_version": PROMPT_VERSION,
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
                time.sleep(0.3)

    pbar.close()
    print(f"\nDone. Responses logged to {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
