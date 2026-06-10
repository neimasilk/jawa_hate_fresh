"""Metrik agreement bersama untuk pilot-pilot (Krippendorff alpha + helpers).

Diekstrak dari experiments/pilot01b_c3_retest/analyze.py (frozen artifact —
tidak diubah) supaya Pilot #3+ tidak duplikasi. Logika identik.
"""
from __future__ import annotations

import json
import random
from collections import Counter
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
