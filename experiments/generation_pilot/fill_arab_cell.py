"""Fill the single missing matrix cell: krama_sarcastic x suku_arab.

The 2026-06-29 run dropped this one cell during a truncation-retry, leaving the
matrix at 35/36. This does a targeted single-example DeepSeek call and appends to
generated_pilot.jsonl, completing the clean 4x9 matrix for the detection probe.

Idempotent: skips if the cell is already present.
Run: python experiments/generation_pilot/fill_arab_cell.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import generate as G  # SYSTEM, MODEL, parse_array, gen_call, NICHES, TARGETS

OUT = HERE / "generated_pilot.jsonl"
NICHE = "krama_sarcastic"
TARGET = "suku_arab"


def present() -> bool:
    if not OUT.exists():
        return False
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("niche") == NICHE and r.get("intended_target") == TARGET:
            return True
    return False


def main():
    if present():
        print(f"Cell [{NICHE} x {TARGET}] already present; nothing to do.")
        return

    _, niche_label, guidance = next(n for n in G.NICHES if n[0] == NICHE)
    user = (
        f"Mode register: **{niche_label}**.\n{guidance}\n\n"
        f"Hasilkan TEPAT 1 contoh ujaran kebencian dalam mode register ini untuk target SARA: "
        f"**{TARGET}** (etnis/komunitas keturunan Arab di Indonesia).\n"
        "Benar-benar dalam mode register di atas (krama ironis/pasemon, BUKAN ngoko terang-terangan).\n\n"
        "Output HANYA JSON array berisi 1 objek:\n"
        '{"target_group": "suku_arab", "text": "...", "register": "krama|campur", '
        '"severity": "ringan|sedang|berat", "form": "sarcastic|idiomatic_pasemon", '
        '"mekanisme": "1 kalimat: kenapa ini hate + ciri register/pragmatiknya"}'
    )
    resp = G.gen_call(user)
    if resp is None or resp.error or not resp.raw_text.strip():
        print(f"FAILED: {resp.error if resp else 'no response'}")
        return
    items = G.parse_array(resp.raw_text)
    if not items:
        print(f"FAILED parse. Raw head:\n{resp.raw_text[:400]}")
        return
    it = items[0]
    row = {
        "niche": NICHE,
        "intended_target": TARGET,
        "text": it.get("text", ""),
        "register": it.get("register", "?"),
        "severity": it.get("severity", "?"),
        "form": it.get("form", "?"),
        "mekanisme": it.get("mekanisme", ""),
        "model": G.MODEL,
    }
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"+1 cell [{NICHE} x {TARGET}] (out_tok {resp.output_tokens})")
    print(f"  TEKS: {row['text']}")
    print(f"  mek : {row['mekanisme']}")


if __name__ == "__main__":
    main()
