# Disagreement diagnosis + E6-lite cross-tab (P0-2/P0-3/P0-4, STRATEGY.md SS12)

Reproduced from `VALIDATION_FORM.xlsx` (Mukhlis) + `VALIDATION_FORM_{yekti,daniel}_FILLED.xlsx` + `_key.csv`. No new native input. See module docstring for the independent-verification note.

## Mukhlis vs yekti: disagreement rows

- **n disagreement = 39**
  - direction (Mukhlis=0, yekti=1): 39
- niche breakdown: krama_sarcastic=19, krama_report=10, krama_cold_contempt=5, ngoko_direct=5
  - **krama_sarcastic: 19/39 = 49% of all yekti disagreements** (this is the correct denominator; do not confuse with the niche's own 19/27 = 70% share of disagreement WITHIN that niche -- both are true, they answer different questions, see STRATEGY.md P0-1)
- yekti's JELAS_HATE among these disagreement rows: 0=34, 1=5
- rows whose yekti CATATAN mentions code-mixing ('campur'): 31 (of which 31 also have JELAS_HATE=0 -- fully nested)

## Mukhlis vs daniel: disagreement rows

- **n disagreement = 12**
  - direction (Mukhlis=1, daniel=0): 11
  - direction (Mukhlis=0, daniel=1): 1
- niche breakdown: ngoko_direct=5, krama_report=5, krama_sarcastic=1, krama_cold_contempt=1
  - **ngoko_direct: 5/12 = 42% of all daniel disagreements** (this is the correct denominator; do not confuse with the niche's own 5/27 = 19% share of disagreement WITHIN that niche -- both are true, they answer different questions, see STRATEGY.md P0-1)
- daniel's JELAS_HATE among these disagreement rows: 0=3, 1=9
- rows whose daniel CATATAN mentions code-mixing ('campur'): 0 (of which 0 also have JELAS_HATE=0 -- fully nested)
- rows where daniel marks JELAS_HATE=1 but OTENTIK=0 (register doubt despite recognizing hate content): 9/12

## Harmonized alpha (OTENTIK AND JELAS_HATE)

Tests whether Mukhlis's single-column instrument conflated the two questions Yekti/Daniel's two-column form kept separate. Uses all 108 items, not just the disagreement subset.

| pair | raw OTENTIK alpha | harmonized alpha | 95% CI |
|---|---|---|---|
| mukhlis vs yekti | 0.095 | 0.519 | [0.352, 0.667] |
| mukhlis vs daniel | 0.779 | 0.448 | [0.274, 0.605] |
| yekti vs daniel | -0.039 | 0.609 | [0.430, 0.754] |

## P0-3(a): JELAS_HATE rate per niche per validator

| niche | yekti | daniel |
|---|---|---|
| ngoko_direct | 25/27 (93%) | 23/27 (85%) |
| krama_report | 8/27 (30%) | 11/27 (41%) |
| krama_sarcastic | 0/27 (0%) | 0/27 (0%) |
| krama_cold_contempt | 18/27 (67%) | 18/27 (67%) |

## P0-3(b): JELAS_HATE x machine_caught cross-tab (36 DeepSeek cells with detector data)

### yekti

| machine_caught | JELAS_HATE=1 | JELAS_HATE=0 |
|---|---|---|
| 0/5 | 0 | 9 |
| 1/5 | 1 | 2 |
| 3/5 | 1 | 3 |
| 4/5 | 2 | 1 |
| 5/5 | 17 | 0 |

### daniel

| machine_caught | JELAS_HATE=1 | JELAS_HATE=0 |
|---|---|---|
| 0/5 | 0 | 9 |
| 1/5 | 1 | 2 |
| 3/5 | 3 | 1 |
| 4/5 | 3 | 0 |
| 5/5 | 16 | 1 |

**The 9 cells that evade ALL 5 detectors** (17, 20, 21, 22, 24, 25, 26, 34, 36):

| niche | yekti JELAS_HATE | daniel JELAS_HATE |
|---|---|---|
| krama_report | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_sarcastic | 0 | 0 |
| krama_cold_contempt | 0 | 0 |
| krama_sarcastic | 0 | 0 |

**0/9 (yekti) and 0/9 (daniel) of the all-detector-evading cells are rated JELAS_HATE=1.** This bears directly on SS4.5's claim that "the hate that detectors miss is real Javanese hate" -- see STRATEGY.md P0-3 guard rail: do not rewrite SS4.5 before this number is reviewed with Bapak if it weakens the claim.

## P0-3(c): Yekti-Daniel Krippendorff alpha on JELAS_HATE (raw, never computed before)

alpha = 0.908 [0.815, 0.981] (n=108)

Compare to Yekti-Daniel OTENTIK alpha = -0.039 (chance-or-below) and harmonized alpha above -- JELAS_HATE alone agrees far better than OTENTIK alone or the raw pool, though high agreement here is partly driven by the KRAMA_SARCASTIC 0% prevalence (see P0-3(a)) inflating chance agreement; read alongside the per-niche table, not in isolation.

## P0-4: per-model x per-validator authenticity table

| model | Mukhlis | Yekti | Daniel |
|---|---|---|---|
| deepseek | 35/36 (97%) | 36/36 (100%) | 35/36 (97%) |
| gemma3:27b | 20/36 (56%) | 35/36 (97%) | 14/36 (39%) |
| qwen3:14b | 4/36 (11%) | 27/36 (75%) | 0/36 (0%) |

DeepSeek ranks #1 across all three validators (the relative model ordering deepseek > gemma3:27b > qwen3:14b also holds for all three) -- the headline generator-quality ranking is robust to which native validator scores it, even though absolute rates differ (Yekti's overall leniency shows up per-model too).
