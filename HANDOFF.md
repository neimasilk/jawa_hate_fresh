# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-05-25, sore — Pilot #1 selesai, Pilot #2 sedang berjalan.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**Pilot #1 SELESAI** — gate GREEN (refusal 0.3%, JSON valid 94%, α=1.000) **TAPI α degenerate**: semua 100 sampel dilabeli `hate=false`/BUK karena sumber FineWeb2 `jav_Latn` nyaris tanpa hate. C2 ✅ + C1 sebagian ✅, tapi **C3 (multi-LLM agreement pada hate asli) BELUM terjawab**.

**Keputusan strategi data (2026-05-25):** survei menemukan tidak ada korpus hate Jawa siap-unduh (dataset UI/WCSE 2021 cuma di paper). Maka: **filter dump hate Indonesia (`haipradana`) → ekstrak subset Jawa/code-mixed**, terima code-mixed sebagai scope sah. Ini sekaligus prototipe Pilot #2 + memecahkan blocker C3.

**Pilot #2 SEDANG BERJALAN** (LLM-as-Jawa-filter, Grok, 250 tweet). Smoke test 4 contoh ✅. Begitu selesai → ekstrak `hot_jawa_subset.jsonl` → re-test C3 di subset itu.

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

**Langkah 1 — selesaikan Pilot #2 (kalau belum):**
```powershell
.venv\Scripts\python.exe experiments\pilot02_llm_jawa_filter\run_filter.py
.venv\Scripts\python.exe experiments\pilot02_llm_jawa_filter\analyze.py
```
- `run_filter.py` resume-aware: kalau run sore tadi terputus, ini lanjut dari yang belum selesai (cek `outputs/pilot02_responses.jsonl`, target 250 baris unik).
- `analyze.py` hasilkan `report.md` + `outputs/hot_jawa_subset.jsonl` (subset Jawa+campuran).
- **Baca yield:** berapa % Jawa+campuran, berapa yang berlabel hate. Ini menentukan langkah 2.

**Langkah 2 — re-test C3 (kalau yield memadai, mis. >=40 teks Jawa-panas):**
- Jalankan karakterisasi 3-LLM (DeepSeek+Grok+Kimi) seperti Pilot #1 TAPI input dari `hot_jawa_subset.jsonl`, bukan FineWeb2.
- Hitung ulang Krippendorff's alpha. Kali ini ada hate beneran -> alpha tidak lagi degenerate -> C3 baru terjawab.
- (Belum ada script khusus; adaptasi `pilot01/run_pilot.py` agar baca dari hot_jawa_subset, atau buat runner kecil baru.)

**Langkah 3 — keputusan framing (perlu Bapak):** putuskan reframe novelty di PRD (lihat flag di TL;DR). Jangan diam-diam ubah PRD; angkat ke Bapak.

**Kalau yield Pilot #2 terlalu kecil:** pertimbangkan sumber lain (dump sosmed Indonesia lebih besar) atau kontak penulis dataset Jawa UI/WCSE 2021.

**Catatan vendor (Pilot #1):** Kimi K2.6 mahal+lambat (91s, 260K out-tok, 11% gagal). Untuk re-test C3 sampel kecil masih OK; bulk pipeline nanti pertimbangkan drop/batasi Kimi.

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
