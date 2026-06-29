# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-06-29 (sesi 4) — **✅ GENERATOR PILOT DIJALANKAN** (eksekusi pivot).

**🆕 SESI 4 (2026-06-29) — generator pilot tuntas dijalankan:**
- **Bug empty-content di-root-cause + diperbaiki:** deepseek-v4-pro reasoning model; minta 12 contoh sekaligus → reasoning makan semua token, content kosong. Request kecil sebenarnya berhasil. **Bukan kegagalan task.**
- **`generate.py` di-redesign** jadi **matriks stratifikasi 4 niche register × 9 target SARA** (per-niche batched, retry-on-truncation, resume-aware) → fix bug + sekaligus bikin tabel yang diminta FINDINGS §5.
- **Hasil: 35/36 contoh hate Jawa fresh** ter-generate (~beberapa sen). 0 museum-krama. **N3b krama cold-contempt ke KELOMPOK SARA BERHASIL** (jawab open-question; device berulang = tuduh kelompok tak punya isin/unggah-ungguh — native nilai otentik vs formulaic).
- **Pipeline lengkap siap:** `generate.py` → `review_generated.py` (auto-triage + `VALIDATION_FORM.xlsx`) → **[isi native]** → `score_validation.py`.
- **⏭️ LANGKAH PERTAMA sesi berikut = VALIDASI NATIVE:** Bapak isi `experiments/generation_pilot/VALIDATION_FORM.xlsx` kolom G (OTENTIK? 1/0) + H (MASALAH), lalu `python experiments/generation_pilot/score_validation.py`. Ini bottleneck inti (by design — native = authenticity referee).
- Detail: `experiments/generation_pilot/README.md`. Teks ofensif sintetis gitignored (policy mirror expert_spotcheck); scripts+README di-commit.

---

### Konteks pivot (sesi 3, tetap berlaku) — **🔄 PIVOT BESAR: LABELER → GENERATOR.**

**Inti pivot (BACA INI DULU):** Seluruh kerja lama = **LLM melabeli data Indonesia yang ADA** (`haipradana/indonesian-twitter-hate-speech-cleaned`, HF publik) yang difilter buat cari Jawa. Tapi yield Jawa cuma **0,9%** (8.269 tweet difilter → 74 "jawa", 62% Indonesia). **Maksud asli Bapak SELALU = GENERATOR** (bikin hate Jawa *fresh* pakai LLM), bukan filter+label. Niat itu tak pernah masuk PRD ("annotation"=labeling) → drift. Bapak kecewa sadar ini. **KEPUTUSAN: pivot ke LLM-as-GENERATOR.**

**Arah baru:** GENERATE (LLM, prompt kultural) → consensus-label + spot-check native (QC) → dataset. **Kerja lama ganti peran (TIDAK dibuang):** taksonomi + prompt v2 = otak generator; pipeline labeling 3-LLM = QC; dataset 728 = jangkar realisme + **bukti kelangkaan** (section Motivasi paper: "collection gagal, 0,9% yield → generation perlu").

**Novelty inti yang ketemu sesi ini:** **register-pragmatik hate Jawa** (`experiments/register_probe/FINDINGS.md`) — register menyandi SUHU benci (panas→ngoko, dingin/contempt/ironis→krama); LLM TERNYATA bisa generate krama otentik (DeepSeek dinilai Bapak "sangat bagus"); blind-spot deteksi = **ironi/pasemon**, bukan kesopanan (qwen3 lolos krama sarkastik).

**⏭️ LANGKAH PERTAMA sesi berikut:** ~~jalankan generator~~ **SUDAH DIJALANKAN sesi 4** (35 contoh, lihat blok sesi 4 di atas). Langkah pertama sekarang = **validasi native** (`VALIDATION_FORM.xlsx`).

**💰 Budget:** DeepSeek balance **$2.23** (murah, PILIH ini buat generate). xAI/Grok mahal/terbatas — stop dipakai buat filter.

**Catatan:** audit sesi 2 (paper v3 + codebook v1.0a + `paper/AUDIT_RESPONSE.md`) tetap valid sebagai perbaikan kejujuran lapisan-labeling. 5 keputusan audit (A-E) kini SUBORDINAT ke pivot generator. Tidak ada run in-flight.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ✅ OPSI A / PILOT #6b SELESAI (2026-06-22): pool diperbesar 332 → 735

Cascade filter (SEA-LION→qwen3 lokal pre-screen → grok verify) dijalankan tuntas. Sempat terblokir xAI **403 kredit habis** (2026-06-18) di pass3 verify (pool mentok 431); resume 2026-06-22 setelah Bapak konfirmasi kredit terisi ($4.55) + live grok test ✅. `scripts/run_cascade_remaining_pipeline.ps1` jalan sampai selesai (verify 1298 sisa → regenerate pool → label 3-rater → analyze).

