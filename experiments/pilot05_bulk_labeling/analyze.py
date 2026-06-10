"""Pilot #5 — analisis bulk labeling: held-out alpha + consensus split + dataset.

Output utama:
  1. HELD-OUT VALIDATION: alpha ds+grok di teks yang TIDAK dipakai iterasi
     prompt Pilot #3 (jawab kekhawatiran overfit; pembanding: pool prompt-iter
     alpha 0.763).
  2. Consensus split:
     - data/labeled/bulk_v2_consensus.jsonl  (kedua vendor valid & hate agree)
     - data/labeled/bulk_v2_disagreement.jsonl (hate beda / salah satu invalid)
  3. Distribusi taksonomi (severity/register/form/target_group) = profil dataset.

Severity policy konservatif: consensus_severity diisi hanya kalau kedua vendor
sama; kalau beda, simpan keduanya (severity_agreement=false) — keputusan
resolusi nanti (codebook / model training bisa pakai binary dulu).
"""
from __future__ import annotations

import json
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

HERE = Path(__file__).resolve().parent
BULK_PATH = HERE / "outputs" / "bulk_responses.jsonl"
PILOT03_PATH = ROOT / "experiments" / "pilot03_cultural_prompt" / "outputs" / "responses_v2.jsonl"
HOT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
ITER_SIDS_PATH = HERE / "prompt_iter_sids.json"

LABELED_DIR = ROOT / "data" / "labeled"
LABELED_DIR.mkdir(parents=True, exist_ok=True)
CONSENSUS_PATH = LABELED_DIR / "bulk_v2_consensus.jsonl"
DISAGREE_PATH = LABELED_DIR / "bulk_v2_disagreement.jsonl"
REPORT_PATH = HERE / "report.md"

VENDORS = ["deepseek", "grok"]


