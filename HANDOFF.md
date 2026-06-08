# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-08 — Pilot #1b (C3 re-test) selesai + novelty reframe (D14).
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**✅ NOVELTY REFRAME (D14, 2026-06-08):** keputusan Bapak — klaim "dataset pertama/from-scratch" **DITINGGALKAN** (dataset hate Jawa sudah ada: UI/WCSE 2021, tak di-release). Novelty utama sekarang 3 pilar: (1) **pipeline fully-automated zero-human**, (2) **taksonomi kultural 4-dimensi register-aware**, (3) **code-mixed realism**. PRD sudah di-update ke v0.3 (D13 retroaktif + D14, Goals G2/G3/G5 sinkron). Dataset tetap deliverable ("first *publicly released*" = fakta sekunder, bukan klaim utama).

**✅ PILOT #1b SELESAI — C3 TERJAWAB (gate YELLOW):** re-test 3-LLM (prompt v0 sama) di 24 teks hot-Jawa (Pilot #2). **α hate = 0.384 NON-DEGENERATE** (CI [0.01, 0.70]), severity 0.376. Multi-LLM consensus **bekerja moderat** pada hate Jawa asli — beda fundamental dari α=1.000 degenerate Pilot #1. Pairwise deepseek-grok **80%**. **Kimi = noise utama** (validity 62.5%, drop Kimi → α 0.48). **CI lebar (n=24) → angka belum robust, scale-up wajib sebelum klaim paper.**

**Konteks lama (tetap berlaku):**
- **Pilot #1** gate GREEN tapi α degenerate (FineWeb2 nyaris tanpa hate) → sudah dipecahkan Pilot #1b.
- **Pilot #2** (LLM-as-Jawa-filter, Grok, 250 tweet): yield Jawa+campuran 9.6% (24 hot, 9 hate). Jawa murni ~nol → code-mixed scope tervalidasi. Densitas hot-Jawa ~3.6% → pool besar perlu filter banyak baris.

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

C3 sudah terjawab (YELLOW, α=0.384). Masalah inti sekarang = **CI lebar karena n=24 kecil**, bukan prompt. Maka prioritas:

**Opsi A (DIREKOMENDASIKAN) — scale filter haipradana → pool besar, lalu C3 ulang untuk α robust:**
- Naikkan `N_SAMPLE` di `experiments/pilot02_llm_jawa_filter/run_filter.py` (mis. 2000-4000) atau loop seluruh haipradana (~12.7K). Estimasi yield ~460 hot-Jawa dari 12.7K. ~6s/call → jalankan background/overnight.
- Lalu re-run `experiments/pilot01b_c3_retest/run_c3.py` (ganti INPUT_PATH ke subset besar baru, atau parametrize). α dengan n~100+ → CI jauh lebih sempit → bisa klaim C3 robust untuk paper.
- **Hemat:** pertimbangkan **2-LLM deepseek+grok** saja (Kimi noise + mahal+lambat 115s/call). Pairwise mereka 80%, drop-Kimi α 0.48. Hemat waktu besar untuk bulk.

**Opsi B (kalau α tetap < 0.5 di pool besar) — iterasi prompt (Pilot #3):**
- Baru relevan kalau scale-up tidak mengangkat α. Sekarang CI lebar bilang "kurang data", belum tentu "prompt jelek".

**Inspeksi kualitatif (cepat, berguna untuk paper):** 9/15 teks orig-label `neutral` haipradana → LLM majority hate=True (umpatan Jawa `asu/ngewe/tae`). Apakah ini **sinyal kultural** (haipradana Indonesia-context melewatkan kekasaran Jawa) atau **over-flag** LLM? Inspeksi 7 disagreement di `report.md`. Ini bahan diskusi menarik untuk paper (gold haipradana bukan Jawa-aware).

**Follow-up Pilot #2:** validasi filter vs langid baseline (belum dikerjakan).

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
