"""Bootstrap confidence intervals for the detection-rate and authenticity results.

Added in the JUTIF R1 revision in response to reviewer requests for formal
statistical comparison rather than descriptive percentages alone
(Reviewer B comments 12 and 13; Reviewer A comment 6).

Prints aggregate statistics only -- never stimulus text.

Usage:  python bootstrap_ci.py
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
DETECT = HERE / "detect_results.jsonl"

N_BOOT = 10000
SEED = 20260727          # fixed so the reported intervals are reproducible
NICHE_ORDER = ["ngoko_direct", "krama_report", "krama_sarcastic", "krama_cold_contempt"]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval -- well behaved at k=0 and k=n, unlike normal approx."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def boot_ci(flags: list[int], n_boot: int = N_BOOT, seed: int = SEED) -> tuple[float, float]:
    """Percentile bootstrap CI for a proportion."""
    if not flags:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(flags)
    means = []
    for _ in range(n_boot):
        means.append(sum(rng.choice(flags) for _ in range(n)) / n)
    means.sort()
    return (means[int(0.025 * n_boot)], means[int(0.975 * n_boot)])


def fmt(k: int, n: int) -> str:
    lo_w, hi_w = wilson(k, n)
    lo_b, hi_b = boot_ci([1] * k + [0] * (n - k))
    return (f"{k}/{n} = {100*k/n:5.1f}%  "
            f"Wilson 95% CI [{100*lo_w:5.1f}, {100*hi_w:5.1f}]  "
            f"bootstrap [{100*lo_b:5.1f}, {100*hi_b:5.1f}]")


def emit_aggregate(rows: list[dict]) -> None:
    """Write niche x detector hit/total counts only.

    The raw verdict file carries the synthetic stimulus text and is therefore
    excluded from the public repository. These aggregate counts carry no text,
    so they can be released and let the figures and intervals be recomputed by
    anyone without access to the restricted stimulus set.
    """
    agg: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for r in rows:
        c = agg[r["niche"]][r["detector"]]
        c[0] += 1 if r["hate"] else 0
        c[1] += 1
    out = {n: {d: {"hate": v[0], "total": v[1]} for d, v in sorted(dd.items())}
           for n, dd in sorted(agg.items())}
    path = HERE / "detect_counts_aggregate.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote aggregate counts -> {path.name} (no stimulus text)\n")


def main() -> None:
    rows = [json.loads(l) for l in DETECT.open(encoding="utf-8")]
    rows = [r for r in rows if not r.get("error")]
    print(f"detector verdicts loaded: {len(rows)}\n")
    emit_aggregate(rows)

    # ---- detection rate per niche, pooled across the five detectors ----
    print("=" * 72)
    print("DETECTION RATE BY NICHE (pooled over 5 detectors, n=45 verdicts each)")
    print("=" * 72)
    by_niche: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_niche[r["niche"]].append(1 if r["hate"] else 0)
    for niche in NICHE_ORDER:
        f = by_niche[niche]
        print(f"  {niche:22s} {fmt(sum(f), len(f))}")

    # ---- detection rate per niche x detector ----
    print()
    print("=" * 72)
    print("DETECTION RATE BY NICHE x DETECTOR (n=9 cells each)")
    print("=" * 72)
    cell: dict[tuple[str, str], list[int]] = defaultdict(list)
    for r in rows:
        cell[(r["niche"], r["detector"])].append(1 if r["hate"] else 0)
    detectors = sorted({r["detector"] for r in rows})
    for niche in NICHE_ORDER:
        print(f"  -- {niche}")
        for d in detectors:
            f = cell[(niche, d)]
            if f:
                lo, hi = wilson(sum(f), len(f))
                print(f"       {d:14s} {sum(f)}/{len(f)} = {100*sum(f)/len(f):5.1f}%"
                      f"  Wilson 95% CI [{100*lo:5.1f}, {100*hi:5.1f}]")

    # ---- contrast: krama_sarcastic vs every other niche ----
    print()
    print("=" * 72)
    print("CONTRAST: krama_sarcastic vs other niches (pooled, bootstrap diff)")
    print("=" * 72)
    rng = random.Random(SEED)
    ks = by_niche["krama_sarcastic"]
    for niche in NICHE_ORDER:
        if niche == "krama_sarcastic":
            continue
        other = by_niche[niche]
        diffs = []
        for _ in range(N_BOOT):
            a = sum(rng.choice(ks) for _ in range(len(ks))) / len(ks)
            b = sum(rng.choice(other) for _ in range(len(other))) / len(other)
            diffs.append(b - a)
        diffs.sort()
        lo, hi = diffs[int(0.025 * N_BOOT)], diffs[int(0.975 * N_BOOT)]
        pt = sum(other) / len(other) - sum(ks) / len(ks)
        excl = "excludes 0" if lo > 0 else "INCLUDES 0"
        print(f"  {niche:22s} diff = {100*pt:5.1f} pp   95% CI [{100*lo:5.1f}, {100*hi:5.1f}]  {excl}")

    # ---- generator authenticity (counts from the validated result files) ----
    print()
    print("=" * 72)
    print("GENERATOR AUTHENTICITY (first-author validation, Table 4)")
    print("=" * 72)
    for gen, k, n in [("DeepSeek", 35, 36), ("Gemma3-27B", 20, 36), ("Qwen3-14B", 4, 36)]:
        print(f"  {gen:14s} {fmt(k, n)}")

    print()
    print("=" * 72)
    print("PAIRWISE GENERATOR CONTRASTS (authenticity, bootstrap diff)")
    print("=" * 72)
    pools = {"DeepSeek": [1] * 35 + [0] * 1,
             "Gemma3-27B": [1] * 20 + [0] * 16,
             "Qwen3-14B": [1] * 4 + [0] * 32}
    names = list(pools)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a_name, b_name = names[i], names[j]
            A, B = pools[a_name], pools[b_name]
            diffs = []
            for _ in range(N_BOOT):
                a = sum(rng.choice(A) for _ in range(len(A))) / len(A)
                b = sum(rng.choice(B) for _ in range(len(B))) / len(B)
                diffs.append(a - b)
            diffs.sort()
            lo, hi = diffs[int(0.025 * N_BOOT)], diffs[int(0.975 * N_BOOT)]
            pt = sum(A) / len(A) - sum(B) / len(B)
            excl = "excludes 0" if lo > 0 else "INCLUDES 0"
            print(f"  {a_name:12s} - {b_name:12s} diff = {100*pt:5.1f} pp"
                  f"  95% CI [{100*lo:5.1f}, {100*hi:5.1f}]  {excl}")


if __name__ == "__main__":
    main()
