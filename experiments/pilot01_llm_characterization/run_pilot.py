"""Pilot #1 — LLM characterization runner.

Pipeline:
  1. Load OSCAR-2301 Javanese subset (streaming, batas memori).
  2. Sample 100 candidate dengan light keyword pre-filter.
  3. Untuk tiap sampel × tiap vendor (Claude, GPT-4o, DeepSeek):
     - Render cultural prompt
     - Call API
     - Log raw response + parsed output + metadata
  4. Save sebagai JSONL ke outputs/ (resumable kalau crash).

Sub-second sleep antar call untuk respect rate limits.
"""
from __future__ import annotations

import json
import random
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from datasets import load_dataset
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.cultural_prompt import (  # noqa: E402
    load_prompt_template,
    parse_llm_output,
    render_user_prompt,
)
from src.llm_clients import call_claude, call_deepseek, call_openai  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_SIZE = 100
RANDOM_SEED = 42
MIN_TEXT_LEN = 30
MAX_TEXT_LEN = 600

# Light keyword pre-filter: minimal salah satu kata muncul → kandidat berpotensi
# untuk variety (BUKAN ground truth labeling, hanya untuk menghindari sample
# yang seluruhnya benign banget seperti definisi wikipedia)
KEYWORD_HINTS = [
    "asu", "jancuk", "bangsat", "goblok", "bodho", "edan", "kethek", "babi",
    "wong", "kowe", "rai", "raimu", "iku", "ki", "tindak", "mangan", "nedha",
    "madura", "tionghoa", "cina", "sunda", "batak", "papua", "arab", "kafir",
    "haram", "syetan", "setan", "monggo", "sampeyan", "panjenengan",
]


def load_javanese_samples(n: int) -> list[dict]:
    """Stream OSCAR-2301 jv subset, filter by length + keyword hint, random sample n."""
    print(f"Loading OSCAR-2301 jv subset (streaming)...", flush=True)

    ds = load_dataset(
        "oscar-corpus/OSCAR-2301",
        language="jv",
        split="train",
        streaming=True,
        trust_remote_code=True,
    )

    rng = random.Random(RANDOM_SEED)
    candidates: list[dict] = []
    seen = 0

    target_pool = n * 30  # ambil 30x untuk diversitas, lalu sample n

    for item in ds:
        seen += 1
        text = item.get("text", "").strip()
        if not (MIN_TEXT_LEN <= len(text) <= MAX_TEXT_LEN):
            continue
        # Pecah jadi kalimat kalau panjang
        first_chunk = text.split("\n")[0].strip()
        if not (MIN_TEXT_LEN <= len(first_chunk) <= MAX_TEXT_LEN):
            continue

        text_lower = first_chunk.lower()
        has_hint = any(kw in text_lower for kw in KEYWORD_HINTS)

        candidates.append(
            {
                "text": first_chunk,
                "has_keyword_hint": has_hint,
                "source_id": f"oscar2301_jv_{seen}",
            }
        )

        if len(candidates) >= target_pool:
            break

    print(f"  Scanned {seen} OSCAR rows, kept {len(candidates)} length-valid candidates", flush=True)

    # Stratified: ambil 70% with keyword hint + 30% random
    with_hint = [c for c in candidates if c["has_keyword_hint"]]
    no_hint = [c for c in candidates if not c["has_keyword_hint"]]

    n_with = min(int(n * 0.7), len(with_hint))
    n_no = n - n_with

    rng.shuffle(with_hint)
    rng.shuffle(no_hint)

    sample = with_hint[:n_with] + no_hint[:n_no]
    rng.shuffle(sample)
    sample = sample[:n]

    print(
        f"  Final sample: {len(sample)} ({n_with} with-keyword + {n_no} no-keyword)",
        flush=True,
    )
    return sample


def already_processed(out_path: Path) -> set[tuple[str, str]]:
    """Return set of (source_id, vendor) yang sudah di-log, untuk resume."""
    done: set[tuple[str, str]] = set()
    if not out_path.exists():
        return done
    with out_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                done.add((rec["source_id"], rec["vendor"]))
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"pilot01_responses.jsonl"
    samples_path = OUTPUT_DIR / f"pilot01_samples.json"

    # Load atau reuse samples (deterministic seed → konsisten kalau re-run)
    if samples_path.exists():
        print(f"Reusing samples from {samples_path.name}", flush=True)
        samples = json.loads(samples_path.read_text(encoding="utf-8"))
    else:
        samples = load_javanese_samples(SAMPLE_SIZE)
        samples_path.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved samples to {samples_path.name}", flush=True)

    system_prompt, user_template = load_prompt_template()
    done = already_processed(out_path)
    if done:
        print(f"Resume mode: {len(done)} (sample, vendor) pairs already logged", flush=True)

    vendors = [
        ("anthropic", call_claude),
        ("openai", call_openai),
        ("deepseek", call_deepseek),
    ]

    total_calls = len(samples) * len(vendors)
    pbar = tqdm(total=total_calls, desc="LLM calls")

    with out_path.open("a", encoding="utf-8") as f:
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
                    "has_keyword_hint": sample["has_keyword_hint"],
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
    print(f"\nDone. Responses logged to {out_path}", flush=True)


if __name__ == "__main__":
    main()
