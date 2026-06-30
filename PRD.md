# PRD — Ujaran Kebencian Jawa: Fully Automated LLM Pipeline

**Document type:** Product Requirement Document (research project)
**Version:** 0.4 (**PIVOT labeler → generator**, D19 2026-06-23; framing dikunci 2026-06-29)
**Last updated:** 2026-06-29
**Owner:** Mukhlis Amien
**Coauthors:** Yekti Asmoro Kanthi, Daniel Rudiaman Sijabat (semua UBHINUS)
**Target:** 1 paper **Sinta 2 (JINITA)** + 1 dataset HKI + 1 codebook HKI

---

## 0. Decisions Log (2026-05-07, updated 2026-06-29)

Sesi Claude Code 2026-05-07 menghasilkan pivot framing besar; sesi 2026-06-23 menghasilkan **pivot kedua yang lebih fundamental: labeler → generator (D19)**. Section deskriptif di PRD ini (terutama §4.2 NEIL + §5 Phases 2–4) **superseded** — baca **§0.1** untuk arah aktif. Decisions di-log di tabel berikut (D1–D18 ringkas; rationale penuh di [`wiki/decisions.md`](wiki/decisions.md)):

| # | Decision | Detail |
|---|----------|--------|
| D1 | **Framing pivot** | Dari "NEIL = native-expert-in-the-loop" ke **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** sebagai core novelty. Fully automated LLM pipeline, zero human in annotation + validation (default). |
| D2 | **Fallback ladder** | Kalau pilot zero-human gagal: (2) minimal sanity check ~50 sampel (~1 jam) → (3) pending rethink. |
| D3 | **Venue** | JINITA (Sinta 2, Politeknik Negeri Cilacap, P-ISSN 27160858 / E-ISSN 27159248, berlaku hingga 2028). Backup Sinta 2 lain pilih saat Fase 6. KUM first author ≈ 25. |
| D4 | **Authorship** | 3 authors UBHINUS: (1) Mukhlis Amien (corresponding, amien@ubhinus.ac.id), (2) Yekti Asmoro Kanthi (yektiasmoro@ubhinus.ac.id), (3) Daniel Rudiaman Sijabat (daniel223@ubhinus.ac.id). |
| D5 | **Dialek scope** | Bahasa **sumber** = Jawa + turunan (Mataraman, Arek, Banyumasan, Cirebonan, Osing, dll). Sunda + Madura excluded sebagai sumber, **tetap target group hate speech**. |
| D6 | **Data source strategy** | Default: existing public dumps (Common Crawl Indonesian, IndoNLP, OSCAR Indonesian/Javanese) + LLM filter Jawa. Live scraping dihindari (sulit + low yield). |
| D7 | **Data scope** | Target tentative 10K, dengan gate di 3K (re-evaluate berdasarkan eksperimen). Pivot dari "anotator burden" jadi "LLM cost + quality threshold". |
| D8 | **Validation strategy (default)** | Cross-LLM consistency (Claude + GPT-4o + DeepSeek), Krippendorff's α antar-LLM, adversarial perturbation testing, XAI (LIME/SHAP). Zero human gold subset (kecuali fallback aktif). |
| D9 | **Riset = exploratory** | Decisions methodologis bisa berubah berdasarkan eksperimen. Detail blueprint a priori → minimum. Pilot dulu, blueprint setelahnya. Dokumentasi tantangan + lessons-learned sambil jalan = potential kontribusi paper. |
| D13 | **Data strategy: code-mixed via dump Indonesia** (2026-05-25) | Tidak ada korpus hate Jawa siap-unduh → filter dump hate Indonesia (`haipradana`) via LLM → ekstrak subset Jawa/code-mixed. **Code-mixed = scope sah** (tervalidasi Pilot #2: Jawa murni ~nol di sosmed, hate Jawa real didominasi code-mixed). |
| D14 | **Novelty reframe** (2026-06-08) | Dataset hate Jawa SUDAH pernah dibuat (UI/WCSE 2021, tidak di-release). Klaim "dataset pertama/from-scratch" DITINGGALKAN. Novelty utama = (1) **pipeline fully-automated zero-human**, (2) **taksonomi kultural 4-dimensi register-aware**, (3) **code-mixed realism**. Dataset tetap deliverable — bisa disebut "first *publicly released*" sebagai fakta sekunder, bukan klaim utama. |
| D15 | **Vendor mix final: 2-LLM deepseek+grok, Kimi DROPPED** (2026-06-10, keputusan Bapak) | Update D8: cross-LLM consistency pakai **DeepSeek V4 Pro + Grok 4.3** (2 rater — α tetap terukur). Kimi K2.6 di-drop: saldo Moonshot habis DAN secara empiris penyumbang noise (validity 73.8% di n=149, 126s/call, out-token 30× grok). Data Kimi v0 n=149 TETAP dipakai di paper sebagai sensitivity analysis 3-vs-2 vendor (drop-Kimi α 0.534, drop-Grok 0.722) — narasi seleksi vendor berbasis data = materi metodologi. |
| D16 | **Vendor mix → 3-rater** (2026-06-11) | Tambah **qwen3:14b lokal** (Ollama, RTX 4080) sebagai rater ke-3 di samping ds+grok (memperluas, bukan ganti Grok). Consensus = majority ≥2. qwen3 = rater paling bising → klaim α utama tetap pasangan **ds+grok**. Sebagian pipeline jadi reproducible tanpa API berbayar. [wiki D16](wiki/decisions.md). |
| D17 | **α dikanonikkan + verifikasi adversarial = SOP** (2026-06-15) | `src/agreement.py` → Krippendorff coincidence-matrix kanonik (bobot per-unit 1/(m_u−1)); angka 2-rater historis tak berubah, 3-rater bergeser tipis. Sebelum angka masuk paper/commit: **code-audit + recompute independen** (dua jalur — recompute saja meniru bug yang sama). [wiki D17](wiki/decisions.md). |
| D18 | **Opsi A: perbesar pool via cascade** (2026-06-22) | Pool **332→735** (728 consensus, 158 hate) via cascade SEA-LION→qwen3 pre-screen → grok-verify. Held-out ds+grok α **0.688** [0.614, 0.759] (menguat vs 0.670) → klaim anti-overfit lebih kuat. Dump `haipradana` habis → 735 ≈ ceiling sumber. [wiki D18](wiki/decisions.md). |
| **D19** | **🔄 PIVOT LABELER → GENERATOR** (2026-06-23, keputusan Bapak) | Maksud asli Bapak SELALU = LLM **generator** hate Jawa *fresh*, BUKAN filter+label data yang ada. Istilah "annotation" lama (= labeling) menyebabkan drift selama berbulan sesi. Pipeline baru: **generate → consensus-QC → native authenticity check**. Kerja lama di-repurpose (taksonomi = otak generator, labeling 3-LLM = QC/detektor, dataset 728 = jangkar realisme + bukti kelangkaan 0,9% yield). **Detail penuh: §0.1.** |

**Catatan:** Section 4.2 (NEIL) + §5 Phases 2–4 di bawah ini = **legacy pre-pivot**. Dipertahankan sebagai konteks historis + sumber komponen yang di-repurpose, BUKAN rencana aktif. Arah aktif = §0.1.

---

## 0.1 PIVOT BESAR: Labeler → Generator (D19, 2026-06-23) — **framing terkunci**

> Section ini = **arah aktif proyek**. Kalau ada konflik dengan section lain di PRD, §0.1 menang.

**Realisasi inti** (lihat memory `generator-not-labeler-pivot`): maksud asli Bapak SELALU = **LLM sebagai GENERATOR** ujaran kebencian Jawa *fresh*, bukan filter+label data yang sudah ada. Istilah "annotation" di PRD lama (di NLP: annotation = labeling) menyebabkan setiap sesi diam-diam membangun *labeler*. Drift ini baru disadari 2026-06-23 → dikunci di sini supaya tak menggelincir lagi (HARD RULE #1).

**Re-definisi human bottleneck:** bukan di *labeling*, tapi di **penciptaan/akuisisi data**. Bukti empiris: filter dump Indonesia `haipradana` (8.269 tweet) → hanya **74 (0,9%) Jawa asli**, 62% Indonesia. Register krama/pasemon (carrier hate antar-priyayi) **uncollectable** dari sosmed — 157/158 hate nyata di dataset = ngoko. Data yang dibutuhkan tidak bisa di-*scrape*; harus di-*generate*.

**Pipeline baru:** GENERATE (LLM + cultural prompt v2, matriks register × SARA) → consensus-label + **native authenticity spot-check** (QC) → dataset. **Kerja lama di-repurpose, bukan dibuang:**
- Taksonomi 4-dim + prompt v2 = **otak generator**.
- Pipeline labeling 3-LLM (ds+grok+qwen3, D16) = **QC / detektor**.
- Dataset 728 nyata = **jangkar realisme + bukti kelangkaan** (Motivasi paper: "0,9% yield → generation perlu").

**Novelty pillars pasca-pivot** (menggeser tiga pilar D14):
1. **Register-pragmatik hate Jawa** — register menyandi *suhu* benci (panas→ngoko; dingin/contempt/ironis→krama). LLM ternyata bisa generate krama otentik (native menilai "sangat bagus"). (`experiments/register_probe/FINDINGS.md`)
2. **Generator untuk register uncollectable** — krama-report (*ngrasani* pihak ketiga), krama-sarkastik (*pasemon*), krama cold-contempt group-directed: nyata di tutur, nyaris nol di dump.
3. **Detection blind-spot** — **pasemon/ironi lolos SEMUA detektor** (cloud 11%, lokal 0%) pada skala 36-sel × 5 detektor; bukan cuma model murah — cloud pun gagal. Yang membutakan = *implikatur*, bukan kesopanan. (`experiments/generation_pilot/RESULTS_probe.md`)

**Status eksekusi (2026-06-29):** matriks generator 36/36 (3 model) dijalankan; detection probe + multi-model gen + QC judge-panel selesai (semua otomatis). **Bottleneck aktif (by design) = validasi keaslian native** oleh Bapak (`experiments/generation_pilot/VALIDATION_FORM.xlsx`, 27 baris PRIORITAS dulu) → `score_validation.py`.

---

## 1. Background & Problem Statement

### 1.1 Konteks

Ujaran kebencian (hate speech) dalam Bahasa Jawa adalah masalah real yang butuh solusi computational, terutama mengingat:
- ~80 juta penutur Bahasa Jawa
- Konflik horizontal SARA di Indonesia yang sering muncul di social media regional
- Belum ada dataset/protocol/sistem deteksi yang grounded di realitas Jawa

### 1.2 Problem yang ingin diselesaikan

Membangun **dataset + taksonomi + protokol annotation** ujaran kebencian Bahasa Jawa yang:
- Grounded di realitas SARA + register + idiom Jawa (bukan terjemahan)
- Dapat dibangun oleh **single domain-native expert + zero budget tim labeler** (kondisi realistis low-resource)
- Reproducible, ethically sound, properly licensed
- Cukup substantif untuk publikasi Sinta 1

### 1.3 Mengapa pendekatan baru, bukan iterasi

Empat alasan struktural kenapa dataset/codebase translasi tidak bisa di-fix dengan tweak:

1. **SARA Jawa spesifik:** target group (Madura, Tionghoa, Sunda, Batak, Dayak, Papua, Arab, intra-Jawa Mataraman/Arek/Banyumasan), agama (Islam/Kristen/Hindu/Konghucu/aliran kepercayaan), kelas/region (kutha vs ndeso), politik lokal — taksonomi Western/Indonesia tidak men-cover.
2. **Register system:** ngoko/madya/krama. Hate speech krama (formal-halus tapi violent) = phenomenon nyata yang tidak ada padanan English. Carrier utama hate speech antar-priyayi/antar-tokoh.
3. **Pasemon dan idiom:** kiasan dan sindiran budaya Jawa hilang dalam translasi otomatis.
4. **Code-switching organik:** Jawa real-world bercampur Indonesia, Inggris, Arab. Translasi monolingualis menghilangkan ini.

---

## 2. Goals

### 2.1 Primary goals

> **Pasca-D19 (§0.1):** G2 + G3 di-reframe dari *labeling* ke *generation*. G1/G4/G5 tetap.

- **G1.** Develop **Cultural Taxonomy** ujaran kebencian Bahasa Jawa dalam 4 dimensi (target group, severity, register, form) — di-release sebagai codebook formal. *(Sekaligus = otak generator, D19.)*
- **G2.** Develop **fully-automated LLM _generation_ pipeline** (zero-human di penciptaan data; labeling 3-LLM di-repurpose jadi QC/detektor) — kontribusi metodologis: eliminasi bottleneck di **akuisisi/penciptaan** data low-resource, bukan sekadar labeling (D19, §0.1).
- **G3.** Build **dataset** ujaran kebencian Jawa: (a) **generated** register-stratified (krama/sarkastik/pasemon yang *uncollectable*) + (b) **anchor 728 data nyata** code-mixed sebagai realisme + bukti kelangkaan (0,9% yield). **Native-validated authenticity**; anonimized, properly licensed.
- **G4.** Train + report **baseline models / detector probe** sebagai *characterization* (bukan dibandingkan dengan paper lain). Detection blind-spot (pasemon) = hasil karakterisasi utama.
- **G5.** Submit **paper Sinta 2 (JINITA, per D3)** dengan novelty pillars §0.1 (register-pragmatik + generator-uncollectable + detection blind-spot) sebagai kontribusi.

### 2.2 Success criteria

| Goal | Success metric |
|------|----------------|
| G1 | Codebook 4-dimensi published sebagai supplementary; reviewer apresiasi cultural specificity |
| G2 | Pipeline fully documented + reproducible; cross-LLM Krippendorff's α > 0.5 pada data hate asli; adversarial perturbation + XAI reported (per D8) |
| G3 | Dataset ≥ 5K instance; per-category balance memadai; release Hugging Face + Zenodo dengan DOI |
| G4 | Baseline F1 macro per kategori reported; per-register breakdown shown; error analysis register-aware vs register-blind |
| G5 | Paper accepted (atau revise & resubmit) di JINITA / jurnal Sinta 2 list |

---

## 3. Non-Goals (Out of Scope)

Eksplisit untuk avoid scope creep:

- ❌ **Comparison dengan dataset / paper sebelumnya** (termasuk paper v1-v4 milik user sendiri). Tidak ada Tabel 1 yang membandingkan F1 dengan prior work. Paper ini standalone characterization.
- ❌ **State-of-the-art F1 pursuit.** Goal bukan "F1 tertinggi". Goal adalah dataset + protocol + taxonomy yang valid. Baseline number cukup reasonable.
- ❌ **Multi-language extension.** Fokus 100% Jawa. Generalisasi NEIL ke bahasa lain = future work.
- ❌ **Production deployment / API / demo.** Scope = riset, bukan engineering produk.
- ❌ **Real-time detection / streaming.** Offline batch evaluation cukup.
- ❌ **Multi-modal (image / video).** Text only.
- ❌ **Auto-data-augmentation untuk balance class.** Class imbalance dihandle di evaluation (per-category metric), bukan augmentation yang menambah noise.
- ❌ **Adversarial robustness, fairness audit deep-dive, dll.** Future work setelah dataset valid.

---

## 4. Three Pillars (Substansi Riset)

### 4.1 Pillar 1 — Cultural Taxonomy

Codebook 4-dimensi:

**4.1.1 Target group dimension**

| Kategori | Sub-kategori |
|----------|--------------|
| Suku | Madura, Tionghoa, Sunda, Batak, Dayak, Papua, Arab, intra-Jawa (Mataraman/Arek/Banyumasan) |
| Agama | Islam (Sunni/Syiah/Ahmadiyah), Kristen, Katolik, Hindu, Buddha, Konghucu, kepercayaan/kebatinan |
| Kelas/region | wong kutha vs ndeso/gunung, priyayi vs cilik |
| Gender / seksualitas | wanita, LGBTQ+ |
| Politik / tokoh lokal | tokoh agama, partai berbasis Jawa, ormas keagamaan |

**4.1.2 Severity dimension**

| Tingkat | Deskripsi |
|---------|-----------|
| BUK | Bukan ujaran kebencian (diskusi, kritik berbasis argumen, pendapat) |
| Ringan | Stereotyping, slur ringan |
| Sedang | Dehumanisasi, generalisasi negatif kuat |
| Berat | Ancaman, hasutan kekerasan |

**4.1.3 Register dimension** (NOVELTY UTAMA)

| Register | Karakter hate speech |
|----------|----------------------|
| Ngoko | Direct, vulgar, mudah dideteksi rule-based |
| Madya | Mixed, ambigu |
| Krama | **Polite-violent** — bahasa halus, isi keras. Carrier utama hate speech antar-priyayi/antar-tokoh |

**4.1.4 Form dimension**

- Direct (eksplisit)
- Sarcastic (sindiran)
- Idiomatic / pasemon (kiasan)
- Code-switched (Jawa-Indo, Jawa-Arab, Jawa-Inggris)

### 4.2 Pillar 2 — NEIL Annotation Protocol

**Native-Expert-in-the-Loop (NEIL):** protokol untuk single domain-native expert + LLM ensemble.

**Komponen:**

| ID | Komponen | Detail |
|----|----------|--------|
| A | **LLM ensemble silver labeler** | Claude (Anthropic) + GPT-4o (OpenAI) + DeepSeek. Cultural prompting dengan taxonomy + few-shot Javanese examples. 3-way labeling parallel per instance. |
| B | **Active learning + uncertainty sampling** | High-agreement (3-of-3) → silver auto-accept (post-spotcheck). Disagreement → user adjudicates (effort focus on ambiguous). |
| C | **Intra-rater reliability** | User re-code sub-sample 300 instance dengan gap 3-4 minggu. Cohen's κ > 0.7 = acceptable. |
| D | **External verifier subset** | 2-3 Javanese-fluent helper code 200 sample subset (1 hari kerja each). Inter-rater κ subset = external validity. Honorarium Rp 200-500K total. |
| E | **Positionality statement** | User declare native dialek, pendidikan, lokasi, agama, posisi sosial. Methodology section explicit: situated knowledge. |

**Kenapa novel:**
- Existing annotation methodology assume tim 3-5 annotator native dengan κ 0.6+ — tidak realistis untuk low-resource Indonesia
- LLM-as-annotator literature exists tapi mostly English/general; cultural + register-aware prompting = gap
- Triangulasi lengkap (ensemble + active learning + intra-rater + external + positionality) = complete reproducible protocol
- Generalisable ke bahasa daerah lain Indonesia (Bali, Bugis, Sunda, Batak, Banjar, Madura, dll)

### 4.3 Pillar 3 — Dataset + Baseline

**Dataset:**
- Target: 5K (slim) atau 10K (full) instance
- Multi-platform: Twitter/X, Facebook public, YouTube, TikTok, news comments
- Multi-region: Mataraman (Jateng-Yogya), Arek (Jatim), opsional Banyumasan
- Anonimisasi penuh, lisensi Creative Commons NC-SA atau setara
- Release: Hugging Face Datasets + Zenodo (DOI permanent)

**Baseline:**
- DAPT RoBERTa Javanese (kalau bisa di-pretrain ulang from-scratch atau train dari nol)
- IndoBERT, XLM-R-Large
- Per-category F1 macro: target group breakdown, severity breakdown, register breakdown
- Error analysis: register-aware vs register-blind
- Posisi hasil: characterization (seberapa hard task), bukan claim SOTA

---

## 5. Pipeline / Phases

> **⚠️ LEGACY pre-pivot (D19).** Fase 2 (Data collection/scraping) + Fase 3 (NEIL annotation) + Fase 4 (intra/external-rater) menggambarkan pipeline *labeling* yang sudah superseded. Arah aktif = generate → QC → native authenticity (§0.1). Komponen yang masih dipakai: Fase 1 (taxonomy = otak generator), labeling 3-LLM (jadi QC), Fase 5 (baseline/detector probe). Fase di bawah dipertahankan sebagai konteks historis.

### Fase 1 — Taxonomy development (1 bulan)

**Deliverables:**
- [ ] Literature review SARA discourse Indonesia (sosiologi + linguistik)
- [ ] Codebook v1 oleh user (intuisi native + literature)
- [ ] Pilot coding 200 sampel oleh user untuk refine codebook
- [ ] Codebook v2 final + positionality statement

**Acceptance:** Codebook stabil, no major changes setelah pilot 200 sampel (additions OK, restructure NOT OK = sinyal taksonomi belum matang).

### Fase 2 — Data collection (1-2 bulan)

**Deliverables:**
- [ ] Scraping protocol per platform (Twitter API/scraper, FB public, YouTube comments, TikTok comments, news comments)
- [ ] Filter heuristik bahasa Jawa (langid/fastText)
- [ ] Stratified sampling untuk diversitas region + platform + topic
- [ ] Pool ~50K candidate → final ~10K (atau 5K) untuk annotation
- [ ] Anonimisasi pipeline (hapus username, link, mention spesifik)

**Acceptance:** Pool memenuhi distribusi target (per region, per platform, ada candidate dari semua kategori target group).

### Fase 3 — NEIL annotation (2-3 bulan)

**Deliverables:**
- [ ] LLM ensemble run (3 model × 10K instances dengan cultural prompting)
- [ ] Agreement analysis: stratify by agreement level
- [ ] User adjudicates disagreement subset (~30%)
- [ ] Spotcheck random 5% high-agreement → quality assurance

**Acceptance:** Semua instance ada label final + confidence; user adjudication selesai untuk semua disagreement.

### Fase 4 — Validation (1 bulan)

**Deliverables:**
- [ ] Intra-rater coding (user re-code 300 sampel setelah gap 3-4 minggu) → Cohen's κ
- [ ] External verifier (2-3 helper × 200 subset) → inter-rater κ
- [ ] Quality report transparant (per-kategori κ, disagreement patterns, dll)

**Acceptance:** Intra-rater κ > 0.7. External κ subset reported (target > 0.6, kalau di bawah → diskusi explicit di paper).

### Fase 5 — Modeling baseline + characterization (1 bulan)

**Deliverables:**
- [ ] Baseline training: DAPT RoBERTa Javanese, IndoBERT, XLM-R-Large
- [ ] Per-category F1 breakdown (target group / severity / register)
- [ ] Error analysis: register-aware vs register-blind
- [ ] Characterization report

**Acceptance:** Baseline reproducible; per-category metric clear; error patterns dokumented.

### Fase 6 — Paper writing + dataset release (1-2 bulan)

**Deliverables:**
- [ ] Draft paper Sinta 1 (~8K words)
- [ ] Dataset upload ke Hugging Face + Zenodo (DOI)
- [ ] Codebook supplementary + positionality statement
- [ ] HKI submission untuk dataset + codebook (paralel)
- [ ] Submit ke target jurnal Sinta 1

**Acceptance:** Paper submitted; dataset live dengan DOI permanent; HKI submission diterima.

**Total timeline:** 6-9 bulan realistic. Slim version (5K, 2 region): 3-4 bulan.

---

## 6. Target Venue

**Primary:** JINITA (Journal of Innovation Information Technology and Application), Politeknik Negeri Cilacap, **Sinta 2** (berlaku hingga 2028).
- P-ISSN 27160858 / E-ISSN 27159248
- OJS: https://ejournal.pnc.ac.id/index.php/jinita
- SINTA profile: https://sinta.kemdiktisaintek.go.id/journals/profile/10719
- Frekuensi: semiannual

**Backup (Sinta 2 lain):** Pilih saat Fase 6 berdasarkan fit topical + turnaround time.

---

## 7. Resource Requirements

### 7.1 Budget

| Item | Estimasi |
|------|----------|
| API LLM (Claude + GPT-4o + DeepSeek) | $50-150 USD untuk 10K × 3 model dengan caching |
| Compute training (RTX 4080 existing) | 0 |
| External verifier honorarium | Rp 200-500K (3 helper × 1 hari) |
| APC venue Sinta 1 | Rp 0-3 juta (variabel per jurnal) |
| **Total** | **Rp 1-5 juta**, bayar sendiri OK |

### 7.2 Time investment user

- Adjudication: ~1.5K-3K instance × 1 menit avg = 25-50 jam, spread 60 hari = ~30-50 menit/hari
- Intra-rater + paper writing: 30-50 jam
- **Total: ~75-100 jam user time spread 6-9 bulan = realistis**

---

## 8. Risks + Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| Reviewer ragu validitas single annotator | Tinggi | Pillar 2C+2D+2E (intra-rater + external + positionality) explicit di Methodology |
| LLM ensemble bias (vendor bias) | Medium | 3 vendor berbeda; report disagreement distribution; cultural prompting |
| Etika scraping (privacy concern) | Medium | Anonimisasi penuh, no re-identification, ethics statement, public posts only |
| Heterogenitas dialek Jawa | Medium | Stratified sampling per region; codebook explicit tentang scope dialek |
| Time slip (6-9 → 12+ bulan) | Tinggi | Slim version backup (5K target, 2 region) |
| Insiden hardware (petir, dll) berulang | Low-medium | Git push ≥ weekly; Cloud backup data labeled |
| LLM API cost overrun | Low | Cache + batch + cheap-first ordering (DeepSeek dulu, Claude/GPT untuk disagreement) |

---

## 9. Open Decisions

**Resolved (lihat §0 Decisions Log):**
- [x] **Scope:** 10K dengan gate 3K (re-evaluate via pilot) — D7
- [x] **Venue commit:** JINITA primary, backup Sinta 2 lain saat Fase 6 — D3
- [x] **Dialek scope:** Jawa + turunan only sebagai sumber, Sunda/Madura tetap target group — D5
- [x] **Authorship:** 3 authors UBHINUS (Mukhlis, Yekti, Daniel) — D4
- [x] **Ethics protocol LPPM:** ya, ajukan paralel Fase 1 (default approval — bisa cancel kalau ternyata pakai existing dumps saja, ethics letter mungkin tidak perlu)
- [x] **Dataset license:** CC BY-NC-SA 4.0 (default approval)

**Still open:**
- [ ] **HKI batch placement:** masuk ke Batch berapa di tridarma tracker UBHINUS? (perlu input user)

---

## 10. Output Catalog (paralel)

| Output | Bentuk | KUM | Timeline |
|--------|--------|-----|----------|
| Paper Sinta 2 first author (JINITA) | Jurnal | 25 | Fase 6 |
| Dataset HKI | Karya Ciptaan (Basis Data) | 15 | Fase 4-6 |
| Codebook HKI | Karya Tulis (Buku/Spec) | 15 | Fase 1-6 |
| **Total** | | **55 KUM** | |

Plus foundational dataset Jawa untuk research masa depan (PhD project, follow-up papers, generalisasi NEIL ke bahasa daerah lain).

---

## 11. Connection to Career Roadmap

**Tridarma:** Bidang B (Penelitian) anchor untuk semester berjalan + ke depan.

**PhD profile:** Methodologically rigorous low-resource NLP paper. Aligned dengan supervisor target:
- Bisazza (Groningen) — low-resource NLP
- Plank (LMU) — low-resource + Hovy social NLP
- Hovy (Bocconi) — social NLP
- Nguyen (Utrecht) — sociolinguistics

NEIL protocol = transferable methodology untuk PhD project di bahasa daerah lain Indonesia, atau bahasa minoritas global. Strong foundation untuk PhD application narrative.

---

## 12. Document History

| Version | Date | Change |
|---------|------|--------|
| 0.1 | 2026-05-07 | Initial draft after concept session with Claude |
| 0.3 | 2026-06-08 | Novelty reframe (D14): drop klaim "dataset pertama" → pipeline + taksonomi + code-mixed |
| 0.4 | 2026-06-29 | **PIVOT labeler → generator dikunci** (D19): tambah §0.1 (framing aktif) + D16–D19 ke Decisions Log; G2/G3 re-anchor ke generation; §4.2 NEIL + §5 Phases 2–4 ditandai legacy. |
