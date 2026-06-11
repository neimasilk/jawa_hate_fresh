"""Hitung biaya riil grok per call (filter vs labeling v2) dari log."""
import json
from pathlib import Path

for name, path, vendor in [
    ("grok FILTER", "experiments/pilot02_llm_jawa_filter/outputs/pilot02_responses.jsonl", "grok"),
    ("grok LABEL v2", "experiments/pilot05_bulk_labeling/outputs/bulk_responses.jsonl", "grok"),
    ("deepseek LABEL v2", "experiments/pilot05_bulk_labeling/outputs/bulk_responses.jsonl", "deepseek"),
]:
    tin = tout = n = 0
    for line in Path(path).open(encoding="utf-8"):
        r = json.loads(line)
        if r.get("error") or r.get("vendor") != vendor:
            continue
        tin += r.get("input_tokens") or 0
        tout += r.get("output_tokens") or 0
        n += 1
    price = {"grok": (1.25, 2.5), "deepseek": (1.0, 3.0)}[vendor]
    cost = tin / 1e6 * price[0] + tout / 1e6 * price[1]
    print(f"{name}: {n} call, ${cost:.2f} total, ${cost / n * 1000:.2f}/1000 call")
