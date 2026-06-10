# Pilot #3 — Cultural Prompt Iteration

**Tujuan:** angkat inter-LLM agreement (α) dengan memperbaiki PROMPT, berdasarkan diagnosis disagreement C3 n=149 (Pilot #1b). Baseline v0: α full-3LLM **0.587** (CI [0.475, 0.698]), α deepseek+grok **0.534**.

**Diagnosis v0 (dari 36 disagreement n=149):**
- Sumber disagreement #1 = boundary **profanity vs hate**: Grok melabeli umpatan kasar non-group-directed (asw, bodo anjir, kritik politik pedas) sebagai hate "ringan" (hate rate 77% vs deepseek 51% / kimi 50%).
- Root cause ada di prompt v0 SENDIRI: system prompt menyebut "ujaran kebencian bisa muncul lewat kekasaran leksikal", dan Contoh 1 few-shot melabeli umpatan personal murni (`Dasar asu! Kowe ki pancen jancuk!`, target `tidak_ada`) sebagai `hate:true, berat`. Grok mengikuti instruksi literal; deepseek/kimi mengabaikannya → split sistematis. **Lesson paper: inkonsistensi internal prompt = sumber inter-LLM disagreement yang bisa diukur.**

**Hipotesis v1:** definisi hate group/identity-directed yang eksplisit + few-shot yang konsisten → hate-rate Grok turun, α (terutama pair deepseek+grok) naik.

## Protokol per iterasi

1. Tulis `prompts/cultural_classification_vN.md` (perubahan TERFOKUS, 1 hipotesis per versi; dokumentasikan di tabel "Catatan iterasi" dalam file prompt).
2. Eval di pool sama (149 teks `hot_jawa_subset.jsonl`):
   ```
   # stage cepat: pair kunci dulu (~50 mnt)
   $env:P3_PROMPT_VERSION="v1"; $env:P3_VENDORS="deepseek,grok"; .venv\Scripts\python experiments\pilot03_cultural_prompt\run_eval.py
   # kimi menyusul (resume-aware, skip yang sudah ada; ~5 jam)
   $env:P3_PROMPT_VERSION="v1"; $env:P3_VENDORS="kimi"; .venv\Scripts\python experiments\pilot03_cultural_prompt\run_eval.py
   ```
3. Analisis komparatif vs baseline v0 (Pilot #1b):
   ```
   $env:P3_PROMPT_VERSION="v1"; .venv\Scripts\python experiments\pilot03_cultural_prompt\analyze.py
   ```
   → `report_v1.md`: Δα per vendor-set, flip table per vendor (T→F vs F→T), hate-rate shift, disagreement listing.
4. Keep/discard (threshold Δα ±0.05) → catat lesson → iterasi berikut.

## Keputusan yang menunggu hasil

- **Vendor mix bulk:** kalau α deepseek+grok naik mendekati/melewati α full (0.587) → 2-LLM deepseek+grok untuk bulk (tercepat+termurah+validity 97.7%). Kimi hanya triangulasi sampel.
- **Catatan kontaminasi:** few-shot vN TIDAK boleh memakai teks dari pool eval 149 (semua contoh baru = sintetis analog).

## Biaya per iterasi

deepseek+grok ≈ $0.95, +kimi ≈ $0.63. Budget total Pilot #3 (5-10 iterasi, sebagian tanpa kimi): ~$5-10.

## Status

| Versi | Tgl run | α ds+grok (Δ vs 0.534) | α 3-LLM (Δ vs 0.587) | Keputusan |
|---|---|---|---|---|
| v1 | 2026-06-10 (launched) | pending | pending | pending |
