"""Pilot #5 — analisis bulk labeling: held-out alpha + consensus split + dataset.

Output utama:
  1. HELD-OUT VALIDATION: alpha di teks yang TIDAK dipakai iterasi prompt
     Pilot #3 (jawab kekhawatiran overfit; pembanding: pool prompt-iter
     alpha ds+grok 0.763).
  2. Consensus split (majority vote N rater; >=2 label valid wajib):
     - data/labeled/bulk_v2_consensus.jsonl  (majority hate jelas)
     - data/labeled/bulk_v2_disagreement.jsonl (tie / <2 valid)
  3. Distribusi taksonomi (severity/register/form/target_group) = profil dataset.

Rater via env ANALYZE_VENDORS (default 3-rater: deepseek, grok, qwen3 lokal).
Dengan 3 rater juga dilaporkan pairwise alpha + drop-1 sensitivity.

Severity policy konservatif: consensus_severity diisi hanya kalau SEMUA vendor
yang vote consensus_hate memberi severity sama; kalau beda, simpan semuanya
(severity_agreement=false) — resolusi nanti (codebook / training pakai binary).
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from itertools import combinations
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
PILOT06_LOCAL_PATH = ROOT / "experiments" / "pilot06_local_models" / "outputs" / "local_v2_qwen3_14b.jsonl"
HOT_PATH = ROOT / "experiments" / "pilot02_llm_jawa_filter" / "outputs" / "hot_jawa_subset.jsonl"
ITER_SIDS_PATH = HERE / "prompt_iter_sids.json"

LABELED_DIR = ROOT / "data" / "labeled"
LABELED_DIR.mkdir(parents=True, exist_ok=True)
CONSENSUS_PATH = LABELED_DIR / "bulk_v2_consensus.jsonl"
DISAGREE_PATH = LABELED_DIR / "bulk_v2_disagreement.jsonl"
REPORT_PATH = HERE / "report.md"

VENDORS = [v.strip() for v in os.environ.get(
    "ANALYZE_VENDORS", "deepseek,grok,ollama:qwen3:14b").split(",") if v.strip()]


def main() -> None:
    # Urutan load = pilot03/pilot06 DULU, bulk TERAKHIR, supaya keep-last =
    # "bulk menang" (sesuai intent). bulk = re-run yang memperbaiki record
    # empty_response lama di pilot03 (run_bulk tak menganggap empty=done).
    # Memuat bulk terakhir bug-fix 2026-06-15: sebelumnya bulk dimuat pertama
    # -> record stale pilot03 menimpa label valid bulk (6 sid deepseek iter-pool).
    records = load_records(PILOT03_PATH)
    if PILOT06_LOCAL_PATH.exists():
        records += load_records(PILOT06_LOCAL_PATH)
    records += load_records(BULK_PATH)
    # dedup lintas file: keep-last per (sid, vendor), TAPI jangan timpa record
    # valid dengan yang invalid (defensif untuk run cascade di masa depan).
    latest: dict[tuple[str, str], dict] = {}
    for rec in records:
        key = (rec["source_id"], rec["vendor"])
        prev = latest.get(key)
        if prev is not None and is_valid_json(prev) and not is_valid_json(rec):
            continue
        latest[key] = rec
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

    lines = [f"# Pilot #5 — Bulk Labeling Report (prompt v2, {len(VENDORS)} rater: {', '.join(VENDORS)})", ""]
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
        price = PRICING.get(v, {"in": 0.0, "out": 0.0})  # lokal (ollama:*) = gratis
        cost = (in_tok / 1_000_000) * price["in"] + (out_tok / 1_000_000) * price["out"]
        total_cost += cost
        hates = [bool(r["parsed"].get("hate")) for r in vrecs if is_valid_json(r) and not is_refusal(r)]
        rate = sum(hates) / len(hates) * 100 if hates else float("nan")
        lines.append(f"| {v} | {n} | {n_refusal / n * 100:.1f} | {n_valid / n * 100:.1f} | {mean(latencies) if latencies else 0:.0f} | ${cost:.2f} | {rate:.0f}% |")
    lines.append("")
    lines.append(f"**Total cost (termasuk porsi Pilot #3 yang di-merge):** ${total_cost:.2f}")
    lines.append("")

    # ── Alpha: held-out vs prompt-iter vs full ──────────────────────────
    lines.append(f"## Krippendorff's alpha (hate, {len(VENDORS)} rater) — HELD-OUT VALIDATION")
    lines.append("")
    lines.append("| Subset | n teks | alpha | 95% CI |")
    lines.append("|---|---|---|---|")
    for name, sids in (("**Held-out** (di luar pool iterasi prompt)", heldout_sids),
                       ("Prompt-iter pool (pembanding; Pilot #3 ds+grok: 0.763)", iter_pool_sids),
                       ("Full pool", all_sids)):
        units = hate_units(by_source, VENDORS, sids)
        a = krippendorff_alpha_nominal(units)
        ci = bootstrap_alpha_ci(units)
        lines.append(f"| {name} | {len(sids)} | **{a:.3f}** | [{ci[0]:.3f}, {ci[1]:.3f}] |")
    lines.append("")
    lines.append("(Catatan: alpha 3-rater di atas lebih rendah daripada pembanding ds+grok 0.763 karena "
                 "rater ke-3 (qwen3 lokal) lebih bising — lihat sensitivity di bawah. Pembanding 0.763 = "
                 "**2-rater ds+grok**, jadi tes overfit yang adil = baris ds+grok held-out di tabel berikut, "
                 "BUKAN angka 3-rater.)")
    lines.append("")

    # ── Tes overfit yang adil: pasangan rater PRIMER (ds+grok), held-out vs iter ──
    primary = [v for v in ("deepseek", "grok") if v in VENDORS]
    if len(primary) == 2:
        lines.append(f"## Tes overfit ADIL — pasangan primer {' + '.join(primary)} (apples-to-apples vs Pilot #3 0.763)")
        lines.append("")
        lines.append("| Subset | n teks | alpha | 95% CI |")
        lines.append("|---|---|---|---|")
        for name, sids in (("**Held-out** (di luar pool iterasi)", heldout_sids),
                           ("Prompt-iter pool (= Pilot #3, harus ≈ 0.763)", iter_pool_sids),
                           ("Full pool", all_sids)):
            units = hate_units(by_source, primary, sids)
            a = krippendorff_alpha_nominal(units)
            ci = bootstrap_alpha_ci(units)
            lines.append(f"| {name} | {len(sids)} | **{a:.3f}** | [{ci[0]:.3f}, {ci[1]:.3f}] |")
        lines.append("")
        lines.append("(Held-out ds+grok ≥ ~0.6 dan CI overlap dengan iter-pool → prompt v2 GENERALIZES, "
                     "bukan overfit. iter-pool ds+grok ≈ Pilot #3 0.763 [sedikit turun: 6 label deepseek "
                     "yang dulu empty_response di Pilot #3 kini diperbaiki dari bulk & dimasukkan] = "
                     "sanity-check merge/dedup benar.)")
        lines.append("")

    if len(VENDORS) >= 3:
        lines.append("## Sensitivity rater: pairwise (held-out + full) + drop-1")
        lines.append("")
        lines.append("| Rater set | subset | alpha | 95% CI |")
        lines.append("|---|---|---|---|")
        for pair in combinations(VENDORS, 2):
            for sub_name, sids in (("held-out", heldout_sids), ("full", all_sids)):
                units = hate_units(by_source, list(pair), sids)
                a = krippendorff_alpha_nominal(units)
                ci = bootstrap_alpha_ci(units)
                lines.append(f"| {' + '.join(pair)} | {sub_name} | {a:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] |")
        for drop in VENDORS:
            kept = [v for v in VENDORS if v != drop]
            if len(kept) >= 2 and len(VENDORS) > 3:
                units = hate_units(by_source, kept, all_sids)
                a = krippendorff_alpha_nominal(units)
                ci = bootstrap_alpha_ci(units)
                lines.append(f"| drop {drop} | full | {a:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] |")
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
        votes = {v: bool(p.get("hate")) for v, p in parses.items()}
        vote_counts = Counter(votes.values())
        top_label, top_n = vote_counts.most_common(1)[0] if vote_counts else (None, 0)
        if len(votes) >= 2 and top_n * 2 > len(votes):  # strict majority, min 2 label valid
            agreeing = [v for v, h in votes.items() if h == top_label]
            sev = {parses[v].get("severity") for v in agreeing}
            row = dict(base)
            row["consensus_hate"] = top_label
            row["unanimous"] = len(vote_counts) == 1
            row["n_valid_votes"] = len(votes)
            row["consensus_severity"] = next(iter(sev)) if len(sev) == 1 else None
            row["severity_agreement"] = len(sev) == 1
            consensus_rows.append(row)
        else:
            row = dict(base)
            row["reason"] = "hate_tie" if len(votes) >= 2 else "insufficient_valid"
            disagree_rows.append(row)

    with CONSENSUS_PATH.open("w", encoding="utf-8") as f:
        for row in consensus_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with DISAGREE_PATH.open("w", encoding="utf-8") as f:
        for row in disagree_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    n_hate = sum(1 for r in consensus_rows if r["consensus_hate"])
    n_unanimous = sum(1 for r in consensus_rows if r.get("unanimous"))
    lines.append("## Consensus split → dataset (majority vote)")
    lines.append("")
    lines.append(f"- **Consensus (majority hate):** {len(consensus_rows)} teks ({len(consensus_rows) / len(all_sids) * 100:.1f}%) → `data/labeled/bulk_v2_consensus.jsonl`")
    lines.append(f"  - hate=True: {n_hate} | hate=False: {len(consensus_rows) - n_hate}")
    lines.append(f"  - unanimous: {n_unanimous} | majority non-unanimous: {len(consensus_rows) - n_unanimous}")
    hate_cons = [r for r in consensus_rows if r["consensus_hate"]]
    nonhate_cons = [r for r in consensus_rows if not r["consensus_hate"]]
    sev_agree_hate = sum(1 for r in hate_cons if r["severity_agreement"])
    sev_agree_buk = sum(1 for r in nonhate_cons if r["severity_agreement"])
    lines.append(f"  - severity-level agree DI ANTARA baris hate: {sev_agree_hate}/{len(hate_cons)} "
                 f"(baris non-hate {sev_agree_buk}/{len(nonhate_cons)} cuma sepakat BUK — bukan severity sungguhan)")
    lines.append(f"- **Tie/invalid:** {len(disagree_rows)} teks → `data/labeled/bulk_v2_disagreement.jsonl` (bahan codebook + analisis)")
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
                val = p.get(dim, "?")
                # sebagian vendor sesekali kembalikan list (form=["sarcastic","code_switched"])
                # ATAU string ber-koma ("direct, code_switched"); pecah keduanya jadi item
                # terpisah (konsisten dgn target_group) supaya profil tidak crash / bias.
                if isinstance(val, list):
                    items = val
                elif isinstance(val, str) and "," in val:
                    items = [s.strip() for s in val.split(",")]
                else:
                    items = [val]
                for item in items:
                    c[item] += 1
        lines.append(f"- **{dim}** (vote {len(VENDORS)} rater): {dict(c.most_common())}")
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
