# Ujaran Kebencian Jawa — Cultural Grounding (CLAUDE.md)

**TLDR:** Riset baru dari awal tentang deteksi ujaran kebencian Bahasa Jawa. **BUKAN iterasi proyek lama**. Fokus: cultural taxonomy + **fully automated LLM pipeline** (low-resource as novelty) + dataset from-scratch. Target paper Sinta 2 (JINITA).

**Owner:** Mukhlis Amien (native Javanese speaker, dosen UBHINUS/STIKI Malang)
**Coauthors:** Yekti Asmoro Kanthi, Daniel Rudiaman Sijabat (semua UBHINUS)
**Status:** Pre-eksperimen — decisions methodologis tentative, di-resolve via pilot
**Started:** 2026-05-07
**Updated:** 2026-05-07 (pivot framing ke Fully LLM)

---

## Apa proyek ini

Bangun dataset + taksonomi + pipeline auto-labeling ujaran kebencian Bahasa Jawa yang grounded di realitas SARA + register + idiom Jawa. Target output:
- 1 paper jurnal Sinta 2 (JINITA)
- 1 dataset HKI (release Hugging Face + Zenodo)
- 1 codebook HKI (release sebagai supplementary)

PRD lengkap: [PRD.md](PRD.md)

---

## HARD RULES untuk sesi Claude Code

### 1. PRD.md adalah source of truth
Semua keputusan riset (scope, metodologi, taksonomi, deliverable) harus konsisten dengan [PRD.md](PRD.md). Kalau ada konflik antara intuisi dan PRD, baca PRD dulu. Kalau PRD perlu di-update karena keputusan baru, update PRD-nya — jangan diam-diam menyimpang.

