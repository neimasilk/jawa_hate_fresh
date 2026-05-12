# Pilot #1 — LLM Characterization Report

**Total records:** 302
**Unique source samples:** 100
**Vendors:** deepseek, grok, kimi

## Per-vendor metrics

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | In tok | Out tok | Cost (USD) | Hate dist |
|---|---|---|---|---|---|---|---|---|
| deepseek | 101 | 0.0 | 91.1 | 21316 | 132746 | 60733 | $0.315 | 0T/92F |
| grok | 100 | 0.0 | 100.0 | 10627 | 142021 | 7415 | $0.196 | 0T/100F |
| kimi | 101 | 0.0 | 1.0 | 37453 | 137406 | 103326 | $0.165 | 0T/1F |

**Total cost across vendors:** $0.676

## Inter-LLM agreement (binary hate label)

Krippendorff's α (nominal): **1.000**

| Pair | N pairs | Agreement % |
|---|---|---|
| deepseek__grok | 92 | 100.0 |
| deepseek__kimi | 1 | 100.0 |
| grok__kimi | 1 | 100.0 |

## Severity distribution per vendor

- **deepseek:** {'BUK': 92}
- **grok:** {'BUK': 100}
- **kimi:** {'BUK': 1}

## Sample disagreements (max 5)


## Decision gate

Threshold per CLAUDE.md HARD RULE #3 fallback ladder:

- Avg refusal rate: **0.0%** (target < 20%)
- Avg JSON validity: **64.0%** (target > 90%)
- Krippendorff's α: **1.000** (target > 0.5)

🔴 **RED — trigger fallback ladder (sanity check 50 sampel atau pending rethink).**