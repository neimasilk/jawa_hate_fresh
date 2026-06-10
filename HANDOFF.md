# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-10 — **PILOT #3 SELESAI: prompt v2, α ds+grok 0.534 → 0.763 (CI [0.624, 0.879]).** Vendor mix final D15 (deepseek+grok). Next: pilih arah (bulk design / codebook / langid baseline).
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ✅ D15 (2026-06-10): KIMI DROPPED — pipeline = 2-LLM deepseek+grok

Saldo Moonshot habis (run Kimi v1 gagal 149/149, 429) → keputusan Bapak: **biarkan, pakai yang ada** = deepseek+grok. Empiris mendukung (Kimi validity 73.8%, 126s/call). α tetap terukur (2 rater); data Kimi v0 n=149 tetap dipakai di paper sebagai sensitivity analysis 3-vs-2 vendor. **Baseline pembanding Pilot #3 sekarang: α ds+grok v0 = 0.534.** Detail: `wiki/decisions.md` D15.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**✅ NOVELTY REFRAME (D14, 2026-06-08):** keputusan Bapak — klaim "dataset pertama/from-scratch" **DITINGGALKAN** (dataset hate Jawa sudah ada: UI/WCSE 2021, tak di-release). Novelty utama sekarang 3 pilar: (1) **pipeline fully-automated zero-human**, (2) **taksonomi kultural 4-dimensi register-aware**, (3) **code-mixed realism**. PRD sudah di-update ke v0.3 (D13 retroaktif + D14, Goals G2/G3/G5 sinkron). Dataset tetap deliverable ("first *publicly released*" = fakta sekunder, bukan klaim utama).

**✅ C3 SCALE-UP SELESAI (2026-06-10, n=149, $1.57) — C3 ROBUST:**
- **α hate = 0.587** (bootstrap 95% CI **[0.475, 0.698]**) — naik dari 0.384 (n=24), CI jauh lebih sempit. **Multi-LLM consensus bekerja moderat-baik pada hate Jawa asli dengan prompt v0 tanpa iterasi.** Severity α = 0.480.
- **Gate YELLOW tipis:** α ✅, refusal 1.8% ✅; hanya validity 89.7% < 90% ❌ — murni diseret Kimi (73.8%); deepseek+grok saja 97.7%.
- **PLOT TWIST vendor:** di n=24 Kimi tampak noise utama; di n=149 **Grok = over-flagger** (115T/34F = 77% hate rate; umpatan kasar non-group → hate "ringan"). **Drop Grok → α 0.722** (tertinggi); drop Kimi → 0.534. Pairwise tertinggi justru deepseek–kimi 86.1%. Kimi tetap impraktis bulk (126s/call, validity 73.8%).
- **Disagreement #1 (36/149) = boundary profanity vs hate** — masalah DEFINISI di prompt, bukan capability vendor → **arah Pilot #3 jelas: pertegas hate = group/identity-directed, umpatan kasar ≠ otomatis hate.**
- **Sinyal kultural (materi paper):** 31/69 teks orig-`neutral` haipradana → LLM majority hate=True (LLM tangkap umpatan Jawa `ngewe/wasu/budek/tae` yang dilewatkan anotasi Indonesia-context).
- Report lengkap: `experiments/pilot01b_c3_retest/report.md`.

**Filter scale-up (selesai sebelumnya):** N=250→2000 tweet haipradana. Pool hot-Jawa **24 → 149 teks (80 hate, 54%)**. Yield 7.5%.

**✅ PILOT #1b n=24 (konteks):** α=0.384 non-degenerate (CI [0.01, 0.70]) — sinyal pertama C3, sudah digantikan angka n=149 di atas.

**Konteks lama (tetap berlaku):**
- **Pilot #1** gate GREEN tapi α degenerate (FineWeb2 nyaris tanpa hate) → sudah dipecahkan Pilot #1b.
- **Pilot #2** (LLM-as-Jawa-filter, Grok): Jawa murni ~nol → code-mixed scope tervalidasi empiris.

---

## Baca Dulu

1. `CLAUDE.md` - hard rules dan daily protocol.
2. `wiki/index.md` - user-facing knowledge base.
3. `wiki/decisions.md` - D1-D12 decision history.
4. `wiki/pilots.md` - status pilot.
5. `STATE.md` - live state dan challenges log.
6. `experiments/pilot01_llm_characterization/report.md` - report awal, tapi baca dengan catatan teknis di bawah.

---

## Status Terbaru

Pilot #1 SELESAI (2026-05-25, di komputer kantor baru). Report final di `experiments/pilot01_llm_characterization/report.md`.

Hasil deduped (100 sampel × 3 LLM):
- DeepSeek: refusal 1%, JSON valid 97%, 20s/call, $0.31
- Grok: refusal 0%, JSON valid 100%, 11s/call, $0.20 (paling efisien)
- Kimi: refusal 0%, JSON valid 85%, **91s/call, 260K out-tok, $0.35** (reasoning model, mahal+lambat, 11/100 masih kosong walau max_tokens=4096)
- Total cost $0.85, runtime 2j32m.

Gate GREEN: refusal 0.3% (<20%), JSON valid 94% (>90%), α=1.000 (>0.5).

**⚠️ CAVEAT KRITIS — jangan dibaca bulat-bulat:**
- α=1.000 itu **degenerate**: ketiga LLM melabeli SEMUA 100 sampel `hate=false`/BUK. Setuju sempurna karena sumber FineWeb2 `jav_Latn` (fallback dari OSCAR yang gated) nyaris tidak mengandung hate — mayoritas teks web/Wikipedia/promosi.
- Yang terkonfirmasi real: C2 (refusal bukan blocker) + C1 sebagian (LLM bisa hasilkan JSON taksonomi valid).
- Yang BELUM terjawab: C3 (apakah multi-LLM consensus bekerja pada hate ASLI). α ini tidak bisa dipakai untuk klaim consensus.