### 2. BUKAN iterasi v1-v4 — jangan tambal sulam
Proyek lama (`D:\documents\ujaran-kebencian-bahasa-jawa\` + repo `neimasilk/ujaran-kebencian-bahasa-jawa`) **TIDAK DIPAKAI** sebagai baseline, comparison, atau acuan apapun. Alasan: dataset lama mayoritas terjemahan English/Indonesia → tidak menangkap realitas SARA Jawa.

**Root cause incident:** Mahasiswa annotator v1-v4 "curang" dengan back-translation English/Indo → Jawa, hanya sedikit yg dianotasi asli. Mahasiswa sudah lulus, tidak available untuk fix. Ini concrete case **mengapa human-in-loop dengan kontrol terbatas = high risk**, dan motivation utama untuk fully-LLM framing. Story ini akan di-cite (anonimized) di paper introduction sebagai concrete failure mode.

Kalau Claude Code sesi mendatang menyarankan "load dataset lama untuk comparison" atau "extend prior pipeline" — **TOLAK**. Ini standalone.

### 3. Eliminating human bottleneck = core novelty
**Tagline definitif:** "Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation".

Default pipeline (zero human end-to-end):
- Existing public dumps → LLM filter Jawa → LLM filter likely-toxic → LLM full-taxonomy label → BERT training → automated eval
- Validation: cross-LLM consistency (Claude + GPT-4o + DeepSeek), Krippendorff's α antar-LLM, adversarial perturbation testing, XAI (LIME/SHAP) untuk interpretability

**Fallback ladder** (kalau pilot gagal):
1. Zero human (default, aim utama)
2. Minimal sanity check (~50 sampel, ~1 jam Bapak) — quick agree/disagree spot-check, bukan annotation
3. Pending — rethink based on pilot data

User waktu sangat terbatas (weekend only, ~5-15 jam/bulan) — pipeline harus auto-by-default, minta user effort cuma kalau benar-benar perlu (decision sessions, paper review).

Jangan menyarankan rekrut multi-annotator manual. Story mahasiswa cheating (HARD RULE #2) = case-in-point.

### 4. Cultural specificity adalah core, bukan optional
Setiap sample, setiap label, setiap baris codebook harus refleksikan SARA Jawa real-world (Madura/Tionghoa/Sunda/Batak/dll, Islam/Kristen/Hindu/Konghucu/aliran kepercayaan, Mataraman/Arek/Banyumasan, krama/ngoko, pasemon, code-switching). Kalau prompt LLM atau metodologi terasa "generic hate speech detection" — itu sinyal red flag, perlu di-ground ulang ke konteks Jawa.

### 5. Output target = Sinta 2 (JINITA primary)
Paper utama target **JINITA** (Journal of Innovation Information Technology and Application, Politeknik Negeri Cilacap, Sinta 2 berlaku hingga 2028). Backup venue Sinta 2 lain bisa dipilih saat Fase 6. Jaga rigor + novelty + reproducibility — fokus pada framing kontribusi (low-resource fully-LLM pipeline), bukan F1 chase.

### 6. Code + data discipline
- Repo Git wajib sejak hari pertama; push ke GitHub (private dulu) minimal weekly. Jangan repeat insiden petir 2026-04-29 yang menghilangkan kerja yang tidak di-push.
- Dataset raw + intermediate + labeled disimpan dengan struktur clear (`data/raw/`, `data/labeled/`, `data/golden/`, dll)
- Code di `src/`, notebook eksplorasi di `notebooks/` — tidak campur
- Setiap LLM run di-log (input prompt + model version + tanggal) untuk reproducibility

### 7. Etika + privacy
- Anonimisasi penuh (hapus username, link, mention spesifik) sebelum analisis
- Tidak pernah re-identify individu
- Public posts only (tidak DM, tidak private group)
- Statement etik di README + paper

### 8. Update progress tracker
File `STATE.md` (akan dibuat saat eksekusi mulai) adalah live state per fase. Update setiap milestone selesai. Kalau drift > 1 minggu dari plan PRD, flag explicit di STATE — jangan diam-diam slip.

---

## Workflow saat ini (Pre-eksperimen → Pilot)

Decisions pondasi sudah disepakati (2026-05-07): venue JINITA, authorship 3 orang, dialek Jawa+turunan, framing pivot ke Fully LLM. Detail metodologis (cultural prompt, multi-LLM consensus, scraping vs dumps, dll) **di-resolve via eksperimen pilot, bukan blueprint a priori**.

Prioritas berikut:
1. Setup repo Git + struktur folder dasar
2. Pilot eksperimen #1: test DeepSeek/Claude/GPT-4o di subset kecil Jawa untuk ukur (a) refusal rate, (b) Jawa quality, (c) inter-LLM agreement
3. Codebook v0 draft (paralel dengan pilot, foundation taksonomi)
4. Update STATE.md "Challenges Log" tiap eksperimen — challenges + lessons = materi paper

### Riset = coba-coba (research is exploratory)
Decisions methodologis bisa berubah berdasarkan hasil eksperimen. Itu fitur, bukan bug. Dokumentasi tantangan + lessons-learned sambil jalan = potential kontribusi paper sendiri.

---

## Konteks dari KB (read-only)

Wiki entry singkat tersedia di KB pribadi user:
`C:\Users\Mukhlis Amien\knowledge-base\research\ujaran-kebencian-jawa-baru.md`

KB itu tracking-only (status + summary). **Source of truth deep work = folder ini, bukan KB.** KB di-update saat ada milestone besar atau decision penting.

Project lain di KB yang related (sister projects, untuk awareness saja, bukan untuk dipakai):
- `research/korupsinlp.md` — Indonesian legal NLP
- `research/ronggo.md` — low-resource MT (Bahasa Sekar)
- `research/jamukg.md` — Indonesian KG
- `research/ujaran-kebencian-jawa.md` — proyek LAMA v1-v4 (jangan di-touch dari sesi ini)

---

## Daily protocol

Saat user buka sesi Claude Code di folder ini:
1. Baca CLAUDE.md (otomatis)
2. Baca PRD.md (full, konfirmasi konteks riset)
3. Baca STATE.md kalau sudah ada (current execution state)
4. Tanya user: "Apa yang mau dikerjakan hari ini?" — fase mana, milestone apa
5. Jangan asumsi user mau implementasi langsung — bisa jadi diskusi codebook, refine PRD, dsb

Saat session selesai:
1. Update STATE.md kalau ada perubahan state
2. Commit + push changes ke Git
3. Catat insight non-obvious ke `notes/` (kalau ada)

---

## Anti-patterns (jangan lakukan)

- ❌ "Mari load dataset lama untuk warm-start" — proyek lama OUT OF SCOPE
- ❌ "Bandingkan F1 baru vs paper v1-v4" — tidak ada comparison dengan prior, ini standalone
- ❌ "Fine-tune dulu pakai data terjemahan untuk transfer" — itu mengulang masalah yang ingin dihindari
- ❌ Push F1 dengan training tricks tanpa validasi label quality dulu — root cause kegagalan v1-v4 adalah label, bukan model
- ❌ "Lebih cepat kalau pakai 1 LLM saja" — multi-LLM consensus (3 model) = wajib untuk validation triangulasi
- ❌ "Tambah human verification untuk legitimacy" — bertentangan framing zero-human; cari automated alternative dulu (cross-LLM, perturbation, XAI)
- ❌ "Rekrut beberapa mahasiswa untuk anotasi gold" — story mahasiswa cheating menunjukkan high-risk approach ini
