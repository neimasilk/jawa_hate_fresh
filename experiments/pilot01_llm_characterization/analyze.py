"""Pilot #1 — Compute metrics dari run_pilot.py output.

Metrics:
  - Refusal rate per vendor (parsed['refusal'] == True OR error)
  - JSON validity rate per vendor (parsed has no '_parse_error')
  - Hate flag distribution per vendor
  - Inter-LLM agreement: pairwise + Krippendorff's α (untuk binary hate label)
  - Latency + token usage + estimated cost per vendor
  - Disagreement examples (sample beberapa untuk inspeksi manual)
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
LOG_PATH = OUTPUT_DIR / "pilot01_responses.jsonl"
REPORT_PATH = Path(__file__).resolve().parent / "report.md"

# Pricing approx per 1M tokens (USD) — TENTATIVE, verify dengan provider docs
# DeepSeek V4 + Kimi K2.6 belum di-verify exact, Grok 4.3 verified per xAI Apr 2026
PRICING = {
    "deepseek": {"in": 1.00, "out": 3.00},   # V4 Pro (placeholder, verify)
    "grok":     {"in": 1.25, "out": 2.50},   # Grok 4.3 (xAI direct, verified)
    "kimi":     {"in": 0.30, "out": 1.20},   # K2.6 (placeholder, verify)
}


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"No log file at {path}. Run run_pilot.py first.")
    latest: dict[tuple[str, str], dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            latest[(rec["source_id"], rec["vendor"])] = rec
    return list(latest.values())


def is_refusal(rec: dict) -> bool:
    if rec.get("error"):
        return True
    parsed = rec.get("parsed") or {}
    return bool(parsed.get("refusal"))


def is_valid_json(rec: dict) -> bool:
    parsed = rec.get("parsed") or {}
    return "_parse_error" not in parsed and not rec.get("error")


def krippendorff_alpha_nominal(units: list[list]) -> float:
    """Krippendorff's α untuk nominal data, units = list per-item per-rater values."""
    pairable = [u for u in units if sum(1 for v in u if v is not None) >= 2]
    if not pairable:
        return float("nan")

    all_vals = [v for u in pairable for v in u if v is not None]
    if not all_vals:
        return float("nan")

    categories = sorted(set(all_vals))
    n_total = len(all_vals)

    # Observed disagreement
    do_num = 0.0
    do_den = 0.0
    for u in pairable:
        ratings = [v for v in u if v is not None]
        m = len(ratings)
        if m < 2:
            continue
        for i in range(len(ratings)):
            for j in range(len(ratings)):
                if i != j and ratings[i] != ratings[j]:
                    do_num += 1
        do_den += m * (m - 1)

    do = do_num / do_den if do_den else 0.0

    # Expected disagreement
    counts = Counter(all_vals)
    de_num = 0.0
    for c1 in categories:
        for c2 in categories:
            if c1 != c2:
                de_num += counts[c1] * counts[c2]
    de_den = n_total * (n_total - 1)
    de = de_num / de_den if de_den else 0.0

    if de == 0:
        return 1.0 if do == 0 else float("nan")
    return 1.0 - (do / de)


