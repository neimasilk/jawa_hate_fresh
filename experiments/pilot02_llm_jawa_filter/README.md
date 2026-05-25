# Pilot #2 — LLM-as-Jawa-filter

**Status:** RUNNING (mulai 2026-05-25)

## Tujuan ganda

1. **Pilot #2 inti:** uji apakah LLM bisa filter Jawa / code-mixed Jawa-Indonesia
   dari dump berbahasa Indonesia. Motivasi: langid Jawa low-resource → false-positive
   tinggi. Kalau LLM akurat, pipeline cascade bisa pakai LLM filter, bukan langid.
2. **Memecahkan blocker C3 Pilot #1:** Pilot #1 gate GREEN tapi α=1.000 *degenerate*
   karena sumber (FineWeb2 `jav_Latn`) nyaris tanpa hate — semua sampel BUK. Untuk
   uji multi-LLM agreement secara bermakna, butuh teks Jawa yang benar-benar
   mengandung hate. Pilot #2 mengekstrak subset "panas" tsb.

## Strategi data (keputusan 2026-05-25)

Survei menemukan: **tidak ada korpus hate speech Jawa siap-unduh**. Dataset Jawa
akademik (UI/WCSE 2021) hanya dideskripsikan di paper, tak ada rilis publik. Yang
accessible (`haipradana`, IndoToxic2024, dll) berbahasa **Indonesia**.

Keputusan: **filter dump hate Indonesia → ekstrak subset Jawa/code-mixed**, dan
**terima register code-mixed sebagai scope sah** (realita hate Jawa online memang
code-mixed). Ini:
- konsisten dengan metodologi yang diusulkan (fully-LLM pipeline, public dumps);
- pakai RAW TEXT saja, BUKAN label hate asli dataset (re-labeling kultural terpisah);
- sekaligus prototipe Pilot #2.

⚠️ **Flag novelty (untuk PRD):** karena dataset hate Jawa sudah pernah dibuat, klaim
"dataset from-scratch" perlu disandarkan ulang ke pipeline fully-automated + taksonomi
kultural lebih dalam (prior = binary hate/abusive; kita = SARA/register/pasemon
multi-dimensi) + metode zero-human. Perlu update PRD.

## Sumber

`haipradana/indonesian-twitter-hate-speech-cleaned` (HF, public) — ~12.7K train,
seimbang hate/neutral. Dipilih karena hate-dense (memaksimalkan yield Jawa-panas).

## Cara jalan

```powershell
.venv\Scripts\python.exe experiments\pilot02_llm_jawa_filter\run_filter.py
.venv\Scripts\python.exe experiments\pilot02_llm_jawa_filter\analyze.py
```

- `run_filter.py`: sampel 250 (seed 42), anonimisasi (@user/URL/RT → placeholder,
  HARD RULE #7), filter via Grok 4.3 (`prompts/jawa_filter_v0.md`), log JSON. Resume-aware.
- `analyze.py`: distribusi bahasa, yield Jawa+campuran, cross-tab × label hate,
  ekstrak `outputs/hot_jawa_subset.jsonl`, contoh per kategori → `report.md`.

## Output

- `outputs/pilot02_responses.jsonl` — log mentah filter
- `outputs/hot_jawa_subset.jsonl` — subset Jawa+campuran (kandidat sumber re-test C3)
- `report.md` — metrik + contoh

## Next setelah ini

- Kalau yield Jawa+campuran memadai → re-run karakterisasi 3-LLM Pilot #1 di
  `hot_jawa_subset.jsonl` untuk uji α non-degenerate (C3 sungguhan).
- Validasi filter vs langid baseline (formal Pilot #2, follow-up).
- Kalau yield terlalu kecil → pertimbangkan sumber lain / kontak penulis dataset Jawa.
