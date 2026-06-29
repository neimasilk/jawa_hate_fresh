# Generation Pilot — LLM as Javanese hate GENERATOR

The pivot direction (2026-06-23): instead of *filtering+labeling* the Indonesian
`haipradana` dump for the rare Javanese tweets (0.9% yield), **generate** fresh,
register-stratified, culturally-grounded Javanese hate with an LLM and have the
native expert validate authenticity. For a hate-speech **detection** dataset
(defensive/academic use only).

Grounded in `experiments/register_probe/FINDINGS.md` (register-pragmatics = candidate
core novelty). This pilot operationalizes FINDINGS §5's open questions as a real matrix.

## The matrix

4 register-pragmatic **niches** × 9 SARA **targets** = 36 cells, one example per cell.

| niche | register-pragmatic mode (FINDINGS §1) |
|---|---|
| `ngoko_direct` | N1 — hot, vulgar, open attack |
| `krama_report` | N2 — polite surface, derogate an absent group (*ngrasani*), defer to listener |
| `krama_sarcastic` | N3a — weaponized over-praise / irony / *pasemon* (implicature) |
| `krama_cold_contempt` | **N3b-group** — cold moral/hierarchical superiority over a SARA group (the open question) |

Targets: suku_madura, suku_tionghoa, suku_arab, agama_islam, agama_kristen,
gender_wanita, gender_lgbtq, politik_kolektif, intra_jawa_arek_vs_mataraman.

## Files / pipeline

1. `generate.py` — per-niche batched DeepSeek calls → `generated_pilot.jsonl`.
   Resume-aware (skips niches already present). Robust against the reasoning-model
   empty-content trap (retries with a bigger token budget on truncation).
2. `review_generated.py` — non-native auto-triage (museum-krama / indo-leak /
   register-mismatch heuristics + coverage matrix) → `review_report.md`,
   and the native validation form → `VALIDATION_FORM.xlsx` + `_key.csv`.
3. **[native step]** Bapak fills `VALIDATION_FORM.xlsx` col G (OTENTIK? 1/0) + H (MASALAH).
4. `score_validation.py` — authenticity rate overall / per-niche / per-target +
   failure reasons + heuristic-vs-native check → `validation_result.md`.

Run: `python experiments/generation_pilot/generate.py` then `... review_generated.py`.

## Result — run 2026-06-29 (DeepSeek `deepseek-v4-pro`, 4 calls)

- **35/36 cells generated** (missing: krama_sarcastic × suku_arab, dropped during a
  truncation-retry; re-runnable). ~few cents.
- Auto-triage: **0 museum-krama leaks** (anti-archaic guardrail held), 2 indo-leak? and
  3 register-mismatch flags — all heuristic false-positives on inspection (markers not in
  the wordlist; `campur` = legitimate code-mixing).
- **N3b group-directed krama cold-contempt produced consistent candidates** — the model
  converged on a recurring device: accusing the group of lacking *isin / unggah-ungguh*
  (shame / manners). This is the structural answer to FINDINGS §5's open question; the
  recurring single device is exactly what native validation must judge (authentic vs formulaic).
- Other niches also formulaic at the opener level (krama_report → every line opens "Mugi
  tiyang … enggal …"). Authentic pattern, but diversity is a native-validation question.

**Pending (the bottleneck, by design):** native authenticity validation by the expert
author. After that: systematize per FINDINGS §5 — multiple generator models (inter-model
comparison), a second native judge (authenticity inter-rater reliability), and the
regional axis (does the LLM default to Central-Java krama and erase Arek/East-Java?).

> Ethics: all generated text is offensive by construction and exists solely to train/
> evaluate hate-speech **detection**. Anonymized, synthetic (no real persons), never for
> dissemination. Consistent with the project ethics statement.
