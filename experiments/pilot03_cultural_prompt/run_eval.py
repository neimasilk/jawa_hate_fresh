"""Pilot #3 — Cultural prompt iteration: eval prompt vN pada pool hot-Jawa n=149.

Tiap versi prompt dievaluasi pada pool dan vendor SAMA dengan baseline C3
(Pilot #1b, prompt v0, alpha=0.587) supaya perbandingan apple-to-apple.

Pipeline identik run_c3.py (resume-aware, append + flush per record), tapi:
  - Versi prompt via env P3_PROMPT_VERSION (default "v1")
    -> prompts/cultural_classification_{ver}.md
  - Output per versi: outputs/responses_{ver}.jsonl
  - Vendor mix via env P3_VENDORS (default semua; "deepseek,grok" untuk
    stage cepat — pair kunci keputusan bulk — lalu rerun kimi menyusul).
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

PROMPT_VERSION = os.environ.get("P3_PROMPT_VERSION", "v1")
PROMPT_PATH = ROOT / "prompts" / f"cultural_classification_{PROMPT_VERSION}.md"

INPUT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUTPUT_DIR / f"responses_{PROMPT_VERSION}.jsonl"

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
                "orig_label": rec.get("orig_label"),  # referensi, bukan gold
                "filter_bahasa": (rec.get("parsed") or {}).get("bahasa"),
            }
    return list(samples.values())


def already_processed(out_path: Path) -> set[tuple[str, str]]:
    """Return set (source_id, vendor) yang sudah sukses di-log, untuk resume.

    Error kuota/saldo (429) TIDAK dihitung done — rerun setelah top-up harus
    retry (lesson: saldo Kimi habis di tengah run v1, 149 record error).
    """
    done: set[tuple[str, str]] = set()
    if not out_path.exists():
        return done
    with out_path.open(encoding="utf-8") as f:
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
    print(f"Prompt {PROMPT_VERSION} ({PROMPT_PATH.name}) | {len(samples)} hot-Jawa samples", flush=True)

    system_prompt, user_template = load_prompt_template(PROMPT_PATH)
    done = already_processed(OUT_PATH)
    if done:
        print(f"Resume mode: {len(done)} (sample, vendor) pairs already logged", flush=True)

    sel = os.environ.get("P3_VENDORS")
    names = [s.strip() for s in sel.split(",")] if sel else list(_ALL_VENDORS)
    vendors = [(n, _ALL_VENDORS[n]) for n in names if n in _ALL_VENDORS]
    print(f"Vendors: {', '.join(n for n, _ in vendors)}", flush=True)

    total_calls = len(samples) * len(vendors)
    pbar = tqdm(total=total_calls, desc=f"LLM calls ({PROMPT_VERSION})")

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
                time.sleep(0.3)  # gentle rate limit

    pbar.close()
    print(f"\nDone. Responses logged to {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
