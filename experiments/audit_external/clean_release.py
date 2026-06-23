"""Release-cleaning pass (2026-06-23): scrub residual PII the labeling pipeline missed.

Found by the adversarial audit: a record carries an intact WhatsApp number in a file
slated for public HuggingFace/Zenodo release (CLAUDE.md HARD RULE #7 + paper ethics §).
This adds the contact-info scrub the pipeline never had.

Produces *_clean.jsonl alongside the originals (originals kept) and prints every change.
Run: python experiments/audit_external/clean_release.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = ["data/labeled/bulk_v2_consensus.jsonl", "data/labeled/bulk_v2_disagreement.jsonl"]

# Indonesian phone numbers: 0-prefixed 9-13 digits, +62..., or 9+ digit runs near WA/telp/BO/HP.
PHONE_RE = re.compile(r"(?:\+?62|0)\d[\d\-\s]{7,13}\d")
LONGNUM_RE = re.compile(r"\b\d{9,15}\b")


def scrub(text: str):
    changes = []
    def repl(m):
        s = m.group(0)
        # keep short numeric tokens; only scrub plausible phone-length digit runs
        digits = re.sub(r"\D", "", s)
        if len(digits) >= 9:
            changes.append(s)
            return "[PHONE]"
        return s
    t = PHONE_RE.sub(repl, text)
    t = LONGNUM_RE.sub(repl, t)
    return t, changes


def main():
    total = 0
    for rel in FILES:
        p = ROOT / rel
        out_lines = []
        changed = 0
        with p.open(encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                new_text, changes = scrub(rec.get("text", ""))
                if changes:
                    print(f"[{rec['source_id']}] scrubbed {changes} ->")
                    print(f"   {rec['text'][:140]}")
                    rec["text"] = new_text
                    rec["pii_scrubbed"] = True
                    changed += 1
                out_lines.append(json.dumps(rec, ensure_ascii=False))
        outp = p.with_name(p.stem + "_clean.jsonl")
        outp.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"-> {outp.name}: {changed} records scrubbed / {len(out_lines)} total")
        total += changed
    print(f"\nTOTAL PII records scrubbed: {total}")
    print("NOTE: release the *_clean.jsonl files; keep originals local for provenance.")


if __name__ == "__main__":
    main()
