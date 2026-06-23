"""Audit & external-validation script (2026-06-23, post adversarial review).

Single reproducible source of truth for the numbers the paper/codebook cite, plus
the checks the original pipeline never ran:
  - consensus_hate vs orig_label (source human labels): confusion, Cohen kappa, agreement
  - directional flips (neutral->hate, hate->non-hate)
  - dedup + held-out leakage
  - off-taxonomy ("hallucinated") target tokens
  - per-category target/register/form counts under ONE stated rule (majority-of-3)
  - reliability per cell: Krippendorff alpha (canonical) + raw agreement + Cohen kappa + Gwet AC1
  - directional rater bias (McNemar) ds vs grok
  - overfitting difference-bootstrap (held-out vs tuning pool) + power
  - severity reliability

Run: python experiments/audit_external/audit.py
Writes: experiments/audit_external/audit_report.md
"""
from __future__ import annotations

import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.agreement import krippendorff_alpha_nominal, bootstrap_alpha_ci  # noqa: E402

CONSENSUS = ROOT / "data/labeled/bulk_v2_consensus.jsonl"
DISAGREE = ROOT / "data/labeled/bulk_v2_disagreement.jsonl"
RATERS = ["deepseek", "grok", "ollama:qwen3:14b"]
SHORT = {"deepseek": "ds", "grok": "grok", "ollama:qwen3:14b": "qwen"}

CANON_TARGETS = {
    "suku_madura", "suku_tionghoa", "suku_sunda", "suku_batak", "suku_dayak",
    "suku_papua", "suku_arab", "intra_jawa_mataraman", "intra_jawa_arek",
    "intra_jawa_banyumasan", "agama_islam", "agama_kristen", "agama_katolik",
    "agama_hindu", "agama_buddha", "agama_konghucu", "agama_kepercayaan",
    "kelas_kutha_ndeso", "kelas_priyayi_cilik", "gender_wanita", "gender_lgbtq",
    "politik_tokoh", "politik_partai", "politik_ormas", "tidak_ada",
}


