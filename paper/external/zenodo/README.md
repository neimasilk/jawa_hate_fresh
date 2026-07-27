# Provenance: `dvi_table1_snapshot.csv`

**Source file:** `D:\documents\twitter\datasets\dvi_scores.csv` (sister project, first author's own data — not part of this project's repository).
**Snapshot date:** 2026-07-09.
**Why this snapshot exists:** `paper/draft_jinita.md` Table 1 cites this sister-project dataset ([8] in the reference list), but the source lives outside this repo, which made Table 1 non-reproducible from `jawa_hate_fresh` alone. This file is a minimal, committed copy of the 10 rows/4 columns Table 1 actually uses, so the paper's numbers are checkable without access to `D:\documents\twitter`.

**Method (one sentence):** For each of 10 Indonesian regional languages, a tweet from a general-topic (non-hate-filtered), 32-city Indonesian Twitter corpus of 1,419,641 cleaned, deduplicated tweets (collected 2017–2020) is counted as "confirmed" for that language if it contains 2 or more lexically distinctive words/particles from a curated per-language lexicon (words also common in standard/informal Indonesian excluded); `detection_rate_pct` = 100 × confirmed_tweets / 1,419,641.

**Verification performed (2026-07-09):** every value in `dvi_table1_snapshot.csv` was compared directly against `D:\documents\twitter\datasets\dvi_scores.csv` (columns `language`, `speakers_M`, `confirmed_tweets`, `detection_rate`) and against the computation script `D:\documents\twitter\experiments\ideas\compute_dvi.py`. All 10 rows matched exactly (speakers, confirmed tweets, and confirmed rate for Javanese and all 9 comparison languages); the corpus total of 1,419,641 text-containing tweets was independently cross-checked against `D:\documents\twitter\experiments\active\EXP-A2_english_penetration\PAPER_FULL_DRAFT.md` ("The dataset comprises 1,419,641 text-containing tweets from 32 Indonesian provincial capital cities..."), a separate paper draft in the same sister project describing the same underlying corpus. No mismatches found — Table 1 in `paper/draft_jinita.md` was left unchanged.

**Columns:**
- `language` — regional language name (lowercase, matches source).
- `speakers_M` — estimated speaker population, millions.
- `confirmed_tweets` — count of tweets meeting the ≥2-distinctive-word threshold.
- `detection_rate_pct` — confirmed_tweets as a percentage of the 1,419,641-tweet corpus (e.g., `0.0931` = 0.0931%, i.e. 1,321/1,419,641). This is the source CSV's `detection_rate` column, renamed here for clarity; it already stores a percentage value, not a 0–1 fraction.

**Permission:** this data belongs to the first author (Mukhlis Amien) as part of an unpublished companion measurement from the `D:\documents\twitter` project. Its use here as reference [8] — an independent scarcity anchor for `jawa_hate_fresh` — was confirmed with the author's permission (decision D20, 2026-07-06; see `STRATEGY.md` §9 Q5 and `wiki/decisions.md`). Only the 10-row/4-column slice needed for Table 1 is copied here; no other part of the sister project's data or unpublished paper drafts is included or referenced.
