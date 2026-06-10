"""Pilot #1b — C3 re-test metrics dari run_c3.py output.

Fokus utama: Krippendorff's alpha pada data dengan VARIASI label asli
(9 hate / 15 non-hate per label haipradana) -> alpha non-degenerate pertama.

Metrics:
  - Refusal + JSON validity per vendor (sanity, sudah GREEN di Pilot #1)
  - Krippendorff's alpha: binary hate + severity (nominal) + bootstrap 95% CI
  - Pairwise agreement
  - Majority-vote vs orig_label haipradana (referensi, BUKAN gold —
    haipradana dianotasi sebagai dataset Indonesia, bukan Jawa-aware)
  - SEMUA disagreement (n kecil, listing penuh untuk inspeksi)
  - Latency + token + cost per vendor
"""
from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
LOG_PATH = OUTPUT_DIR / "c3_responses.jsonl"
REPORT_PATH = Path(__file__).resolve().parent / "report.md"

BOOTSTRAP_N = 2000
BOOTSTRAP_SEED = 42

# Pricing approx per 1M tokens (USD) — sama dengan pilot01/analyze.py
PRICING = {
    "deepseek": {"in": 1.00, "out": 3.00},
    "grok":     {"in": 1.25, "out": 2.50},
    "kimi":     {"in": 0.30, "out": 1.20},
}


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"No log file at {path}. Run run_c3.py first.")
    latest: dict[tuple[str, str], dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            latest[(rec["source_id"], rec["vendor"])] = rec  # dedup keep-last (retry menang)
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
    """Krippendorff's alpha untuk nominal data, units = list per-item per-rater values."""
    pairable = [u for u in units if sum(1 for v in u if v is not None) >= 2]
    if not pairable:
        return float("nan")

    all_vals = [v for u in pairable for v in u if v is not None]
    if not all_vals:
        return float("nan")

    categories = sorted(set(str(v) for v in all_vals))
    n_total = len(all_vals)

    do_num = 0.0
    do_den = 0.0
    for u in pairable:
        ratings = [str(v) for v in u if v is not None]
        m = len(ratings)
        if m < 2:
            continue
        for i in range(len(ratings)):
            for j in range(len(ratings)):
                if i != j and ratings[i] != ratings[j]:
                    do_num += 1
        do_den += m * (m - 1)

    do = do_num / do_den if do_den else 0.0

    counts = Counter(str(v) for v in all_vals)
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


def bootstrap_alpha_ci(units: list[list], n_boot: int = BOOTSTRAP_N, seed: int = BOOTSTRAP_SEED) -> tuple[float, float]:
    """Bootstrap 95% CI untuk alpha dengan resampling units (n kecil -> CI wajib)."""
    rng = random.Random(seed)
    alphas = []
    n = len(units)
    for _ in range(n_boot):
        resampled = [units[rng.randrange(n)] for _ in range(n)]
        a = krippendorff_alpha_nominal(resampled)
        if a == a:  # skip NaN
            alphas.append(a)
    if not alphas:
        return float("nan"), float("nan")
    alphas.sort()
    lo = alphas[int(0.025 * len(alphas))]
    hi = alphas[min(int(0.975 * len(alphas)), len(alphas) - 1)]
    return lo, hi


def main() -> None:
    records = load_records(LOG_PATH)
    by_source: dict[str, dict[str, dict]] = defaultdict(dict)
    for rec in records:
        by_source[rec["source_id"]][rec["vendor"]] = rec

    vendors = sorted({r["vendor"] for r in records})

    # ── Per-vendor metrics ──────────────────────────────────────────────
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
            "input_tokens_total": in_tok,
            "output_tokens_total": out_tok,
            "cost_usd": cost,
            "hate_dist": dict(hate_dist),
            "severity_dist": dict(severity_dist),
        }

    # ── Units untuk alpha ───────────────────────────────────────────────
    sids = sorted(by_source.keys())
    units_hate: list[list] = []
    units_severity: list[list] = []
    for sid in sids:
        by_vendor = by_source[sid]
        vec_h, vec_s = [], []
        for v in vendors:
            r = by_vendor.get(v)
            if r is None or is_refusal(r) or not is_valid_json(r):
                vec_h.append(None)
                vec_s.append(None)
            else:
                vec_h.append(bool(r["parsed"].get("hate")))
                vec_s.append(r["parsed"].get("severity"))
        units_hate.append(vec_h)
        units_severity.append(vec_s)

    alpha_hate = krippendorff_alpha_nominal(units_hate)
    alpha_hate_ci = bootstrap_alpha_ci(units_hate)
    alpha_sev = krippendorff_alpha_nominal(units_severity)
    alpha_sev_ci = bootstrap_alpha_ci(units_severity)

    # Sensitivity: drop Kimi (Pilot #1 menandai Kimi mahal+lambat+validity rendah).
    # Kalau alpha naik signifikan tanpa Kimi -> Kimi sumber noise utama, relevan
    # untuk seleksi vendor bulk pipeline.
    alpha_drop = {}
    for drop in vendors:
        keep = [v for v in vendors if v != drop]
        units_k = []
        for sid in sids:
            bv = by_source[sid]
            vec = []
            for v in keep:
                r = bv.get(v)
                vec.append(None if (r is None or is_refusal(r) or not is_valid_json(r)) else bool(r["parsed"].get("hate")))
            units_k.append(vec)
        a = krippendorff_alpha_nominal(units_k)
        ci = bootstrap_alpha_ci(units_k)
        npair = sum(1 for u in units_k if sum(1 for x in u if x is not None) >= 2)
        alpha_drop[drop] = {"keep": keep, "alpha": a, "ci": ci, "n_pairable": npair}

    # Degeneracy check: alpha bermakna hanya kalau ada variasi label
    hate_vals = Counter(v for u in units_hate for v in u if v is not None)
    is_degenerate = len(hate_vals) < 2

    # ── Pairwise agreement ──────────────────────────────────────────────
    pairwise = {}
    for i, va in enumerate(vendors):
        for vb in vendors[i + 1:]:
            agree = total = 0
            for vec in units_hate:
                a, b = vec[vendors.index(va)], vec[vendors.index(vb)]
                if a is None or b is None:
                    continue
                total += 1
                if a == b:
                    agree += 1
            pairwise[f"{va}__{vb}"] = {
                "n_pairs": total,
                "agreement_rate": agree / total if total else 0,
            }

    # ── Majority vote vs orig_label haipradana ──────────────────────────
    # CATATAN: orig_label = anotasi haipradana utk konteks INDONESIA, bukan
    # Jawa-aware. Ini referensi sanity, BUKAN gold standard.
    confusion = Counter()  # (orig_label, majority_hate)
    majority_rows = []
    for idx, sid in enumerate(sids):
        votes = [v for v in units_hate[idx] if v is not None]
        if not votes:
            continue
        maj = Counter(votes).most_common(1)[0][0] if len(set(votes)) == 1 or len(votes) >= 2 else votes[0]
        # majority = label terbanyak; tie 1-1 (1 missing) -> pakai True (conservative flag)
        c = Counter(votes)
        if len(c) > 1 and c.most_common(2)[0][1] == c.most_common(2)[1][1]:
            maj = True
        orig = next(iter(by_source[sid].values())).get("orig_label")
        confusion[(orig, maj)] += 1
        majority_rows.append({"source_id": sid, "orig_label": orig, "majority_hate": maj, "votes": dict(Counter(str(v) for v in votes))})

    # ── Semua disagreement (n kecil, listing penuh) ─────────────────────
    disagreements = []
    for idx, sid in enumerate(sids):
        labels = {}
        for v in vendors:
            r = by_source[sid].get(v)
            if r and is_valid_json(r) and not is_refusal(r):
                labels[v] = bool(r["parsed"].get("hate"))
        if len(set(labels.values())) > 1:
            rec0 = next(iter(by_source[sid].values()))
            sev = {v: by_source[sid][v]["parsed"].get("severity") for v in labels}
            disagreements.append({
                "source_id": sid,
                "orig_label": rec0.get("orig_label"),
                "text": rec0["text"],
                "labels": labels,
                "severity": sev,
            })

    # ── Build report ────────────────────────────────────────────────────
    lines = ["# Pilot #1b — C3 Re-test Report (3-LLM pada subset Jawa-panas)", ""]
    lines.append("**Pertanyaan C3:** apakah multi-LLM agreement bekerja pada hate Jawa ASLI?")
    lines.append("")
    lines.append(f"**Input:** {len(by_source)} teks `hot_jawa_subset.jsonl` (Pilot #2, haipradana code-mixed)")
    lines.append(f"**Total records:** {len(records)} | **Vendors:** {', '.join(vendors)}")
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
    lines.append(f"\n**Total cost:** ${total_cost:.3f}")
    lines.append("")
    lines.append("## Krippendorff's alpha (CORE metric C3)")
    lines.append("")
    lines.append(f"- **Binary hate:** alpha = **{alpha_hate:.3f}** (bootstrap 95% CI [{alpha_hate_ci[0]:.3f}, {alpha_hate_ci[1]:.3f}], n_boot={BOOTSTRAP_N})")
    lines.append(f"- **Severity (4 kategori):** alpha = **{alpha_sev:.3f}** (95% CI [{alpha_sev_ci[0]:.3f}, {alpha_sev_ci[1]:.3f}])")
    lines.append(f"- Label distribution (hate): {dict(hate_vals)} — {'**DEGENERATE lagi!**' if is_degenerate else 'non-degenerate, alpha bermakna'}")
    lines.append("")
    lines.append("| Pair | N pairs | Agreement % |")
    lines.append("|---|---|---|")
    for pair, m in pairwise.items():
        lines.append(f"| {pair} | {m['n_pairs']} | {m['agreement_rate']*100:.1f} |")
    lines.append("")
    lines.append("### Sensitivitas: alpha hate setelah drop 1 vendor")
    lines.append("")
    lines.append("| Drop | Keep | alpha | 95% CI | n pairable |")
    lines.append("|---|---|---|---|---|")
    for drop, m in alpha_drop.items():
        lines.append(f"| {drop} | {'+'.join(m['keep'])} | {m['alpha']:.3f} | [{m['ci'][0]:.3f}, {m['ci'][1]:.3f}] | {m['n_pairable']} |")
    lines.append("")
    lines.append("## Majority vote vs label asli haipradana")
    lines.append("")
    lines.append("(orig_label = anotasi Indonesia-context, referensi sanity — BUKAN gold)")
    lines.append("")
    lines.append("| orig_label | majority hate=True | majority hate=False |")
    lines.append("|---|---|---|")
    for orig in ("hate", "neutral"):
        t = confusion.get((orig, True), 0)
        f_ = confusion.get((orig, False), 0)
        lines.append(f"| {orig} | {t} | {f_} |")
    lines.append("")
    lines.append("## Severity distribution per vendor")
    lines.append("")
    for v in vendors:
        lines.append(f"- **{v}:** {per_vendor[v]['severity_dist']}")
    lines.append("")
    lines.append(f"## Disagreements ({len(disagreements)} dari {len(by_source)} teks)")
    lines.append("")
    for d in disagreements:
        lines.append(f"- `{d['source_id']}` (orig: {d['orig_label']}) — hate: {d['labels']} | severity: {d['severity']}")
        lines.append(f"  > {d['text'][:200]}{'...' if len(d['text']) > 200 else ''}")
    lines.append("")
    lines.append("## Decision gate C3")
    lines.append("")
    avg_refusal = mean(per_vendor[v]["refusal_rate"] for v in vendors) * 100
    avg_validity = mean(per_vendor[v]["json_validity_rate"] for v in vendors) * 100
    lines.append(f"- Avg refusal rate: **{avg_refusal:.1f}%** (target < 20%)")
    lines.append(f"- Avg JSON validity: **{avg_validity:.1f}%** (target > 90%)")
    lines.append(f"- Krippendorff's alpha (hate): **{alpha_hate:.3f}** (target > 0.5) {'[DEGENERATE - tidak bermakna]' if is_degenerate else ''}")
    lines.append("")
    if is_degenerate:
        lines.append("⚠️ **Alpha degenerate lagi — cek sumber data.**")
    elif avg_refusal < 20 and avg_validity > 90 and alpha_hate > 0.5:
        lines.append(f"✅ **GREEN — C3 terjawab positif: multi-LLM consensus bekerja pada hate Jawa asli (n={len(by_source)}).**")
    elif avg_refusal > 50 or avg_validity < 70 or alpha_hate < 0.2:
        lines.append("🔴 **RED — alpha rendah pada hate asli = temuan besar. STOP scale-up, dokumentasikan, diskusikan fallback ladder dengan Bapak.**")
    else:
        lines.append("🟡 **YELLOW — alpha moderat. Inspeksi disagreement (boundary case atau noise?), pertimbangkan iterasi prompt (Pilot #3) sebelum scale-up.**")
    lines.append("")
    lines.append(f"**Catatan:** n={len(by_source)} teks. CI bootstrap di atas WAJIB dikutip bersama alpha.")

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")
    print("\n" + report_text.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
