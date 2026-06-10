# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-10 — **C3 scale-up SELESAI: α=0.587 (CI [0.475, 0.698]) di n=149 — C3 ROBUST.** Next: Pilot #3.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai besok:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ⚠️ BLOCKER USER ACTION: saldo Kimi (Moonshot) HABIS

Run Kimi v1 Pilot #3 gagal total: 149/149 call kena **429 insufficient balance** (akun `org-fd4daff...` suspended). **Perlu Bapak top-up akun Moonshot** kalau mau triangulasi 3-LLM lanjut. Iterasi Pilot #3 TIDAK terblokir (jalan dengan deepseek+grok, pair kunci); Kimi hanya dibutuhkan untuk α 3-LLM final vs baseline 0.587. Record error sudah dibersihkan + resume logic di-patch (429 tidak dihitung done) — setelah top-up tinggal rerun `run_eval.py` dengan `P3_VENDORS=kimi`.

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

**#1 PRIORITAS — Pilot #3: cultural prompt iteration (v1, v2, ...).** C3 sudah robust (α 0.587 baseline v0). Target perbaikan TERFOKUS dari data disagreement n=149:
1. **Pertegas definisi hate di prompt:** hate = diarahkan ke group/identitas (SARA, gender, dll); **umpatan kasar / kritik politik pedas ≠ otomatis hate**. Ini sumber disagreement #1 (Grok over-flag umpatan → "ringan").
2. Eval tiap versi prompt di pool 149 yang sama (infra `run_c3.py`/`analyze.py` reusable, ~$1.6/iterasi 3-LLM, atau ~$0.9 tanpa Kimi) → bandingkan α vs baseline 0.587.
3. **Keputusan vendor mix bulk DITUNDA sampai sesudah Pilot #3** — kalau definisi dipertegas, α deepseek+grok (sekarang 0.534) kemungkinan naik; deepseek+grok unggul di speed/cost/validity (97.7%).
4. Inspeksi disagreement n=149 (36 teks, sudah ada di `report.md`) = input langsung untuk few-shot baru + draft codebook v0.

**Follow-up Pilot #2 (belum dikerjakan):** validasi filter vs langid baseline.

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
