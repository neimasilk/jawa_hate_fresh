# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-08 malam — novelty reframe (D14) + Pilot #1b selesai + **C3 scale-up SEDANG BERJALAN** (n=149).
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ⏳ HAL PERTAMA YANG DICEK BESOK

**C3 scale-up (3-LLM × 149 teks) dijalankan background tadi malam.** Saat handoff ini ditulis: **236/447 call (~53%)**, ETA ~1-2 jam → kemungkinan SUDAH SELESAI saat Bapak buka sesi.

Langkah cek (urut):
1. Lihat apakah ada notifikasi "background command completed" untuk run C3, ATAU cek baris terakhir `experiments/pilot01b_c3_retest/outputs/c3_responses.jsonl` (target: 447 record unik = 149×3).
2. **Kalau sudah 447 / run selesai:** jalankan
   `.venv\Scripts\python experiments\pilot01b_c3_retest\analyze.py`
   → baca `report.md`. **Ini angka C3 robust yang ditunggu** (α di n=149, CI jauh lebih sempit dari n=24). Lalu update STATE/HANDOFF/wiki/pilots.md + commit.
3. **Kalau run mati di tengah** (mesin tidur / crash): cukup jalankan ulang
   `.venv\Scripts\python experiments\pilot01b_c3_retest\run_c3.py`
   — **resume-aware**, skip pasangan (source_id, vendor) yang sudah ada, lanjut dari sisanya. Kimi lambat (~115s/call) jadi penyebab utama durasi.
4. Interpretasi gate ada di `analyze.py` (GREEN/YELLOW/RED) + tabel sensitivitas drop-1-vendor. **Bandingkan α n=149 vs α n=24 (0.384):** kalau naik & CI sempit → C3 robust ✅; kalau tetap < 0.5 → pertimbangkan iterasi prompt (Pilot #3).

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**✅ NOVELTY REFRAME (D14, 2026-06-08):** keputusan Bapak — klaim "dataset pertama/from-scratch" **DITINGGALKAN** (dataset hate Jawa sudah ada: UI/WCSE 2021, tak di-release). Novelty utama sekarang 3 pilar: (1) **pipeline fully-automated zero-human**, (2) **taksonomi kultural 4-dimensi register-aware**, (3) **code-mixed realism**. PRD sudah di-update ke v0.3 (D13 retroaktif + D14, Goals G2/G3/G5 sinkron). Dataset tetap deliverable ("first *publicly released*" = fakta sekunder, bukan klaim utama).

**✅ PILOT #1b SELESAI — C3 TERJAWAB (gate YELLOW, n=24):** re-test 3-LLM (prompt v0 sama) di 24 teks hot-Jawa. **α hate = 0.384 NON-DEGENERATE** (CI [0.01, 0.70]), severity 0.376. Multi-LLM consensus **bekerja moderat** pada hate Jawa asli — beda fundamental dari α=1.000 degenerate Pilot #1. Pairwise deepseek-grok **80%**. **Kimi = noise utama** (validity 62.5%, drop Kimi → α 0.48). CI lebar (n=24) → scale-up dilakukan ↓.

**🔄 SCALE-UP BERJALAN (untuk CI robust):**
- **Filter scale-up SELESAI:** N=250→2000 tweet haipradana. Pool hot-Jawa **24 → 149 teks (80 hate, 54%)**. Yield Jawa+campuran 7.5% (konsisten dgn 9.6% awal). Tersimpan ulang di `hot_jawa_subset.jsonl`.
- **C3 scale-up SEDANG BERJALAN** (lihat box ⏳ di atas): 3-LLM × 149 teks → α n=149, CI lebih sempit. Saat handoff ~53%. **Ini deliverable utama besok.**

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

**#1 PRIORITAS — selesaikan C3 scale-up** (lihat box ⏳ di atas). Filter sudah selesai (pool 149). C3 3-LLM tinggal tunggu selesai → `analyze.py` → α robust n=149. Itu deliverable utama.

**Setelah C3 robust ada — pilih berdasarkan hasil α:**
- **α n=149 > 0.5, CI sempit** → C3 robust ✅. Lanjut: putuskan vendor mix final bulk pipeline (rekomendasi kuat: **2-LLM deepseek+grok**, Kimi noise + lambat 115s; pairwise 80%, drop-Kimi α 0.48). Lalu mulai rancang Pilot #3 (prompt iteration) atau langsung bulk labeling.
- **α tetap < 0.5** → iterasi prompt dulu (Pilot #3). CI sempit + α rendah = prompt/task issue, bukan kurang data.

**Inspeksi kualitatif (cepat, bahan paper):** di n=24, 9/15 teks orig-label `neutral` haipradana → LLM majority hate=True (umpatan Jawa `asu/ngewe/tae`). **Sinyal kultural** (gold haipradana Indonesia-context melewatkan kekasaran Jawa) atau **over-flag** LLM? Cek lagi di n=149 (`report.md` majority-vs-orig_label + disagreement). Bahan diskusi kuat untuk paper.

**Follow-up Pilot #2:** validasi filter vs langid baseline (belum dikerjakan).

### ⚡ Ketahanan run (lampu mati / crash) — penting (ingat insiden petir 2026-04-29)

- **Resume aman.** `run_c3.py` & `run_filter.py` `f.flush()` SETIAP record ke disk → tiap call yang sudah selesai tersimpan permanen. Kalau lampu mati / mesin tidur: proses background mati, TAPI file `outputs/c3_responses.jsonl` lokal selamat. **Cukup jalankan ulang `run_c3.py`** → skip yang sudah ada, lanjut sisanya. Yang hilang hanya 1 call yang lagi in-flight saat mati (akan diulang).
- **Batas:** file in-progress BELUM di-commit ke Git (tak bisa commit file yang sedang ditulis). Lampu mati biasa → file lokal aman (cuma butuh re-run). Tapi kerusakan disk fatal (skenario petir) → progres C3 lokal bisa hilang. Mitigasi: murah diulang (~$1, resume-aware) DAN hasil di-commit+push begitu run selesai. Kalau Bapak khawatir cuaca buruk, bisa minta agent commit checkpoint parsial sebelum tidur.

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
