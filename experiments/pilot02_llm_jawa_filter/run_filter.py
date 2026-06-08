"""Pilot #2 — LLM-as-Jawa-filter (prototype).

Tujuan ganda:
  1. Uji apakah LLM bisa filter Jawa / code-mixed Jawa-Indonesia dari dump
     berbahasa Indonesia (motivasi: langid Jawa low-resource, false-positive tinggi).
  2. Mengekstrak subset "panas" (Jawa + hate) untuk re-test C3 Pilot #1 secara
     non-degenerate (Pilot #1 gagal karena FineWeb2 nyaris tanpa hate).

Sumber: `haipradana/indonesian-twitter-hate-speech-cleaned` (HF, public).
  - Tweet Indonesia berlabel hate/neutral (~12.7K train, ~50/50).
  - Kita pakai RAW TEXT saja; label asli (hate/neutral) cuma untuk cross-tab,
    BUKAN sebagai label pipeline kita. Re-labeling kultural dilakukan terpisah.

Single-LLM filter (Grok 4.3 — paling cepat & murah di Pilot #1). Resume-aware.
"""
from __future__ import annotations

import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from datasets import load_dataset
from tqdm import tqdm

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))

from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt  # noqa: E402
from src.llm_clients import call_grok  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)
LOG_PATH = OUT_DIR / "pilot02_responses.jsonl"
PROMPT_PATH = _ROOT / "prompts" / "jawa_filter_v0.md"

DATASET = "haipradana/indonesian-twitter-hate-speech-cleaned"
# 2026-06-08 scale-up: 250 -> 2000 untuk pool hot-Jawa lebih besar (C3 robust,
# CI sempit). Seed sama -> 250 pertama identik -> resume skip otomatis, hanya
# proses ~1750 baris baru. Yield ~9.6% Jawa+campuran -> estimasi ~168 teks.
N_SAMPLE = 2000
SEED = 42

_MENTION = re.compile(r"@\w+")
_URL = re.compile(r"https?://\S+|www\.\S+")
_RT = re.compile(r"^\s*RT[:\s]", re.I)


def anonymize(text: str) -> str:
    """HARD RULE #7: hapus username/link sebelum analisis."""
    t = _RT.sub("", text)
    t = _MENTION.sub("[USER]", t)
    t = _URL.sub("[URL]", t)
    return t.strip()


def sample_rows() -> list[dict]:
    ds = load_dataset(DATASET, split="train")
    idx = list(range(len(ds)))
    random.Random(SEED).shuffle(idx)
    rows = []
    for i in idx[:N_SAMPLE]:
        r = ds[i]
        rows.append(
            {
                "source_id": f"haipradana-train-{i}",
                "orig_label": r.get("label"),
                "text": anonymize(r["text"]),
            }
        )
    return rows


def already_done(path: Path) -> set[str]:
    done: set[str] = set()
    if not path.exists():
        return done
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            raw = (rec.get("raw_text") or "").strip()
            if rec.get("error") or raw:
                done.add(rec["source_id"])
    return done


def main() -> None:
    system, user_tpl = load_prompt_template(PROMPT_PATH)
    rows = sample_rows()
    done = already_done(LOG_PATH)
    if done:
        print(f"Resume mode: {len(done)} sudah selesai", flush=True)

    with LOG_PATH.open("a", encoding="utf-8") as f:
        for row in tqdm(rows, desc="Jawa filter"):
            if row["source_id"] in done:
                continue
            user = render_user_prompt(user_tpl, row["text"])
            resp = call_grok(system, user)
            parsed = parse_llm_output(resp.raw_text)
            rec = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "source_id": row["source_id"],
                "orig_label": row["orig_label"],
                "text": row["text"],
                "vendor": resp.vendor,
                "model": resp.model,
                "raw_text": resp.raw_text,
                "parsed": parsed,
                "latency_ms": resp.latency_ms,
                "input_tokens": resp.input_tokens,
                "output_tokens": resp.output_tokens,
                "error": resp.error,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()

    print(f"Done. Logged to {LOG_PATH}", flush=True)


if __name__ == "__main__":
    main()