def main() -> None:
    records = load_records(LOG_PATH)
    by_source: dict[str, dict[str, dict]] = defaultdict(dict)
    for rec in records:
        by_source[rec["source_id"]][rec["vendor"]] = rec

    vendors = sorted({r["vendor"] for r in records})

    # Per-vendor metrics
    per_vendor: dict[str, dict] = {}
    for v in vendors:
        vrecs = [r for r in records if r["vendor"] == v]
        n = len(vrecs)
        n_refusal = sum(1 for r in vrecs if is_refusal(r))
        n_valid = sum(1 for r in vrecs if is_valid_json(r))
        latencies = [r["latency_ms"] for r in vrecs if r.get("latency_ms")]
        in_tok = sum((r.get("input_tokens") or 0) for r in vrecs)
        out_tok = sum((r.get("output_tokens") or 0) for r in vrecs)
        cost = (in_tok / 1_000_000) * PRICING[v]["in"] + (out_tok / 1_000_000) * PRICING[v]["out"]

        hate_dist = Counter()
        severity_dist = Counter()
        for r in vrecs:
            if not is_valid_json(r) or is_refusal(r):
                continue
            parsed = r["parsed"]
            hate_dist[bool(parsed.get("hate"))] += 1
            severity_dist[parsed.get("severity", "?")] += 1

        per_vendor[v] = {
            "n": n,
            "refusal_rate": n_refusal / n if n else 0,
            "json_validity_rate": n_valid / n if n else 0,
            "latency_ms_mean": mean(latencies) if latencies else 0,
            "latency_ms_stdev": stdev(latencies) if len(latencies) > 1 else 0,
            "input_tokens_total": in_tok,
            "output_tokens_total": out_tok,
            "cost_usd": cost,
            "hate_dist": dict(hate_dist),
            "severity_dist": dict(severity_dist),
        }

    # Inter-LLM agreement on binary hate label (skip refusals + invalid)
    units = []
    for sid, by_vendor in by_source.items():
        vec = []
        for v in vendors:
            r = by_vendor.get(v)
            if r is None or is_refusal(r) or not is_valid_json(r):
                vec.append(None)
            else:
                vec.append(bool(r["parsed"].get("hate")))
        units.append(vec)

    alpha_hate = krippendorff_alpha_nominal(units)

    # Pairwise agreement (raw %)
    pairwise = {}
    for i, va in enumerate(vendors):
        for vb in vendors[i + 1 :]:
            agree = total = 0
            for vec in units:
                if vec[vendors.index(va)] is None or vec[vendors.index(vb)] is None:
                    continue
                total += 1
                if vec[vendors.index(va)] == vec[vendors.index(vb)]:
                    agree += 1
            pairwise[f"{va}__{vb}"] = {
                "n_pairs": total,
                "agreement_rate": agree / total if total else 0,
            }

    # Disagreement examples (max 5)
    disagreements = []
    for sid, by_vendor in by_source.items():
        labels = {}
        for v in vendors:
            r = by_vendor.get(v)
            if r and is_valid_json(r) and not is_refusal(r):
                labels[v] = bool(r["parsed"].get("hate"))
        if len(set(labels.values())) > 1:
            disagreements.append(
                {
                    "source_id": sid,
                    "text": next(iter(by_vendor.values()))["text"],
                    "labels": labels,
                }
            )
        if len(disagreements) >= 5:
            break

    # Build report
    lines = ["# Pilot #1 — LLM Characterization Report", ""]
    lines.append(f"**Total records:** {len(records)}")
    lines.append(f"**Unique source samples:** {len(by_source)}")
    lines.append(f"**Vendors:** {', '.join(vendors)}")
    lines.append("")
    lines.append("## Per-vendor metrics")
    lines.append("")
    lines.append("| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | In tok | Out tok | Cost (USD) | Hate dist |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    total_cost = 0.0
    for v in vendors:
        m = per_vendor[v]
        hate_summary = f"{m['hate_dist'].get(True, 0)}T/{m['hate_dist'].get(False, 0)}F"
        lines.append(
            f"| {v} | {m['n']} | {m['refusal_rate']*100:.1f} | {m['json_validity_rate']*100:.1f} "
            f"| {m['latency_ms_mean']:.0f} | {m['input_tokens_total']} | {m['output_tokens_total']} "
            f"| ${m['cost_usd']:.3f} | {hate_summary} |"
        )
        total_cost += m["cost_usd"]
    lines.append(f"\n**Total cost across vendors:** ${total_cost:.3f}")
    lines.append("")
    lines.append("## Inter-LLM agreement (binary hate label)")
    lines.append(f"\nKrippendorff's α (nominal): **{alpha_hate:.3f}**\n")
    lines.append("| Pair | N pairs | Agreement % |")
    lines.append("|---|---|---|")
    for pair, m in pairwise.items():
        lines.append(f"| {pair} | {m['n_pairs']} | {m['agreement_rate']*100:.1f} |")
    lines.append("")
    lines.append("## Severity distribution per vendor")
    lines.append("")
    for v in vendors:
        lines.append(f"- **{v}:** {per_vendor[v]['severity_dist']}")
    lines.append("")
    lines.append("## Sample disagreements (max 5)")
    lines.append("")
    for d in disagreements:
        lines.append(f"- `{d['source_id']}` — labels: {d['labels']}")
        lines.append(f"  > {d['text'][:200]}{'...' if len(d['text']) > 200 else ''}")
    lines.append("")
    lines.append("## Decision gate")
    lines.append("")
    lines.append("Threshold per CLAUDE.md HARD RULE #3 fallback ladder:")
    lines.append("")
    avg_refusal = mean(per_vendor[v]["refusal_rate"] for v in vendors) * 100
    avg_validity = mean(per_vendor[v]["json_validity_rate"] for v in vendors) * 100
    lines.append(f"- Avg refusal rate: **{avg_refusal:.1f}%** (target < 20%)")
    lines.append(f"- Avg JSON validity: **{avg_validity:.1f}%** (target > 90%)")
    lines.append(f"- Krippendorff's α: **{alpha_hate:.3f}** (target > 0.5)")
    lines.append("")
    if avg_refusal < 20 and avg_validity > 90 and alpha_hate > 0.5:
        lines.append("✅ **GREEN — lanjut fully-LLM framing.**")
    elif avg_refusal > 50 or avg_validity < 70 or alpha_hate < 0.2:
        lines.append("🔴 **RED — trigger fallback ladder (sanity check 50 sampel atau pending rethink).**")
    else:
        lines.append("🟡 **YELLOW — iterasi prompt (pilot #3) sebelum scale up.**")

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print("\n" + report_text.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
