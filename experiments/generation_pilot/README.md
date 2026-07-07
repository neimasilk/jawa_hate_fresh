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

## Update — 2026-06-29 sesi 5: detection probe + multi-model + QC panel

Three automated analyses (no native input) systematized FINDINGS §5 into a real matrix.
Full numbers + interpretation: **`RESULTS_probe.md`** (committed; verbatim text gitignored).

- **Detection blind-spot probe** (`detect_probe.py`, 36 cells × 5 detectors, 0 parse fails,
  recompute-verified): the headline — **krama_sarcastic (irony/pasemon) evades ALL detectors**
  (cloud 11%, local 0%), not just cheap ones; ngoko_direct 100% everywhere; krama_report 78–89%
  (cloud) → politeness alone does not blind. Corrected the earlier minimal-pair claim.
- **Multi-model generation** (`gen_local.py`, gemma3:27b + qwen3:14b): qwen3 **defaults to
  Indonesian** for krama (can't generate the uncollectable register); DeepSeek/gemma3 produce
  Javanese. Generation capability is model-dependent, mirroring detection.
- **QC judge panel** (4-agent workflow): 0 museum-krama / 0 indo-leak (advisory), flagged #21
  (sincere-blessing) + #26 (weak Arek) + 12 formulaic clones → focuses native time.
- **Form rebuilt** (`rebuild_form.py`): 108 examples (3 models), **27 PRIORITAS** rows so the
  native validates the contested ~30, not 108 blind. Scorer (`score_validation.py`) upgraded:
  per-model, model×niche, and detector-evasion×native-authenticity cross-tabs.

**Pending (the bottleneck, by design):** native authenticity validation by the expert
author — now far more informative (PRIORITAS-ordered, multi-model). A second native judge
(authenticity inter-rater reliability) remains the other open human step.

## Update — 2026-07-06 sesi 9: multi-validator forms (E1, STRATEGY.md)

Mukhlis's 55% (59/108) authenticity result is a single-evaluator estimate (paper
Limitation #1) — a real problem for anything beyond JINITA. Yekti Asmoro Kanthi is a
confirmed native Javanese speaker; Daniel Rudiaman Sijabat is **not** a native speaker
but has lived in East Java for 30 years and is highly proficient in Javanese as an
additional language (credential corrected 2026-07-07, D21 — earlier drafts of this
file wrongly called both "confirmed active Javanese speakers"). A second/third
independent judgment was still feasible from both.

1. `build_multivalidator_forms.py` — generates `VALIDATION_FORM_yekti.xlsx` +
   `VALIDATION_FORM_daniel.xlsx` from the same `_key.csv` (108 items), BLIND (no
   pre-filled verdicts, and blind to Mukhlis's answers). Adds a second judgment column
   not present in the original form: `OTENTIK?` (same question Mukhlis answered, for
   direct comparability) AND `JELAS_HATE?` (separate question — is this clearly an
   attack on group identity, independent of how authentically Javanese it sounds).
   Separating these matters because "authentic Javanese but not actually hate" (e.g.
   example #21, sarcasm read as sincere praise) and "clearly hate but not quite
   authentic-sounding" are different failure modes that a single OTENTIK column
   conflates. Never overwrites a form that already has answers.
2. **[native step, not automatable]** Give each `.xlsx` to the named validator with the
   instructions in its `Petunjuk` sheet. Ask them not to compare notes with Mukhlis or
   each other until both are done — the point is independent judgment. ~1-2 hours each,
   comprehension-only (read + judge), not annotation labor.
3. `score_multivalidator.py` — once one or both forms are filled, computes per-validator
   authenticity rate, pairwise raw agreement + canonical Krippendorff's alpha (reuses
   `src/agreement.py`, same formula as the main labeling pipeline) against Mukhlis's
   existing scored form, and the OTENTIK-vs-JELAS_HATE cross-tab → `multivalidator_result.md`.
   Safe to run before any form is filled (prints a "not yet filled" placeholder).

Run order: `python build_multivalidator_forms.py` → [Yekti/Daniel fill their .xlsx] →
`python score_multivalidator.py`.

## Update — 2026-07-07 sesi 10: results (E1 done, D21)

Both forms came back filled (`VALIDATION_FORM_yekti_FILLED.xlsx`,
`VALIDATION_FORM_daniel_FILLED.xlsx`, 108/108 rows each, genuinely blind).
`score_multivalidator.py` was re-pointed at the `_FILLED` filenames and run — see
`multivalidator_result.md` for the full table. Headline: authenticity rates were 55%
(Mukhlis), 91% (Yekti), 45% (Daniel); pairwise Krippendorff's alpha was 0.095
(Mukhlis-Yekti), 0.779 (Mukhlis-Daniel), -0.039 (Yekti-Daniel), 3-rater 0.336 — below
the conventional 0.667 threshold. This does **not** close Limitation #1 as a clean
confirmation: the two actual native speakers (Mukhlis, Yekti) disagree at a level
indistinguishable from chance. Reported honestly in `paper/draft_jinita.md` §4.7 (1)
rather than pooled into a single headline number.

> Ethics: all generated text is offensive by construction and exists solely to train/
> evaluate hate-speech **detection**. Anonymized, synthetic (no real persons), never for
> dissemination. Consistent with the project ethics statement.
