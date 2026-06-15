# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-15 — **Pilot #5 SELESAI: dataset berlabel pertama jadi (331 consensus, 74 hate). Held-out validation LULUS — prompt v2 GENERALIZES** (α ds+grok held-out 0.670 vs iter 0.747, CI overlap). Pipeline fully-LLM zero-human terbukti end-to-end. Vendor mix final = **ds+grok+qwen3** (D16). **Blocker hilang — keputusan berikut: perbesar pool (cascade filter) atau ship dataset v1 + modeling.**
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ✅ PILOT #5 SELESAI (2026-06-15): dataset berlabel pertama + held-out validation

Pipeline produksi penuh dijalankan sampai tuntas (3-rater **ds + grok + qwen3-lokal** = D16) di pool **332 teks hot-Jawa**. `analyze.py` menghasilkan dataset + report + validasi anti-overfit.

**HELD-OUT VALIDATION (klaim kunci paper — prompt v2 tidak overfit ke pool iterasi 149):**
- Tes ADIL same-rater-set ds+grok: **held-out α = 0.670 [0.525, 0.792]** vs iter-pool **0.747** → di atas ambang 0.6 + CI overlap = **GENERALIZES ✅**.
- α 3-rater (ds+grok+qwen3): held-out 0.565, full 0.610. Lebih rendah karena **qwen3 = rater paling bising** (lone-dissenter 31/64 baris non-unanimous; konsisten Pilot #6). Pakai angka ds+grok untuk klaim utama, qwen3 = rater ke-3 gratis/reproducible.

**DATASET v1** (`data/labeled/`, gitignored → rilis HF/Zenodo nanti):
- `bulk_v2_consensus.jsonl`: **331 teks** (74 hate / 257 non-hate, ~22% hate stabil held-out vs iter) — majority-vote ≥2 rater valid.
- `bulk_v2_disagreement.jsonl`: **1 tie** (sid 3009, "komunis Rusia" — borderline politis) = bahan codebook.
- Target group teratas: gender_wanita 60, gender_lgbtq 33, politik 44, suku_tionghoa 18, agama_islam 18. Severity sepakat hanya 41/74 baris hate → **label inti tetap binary**, severity noisier.

**⚠️ Ukuran:** 331 label (74 hate) = bukti pipeline solid + held-out valid, TAPI jauh di bawah target D7 (10K, gate 3K) untuk training BERT. Pool perlu diperbesar (lihat Next Action).

**Verifikasi adversarial (materi paper metodologi):** sebelum commit, analisis di-audit multi-agent + recompute independen. Menemukan **2 bug nyata** yang sudah diperbaiki: (1) dedup load-order (record stale menimpa label valid → consensus 330/2 jadi 331/1, ds+grok iter 0.763→0.747); (2) formula α non-kanonik (diperbaiki ke coincidence-matrix Krippendorff, validasi vs dataset rujukan 0.743). Lesson: recompute independen *meniru* bug yang sama → hanya **code-audit** yang menangkapnya. Detail: `experiments/pilot05_bulk_labeling/report.md` + commit `fbd59a2`/`2ac5db3`.

---

## ✅ D16 (2026-06-11): vendor mix final = 3-rater ds + grok + qwen3-lokal

Setelah Pilot #6, Bapak putuskan pakai **3 rater**: deepseek + grok (cloud) + qwen3:14b (lokal gratis). Bukan ganti Grok, tapi **tambah** qwen3 sebagai rater independen ke-3 → triangulasi lebih kuat + sebagian reproducible tanpa API berbayar. Cascade filter (Pilot #6b) dibangun untuk perbesar pool murah: lokal pre-screen → grok verify (pool tetap grok-confirmed). Catatan: kredit xAI sudah terisi (labeling pool 332 cloud sukses 0 error).

---

## ✅ PILOT #6 SELESAI (2026-06-11): lokal bisa gantikan Grok

Validasi penuh di pool 149 (prompt v2, pembanding α ds+grok = 0.763):

| Rater ke-2 vs deepseek | JSON valid | Pairwise | α | 95% CI | Biaya |
|---|---|---|---|---|---|
| grok (pembanding) | — | — | 0.763 | [0.624, 0.879] | $ mahal |
| **qwen3:14b /no_think** | 100% | 90% | **0.660** | [0.480, 0.807] | **gratis** |
| SEA-LION v3.5-8B-R | 100% | 80% | 0.422 | [0.238, 0.581] | gratis |

- **qwen3 LOLOS** — CI overlap kuat dengan 0.763. **deepseek(murah) + qwen3(gratis) = consensus viable tanpa xAI.**
- **SEA-LION GAGAL** gate consensus (noise dua arah: 18 over-flag + 10 miss). Temuan paper menarik: model Jawa-native ≠ otomatis rater lebih baik. Masih kandidat untuk tugas FILTER (2.2s/call).
- Infra bulk SIAP untuk lokal: `run_filter.py` (`FILTER_VENDOR="ollama"`) & `run_bulk.py` (`BULK_VENDORS="deepseek,ollama"`) sudah diparametrize; 2.225 record error 403 (xAI habis) sekarang dihitung transient → rerun otomatis retry.

**Pending keputusan Bapak (satu-satunya blocker):** vendor mix final — lihat Next Concrete Action.

---

## ✅ D15 (2026-06-10): KIMI DROPPED — pipeline = 2-LLM deepseek+grok

Saldo Moonshot habis (run Kimi v1 gagal 149/149, 429) → keputusan Bapak: **biarkan, pakai yang ada** = deepseek+grok. Empiris mendukung (Kimi validity 73.8%, 126s/call). α tetap terukur (2 rater); data Kimi v0 n=149 tetap dipakai di paper sebagai sensitivity analysis 3-vs-2 vendor. **Baseline pembanding Pilot #3 sekarang: α ds+grok v0 = 0.534.** Detail: `wiki/decisions.md` D15.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**🔆 STATUS TERKINI (2026-06-15):** **Pilot #5 SELESAI** — dataset berlabel pertama (331 consensus, 74 hate) + held-out validation **LULUS** (ds+grok held-out α 0.670 vs iter 0.747 → prompt v2 generalizes). Vendor mix final 3-rater ds+grok+qwen3 (D16). Prompt kerja `prompts/cultural_classification_v2.md`. Analisis sudah diverifikasi adversarial (2 bug diperbaiki, formula α dikanonikkan). **Blocker hilang.** Pilot #6 sebelumnya: qwen3 LOLOS (0.660), SEA-LION GAGAL (0.422).

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

## Next Concrete Action (urutan)

Konteks: Pilot #5 tuntas — pipeline fully-LLM zero-human terbukti end-to-end, held-out validation lulus, dataset v1 (331 teks) jadi & terverifikasi. Tinggal **keputusan arah** dari Bapak.

**KEPUTUSAN UTAMA (BUTUH INPUT BAPAK): perbesar pool atau ship + modeling?**

- **Opsi A (rekomendasi): perbesar pool via cascade filter (Pilot #6b).** Dataset sekarang cuma 331 (74 hate) — jauh di bawah target D7 (10K, gate 3K) untuk training BERT. Cascade filter sudah siap: SEA-LION (pass 1) → qwen3 (pass 2) lokal gratis pre-screen → grok verify (pass 3, ~$1.2 est) sisa ~8.3K teks. Estimasi pool jadi **~950 teks**. Jalan overnight (GPU RTX 4080 — pastikan mesin tidak sleep). Lalu rerun bulk label 3-rater + analyze (semua resume-aware). **Butuh: mesin nyala + kredit grok + xAI.**
  ```powershell
  # pass 1+2 lokal gratis (pre-screen) lalu pass 3 grok verify:
  .venv\Scripts\python experiments\pilot06_local_models\run_cascade.py
  # regenerate pool, lalu label 3-rater (resume-aware, 332 lama di-skip):
  $env:BULK_VENDORS="deepseek,grok"; .venv\Scripts\python experiments\pilot05_bulk_labeling\run_bulk.py
  $env:BULK_VENDORS="ollama"; $env:LOCAL_MODEL="qwen3:14b"; $env:LOCAL_NO_THINK="1"
  .venv\Scripts\python experiments\pilot05_bulk_labeling\run_bulk.py
  .venv\Scripts\python experiments\pilot05_bulk_labeling\analyze.py
  ```
- **Opsi B: ship dataset v1 (331) sekarang + mulai paralel:** (1) **codebook** dari `bulk_v2_disagreement.jsonl` + profil taksonomi (deliverable HKI), (2) draft section metodologi paper (held-out validation + verifikasi adversarial = materi kuat). Modeling BERT ditunda sampai pool cukup.

**Catatan teknis untuk eksekusi Opsi A:** `run_cascade.py` (Pilot #6b) menulis pre-screen lokal ke log terpisah; pool regeneration tetap grok-confirmed. Cek `experiments/pilot06_local_models/run_cascade.py` + commit `3207869` sebelum jalan. `analyze.py` default 3-rater `deepseek,grok,ollama:qwen3:14b` (override via `ANALYZE_VENDORS`).

---

## 📖 PANDUAN BAPAK

1. **Keputusan yang ditunggu:** arah berikutnya — **Opsi A** perbesar pool via cascade filter (overnight, rekomendasi — dataset 331 masih kecil) atau **Opsi B** ship dataset v1 + mulai codebook/paper paralel. Lihat Next Concrete Action.
2. **Mesin & sleep:** cascade filter & qwen3 jalan di GPU RTX 4080 — kalau pilih Opsi A pastikan mesin tidak sleep. Settings → System → Power → sleep "Never" (plugged in).
3. **Saldo:** Opsi A butuh DeepSeek (~$2-3) + grok/xAI (~$1-2 untuk verify pass + labeling pool baru). Opsi B tidak butuh saldo.
4. **Tinggal bilang "lanjut" + sebut pilihan** (mis. "lanjut, opsi A") — agent langsung eksekusi.
5. **Zero-human tetap** — tidak ada anotasi manual. Dataset v1 (331) sudah siap di `data/labeled/` (lokal, belum dirilis).

### Cara cek progres background (PowerShell di folder proyek)
```powershell
# Hasil validasi lokal qwen3 (cari baris "alpha"):
Get-Content experiments\pilot06_local_models\outputs\local_v2_qwen3_14b.jsonl | Measure-Object -Line
# Filter pool (berhenti di 4351, kalau mau lanjut lokal):
(Get-Content experiments\pilot02_llm_jawa_filter\outputs\pilot02_responses.jsonl | Measure-Object -Line).Lines
```

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
