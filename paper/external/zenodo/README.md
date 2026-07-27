# Digital Vitality Index for Indonesian Regional Languages on Twitter

Confirmed-tweet counts and rates for ten Indonesian regional languages, measured over a
general-topic Indonesian Twitter corpus spanning 32 cities.

This dataset is deposited as the citable record for a comparative claim in the paper
"Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection via
LLM-Generated Register-Stratified Stimuli" (Amien, Kanthi, Sijabat & Yusuf), where it
appears as Table 1. It is a companion measurement: the paper's primary evidence comes
from its own labeling run, and this measurement corroborates that evidence from an
independent direction.

## Contents

| File | Description |
|---|---|
| `dvi_table1_snapshot.csv` | Ten rows, four columns — the full dataset. |
| `README.md` | This file. |

## Columns

- `language` — regional language name.
- `speakers_M` — estimated speaker population, in millions.
- `confirmed_tweets` — number of tweets meeting the detection threshold (see Method).
- `detection_rate_pct` — `confirmed_tweets` as a percentage of the corpus. Stored as a
  percentage, not a 0–1 fraction: `0.0931` means 0.0931%, i.e. 1,321 of 1,419,641.

## Corpus

General-topic (not hate-filtered) Indonesian Twitter data collected from 32 Indonesian
provincial capital cities, 2017–2020. After cleaning and deduplication the corpus contains
**1,419,641 text-containing tweets**. Language measurement was performed over this full set.

## Method

For each of the ten languages, a tweet is counted as *confirmed* for that language if it
contains **two or more** lexically distinctive words or particles drawn from a curated
per-language lexicon. Words that are also common in standard or informal Indonesian are
excluded from every lexicon, so that shared slang and widely borrowed vocabulary do not
generate false positives. The two-marker threshold is deliberately conservative: a single
shared token is not treated as evidence.

The detection rate is computed as:

```
detection_rate_pct = 100 * confirmed_tweets / 1,419,641
```

## Interpretation and limitations

- These are **lower-bound presence estimates**, not speaker or usage statistics. A
  conservative lexicon threshold and the exclusion of Indonesian-shared vocabulary both
  push counts down; short tweets carrying only one distinctive marker are not counted.
- The measure captures *written, public* language use on one platform in one period. It
  should not be read as a measure of a language's overall vitality, which depends on
  spoken and domestic domains this corpus cannot observe.
- The cross-language comparison is meaningful because the same corpus, threshold, and
  procedure were applied to all ten languages; the absolute rates are specific to this
  corpus and this period.
- Lexicon size and coverage differ between languages, which affects sensitivity. A
  language with a smaller curated lexicon is more likely to be undercounted.

## Ethics and scope

This deposit contains **aggregate per-language counts only**. It contains no tweet text,
no usernames, no user identifiers, no geographic coordinates, and no personally
identifiable information of any kind. No individual is identifiable from these ten rows.

## Citation

If you use this dataset, please cite it via its Zenodo DOI, and where relevant also cite
the associated paper.

## Licence

Creative Commons Attribution 4.0 International (CC BY 4.0).

## Contact

Mukhlis Amien — Informatics, Universitas Bhinneka Nusantara, Malang, Indonesia
`amien@ubhinus.ac.id`
