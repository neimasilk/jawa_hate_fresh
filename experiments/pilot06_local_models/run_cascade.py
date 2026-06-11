"""Pilot #6b — cascade filter pass 2+3 (setelah pass 1 SEA-LION selesai).

Desain cascade (hemat $; lihat filter_validation_summary.md):
  pass 1: SEA-LION pre-screen 8.3K sisa (gratis, cepat 3.5s) -> kandidat keep
  pass 2: qwen3 re-screen kandidat pass 1 (gratis; drop-agree lebih baik 75%)
  pass 3: Grok verifikasi kandidat lolos pass 2 (~$1.2) -> append ke
          pilot02_responses.jsonl (pool authority TETAP grok; analyze.py
          pilot02 regenerate pool homogen grok-confirmed)

Tiap pass resume-aware (log terpisah per pass). Jalankan ulang kapan pun.

Pemakaian (setelah pass 1 selesai):
  .venv\Scripts\python experiments\pilot06_local_models\run_cascade.py
Env: CASCADE_PASS2_MODEL (default qwen3:14b), SKIP_PASS3="1" untuk dry tanpa Grok.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt  # noqa: E402
from src.llm_clients import call_grok, call_ollama  # noqa: E402

P02_OUT = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs"
MAIN_LOG = P02_OUT / "pilot02_responses.jsonl"  # grok, pool authority
PASS1_LOG = P02_OUT / "pilot02_responses_local_aisingapore_Llama-SEA-LION-v3.5-8B-R_q5_k_m.jsonl"
PROMPT_PATH = ROOT / "prompts" / "jawa_filter_v0.md"

PASS2_MODEL = os.environ.get("CASCADE_PASS2_MODEL", "qwen3:14b")
NO_THINK_TAG = "\n\n/no_think"
KEEP_CATS = {"jawa", "campuran"}

PASS2_LOG = P02_OUT / f"cascade_pass2_{PASS2_MODEL.replace('/', '_').replace(':', '_')}.jsonl"


def load_keeps(path: Path) -> list[dict]:
    """Record valid dengan bahasa di KEEP_CATS, dedup keep-last."""
    latest: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            latest[rec["source_id"]] = rec
    out = []
    for rec in latest.values():
        p = rec.get("parsed") or {}
        if rec.get("error") or "_parse_error" in p:
            continue
        if p.get("bahasa") in KEEP_CATS:
            out.append({"source_id": rec["source_id"], "text": rec["text"],
                        "orig_label": rec.get("orig_label")})
    return out


def already_done(path: Path) -> set[str]:
    done = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                err = r.get("error") or ""
                el = err.lower()
                if "429" in err or "403" in err or "insufficient balance" in el or "permission-denied" in el:
                    continue
                if err or (r.get("raw_text") or "").strip():
                    done.add(r["source_id"])
        return done
    return done


def grok_processed() -> set[str]:
    """source_id yang sudah pernah difilter grok (valid) — tak perlu diverifikasi lagi."""
    done = set()
    with MAIN_LOG.open(encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            p = r.get("parsed") or {}
            if not r.get("error") and "_parse_error" not in p and p.get("bahasa"):
                done.add(r["source_id"])
    return done


def run_pass(rows: list[dict], out_path: Path, call_fn, desc: str) -> None:
    done = already_done(out_path)
    print(f"{desc}: {len(rows)} kandidat | {len(done)} sudah ada", flush=True)
    system, user_tpl = load_prompt_template(PROMPT_PATH)
    with out_path.open("a", encoding="utf-8") as f:
        for row in tqdm(rows, desc=desc):
            if row["source_id"] in done:
                continue
            resp = call_fn(system, render_user_prompt(user_tpl, row["text"]))
            parsed = parse_llm_output(resp.raw_text)
            rec = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "source_id": row["source_id"], "orig_label": row["orig_label"],
                "text": row["text"], "vendor": resp.vendor, "model": resp.model,
                "raw_text": resp.raw_text, "parsed": parsed,
                "latency_ms": resp.latency_ms, "input_tokens": resp.input_tokens,
                "output_tokens": resp.output_tokens, "error": resp.error,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()


def main() -> None:
    if not PASS1_LOG.exists():
        raise SystemExit(f"Pass 1 (SEA-LION) belum jalan: {PASS1_LOG} tidak ada.")

    pass1_keeps = load_keeps(PASS1_LOG)
    print(f"Pass 1 keeps (SEA-LION): {len(pass1_keeps)}", flush=True)

    # pass 2: qwen3 re-screen
    run_pass(pass1_keeps, PASS2_LOG,
             lambda s, u: call_ollama(s + NO_THINK_TAG, u, model=PASS2_MODEL),
             f"pass2 {PASS2_MODEL}")
    pass2_keeps = load_keeps(PASS2_LOG)
    print(f"Pass 2 keeps (qwen3): {len(pass2_keeps)}", flush=True)

    if os.environ.get("SKIP_PASS3") == "1":
        print("SKIP_PASS3=1 — berhenti sebelum Grok.", flush=True)
        return

    # pass 3: grok verifikasi, append ke MAIN_LOG (pool authority)
    seen = grok_processed()
    to_verify = [r for r in pass2_keeps if r["source_id"] not in seen]
    est = len(to_verify) * 0.00114
    print(f"Pass 3 (grok verify): {len(to_verify)} kandidat, est ${est:.2f}", flush=True)
    run_pass(to_verify, MAIN_LOG, call_grok, "pass3 grok-verify")

    # ringkasan akhir
    final_keeps = load_keeps(MAIN_LOG)
    print(f"\nPool grok-confirmed sekarang: {len(final_keeps)} teks "
          f"(jalankan pilot02 analyze.py untuk regenerate hot_jawa_subset.jsonl)", flush=True)


if __name__ == "__main__":
    main()
