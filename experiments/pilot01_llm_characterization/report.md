# Pilot #1 — LLM Characterization Report

**Total records:** 300
**Unique source samples:** 100
**Vendors:** deepseek, grok, kimi

## Per-vendor metrics

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | In tok | Out tok | Cost (USD) | Hate dist |
|---|---|---|---|---|---|---|---|---|
| deepseek | 100 | 1.0 | 97.0 | 20159 | 131498 | 57893 | $0.305 | 0T/96F |
| grok | 100 | 0.0 | 100.0 | 10627 | 142021 | 7415 | $0.196 | 0T/100F |
| kimi | 100 | 0.0 | 85.0 | 91357 | 136107 | 259936 | $0.353 | 0T/85F |

**Total cost across vendors:** $0.854

## Inter-LLM agreement (binary hate label)

Krippendorff's α (nominal): **1.000**

| Pair | N pairs | Agreement % |
|---|---|---|
| deepseek__grok | 96 | 100.0 |
| deepseek__kimi | 81 | 100.0 |
| grok__kimi | 85 | 100.0 |

## Severity distribution per vendor

- **deepseek:** {'BUK': 96}
- **grok:** {'BUK': 100}
- **kimi:** {'BUK': 85}

## Sample disagreements (max 5)


## Decision gate

Threshold per CLAUDE.md HARD RULE #3 fallback ladder:

- Avg refusal rate: **0.3%** (target < 20%)
- Avg JSON validity: **94.0%** (target > 90%)
- Krippendorff's α: **1.000** (target > 0.5)

✅ **GREEN — lanjut fully-LLM framing.**