**Hasil kunci:**
- **Pool 332 → 735** (held-out 586 | prompt-iter 149). Grok confirm-rate di pass2-keeps cuma **25.4%** (1687→+304) → local pre-screen over-keep (temuan cascade-design). **Dump 12.7K habis → 735 ≈ ceiling** sumber ini (estimasi ~950 optimis).
- **Held-out validation MENGUAT:** ds+grok held-out α **0.688** [0.614, 0.759] di 586 teks (vs Pilot #5 0.670 di held-out lebih kecil, CI lebih sempit), full 0.701, iter 0.747 → prompt v2 generalizes robust. 3-rater held-out 0.513 / full 0.545 (qwen3 tetap rater paling bising: ds+qwen3 0.462, grok+qwen3 0.438). **Pakai ds+grok untuk klaim utama.** Angka diverifikasi **recompute independen** (cocok persis).
- **Dataset (`data/labeled/`, gitignored):** `bulk_v2_consensus.jsonl` **728 teks** (158 hate / 570 non-hate, ~22% stabil; unanimous 569) + `bulk_v2_disagreement.jsonl` 7 ties. Dataset 331 lama di-backup `_backup_pilot05_3rater_20260622_*`.
- **SARA lebih kaya:** gender_wanita 111, politik 112, gender_lgbtq 55, tionghoa 37, islam 31, **+ kristen 18, arab 11, kepercayaan 12, hindu 3, rohingya 3**. Register ngoko dominan; form direct/code_switched/sarcastic/pasemon.
- Biaya sesi ~$2.8 grok (verify + label) dari $4.55. **⚠️ 728 < gate D7 BERT (3K)** → lihat Next Action (D-OPEN-3).

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

**🔆 STATUS TERKINI (2026-06-22):** **OPSI A / Pilot #6b SELESAI** — pool diperbesar **332 → 735**, dataset **728 consensus (158 hate)**, **held-out ds+grok α 0.688** (menguat vs Pilot #5 0.670). Dump habis → 735 ceiling. Vendor mix 3-rater ds+grok+qwen3 (D16), prompt `prompts/cultural_classification_v2.md`. Angka diverifikasi recompute independen. **Tidak ada run in-flight, blocker hilang.** Pilot #5 (2026-06-15): dataset 331 + held-out 0.670. Pilot #6: qwen3 LOLOS (0.660), SEA-LION GAGAL (0.422).

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

Konteks: **PIVOT ke GENERATOR (2026-06-23 sesi 3).** Lihat status atas. Urutan:

1. ✅ **GENERATOR PILOT SUDAH DIJALANKAN (sesi 4, 2026-06-29)** — 35/36 contoh fresh, matriks 4 niche × 9 target. **Langkah aktif sekarang: Bapak isi `experiments/generation_pilot/VALIDATION_FORM.xlsx`** (kolom G OTENTIK 1/0, H MASALAH) → `python experiments/generation_pilot/score_validation.py` → `validation_result.md` (rate keaslian per-niche; konfirmasi N3b group cold-contempt otentik atau formulaic).
2. **Kunci PRD ke framing generator** (HARD RULE #1) — biar niat tak menggelincir lagi. Tulis: human-bottleneck = *penciptaan/akuisisi data* (bukan labeling); solusi = LLM generator; labeling jadi QC; bukti kelangkaan dari kerja filter (0,9% yield).
3. **Sistematisasi generasi**: matriks register × target SARA × (severity/form), termasuk **krama group-directed** (yg belum diuji — contoh krama sesi ini interpersonal). Native validasi → tabel paper.
4. **Pipeline GENERATE→QC→anchor**: generated → consensus-label (3-LLM) + spot-check native → uji transfer ke 728 data nyata (detektor sintetis jalan di hate nyata?).
5. **Judge ke-2** (Yekti/Daniel kalau penutur Jawa) → reliabilitas validasi keaslian.

**Catatan paper:** novelty inti = register-pragmatik (`experiments/register_probe/FINDINGS.md`) + generator-untuk-uncollectable + bukti kelangkaan. Paper-labeling lama (audit sesi 2) jadi bahan pendukung.

---

### Keputusan audit sesi 2 (kini subordinat ke pivot — `paper/AUDIT_RESPONSE.md`):
1. **(TERTINGGI) Spot-check pakar ~100 item** — Bapak native, ~1 jam, stratifikasi pada disagreement LLM-vs-sumber. Ubah κ0.19 dari pembunuh → fitur. Tidak melanggar zero-human. **Ini pengubah accept/reject.**
2. **Aturan label**: konfirmasi tetap 3-rater (headline 0.513, sudah saya pilih jujur) atau ganti ds+grok-only (0.688).
3. **Anekdot mahasiswa nyontek**: demote jadi 1 kalimat? (judgement coauthor — isu integritas).
4. **Lit-pass referensi** (≥20 IEEE, verifikasi DOI).
5. **Legal lisensi `haipradana`** (boleh rilis turunan CC BY-NC-SA?) — potensi blocker rilis.

Lalu: pindah paper ke Word template JINITA + review Yekti/Daniel.

---

### Konteks lama (D-OPEN-3, masih berlaku)

**D-OPEN-3 SELESAI — Bapak pilih Opsi 1 (codebook + draft paper).** Keduanya dibuat 2026-06-23. Petunjuk JINITA sudah di-download + paper disesuaikan ke template. **Tidak ada run in-flight, tidak butuh saldo.**

**Sudah jadi:**
- `codebook/CODEBOOK.md` v1.0 — taksonomi 4-dimensi grounded di dataset 728, 7 boundary cases dengan adjudikasi, distribusi empiris, limitasi jujur (termasuk temuan register krama langka 157/158 ngoko).
- `paper/draft_jinita.md` v2 — draft Inggris, **conform template JINITA**: judul ≤12 kata tanpa akronim, abstrak ≤250 kata tanpa sitasi, 5 keywords, IMRaD bernomor (1 INTRO / 2 TAXONOMY / 3 METHOD / 4 RESULTS&DISCUSSION / 5 CONCLUSION), sitasi IEEE `[n]`, ≥20 referensi anchor, **Gen AI disclosure**, Ethics, Acknowledgements.
- `paper/jinita_guidelines/` — petunjuk JINITA terunduh (`submissions.html`, `template.txt`, `gen_ai_policy.html`) + `SUMMARY.md` (checklist kepatuhan + sisa TODO).

**Sisa TODO (untuk sesi berikut / review Bapak):**
1. **Lit-pass referensi:** lengkapi & verifikasi ≥20 referensi IEEE (DOI/vol/hal), ≥80% jurnal ≤5 tahun. Anchor sudah nyata (Ibrohim&Budi 2019, Putri/Ibrohim/Budi Javanese-Sunda = kemungkinan "UI 2021" yang kita rujuk, NusaCrowd, Gilardi PNAS, dll); tinggal verifikasi presisi (jangan fabricate — per Gen AI policy).
2. **Pindah ke Word template** JINITA (TNR 10pt, A4, kolom) untuk submission final.
3. **Review Bapak + coauthor** (Yekti, Daniel) atas isi codebook + paper.
4. Opsional: modeling baseline (IndoBERT/XLM-R) sebagai karakterisasi dataset (future-work, bisa kuatkan Results) — butuh GPU lokal gratis.
5. Versi blind (anonim) untuk peer review.

**Catatan teknis:** dataset final `data/labeled/bulk_v2_consensus.jsonl` (728) + `_disagreement.jsonl` (7). Pool `experiments/pilot02_llm_jawa_filter/outputs/hot_jawa_subset.jsonl` (735). Report `experiments/pilot05_bulk_labeling/report.md`. Backup dataset 331 lama: `data/labeled/_backup_pilot05_3rater_20260622_*`. APC JINITA Rp1.5jt/$100 (hanya jika diterima).

---

## 📖 PANDUAN BAPAK

1. **Keputusan yang ditunggu (D-OPEN-3):** arah setelah pool 735 — **Opsi 1** codebook + draft paper metodologi (rekomendasi, tidak butuh saldo), **Opsi 2** cari sumber data tambahan (dump habis), atau **Opsi 3** modeling BERT di 728 + future-work. Lihat Next Concrete Action.
2. **Tidak ada run in-flight** — Opsi A sudah tuntas, mesin boleh sleep. Kredit xAI sisa ~$1.7 (dari $4.55, sesi pakai ~$2.8).
3. **Saldo:** Opsi 1 tidak butuh saldo. Opsi 2 butuh grok/deepseek untuk filter sumber baru. Opsi 3 butuh GPU lokal (gratis).
4. **Tinggal bilang "lanjut" + sebut pilihan** (mis. "lanjut, opsi 1") — agent langsung eksekusi.
5. **Zero-human tetap** — tidak ada anotasi manual. Dataset 728 sudah siap di `data/labeled/` (lokal, belum dirilis; backup 331 lama tersimpan).

### Cara cek progres background (PowerShell di folder proyek)
```powershell
# Hasil validasi lokal qwen3 (cari baris "alpha"):
Get-Content experiments\pilot06_local_models\outputs\local_v2_qwen3_14b.jsonl | Measure-Object -Line
# Filter pool (berhenti di 4351, kalau mau lanjut lokal):
(Get-Content experiments\pilot02_llm_jawa_filter\outputs\pilot02_responses.jsonl | Measure-Object -Line).Lines
```

### ⚡ Ketahanan run (lampu mati / crash)

- Semua runner (`run_cascade.py`, `run_bulk.py`, `run_filter.py`, `analyze.py`) resume-aware (`f.flush()` per record; rerun = skip yang sudah ada; 403/429 dihitung transient → di-retry). Pipeline `scripts/run_cascade_remaining_pipeline.ps1` idempotent end-to-end. **Tidak ada run in-flight saat ini** (Opsi A tuntas 2026-06-22).

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
