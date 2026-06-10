"""Pilot #3 — analisis prompt vN vs baseline v0 (Pilot #1b, n=149).

Fokus perbandingan (semua pada pool source_id yang SAMA):
  - alpha hate vN vs v0, full vendor set DAN per-subset (terutama deepseek+grok
    = pair kunci keputusan vendor mix bulk; baseline v0: full 0.587, ds+grok 0.534)
  - Hate-rate per vendor (baseline Grok 77% = over-flag; target turun)
  - Flip table: berapa label per vendor yang berubah v0 -> vN, ke arah mana
  - Majority-vs-orig_label shift
  - Disagreement listing vN (apakah boundary profanity-vs-hate sudah hilang?)

Pemakaian:
  P3_PROMPT_VERSION=v1 .venv/Scripts/python experiments/pilot03_cultural_prompt/analyze.py
Output: report_{ver}.md di folder ini.
"""
from __future__ import annotations

import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.agreement import (  # noqa: E402
    PRICING,
    bootstrap_alpha_ci,
    hate_units,
    is_refusal,
    is_valid_json,
    krippendorff_alpha_nominal,
    load_records,
)

PROMPT_VERSION = os.environ.get("P3_PROMPT_VERSION", "v1")
HERE = Path(__file__).resolve().parent
NEW_PATH = HERE / "outputs" / f"responses_{PROMPT_VERSION}.jsonl"
BASELINE_PATH = ROOT / "experiments" / "pilot01b_c3_retest" / "outputs" / "c3_responses.jsonl"
REPORT_PATH = HERE / f"report_{PROMPT_VERSION}.md"


def index_by_source(records: list[dict]) -> dict[str, dict[str, dict]]:
    by_source: dict[str, dict[str, dict]] = defaultdict(dict)
    for rec in records:
        by_source[rec["source_id"]][rec["vendor"]] = rec
    return by_source


def alpha_with_ci(by_source, vendors, sids):
    units = hate_units(by_source, vendors, sids)
    a = krippendorff_alpha_nominal(units)
    ci = bootstrap_alpha_ci(units)
    npair = sum(1 for u in units if sum(1 for x in u if x is not None) >= 2)
    return a, ci, npair


def vendor_label(by_source, sid, vendor):
    """Label hate vendor untuk sid, atau None kalau invalid/refusal/absent."""
    r = by_source.get(sid, {}).get(vendor)
    if r is None or is_refusal(r) or not is_valid_json(r):
        return None
    return bool(r["parsed"].get("hate"))