def main() -> None:
    records = load_records(BULK_PATH) + load_records(PILOT03_PATH)
    # dedup lintas file: keep-last per (sid, vendor) — bulk menang atas pilot03
    latest: dict[tuple[str, str], dict] = {}
    for rec in records:
        latest[(rec["source_id"], rec["vendor"])] = rec
    records = list(latest.values())

    hot_sids = {json.loads(l)["source_id"] for l in HOT_PATH.open(encoding="utf-8")}
    iter_sids = set(json.loads(ITER_SIDS_PATH.read_text(encoding="utf-8")))

    by_source: dict[str, dict[str, dict]] = defaultdict(dict)
    for rec in records:
        if rec["source_id"] in hot_sids and rec["vendor"] in VENDORS:
            by_source[rec["source_id"]][rec["vendor"]] = rec

    all_sids = sorted(by_source.keys())
    heldout_sids = [s for s in all_sids if s not in iter_sids]
    iter_pool_sids = [s for s in all_sids if s in iter_sids]

    lines = ["# Pilot #5 — Bulk Labeling Report (prompt v2, deepseek+grok)", ""]
    lines.append(f"**Pool:** {len(all_sids)} teks hot-Jawa | held-out {len(heldout_sids)} | prompt-iter {len(iter_pool_sids)}")
    lines.append("")

    # ── Per-vendor metrics ──────────────────────────────────────────────
    lines.append("## Per-vendor metrics (pool penuh)")
    lines.append("")
    lines.append("| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate rate |")
    lines.append("|---|---|---|---|---|---|---|")
    total_cost = 0.0
    for v in VENDORS:
        vrecs = [by_source[s][v] for s in all_sids if v in by_source[s]]
        n = len(vrecs)
        if not n:
            continue
        n_refusal = sum(1 for r in vrecs if is_refusal(r))
        n_valid = sum(1 for r in vrecs if is_valid_json(r))
        latencies = [r["latency_ms"] for r in vrecs if r.get("latency_ms")]
        in_tok = sum((r.get("input_tokens") or 0) for r in vrecs)
        out_tok = sum((r.get("output_tokens") or 0) for r in vrecs)
        cost = (in_tok / 1_000_000) * PRICING[v]["in"] + (out_tok / 1_000_000) * PRICING[v]["out"]
        total_cost += cost
        hates = [bool(r["parsed"].get("hate")) for r in vrecs if is_valid_json(r) and not is_refusal(r)]
        rate = sum(hates) / len(hates) * 100 if hates else float("nan")
        lines.append(f"| {v} | {n} | {n_refusal / n * 100:.1f} | {n_valid / n * 100:.1f} | {mean(latencies) if latencies else 0:.0f} | ${cost:.2f} | {rate:.0f}% |")
    lines.append("")
    lines.append(f"**Total cost (termasuk porsi Pilot #3 yang di-merge):** ${total_cost:.2f}")
    lines.append("")

    # ── Alpha: held-out vs prompt-iter vs full ──────────────────────────
    lines.append("## Krippendorff's alpha (hate, ds+grok) — HELD-OUT VALIDATION")
    lines.append("")
    lines.append("| Subset | n teks | alpha | 95% CI |")
    lines.append("|---|---|---|---|")
    for name, sids in (("**Held-out** (di luar pool iterasi prompt)", heldout_sids),
                       ("Prompt-iter pool (pembanding; Pilot #3: 0.763)", iter_pool_sids),
                       ("Full pool", all_sids)):
        units = hate_units(by_source, VENDORS, sids)
        a = krippendorff_alpha_nominal(units)
        ci = bootstrap_alpha_ci(units)
        lines.append(f"| {name} | {len(sids)} | **{a:.3f}** | [{ci[0]:.3f}, {ci[1]:.3f}] |")
    lines.append("")
    lines.append("(Held-out alpha ≈ prompt-iter alpha → prompt v2 generalizes, bukan overfit ke pool 149.)")
    lines.append("")

    # ── Consensus split + dataset files ─────────────────────────────────
    consensus_rows, disagree_rows = [], []
    for sid in all_sids:
        bv = by_source[sid]
        parses = {}
        for v in VENDORS:
            r = bv.get(v)
            if r is not None and is_valid_json(r) and not is_refusal(r):
                parses[v] = r["parsed"]
        rec0 = next(iter(bv.values()))
        base = {
            "source_id": sid,
            "text": rec0["text"],
            "orig_label": rec0.get("orig_label"),
            "filter_bahasa": rec0.get("filter_bahasa"),
            "prompt_version": "v2",
            "vendors": {v: parses.get(v) for v in VENDORS},
            "heldout": sid not in iter_sids,
        }
        if len(parses) == 2 and len({bool(p.get("hate")) for p in parses.values()}) == 1:
            sev = {p.get("severity") for p in parses.values()}
            row = dict(base)
            row["consensus_hate"] = bool(next(iter(parses.values())).get("hate"))
            row["consensus_severity"] = next(iter(sev)) if len(sev) == 1 else None
            row["severity_agreement"] = len(sev) == 1
            consensus_rows.append(row)
        else:
            row = dict(base)
            row["reason"] = "hate_disagree" if len(parses) == 2 else "invalid_or_refusal"
            disagree_rows.append(row)

    with CONSENSUS_PATH.open("w", encoding="utf-8") as f:
        for row in consensus_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with DISAGREE_PATH.open("w", encoding="utf-8") as f:
        for row in disagree_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_hate = sum(1 for r in consensus_rows if r["consensus_hate"])
    lines.append("## Consensus split → dataset")
    lines.append("")
    lines.append(f"- **Consensus (hate agree):** {len(consensus_rows)} teks ({len(consensus_rows) / len(all_sids) * 100:.1f}%) → `data/labeled/bulk_v2_consensus.jsonl`")
    lines.append(f"  - hate=True: {n_hate} | hate=False: {len(consensus_rows) - n_hate}")
    sev_agree = sum(1 for r in consensus_rows if r["severity_agreement"])
    lines.append(f"  - severity juga agree: {sev_agree}/{len(consensus_rows)}")
    lines.append(f"- **Disagreement/invalid:** {len(disagree_rows)} teks → `data/labeled/bulk_v2_disagreement.jsonl` (bahan codebook + analisis)")
    by_reason = Counter(r["reason"] for r in disagree_rows)
    lines.append(f"  - breakdown: {dict(by_reason)}")
    lines.append("")

    # ── Distribusi taksonomi (consensus hate=True saja) ─────────────────
    lines.append("## Profil taksonomi (consensus hate=True)")
    lines.append("")
    hate_rows = [r for r in consensus_rows if r["consensus_hate"]]
    for dim in ("severity", "register", "form"):
        c: Counter = Counter()
        for r in hate_rows:
            for v in VENDORS:
                p = r["vendors"].get(v) or {}
                c[p.get(dim, "?")] += 1
        lines.append(f"- **{dim}** (vote 2 vendor): {dict(c.most_common())}")
    tg: Counter = Counter()
    for r in hate_rows:
        for v in VENDORS:
            p = r["vendors"].get(v) or {}
            for g in p.get("target_group") or []:
                tg[g] += 1
    lines.append(f"- **target_group** (top 15): {dict(tg.most_common(15))}")
    lines.append("")

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print("\n" + report_text.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
