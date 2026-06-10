# Pilot #5 — Bulk Labeling (produksi pertama)

**Tujuan:** dataset berlabel pertama dari pipeline penuh: filter full haipradana → pool hot-Jawa (~950 est) → label prompt v2 × deepseek+grok (D15) → consensus split → **held-out validation α** (jawab kekhawatiran overfit prompt v2 ke pool iterasi 149).

## Pipeline (urutan)

1. **Filter full** (Pilot #2 infra): `run_filter.py` N_SAMPLE=full (~12.7K; resume skip 2000 lama → ~10.7K call Grok baru, est 8-14 jam).
2. **Regenerate pool:** `experiments/pilot02_llm_jawa_filter/analyze.py` → tulis ulang `hot_jawa_subset.jsonl`.
3. **Bulk label:** `run_bulk.py` — pool × 2 vendor, prompt v2. Skip otomatis 149×2 yang sudah dilabel di Pilot #3 (di-merge saat analisis). Est ~800 teks baru × 2 × ~27s ≈ 6 jam, ~$8.
4. **Analisis:** `analyze.py` →
   - α held-out (`prompt_iter_sids.json` = snapshot 149) vs prompt-iter vs full
   - `data/labeled/bulk_v2_consensus.jsonl` (kedua vendor agree → label final)
   - `data/labeled/bulk_v2_disagreement.jsonl` (bahan codebook)
   - profil taksonomi (severity/register/form/target_group)

## Interpretasi held-out

- α held-out ≈ 0.763 (CI overlap) → v2 generalizes ✅, consensus dataset sah.
- α held-out jauh di bawah (mis. < 0.6) → indikasi overfit ke pool 149 → diskusi: prompt robustness perlu re-iterasi di pool campuran.

## Ketahanan

Semua runner resume-aware + 429-aware (`f.flush()` per record; rerun = lanjut dari sisa). Kalau mesin mati: jalankan ulang command yang sama.

## Status

| Tahap | Status |
|---|---|
| Filter full ~12.7K | 🔄 launched 2026-06-10 |
| Bulk label v2 ds+grok | ⏳ menunggu filter |
| Analisis + dataset | ⏳ |