Patch yang sudah final dan ter-commit:
- `src/llm_clients.py`: max_tokens DeepSeek 2048, Kimi 4096.
- `run_pilot.py`: resume retry record kosong (done = ada raw_text atau error).
- `analyze.py`: dedup `(source_id, vendor)` keep-last (retry menang), print ASCII-safe.

Catatan dedup: rerun meng-APPEND record baru (responses.jsonl punya 300 unik tapi ~106 baris duplikat untuk Kimi/DeepSeek yang di-retry). `analyze.py` dedup keep-last sudah benar memilih retry yang valid.

---

## Next Concrete Action

**PILOT #5 (BULK) BERJALAN sejak 2026-06-10 malam.** Pipeline: filter full haipradana (~12.7K, Grok) → pool hot-Jawa (~950 est) → label prompt v2 × ds+grok → held-out α + consensus dataset. Detail: `experiments/pilot05_bulk_labeling/README.md`.

**Status saat handoff:** step 1 (filter, ~10.7K call baru) berjalan background, est 8-15 jam. Step 2-4 menyusul otomatis (kalau sesi agent masih hidup) ATAU via `scripts\run_bulk_pipeline.ps1` (idempotent, lihat Panduan di bawah).

**Setelah bulk selesai:** baca `experiments/pilot05_bulk_labeling/report.md` — angka kunci = **α held-out** (harapan ≈ 0.763 prompt-iter; jauh di bawah 0.6 = indikasi overfit). Lalu: codebook v0 (disagreement = bahan), langid baseline, atau rancang training BERT.

---

## 📖 PANDUAN BAPAK — bulk run (apa yang perlu dilakukan)

1. **Biarkan komputer menyala** sampai pipeline selesai (total ±15-20 jam). Matikan auto-sleep: Settings → System → Power → "Put my device to sleep: Never" (saat plugged in). Layar boleh mati, yang penting mesin tidak sleep.
2. **Cek saldo 2 vendor** (estimasi pemakaian total ~$12-15):
   - DeepSeek: https://platform.deepseek.com (butuh ~$6-8)
   - xAI/Grok: https://console.x.ai (butuh ~$6-8)
   - Saldo habis di tengah = run berhenti dengan error 429 → top-up → jalankan ulang (aman, resume otomatis).
3. **Cek progres kapan saja** (PowerShell di folder proyek):
   ```powershell
   # Filter (target 12703):
   (Get-Content experiments\pilot02_llm_jawa_filter\outputs\pilot02_responses.jsonl | Measure-Object -Line).Lines
   # Label (muncul setelah filter selesai):
   (Get-Content experiments\pilot05_bulk_labeling\outputs\bulk_responses.jsonl | Measure-Object -Line).Lines
   ```
4. **Kalau mati lampu / crash / run berhenti:** TIDAK ada yang hilang (tersimpan per record). Pilih salah satu:
   - Buka Claude Code di folder ini, bilang **"lanjut"** (agent baca HANDOFF ini dan resume), ATAU
   - Manual: jalankan `.\scripts\run_bulk_pipeline.ps1` — script idempotent, lanjut dari posisi terakhir.
5. **Selesai?** Baca `experiments\pilot05_bulk_labeling\report.md`. Dataset pertama ada di `data\labeled\bulk_v2_consensus.jsonl`. Tidak ada anotasi manual apa pun yang perlu Bapak lakukan (zero-human tetap).

### ⚡ Ketahanan run (lampu mati / crash)

- `run_c3.py` & `run_filter.py` resume-aware (`f.flush()` per record; rerun = skip yang sudah ada). C3 scale-up sudah SELESAI + di-commit, tidak ada run in-flight saat ini. Pattern yang sama dipakai lagi untuk run Pilot #3.

---

## Konteks Keputusan Final

- Proyek lama v1-v4 **jangan dipakai** sebagai baseline, warm-start, atau data training. Alasan: dataset lama mayoritas hasil back-translation mahasiswa, bukan ujaran Jawa natural.
- Human annotation bukan default. Fallback maksimal adalah sanity check kecil oleh Bapak jika pilot benar-benar gagal.
- Data source default adalah public dumps, bukan live scraping.
- Scope bahasa sumber: Jawa dan turunannya; Sunda/Madura bukan sumber, tetapi bisa menjadi target group dalam ujaran Jawa.
- Vendor Pilot #1: DeepSeek V4 Pro, Grok 4.3, Kimi K2.6.

---

## Catatan Teknis

- `.env.txt` dipakai untuk API keys dan gitignored.
- Kimi hanya menerima `temperature=1.0`; sudah di-handle.
- FineWeb2 `jav_Latn` publik dan berhasil streaming, tapi contoh awal banyak teks web/Wikipedia/promosi. Ini mungkin membuat hate rate sangat rendah; jangan simpulkan kualitas hate detection hanya dari distribusi BUK di fallback source.
- Runtime aktual lebih lama dari estimasi awal: sekitar 2 jam total karena Kimi lambat. Rerun resume seharusnya lebih pendek, tetapi tetap bisa puluhan menit.
- Worktree saat handoff belum clean: ada patch di `src/llm_clients.py`, `run_pilot.py`, `analyze.py`, plus `outputs/` dan `report.md`.

---

## User Communication

Bahasa Indonesia, ringkas. User prefer eksperimen kecil daripada blueprint panjang. Jangan re-litigate decisions final kecuali diminta. Jika ada hasil buruk, dokumentasikan sebagai lesson learned, bukan disembunyikan.
