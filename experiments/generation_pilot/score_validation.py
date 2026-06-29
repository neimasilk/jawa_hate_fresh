"""Score the native expert's authenticity validation of the generated hate.

Run AFTER Bapak fills VALIDATION_FORM.xlsx (sheet 'Validasi'):
  col G  OTENTIK?  -> 1 (authentic Javanese hate) / 0 (not)
  col H  MASALAH   -> museum_krama | bocor_indonesia | bukan_hate | salah_register | lainnya
  col I  CATATAN   -> free text

  python experiments/generation_pilot/score_validation.py

Computes the questions that matter for the paper:
  - overall authenticity rate of LLM-generated Javanese hate
  - PER-NICHE rate -> does N3b group-directed krama cold-contempt hold up natively?
    (the open question from register_probe/FINDINGS.md §5)
  - per-target rate, breakdown of failure reasons
  - does the non-native auto-flag heuristic predict native rejections?
Writes validation_result.md
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

HERE = Path(__file__).parent
FORM = HERE / "VALIDATION_FORM.xlsx"
KEY = HERE / "_key.csv"


def main():
    if not FORM.exists() or not KEY.exists():
        print("Missing VALIDATION_FORM.xlsx or _key.csv. Run review_generated.py first.")
        return
    key = {}
    with KEY.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key[str(row["no"])] = row

    wb = load_workbook(FORM)
    ws = wb["Validasi"]
    recs, missing = [], []
    for r in range(2, ws.max_row + 1):
        no = ws.cell(r, 1).value
        if no is None:
            continue
        auth = ws.cell(r, 7).value          # G OTENTIK?
        masalah = (ws.cell(r, 8).value or "").strip()
        catatan = (ws.cell(r, 9).value or "").strip()
        if auth in (None, ""):
            missing.append(str(no))
            continue
        k = key.get(str(no), {})
        recs.append(dict(
            no=str(no), niche=k.get("niche", "?"), target=k.get("intended_target", "?"),
            auth=1 if str(auth).strip() in ("1", "1.0", "ya", "Ya") else 0,
            masalah=masalah, catatan=catatan, auto_flags=k.get("auto_flags", ""),
        ))

    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))
    P("# Generation pilot — native authenticity validation\n")
    if not recs:
        P("> No rows scored yet. Fill column G (OTENTIK?) in VALIDATION_FORM.xlsx.")
        (HERE / "validation_result.md").write_text("\n".join(out), encoding="utf-8")
        print("\n".join(out))
        return
    if missing:
        P(f"> NOTE: {len(missing)} rows unrated ({','.join(missing[:20])}...).\n")

    n = len(recs)
    ok = sum(r["auth"] for r in recs)
    P(f"Scored **{ok}/{n} = {ok/n:.0%}** judged authentic Javanese hate.\n")

    # per niche (THE register-pragmatic result)
    P("## Per niche (register-pragmatic axis)\n")
    P("| niche | authentic | rate |")
    P("|---|---|---|")
    byn = defaultdict(list)
    for r in recs:
        byn[r["niche"]].append(r["auth"])
    for niche in ["ngoko_direct", "krama_report", "krama_sarcastic", "krama_cold_contempt"]:
        v = byn.get(niche)
        if v:
            P(f"| {niche} | {sum(v)}/{len(v)} | {sum(v)/len(v):.0%} |")
    P("\n_krama_cold_contempt = the open N3b-group question: can SARA-group cold-contempt "
      "krama hate be generated authentically?_\n")

    # per target
    P("## Per target (SARA coverage)\n")
    P("| target | authentic | rate |")
    P("|---|---|---|")
    byt = defaultdict(list)
    for r in recs:
        byt[r["target"]].append(r["auth"])
    for t, v in sorted(byt.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
        P(f"| {t} | {sum(v)}/{len(v)} | {sum(v)/len(v):.0%} |")

    # failure reasons
    fails = [r for r in recs if not r["auth"]]
    P(f"\n## Failure reasons ({len(fails)} rejected)\n")
    reasons = defaultdict(int)
    for r in fails:
        reasons[r["masalah"] or "(unspecified)"] += 1
    for reason, c in sorted(reasons.items(), key=lambda kv: -kv[1]):
        P(f"- {reason}: {c}")
    if fails:
        P("\nRejected items:")
        for r in fails:
            note = f" — {r['catatan']}" if r["catatan"] else ""
            P(f"- [{r['niche']}/{r['target']}] {r['masalah']}{note}")

    # does the auto-flag heuristic predict native rejection?
    P("\n## Auto-flag heuristic vs native verdict\n")
    flagged = [r for r in recs if r["auto_flags"]]
    if flagged:
        tp = sum(1 for r in flagged if not r["auth"])
        P(f"- {len(flagged)} auto-flagged; {tp} of them natively rejected "
          f"(heuristic precision {tp/len(flagged):.0%}).")
    flagged_rej = sum(1 for r in fails if r["auto_flags"])
    if fails:
        P(f"- of {len(fails)} native rejections, {flagged_rej} were auto-flagged "
          f"(heuristic recall {flagged_rej/len(fails):.0%}).")

    P("\n## Interpretation guide")
    P("- High overall rate => LLM is a viable generator for a register-stratified Javanese hate set.")
    P("- krama_cold_contempt authentic => N3b-group is generable (paper contribution: the "
      "uncollectable register can be synthesized + native-validated).")
    P("- If failures cluster in one niche/target => that cell needs prompt work or a different model.")
    P("- Low heuristic recall => non-native auto-checks miss native-only judgments "
      "=> confirms the irreducible native-referee role (consistent with the framing).")

    (HERE / "validation_result.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