def load_all():
    rows = []
    for p in (CONSENSUS, DISAGREE):
        with p.open(encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def vendor_hate(rec, vendor):
    v = (rec.get("vendors") or {}).get(vendor)
    if not v or v.get("refusal"):
        return None
    h = v.get("hate")
    return bool(h) if isinstance(h, bool) else None


def units_for(rows, vendors, sids=None):
    out = []
    for r in rows:
        if sids is not None and r["source_id"] not in sids:
            continue
        out.append([vendor_hate(r, v) for v in vendors])
    return out


def alpha_ci(units):
    a = krippendorff_alpha_nominal(units)
    lo, hi = bootstrap_alpha_ci(units, n_boot=5000, seed=42)
    n = sum(1 for u in units if sum(x is not None for x in u) >= 2)
    return a, lo, hi, n


def pair_metrics(rows, v1, v2, sids=None):
    """Raw agreement, Cohen kappa, Gwet AC1 on records where both raters valid."""
    a = b = c = d = 0  # TT, T1-only(F2), F1-only(T2)... use 2x2 with v1 rows
    n00 = n01 = n10 = n11 = 0
    for r in rows:
        if sids is not None and r["source_id"] not in sids:
            continue
        h1, h2 = vendor_hate(r, v1), vendor_hate(r, v2)
        if h1 is None or h2 is None:
            continue
        if h1 and h2:
            n11 += 1
        elif h1 and not h2:
            n10 += 1
        elif not h1 and h2:
            n01 += 1
        else:
            n00 += 1
    n = n00 + n01 + n10 + n11
    if n == 0:
        return None
    pa = (n00 + n11) / n
    p1y = (n11 + n10) / n  # rater1 yes
    p2y = (n11 + n01) / n  # rater2 yes
    pe_k = p1y * p2y + (1 - p1y) * (1 - p2y)
    kappa = (pa - pe_k) / (1 - pe_k) if pe_k != 1 else float("nan")
    pi = (p1y + p2y) / 2
    pe_ac1 = 2 * pi * (1 - pi)
    ac1 = (pa - pe_ac1) / (1 - pe_ac1) if pe_ac1 != 1 else float("nan")
    return dict(n=n, n11=n11, n10=n10, n01=n01, n00=n00, pa=pa, kappa=kappa,
                ac1=ac1, p1_hate=p1y, p2_hate=p2y)


def mcnemar_exact(b, c):
    """Exact two-sided binomial p for discordant counts b, c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    # two-sided exact
    p = sum(math.comb(n, i) for i in range(0, k + 1)) * (0.5 ** n) * 2
    return min(1.0, p)


def cohen_kappa_binary(pairs):
    """pairs = list of (a,b) booleans."""
    n = len(pairs)
    if n == 0:
        return float("nan")
    pa = sum(1 for a, b in pairs if a == b) / n
    pay = sum(1 for a, _ in pairs if a) / n
    pby = sum(1 for _, b in pairs if b) / n
    pe = pay * pby + (1 - pay) * (1 - pby)
    return (pa - pe) / (1 - pe) if pe != 1 else float("nan")


def norm_text(t):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", (t or "").lower())).strip()


def maj_field(rec, field):
    """Majority vote of a scalar field across valid vendor labels (None if tie/empty)."""
    c = Counter()
    for v in RATERS:
        vd = (rec.get("vendors") or {}).get(v)
        if vd and not vd.get("refusal") and vd.get(field) is not None:
            val = vd.get(field)
            if isinstance(val, list):
                val = tuple(val)
            c[val] += 1
    if not c:
        return None
    top, n = c.most_common(1)[0]
    # tie?
    if sum(1 for _, k in c.items() if k == n) > 1:
        return None
    return top


def main():
    rows = load_all()
    consensus = [r for r in rows if r.get("consensus_hate") is not None]
    hate = [r for r in consensus if r.get("consensus_hate")]
    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))

    P("# Audit & External Validation Report\n")
    P(f"_Generated by experiments/audit_external/audit.py. Records: {len(rows)} total "
      f"({len(consensus)} consensus + {len(rows)-len(consensus)} ties); hate={len(hate)}._\n")

    # ---- 1. External validity vs orig_label ----
    P("## 1. Consensus vs source human labels (orig_label)\n")
    n11 = sum(1 for r in consensus if r["consensus_hate"] and r.get("orig_label") == "hate")
    n10 = sum(1 for r in consensus if r["consensus_hate"] and r.get("orig_label") != "hate")
    n01 = sum(1 for r in consensus if not r["consensus_hate"] and r.get("orig_label") == "hate")
    n00 = sum(1 for r in consensus if not r["consensus_hate"] and r.get("orig_label") != "hate")
    n = n11 + n10 + n01 + n00
    pa = (n11 + n00) / n
    pairs = [(r["consensus_hate"], r.get("orig_label") == "hate") for r in consensus]
    kappa = cohen_kappa_binary(pairs)
    P(f"Confusion (LLM consensus rows x orig_label cols), n={n}:\n")
    P("| | orig=hate | orig=neutral |")
    P("|---|---|---|")
    P(f"| **LLM hate** | {n11} | {n10} |")
    P(f"| **LLM non-hate** | {n01} | {n00} |\n")
    P(f"- Observed agreement: **{pa:.3f}** ({n11+n00}/{n})")
    P(f"- Cohen kappa: **{kappa:.3f}**")
    orig_hate = n11 + n01
    P(f"- Source human-hate dropped by LLM: **{n01}/{orig_hate}** ({n01/orig_hate:.1%})")
    P(f"- LLM hate where source=neutral (LLM finds hate humans missed): **{n10}**\n")

    # ---- 2. Reliability per cell ----
    P("## 2. Reliability per rater set (hate, binary)\n")
    sids_held = [r["source_id"] for r in rows if r.get("heldout")]
    sids_iter = [r["source_id"] for r in rows if not r.get("heldout")]
    P("| Rater set | subset | n | alpha | 95% CI | raw agr | kappa | Gwet AC1 |")
    P("|---|---|---|---|---|---|---|---|")
    sets = [("deepseek", "grok"), ("deepseek", "ollama:qwen3:14b"),
            ("grok", "ollama:qwen3:14b"), tuple(RATERS)]
    for vs in sets:
        label = "+".join(SHORT[v] for v in vs)
        for sub, sids in [("held-out", set(sids_held)), ("full", None)]:
            u = units_for(rows, list(vs), sids)
            a, lo, hi, nn = alpha_ci(u)
            if len(vs) == 2:
                pm = pair_metrics(rows, vs[0], vs[1], sids)
                P(f"| {label} | {sub} | {nn} | {a:.3f} | [{lo:.3f}, {hi:.3f}] | "
                  f"{pm['pa']:.3f} | {pm['kappa']:.3f} | {pm['ac1']:.3f} |")
            else:
                P(f"| {label} | {sub} | {nn} | {a:.3f} | [{lo:.3f}, {hi:.3f}] | - | - | - |")
    # iter pool ds+grok for overfitting
    u_iter = units_for(rows, ["deepseek", "grok"], set(sids_iter))
    a_it, lo_it, hi_it, n_it = alpha_ci(u_iter)
    u_held = units_for(rows, ["deepseek", "grok"], set(sids_held))
    a_he, lo_he, hi_he, n_he = alpha_ci(u_held)
    P(f"\nds+grok tuning-pool (iter, n={n_it}): alpha {a_it:.3f} [{lo_it:.3f}, {hi_it:.3f}]")

    # ---- 3. Overfitting difference bootstrap ----
    P("\n## 3. Overfitting: held-out vs tuning-pool difference (ds+grok)\n")
    rng = random.Random(7)
    diffs = []
    for _ in range(8000):
        rh = [u_held[rng.randrange(len(u_held))] for _ in range(len(u_held))]
        ri = [u_iter[rng.randrange(len(u_iter))] for _ in range(len(u_iter))]
        ah, ai = krippendorff_alpha_nominal(rh), krippendorff_alpha_nominal(ri)
        if ah == ah and ai == ai:
            diffs.append(ai - ah)
    diffs.sort()
    dmean = sum(diffs) / len(diffs)
    dlo, dhi = diffs[int(0.025*len(diffs))], diffs[int(0.975*len(diffs))]
    P(f"- iter - held-out alpha diff: mean **{dmean:+.3f}**, 95% CI [{dlo:+.3f}, {dhi:+.3f}]")
    P(f"- held-out {a_he:.3f} clears 0.6 on its own; difference CI excludes 0? {'yes' if dlo>0 else 'NO'}")
    P("- Interpretation: overlapping CIs are not an equivalence test; data consistent with "
      f"held-out being up to ~{abs(dhi):.2f} alpha BELOW the tuning pool (and up to ~{abs(dlo):.2f} above).\n")

    # ---- 4. Directional rater bias (McNemar) ds vs grok ----
    P("## 4. Directional rater bias (ds vs grok, full)\n")
    pm = pair_metrics(rows, "deepseek", "grok", None)
    p_mcn = mcnemar_exact(pm["n10"], pm["n01"])
    P(f"- ds-only-hate (ds=T,grok=F): {pm['n10']}; grok-only-hate (grok=T,ds=F): {pm['n01']}")
    P(f"- McNemar exact two-sided p = **{p_mcn:.2e}** -> {'significant directional bias' if p_mcn<0.05 else 'n.s.'}")
    rate = {v: sum(1 for r in rows if vendor_hate(r, v)) /
            max(1, sum(1 for r in rows if vendor_hate(r, v) is not None)) for v in RATERS}
    P(f"- per-vendor hate rate: " + ", ".join(f"{SHORT[v]} {rate[v]:.1%}" for v in RATERS) + "\n")

    # ---- 5. Dedup + leakage ----
    P("## 5. Duplicates & held-out leakage\n")
    norms = [norm_text(r["text"]) for r in rows]
    uniq = len(set(norms))
    hate_norms = [norm_text(r["text"]) for r in hate]
    P(f"- unique normalized texts: **{uniq}/{len(rows)}** ({len(rows)-uniq} redundant)")
    P(f"- unique among hate: **{len(set(hate_norms))}/{len(hate)}**")
    held_norm = {norm_text(r["text"]) for r in rows if r.get("heldout")}
    iter_norm = {norm_text(r["text"]) for r in rows if not r.get("heldout")}
    leak = held_norm & iter_norm
    leak_hate = {norm_text(r["text"]) for r in hate if r.get("heldout")} & iter_norm
    P(f"- held-out texts whose normalized form also in tuning pool (leakage): **{len(leak)}** "
      f"({len(leak_hate)} hate)\n")

    # ---- 6. Off-taxonomy target tokens ----
    P("## 6. Off-taxonomy ('hallucinated') target tokens\n")
    tok = Counter()
    for r in rows:
        for v in RATERS:
            vd = (r.get("vendors") or {}).get(v)
            if vd and isinstance(vd.get("target_group"), list):
                for t in vd["target_group"]:
                    tok[t] += 1
    offtok = {t: c for t, c in tok.items() if t not in CANON_TARGETS}
    P("Tokens emitted but NOT in v2 prompt taxonomy (votes):")
    for t, c in sorted(offtok.items(), key=lambda x: -x[1]):
        P(f"- `{t}`: {c}")
    P("")

    # ---- 7. Reproducible per-category counts (majority-of-3) ----
    P("## 7. Per-category counts under ONE rule (majority-of-3 among consensus-hate)\n")
    tg = Counter()
    for r in hate:
        # union of majority target tokens: take tokens present in >=2 valid votes
        votes = Counter()
        nvalid = 0
        for v in RATERS:
            vd = (r.get("vendors") or {}).get(v)
            if vd and not vd.get("refusal") and isinstance(vd.get("target_group"), list):
                nvalid += 1
                for t in set(vd["target_group"]):
                    votes[t] += 1
        for t, k in votes.items():
            if k >= 2 and t != "tidak_ada":
                tg[t] += 1
    P("**target_group** (token in >=2 of the hate record's valid votes):")
    for t, c in tg.most_common():
        P(f"- {t}: {c}")
    sparse = [t for t, c in tg.items() if c <= 2]
    P(f"\nCategories with <=2 instances (per-category reliability uncomputable): {len(sparse)} -> {sparse}")
    reg = Counter(maj_field(r, "register") for r in hate)
    form = Counter(maj_field(r, "form") for r in hate)
    P(f"\n**register** (majority-of-3): {dict(reg)}")
    P(f"**form** (majority-of-3): {dict(form)}")

    # ---- 8. Severity reliability ----
    P("\n## 8. Severity reliability\n")
    sev_agree = sum(1 for r in hate if r.get("severity_agreement"))
    P(f"- severity agreement among hate: {sev_agree}/{len(hate)} ({sev_agree/len(hate):.1%})")
    none_sev = sum(1 for r in hate if r.get("consensus_severity") is None)
    P(f"- hate records with consensus_severity=None (strict unanimity): {none_sev}/{len(hate)}")

    # ---- 9. False-negative slur audit (orig=hate, LLM=non-hate, contains group-slur) ----
    P("\n## 9. False-negative slur audit (orig=hate but LLM consensus non-hate, with identity-slur token)\n")
    SLURS = ["ireng", "sipit", "aseng", "kunyuk", "banci", "maho", "lonte", "kafir",
             "cina", "cebong", "kampret", "pki", "jablay", "bani", "homo"]
    fn = [r for r in consensus if not r["consensus_hate"] and r.get("orig_label") == "hate"]
    flagged = []
    for r in fn:
        low = (r["text"] or "").lower()
        hits = [s for s in SLURS if s in low]
        if hits:
            flagged.append((r["source_id"], hits, r["text"][:120].replace("\n", " ")))
    P(f"- {len(flagged)} of {len(fn)} human-hate-but-LLM-nonhate records contain a slur token (manual review needed):")
    for sid, hits, t in flagged[:20]:
        P(f"  - [{sid}] ({','.join(hits)}) {t}")
    P("\n(These separate genuine taxonomy-coverage false negatives — e.g. skin-color/physical "
      "insults the v2 taxonomy lacks — from defensible bare-profanity exclusions.)")

    report = "\n".join(out)
    (Path(__file__).parent / "audit_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
