# Inter-rater reliability — native authenticity validation

Validators with data: mukhlis, yekti, daniel

## Per-validator authenticity rate

| validator | authentic | rate |
|---|---|---|
| mukhlis | 59/108 | 55% |
| yekti | 98/108 | 91% |
| daniel | 49/108 | 45% |

## Pairwise inter-rater reliability (OTENTIK)

| pair | n shared | raw agreement | Krippendorff alpha | 95% CI |
|---|---|---|---|---|
| mukhlis vs yekti | 108 | 69/108 (64%) | 0.095 | [-0.109, 0.293] |
| mukhlis vs daniel | 108 | 96/108 (89%) | 0.779 | [0.650, 0.889] |
| yekti vs daniel | 108 | 59/108 (55%) | -0.039 | [-0.220, 0.146] |

**All-3-validator alpha** (n=108): 0.336 [0.224, 0.449]

## yekti: OTENTIK vs JELAS_HATE cross-tab

| | JELAS_HATE=1 | JELAS_HATE=0 |
|---|---|---|
| OTENTIK=1 | 43 | 55 |
| OTENTIK=0 | 8 | 2 |

63/108 items diverge (authentic-but-not-clearly-hate, or vice versa) — these are the cases where the single-dimension OTENTIK column in the original form would have been ambiguous.

## daniel: OTENTIK vs JELAS_HATE cross-tab

| | JELAS_HATE=1 | JELAS_HATE=0 |
|---|---|---|
| OTENTIK=1 | 30 | 19 |
| OTENTIK=0 | 22 | 37 |

41/108 items diverge (authentic-but-not-clearly-hate, or vice versa) — these are the cases where the single-dimension OTENTIK column in the original form would have been ambiguous.

## Interpretation guide
- High pairwise agreement / alpha => the 55% single-evaluator authenticity rate generalizes across native speakers, closing Limitation #1 in the paper.
- Low agreement => authenticity judgment is itself noisy/subjective for some items; report per-validator rates separately rather than a pooled headline number.
- Large OTENTIK/JELAS_HATE divergence => the two dimensions genuinely need to stay separate in future validation rounds (don't collapse back into one column).