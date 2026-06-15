"""Metrik agreement bersama untuk pilot-pilot (Krippendorff alpha + helpers).

Asal: diekstrak dari experiments/pilot01b_c3_retest/analyze.py supaya Pilot #3+
tidak duplikasi.

Koreksi 2026-06-15 (temuan verifikasi adversarial Pilot #5):
  - `krippendorff_alpha_nominal` kini bentuk KANONIK coincidence-matrix dengan
    bobot per-unit 1/(m_u-1) (sebelumnya pooled-pairs tanpa bobot). Identik untuk
    data 2-rater (semua angka headline ds+grok tak berubah); angka 3-rater bergeser
    <=0.007. Divalidasi vs dataset rujukan Krippendorff (alpha = 0.743).
  - `is_valid_json` kini WAJIB ada key 'hate' (refusal/partial parse tak lagi
    dihitung "valid label"). Tak mempengaruhi alpha (hate_units sudah exclude
    refusal via is_refusal).
"""
from __future__ import annotations

import json
import random
from pathlib import Path

BOOTSTRAP_N = 2000
BOOTSTRAP_SEED = 42

# Pricing approx per 1M tokens (USD) — sama dengan pilot01/pilot01b
PRICING = {
    "deepseek": {"in": 1.00, "out": 3.00},
    "grok":     {"in": 1.25, "out": 2.50},
    "kimi":     {"in": 0.30, "out": 1.20},
}


def load_records(path: Path) -> list[dict]:
    """Load JSONL responses, dedup (source_id, vendor) keep-last (retry menang)."""
    if not path.exists():
        raise FileNotFoundError(f"No log file at {path}.")
    latest: dict[tuple[str, str], dict] = {}
    with path.open(encoding="utf-8-sig") as f:
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
    # valid = parse sukses, tidak error, DAN ada key 'hate' (label inti yang kita pakai)
    return "_parse_error" not in parsed and not rec.get("error") and "hate" in parsed


def krippendorff_alpha_nominal(units: list[list]) -> float:
    """Krippendorff's alpha (nominal). units = list per-item per-rater values (None = missing).

    Bentuk kanonik coincidence-matrix: tiap unit dengan m_u rater diberi bobot
    1/(m_u - 1) saat mengisi matriks koinsidensi (Krippendorff 2011). Ini PENTING
    saat jumlah rater per unit berbeda (mis. sebagian 2, sebagian 3) — bentuk
    "pooled pairs" tanpa bobot membiaskan Do. Untuk data 2-rater murni keduanya
    identik. Divalidasi vs dataset rujukan Krippendorff (alpha nominal = 0.743).
    """
    pairable = [u for u in units if sum(1 for v in u if v is not None) >= 2]
    if not pairable:
        return float("nan")

    # Matriks koinsidensi o[(c,k)] dengan bobot per-unit 1/(m_u - 1).
    o: dict[tuple[str, str], float] = {}
    for u in pairable:
        ratings = [str(v) for v in u if v is not None]
        m = len(ratings)
        if m < 2:
            continue
        w = 1.0 / (m - 1)
        for i in range(m):
            for j in range(m):
                if i != j:
                    key = (ratings[i], ratings[j])
                    o[key] = o.get(key, 0.0) + w

    categories = sorted({c for c, _ in o} | {k for _, k in o})
    n_c = {c: sum(o.get((c, k), 0.0) for k in categories) for c in categories}
    n_total = sum(n_c.values())
    if n_total < 2:
        return float("nan")

    do_sum = sum(o.get((c, k), 0.0) for c in categories for k in categories if c != k)
    de_sum = sum(n_c[c] * n_c[k] for c in categories for k in categories if c != k)
    if de_sum == 0:
        return 1.0 if do_sum == 0 else float("nan")
    # alpha = 1 - Do/De ; Do = do_sum/n, De = de_sum/(n(n-1)) -> 1 - (n-1)*do_sum/de_sum
    return 1.0 - (n_total - 1) * do_sum / de_sum


def bootstrap_alpha_ci(units: list[list], n_boot: int = BOOTSTRAP_N, seed: int = BOOTSTRAP_SEED) -> tuple[float, float]:
    """Bootstrap 95% CI untuk alpha dengan resampling units."""
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


def hate_units(by_source: dict[str, dict[str, dict]], vendors: list[str], sids: list[str]) -> list[list]:
    """Bangun units binary-hate per source untuk subset vendor tertentu."""
    units: list[list] = []
    for sid in sids:
        bv = by_source.get(sid, {})
        vec = []
        for v in vendors:
            r = bv.get(v)
            if r is None or is_refusal(r) or not is_valid_json(r):
                vec.append(None)
            else:
                vec.append(bool(r["parsed"].get("hate")))
        units.append(vec)
    return units
