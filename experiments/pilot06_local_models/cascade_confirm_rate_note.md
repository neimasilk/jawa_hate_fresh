# Reproducibility note: the "25.4%" cascade cloud-confirmation rate (paper §3.1)

**Question investigated (2026-07-09):** `paper/draft_jinita.md` §3.1 states "The cascade's cloud confirmation rate of **25.4%** for pre-screen survivors." A prior session's secondary note said "1687→+304" (= 18.0%), and the exact provenance of 25.4% was not recorded anywhere reproducible. This note documents a direct recomputation from the committed pipeline artifacts (no offensive verbatim text below — counts only).

## Recomputation from committed data

Source files (both committed, both counts-only reproducible):
- `experiments/pilot02_llm_jawa_filter/outputs/cascade_pass2_qwen3_14b.jsonl` — pass-2 (qwen3 re-screen) keeps: candidates handed to Grok for pass-3 verification.
- `experiments/pilot02_llm_jawa_filter/outputs/pilot02_responses.jsonl` — pass-3 Grok verify results (pool-authority log), which also contains original (pre-cascade) Grok filter calls.

Recompute (dedup keep-last per `source_id`, matching `run_cascade.py`'s own `load_keeps` logic):

| Quantity | Value |
|---|---|
| Pass-2 (qwen3) keeps handed to Grok verify | 1,687 |
| Of those, verified by Grok (valid parse, any category) | 1,686 (1 candidate never received a valid verify record) |
| Of those, confirmed `jawa`/`campuran` by Grok | 403 |
| **Overall confirm rate (403/1,687)** | **23.9%** |

## Splitting by the xAI-403 outage (2026-06-18 → resume 2026-06-22)

Using each record's `ts` timestamp to separate verify calls made before the outage from those made after resuming:

| Batch | Verified | Confirmed | Confirm rate |
|---|---|---|---|
| Pre-outage (ts < 2026-06-19) | 389 | 99 | **99/389 = 25.45% ≈ 25.4%** |
| Post-resume (ts ≥ 2026-06-19) | 1,297 | 304 | 304/1,297 = 23.4% |
| **Total** | **1,686** | **403** | **23.9%** |

## Finding

The paper's cited **25.4%** reproduces **exactly** — but as the confirm rate of the *first, pre-outage verification batch only* (99 of the 389 candidates Grok verified on 2026-06-18, before hitting the xAI credit-exhaustion 403 error), not as the confirm rate of the full cascade. The full-pipeline confirm rate (all 1,687 pass-2 candidates verified across both the pre-outage and the 2026-06-22 resumed run) is **23.9%** (403/1,687), close to but distinct from 25.4%.

This matches the "pool sempat mentok 431" note already in `STATE.md`/`wiki/decisions.md` (332 starting pool + 99 pre-outage confirms = 431) and the commit message of `eccc3f4` ("confirm-rate 25.4% -> +304 keeps", which conflated the pre-outage batch's rate with the post-resume batch's keep-count in one sentence — the likely origin of the ambiguity).

**Disposition:** per task instructions, since a reproducing computation was found, the paper text is left unchanged. Whoever revisits §3.1 wording later should decide whether "25.4%" (accurate for the pre-outage batch specifically) or "23.9%" (accurate for the whole cascade, arguably the more natural reading of "the cascade's... confirmation rate") is the intended claim, and word the sentence to disambiguate which batch it refers to.

Recompute script used: ad-hoc, not committed (pure aggregation over the two jsonl files above using each record's `source_id` and `ts` fields; no offensive text loaded or printed, only counts).