def main() -> None:
    new_records = load_records(NEW_PATH)
    base_records = load_records(BASELINE_PATH)
    new_by_source = index_by_source(new_records)
    base_by_source = index_by_source(base_records)

    new_vendors = sorted({r["vendor"] for r in new_records})
    base_vendors = sorted({r["vendor"] for r in base_records})
    # Pool = source_id yang ada di kedua run (harusnya identik: 149)
    sids = sorted(set(new_by_source) & set(base_by_source))

    lines = [f"# Pilot #3 — Prompt {PROMPT_VERSION} vs v0 (pool n={len(sids)})", ""]
    lines.append(f"**Baseline v0:** Pilot #1b scale-up (α full-3LLM = 0.587). **Vendors {PROMPT_VERSION}:** {', '.join(new_vendors)}")
    lines.append("")

    # ── Per-vendor metrics (vN) ─────────────────────────────────────────
    lines.append(f"## Per-vendor metrics ({PROMPT_VERSION})")
    lines.append("")
    lines.append("| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate dist | Hate rate v0 → vN |")
    lines.append("|---|---|---|---|---|---|---|---|")
    total_cost = 0.0
    for v in new_vendors:
        vrecs = [r for r in new_records if r["vendor"] == v]
        n = len(vrecs)
        n_refusal = sum(1 for r in vrecs if is_refusal(r))
        n_valid = sum(1 for r in vrecs if is_valid_json(r))
        latencies = [r["latency_ms"] for r in vrecs if r.get("latency_ms")]
        in_tok = sum((r.get("input_tokens") or 0) for r in vrecs)
        out_tok = sum((r.get("output_tokens") or 0) for r in vrecs)
        cost = (in_tok / 1_000_000) * PRICING[v]["in"] + (out_tok / 1_000_000) * PRICING[v]["out"]
        total_cost += cost

        def hate_rate(by_source):
            labels = [vendor_label(by_source, sid, v) for sid in sids]
            labels = [x for x in labels if x is not None]
            return (sum(labels) / len(labels) * 100) if labels else float("nan"), len(labels)

        new_rate, n_new = hate_rate(new_by_source)
        base_rate, n_base = hate_rate(base_by_source)
        dist = Counter(vendor_label(new_by_source, sid, v) for sid in sids)
        lines.append(
            f"| {v} | {n} | {n_refusal / n * 100:.1f} | {n_valid / n * 100:.1f} | {mean(latencies) if latencies else 0:.0f} "
            f"| ${cost:.3f} | {dist.get(True, 0)}T/{dist.get(False, 0)}F | {base_rate:.0f}% → **{new_rate:.0f}%** |"
        )
    lines.append("")
    lines.append(f"**Total cost {PROMPT_VERSION}:** ${total_cost:.3f}")
    lines.append("")

    # ── Alpha: vN vs v0, per vendor-set ─────────────────────────────────
    lines.append("## Krippendorff's alpha (hate) — vN vs v0, pool sama")
    lines.append("")
    lines.append("| Vendor set | α v0 | 95% CI | α " + PROMPT_VERSION + " | 95% CI | Δ |")
    lines.append("|---|---|---|---|---|---|")

    vendor_sets = [new_vendors]  # full set yang tersedia di vN
    if len(new_vendors) > 2:
        vendor_sets += [[a, b] for i, a in enumerate(new_vendors) for b in new_vendors[i + 1:]]
    elif new_vendors != ["deepseek", "grok"]:
        vendor_sets.append(["deepseek", "grok"])  # pair kunci selalu dilaporkan kalau ada

    for vset in vendor_sets:
        if not all(v in new_vendors for v in vset):
            continue
        a_new, ci_new, _ = alpha_with_ci(new_by_source, vset, sids)
        a_base, ci_base, _ = alpha_with_ci(base_by_source, vset, sids)
        delta = a_new - a_base
        lines.append(
            f"| {'+'.join(vset)} | {a_base:.3f} | [{ci_base[0]:.3f}, {ci_base[1]:.3f}] "
            f"| **{a_new:.3f}** | [{ci_new[0]:.3f}, {ci_new[1]:.3f}] | {delta:+.3f} |"
        )
    lines.append("")

    # ── Flip table per vendor ───────────────────────────────────────────
    lines.append("## Flip label per vendor (v0 → " + PROMPT_VERSION + ")")
    lines.append("")
    lines.append("| Vendor | T→F | F→T | tetap | unpairable |")
    lines.append("|---|---|---|---|---|")
    flips_detail: dict[str, list[str]] = defaultdict(list)
    for v in new_vendors:
        t2f = f2t = same = unpair = 0
        for sid in sids:
            old = vendor_label(base_by_source, sid, v)
            new = vendor_label(new_by_source, sid, v)
            if old is None or new is None:
                unpair += 1
            elif old == new:
                same += 1
            elif old and not new:
                t2f += 1
                flips_detail[v].append(sid)
            else:
                f2t += 1
        lines.append(f"| {v} | {t2f} | {f2t} | {same} | {unpair} |")
    lines.append("")
    lines.append("(T→F diharapkan dominan di Grok kalau definisi profanity-vs-hate bekerja; F→T besar = red flag under/over-correction.)")
    lines.append("")

    # ── Majority vote vs orig_label ─────────────────────────────────────
    lines.append("## Majority vote vs label asli haipradana (" + PROMPT_VERSION + ")")
    lines.append("")
    confusion = Counter()
    for sid in sids:
        votes = [vendor_label(new_by_source, sid, v) for v in new_vendors]
        votes = [x for x in votes if x is not None]
        if not votes:
            continue
        c = Counter(votes)
        maj = c.most_common(1)[0][0]
        if len(c) > 1 and c.most_common(2)[0][1] == c.most_common(2)[1][1]:
            maj = True  # tie -> conservative flag
        orig = next(iter(new_by_source[sid].values())).get("orig_label")
        confusion[(orig, maj)] += 1
    lines.append("| orig_label | majority hate=True | majority hate=False |")
    lines.append("|---|---|---|")
    for orig in ("hate", "neutral"):
        lines.append(f"| {orig} | {confusion.get((orig, True), 0)} | {confusion.get((orig, False), 0)} |")
    lines.append("")

    # ── Disagreements (vN) ──────────────────────────────────────────────
    disagreements = []
    for sid in sids:
        labels = {v: vendor_label(new_by_source, sid, v) for v in new_vendors}
        labels = {v: x for v, x in labels.items() if x is not None}
        if len(set(labels.values())) > 1:
            rec0 = next(iter(new_by_source[sid].values()))
            sev = {v: new_by_source[sid][v]["parsed"].get("severity") for v in labels}
            disagreements.append({"source_id": sid, "orig_label": rec0.get("orig_label"), "text": rec0["text"], "labels": labels, "severity": sev})
    lines.append(f"## Disagreements {PROMPT_VERSION} ({len(disagreements)} dari {len(sids)} teks)")
    lines.append("")
    for d in disagreements:
        lines.append(f"- `{d['source_id']}` (orig: {d['orig_label']}) — hate: {d['labels']} | severity: {d['severity']}")
        lines.append(f"  > {d['text'][:200]}{'...' if len(d['text']) > 200 else ''}")
    lines.append("")

    # ── Gate ────────────────────────────────────────────────────────────
    a_full, ci_full, _ = alpha_with_ci(new_by_source, new_vendors, sids)
    a_base_full, _, _ = alpha_with_ci(base_by_source, new_vendors, sids)
    lines.append("## Kesimpulan iterasi")
    lines.append("")
    lines.append(f"- α({'+'.join(new_vendors)}): v0 {a_base_full:.3f} → {PROMPT_VERSION} **{a_full:.3f}** (CI [{ci_full[0]:.3f}, {ci_full[1]:.3f}])")
    if a_full > a_base_full + 0.05:
        lines.append(f"- ✅ **{PROMPT_VERSION} NAIK signifikan** — keep, jadikan baseline iterasi berikut.")
    elif a_full < a_base_full - 0.05:
        lines.append(f"- 🔴 **{PROMPT_VERSION} TURUN** — discard, inspeksi flip F→T/T→F untuk diagnosis.")
    else:
        lines.append(f"- 🟡 **{PROMPT_VERSION} ≈ v0** — cek flip table & disagreement: mungkin perbaikan kualitatif tanpa α naik.")

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print("\n" + report_text.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
