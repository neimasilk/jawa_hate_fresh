# Pilot #1b — C3 Re-test: Multi-LLM Agreement pada Hate Jawa Asli

**Status:** dibuat 2026-06-08
**Pertanyaan:** C3 — apakah multi-LLM consensus (Krippendorff's α) bekerja pada hate Jawa **asli**?

## Latar belakang

Pilot #1 gate GREEN tapi α=1.000 **degenerate**: ketiga LLM melabeli semua 100 sampel
FineWeb2 `jav_Latn` sebagai `hate=false`/BUK karena sumbernya nyaris tanpa hate.
α itu tidak bisa dipakai untuk klaim consensus.

Pilot #2 menghasilkan `hot_jawa_subset.jsonl`: 24 teks Jawa/code-mixed dari dump hate
Indonesia (haipradana), 9 di antaranya berlabel asli "hate". Ada variasi label →
α tidak lagi degenerate → sinyal C3 pertama yang real.

**Logika gate:** kalau α jelek bahkan di sini, itu temuan besar — wajib tahu SEBELUM
invest scale-up filter (Opsi B di HANDOFF).

## Cara run

```
.venv\Scripts\python experiments\pilot01b_c3_retest\run_c3.py     # ~72 call, ~40-50 mnt (Kimi lambat)
.venv\Scripts\python experiments\pilot01b_c3_retest\analyze.py    # report.md
```

Resumable: re-run `run_c3.py` skip pasangan (sample, vendor) yang sudah ada
raw_text/error di `outputs/c3_responses.jsonl` (logika sama dengan Pilot #1 pasca-patch).

## Desain

- Prompt: `prompts/cultural_classification_v0.md` (sama dengan Pilot #1 — sengaja,
  supaya beda hasil atribusi ke DATA bukan prompt).
- Vendor: DeepSeek V4 Pro + Grok 4.3 + Kimi K2.6 (sama dengan Pilot #1).
- Metrics tambahan vs Pilot #1: α severity (4 kategori), bootstrap 95% CI
  (n=24 kecil → CI wajib), majority-vote vs `orig_label` haipradana (referensi
  sanity — haipradana dianotasi Indonesia-context, BUKAN gold Jawa), listing
  SEMUA disagreement.

## Interpretasi

| Hasil | Arti | Next |
|---|---|---|
| α > 0.5, CI tidak menyentuh 0 | C3 sinyal positif | Scale filter (Opsi B) → konfirmasi di pool besar |
| α 0.2–0.5 | Boundary: inspeksi disagreement | Iterasi prompt (Pilot #3) dulu |
| α < 0.2 | Multi-LLM consensus diragukan pada hate asli | STOP scale-up; diskusi fallback ladder dengan Bapak |
