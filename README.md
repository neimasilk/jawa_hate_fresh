# Ujaran Kebencian Jawa — Fully Automated LLM Pipeline

Riset deteksi ujaran kebencian Bahasa Jawa dengan pipeline **fully automated LLM-based annotation** sebagai core methodological contribution. Target paper Sinta 2 (JINITA), dataset HKI, codebook HKI.

**Tagline:** "Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"

## Status

Pre-eksperimen → Pilot #1. Lihat [STATE.md](STATE.md).

## Dokumen utama

- [CLAUDE.md](CLAUDE.md) — instruksi sesi Claude Code, hard rules
- [PRD.md](PRD.md) — Product Requirement Document (lihat §0 Decisions Log)
- [STATE.md](STATE.md) — live execution state + Challenges Log
- [Ujaran Kebencian Jawa_ Riset Mendalam_.md](Ujaran%20Kebencian%20Jawa_%20Riset%20Mendalam_.md) — riset mendalam (pre-pivot, sebagai background literature)

## Struktur folder

```
data/
  raw/            # raw dump dari sumber existing (gitignored)
  intermediate/   # post-filter, pre-label
  labeled/        # LLM-labeled (full dataset)
  golden/         # gold subset (kalau fallback aktif)
src/              # pipeline code (scraping/dump-loader, filter, prompt, label, train, eval)
notebooks/        # exploratory notebooks
experiments/
  pilot01_llm_characterization/
  pilot02_llm_jawa_filter/
  pilot03_cultural_prompt/
prompts/          # prompt templates (versioned)
logs/             # LLM run logs (raw responses gitignored, summaries committed)
notes/            # insight non-obvious + lessons-learned
```

## Etika

- Public posts only (tidak DM, tidak private group)
- Anonimisasi penuh sebelum analisis
- Tidak pernah re-identify individu
- Lihat ethics statement di paper / dataset card

## Authors

- Mukhlis Amien (corresponding) — amien@ubhinus.ac.id
- Yekti Asmoro Kanthi — yektiasmoro@ubhinus.ac.id
- Daniel Rudiaman Sijabat — daniel223@ubhinus.ac.id

Universitas Bhinneka Nusantara (UBHINUS / STIKI Malang).
