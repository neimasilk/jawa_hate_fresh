# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-05-25, sore — Pilot #1 selesai, Pilot #2 sedang berjalan.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**Pilot #1 SELESAI** — gate GREEN (refusal 0.3%, JSON valid 94%, α=1.000) **TAPI α degenerate**: semua 100 sampel dilabeli `hate=false`/BUK karena sumber FineWeb2 `jav_Latn` nyaris tanpa hate. C2 ✅ + C1 sebagian ✅, tapi **C3 (multi-LLM agreement pada hate asli) BELUM terjawab**.

**Keputusan strategi data (2026-05-25):** survei menemukan tidak ada korpus hate Jawa siap-unduh (dataset UI/WCSE 2021 cuma di paper). Maka: **filter dump hate Indonesia (`haipradana`) → ekstrak subset Jawa/code-mixed**, terima code-mixed sebagai scope sah. Ini sekaligus prototipe Pilot #2 + memecahkan blocker C3.

**Pilot #2 SELESAI** (LLM-as-Jawa-filter, Grok, 250 tweet): filter 100% valid; yield Jawa+campuran **9.6%** (24 teks, 9 hate). Jawa murni ~nol → **code-mixed scope tervalidasi empiris**. Subset panas → `experiments/pilot02_llm_jawa_filter/outputs/hot_jawa_subset.jsonl` (24 teks). Densitas hot-Jawa di dump Indonesia rendah (~3.6%) → untuk pool besar perlu filter banyak baris.

**⚠️ Flag novelty (butuh keputusan Bapak):** dataset hate Jawa SUDAH pernah dibuat orang lain → klaim "dataset from-scratch" perlu disandarkan ulang ke pipeline fully-automated + taksonomi kultural lebih dalam + zero-human. **PRD belum diubah** — menunggu keputusan Bapak.

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

Pilot #1 & #2 sudah selesai. Open question utama tetap **C3: apakah multi-LLM agreement bekerja pada hate Jawa ASLI?** Sekarang sudah ada bahan (`hot_jawa_subset.jsonl`, 24 teks, 9 hate).

**Opsi A (cepat, direkomendasikan dulu) — C3 re-test di 24 teks yang sudah ada:**
- Jalankan karakterisasi 3-LLM (DeepSeek+Grok+Kimi, prompt `cultural_classification_v0`) di `experiments/pilot02_llm_jawa_filter/outputs/hot_jawa_subset.jsonl`.
- Hitung Krippendorff's α. Karena ada 9 hate + 15 non-hate → ada variasi label → α tidak lagi degenerate. Ini **sinyal C3 pertama** (n kecil tapi real). Murah (~72 call, ~15 mnt).
- Belum ada script khusus; adaptasi `pilot01/run_pilot.py` agar input dari hot_jawa_subset (ganti bagian sampling), atau buat runner kecil baru.
- **Logika:** kalau α jelek bahkan di sini, itu temuan besar — wajib tahu SEBELUM invest scale-up.

**Opsi B (kalau mau angka robust) — scale filter dulu:**
- Naikkan `N_SAMPLE` di `pilot02/run_filter.py` (mis. 1500-2000) atau loop seluruh haipradana (~12.7K). Estimasi yield ~460 hot-Jawa dari 12.7K. Mahal waktu (~6s/call), jalankan overnight/background. Lalu C3 re-test di pool besar.

**Langkah framing (perlu Bapak):** reframe novelty di PRD (dataset Jawa sudah ada → sandarkan ke pipeline fully-automated + taksonomi lebih dalam + zero-human). Jangan diam-diam ubah PRD; angkat ke Bapak. Pilot #2 sudah kasih bukti kuat untuk argumen "kontribusi = taksonomi kultural dalam + code-mixed realita", bukan "dataset pertama".

**Follow-up Pilot #2:** validasi filter vs langid baseline (belum dikerjakan).

**Catatan vendor (Pilot #1):** Kimi K2.6 mahal+lambat (91s, 260K out-tok, 11% gagal). Untuk C3 re-test sampel kecil masih OK; bulk pipeline nanti pertimbangkan drop/batasi Kimi.

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
