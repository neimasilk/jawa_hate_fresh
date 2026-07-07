# Decisions Log

_Last touched: 2026-07-06 (D20 reframe paper generator→diagnostic-suite + venue=JINITA saja; strategic review Fable 5). Source-of-truth untuk decision rationale._

Cross-ref: [`PRD.md` §0](../PRD.md) (kanonik), [STATE.md sesi log](../STATE.md), [memory project files](../../.claude/projects/C--Users-Mukhlis-Amien-Documents-ujaran-kebencian-jawa-fresh/memory/MEMORY.md).

---

## D1 — Framing pivot ke "Fully Automated LLM Pipeline"

**Date:** 2026-05-07
**Decision:** Dari "NEIL = native-expert-in-the-loop" ke **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** sebagai core novelty paper.

**Rationale:**
- User constraint: weekend only, ~5-15 jam/bulan → human-in-loop tidak realistis
- Story konkret: mahasiswa annotator v1-v4 "curang" dengan back-translate English/Indo → Jawa, hanya sedikit yg dianotasi asli. Mahasiswa sudah lulus, tidak available untuk fix. **Human-in-loop bisa jadi sumber error**, bukan otomatis solusi.
- Framing flip: bukan kompromi (limitation), tapi novelty (low-resource × LLM = research contribution).

**Konsekuensi:** Riset mendalam §4.1 (3 anotator + Cohen's κ) DIABAIKAN. CLAUDE.md HARD RULE #3 di-rewrite ke "eliminate human bottleneck = core novelty".

**Tagline:** "Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"

**See also:** [glossary: NEIL](glossary.md#neil), [pilots.md](pilots.md).

---

## D2 — Fallback ladder kalau pilot gagal

**Date:** 2026-05-07
**Decision:** Kalau Pilot #1 gagal (refusal tinggi / α rendah / validity rendah), fallback ladder:
1. **Default:** Zero human (target utama)
2. **Marginal pilot:** Minimal sanity check ~50 sampel (~1 jam Bapak), spot-check agree/disagree, BUKAN annotation
3. **Buruk pilot:** Pending, rethink based on data

**Rationale:** User pilih "tertarik dengan opsi 1, tapi kalau gagal pivot ke 2 atau 3" — aim high, safety net.

---

## D3 — Venue: JINITA Sinta 2

**Date:** 2026-05-07
**Decision:** JINITA (Politeknik Negeri Cilacap, Sinta 2 berlaku hingga 2028) sebagai venue utama.

**Rationale:** User pilih eksplisit. Original plan target Sinta 1 (di CLAUDE.md awal), Bapak prefer JINITA. Asumsi alasan: turnaround time / fit topical / akses editor.

**Konsekuensi:** CLAUDE.md HARD RULE #5 update ke Sinta 2. KUM first author 25 (bukan 40). Total output catalog: 25 (paper) + 15 (dataset HKI) + 15 (codebook HKI) = **55 KUM**.

**Verified:**
- P-ISSN 27160858 / E-ISSN 27159248
- OJS: https://ejournal.pnc.ac.id/index.php/jinita
- SINTA: https://sinta.kemdiktisaintek.go.id/journals/profile/10719
- Frekuensi: semiannual

---

## D4 — Authorship: 3 authors UBHINUS

**Date:** 2026-05-07
**Decision:** 3 authors:
1. Mukhlis Amien — corresponding, amien@ubhinus.ac.id
2. Yekti Asmoro Kanthi — yektiasmoro@ubhinus.ac.id
3. Daniel Rudiaman Sijabat — daniel223@ubhinus.ac.id

Semua afiliasi UBHINUS / STIKI Malang.

---

## D5 — Dialek scope

**Date:** 2026-05-07
**Decision:**
- **Bahasa sumber dataset** = Jawa + turunan (Mataraman, Arek, Banyumasan, Cirebonan, Osing, Tengger, dll). **Sunda + Madura excluded** dari sumber.
- **Target group hate speech** = TETAP include semua suku (Madura, Sunda, Tionghoa, Batak, Dayak, Papua, Arab, dll), karena mereka bisa jadi sasaran ujaran kebencian dalam tuturan Jawa.

**Rationale:** User: "jawa keseluruhan, asalkan masih jawa dan turunannya, bukan sunda dan madura". Hindari konflasi bahasa daerah Indonesia lain dengan Jawa.

**Implikasi:** Saat sampling, filter via langid/LLM untuk Jawa + turunan. Code-switching Jawa-Indo OK. Sampel pure Sunda atau pure Madura → reject.

---

## D6 — Data source: existing public dumps

**Date:** 2026-05-07
**Decision:** Default pakai **OSCAR-2301 jv subset** + **CC100** + opsional **manueltonneau/indonesian-hate-speech-superset**. Live scraping dihindari.

**Rationale:** User flag "scrapping ujaran kebencian di internet ga gampang". Hate speech minority class + platform aktif moderasi + API mahal/tertutup + langid Jawa false-positive tinggi. Realistis bisa butuh scrape 100K-1M comment untuk 10K hate speech murni.

**Implikasi:** Pipeline jadi `existing dumps → LLM filter Jawa → LLM filter likely-toxic → LLM full-taxonomy label → BERT training → automated eval`.

---

## D7 — Data scope: 10K dengan gate di 3K

**Date:** 2026-05-07
**Decision:** Target 10K samples, dengan **go/no-go gate di 3K** sampel pertama. Re-evaluate setelah 3K via cross-LLM α + cost track.

**Rationale:** BERT-family classifier sweet-spot 5K-50K. 10K = ~167 sample/cell untuk taxonomy 60 cells (4-dim cross). Gate 3K = exit valve kalau LLM quality tidak cukup.

---

## D8 — Validation strategy

**Date:** 2026-05-07
**Decision:** Default **zero human in validation**. Pakai:
- Cross-LLM consistency (DeepSeek + Grok + Kimi)
- Krippendorff's α antar-LLM
- Adversarial perturbation testing
- XAI (LIME/SHAP) untuk interpretability

**Fallback** kalau zero-human tidak credible: minimal sanity check ~50 sampel oleh Bapak (lihat D2).

---

## D9 — Riset = exploratory, dokumentasi tantangan = kontribusi

**Date:** 2026-05-07
**Decision:** Decisions methodologis bisa berubah berdasarkan eksperimen. Detail blueprint a priori = minimum. Pilot dulu, blueprint setelahnya. **Dokumentasi tantangan + lessons-learned sambil jalan = potential kontribusi paper sendiri.**

**Rationale:** User: "riset itu khan coba2, ga ada yg pasti, dokumentasi tantangan sambil jalan, dan ini bisa jadi kontribusi". Methodology paper sering dibangun dari lesson-learned.

**Konsekuensi:** STATE.md punya **Challenges Log** section — update setiap eksperimen dengan tantangan, hipotesis, eksperimen, hasil, lesson.

---

## D10 — Vendor mix: DeepSeek V4 + Grok 4.3 + Kimi K2.6

**Date:** 2026-05-07
**Decision:** Drop Anthropic Claude + OpenAI GPT-4o. Pakai 3 LLM lain sesuai API keys yang user provide:
- DeepSeek V4 Pro (`deepseek-v4-pro`)
- xAI Grok 4.3 (`grok-4.3`)
- Moonshot Kimi K2.6 (`kimi-k2.6`)

Semua OpenAI-compatible API → code simpler (1 SDK + 3 base_url).

**Verified:** Connectivity test 3/3 ✅ per 2026-05-07. Semua paham Jawa krama.

**Quirks:** Kimi K2.6 force `temperature=1.0` (only value allowed). Sudah di-override di `call_kimi()`. Determinism diandalkan dari few-shot + structured output prompt.

---

## D11 — Adopsi pattern Karpathy autoresearch (Pilot #4)

**Date:** 2026-05-07
**Decision:** Pilot #4 adopsi pattern Karpathy autoresearch (`~/Documents/autoresearch/`) untuk autonomous prompt iteration loop.

**Rationale:** Pattern fit dengan framing "eliminate human bottleneck" + "tantangan = kontribusi" + user weekend-only constraint. Agent kerja overnight, Bapak bangun lihat hasil.

**Adaptasi:** Edit `prompts/cultural_classification_vN.md` (single file scope), eval 50-sample subset × 3 LLM, composite metric (refusal + validity + α + entropy), bounded loop ~$12.5/run, cultural injection di `program_prompt_research.md`.

**Eksekusi:** Setelah Pilot #1-3 baseline jelas. Detail di [pilots.md#pilot-4](pilots.md#pilot-4--autoresearch-loop).

---

## D12 — Adopsi pattern Karpathy LLM Wiki (dokumentasi)

**Date:** 2026-05-07
**Decision:** Adopsi pattern Karpathy LLM Wiki (Apr 2026 gist) untuk struktur dokumentasi proyek. User fokus baca `wiki/`, agent maintain.

**Rationale:** Match dengan user preference "saya fokusnya hanya melihat wiki, kamu yg mengatur". Lean version: 6 file (SCHEMA, index, log, decisions, pilots, glossary). Expand sesuai pattern incremental kalau butuh.

---

## D13 — Data strategy: code-mixed via dump hate Indonesia

**Date:** 2026-05-25 (dinomori retroaktif 2026-06-08)
**Decision:** Tidak ada korpus hate Jawa siap-unduh (survei: dataset UI/WCSE 2021 cuma di paper, tidak di-release). Maka: **filter dump hate Indonesia (`haipradana`, ~12.7K tweet) via LLM → ekstrak subset Jawa/code-mixed**. Code-mixed diterima sebagai scope sah.

**Rationale:** Pilot #2 memvalidasi empiris: Jawa murni nyaris nol di sosmed (1/250), hate Jawa real didominasi code-mixed. Insisting "ngoko/krama murni" akan bias jauh dari realita.

**Konsekuensi:** Pipeline D6 di-refine: `dump hate Indonesia → LLM filter Jawa/code-mixed → LLM full-taxonomy label → ...`. Yield rendah (~9.6% Jawa+campuran, ~3.6% hot) → pool besar butuh filter banyak baris.

**See also:** [pilots.md Pilot #2](pilots.md), STATE.md Challenges Log C4 + C-scope.

---

## D14 — Novelty reframe: pipeline + taksonomi, bukan "dataset pertama"

**Date:** 2026-06-08
**Decision:** Klaim "dataset from-scratch / pertama" **DITINGGALKAN** (dataset hate Jawa sudah pernah dibuat: UI/WCSE 2021). Novelty utama paper di-reframe ke tiga pilar:
1. **Pipeline fully-automated zero-human** (eliminating human bottleneck)
2. **Taksonomi kultural 4-dimensi register-aware** (lebih dalam dari prior work)
3. **Code-mixed realism** (grounded di realita sosmed, bukan Jawa murni idealisasi)

Dataset tetap deliverable (HKI + release HF/Zenodo) — boleh disebut "first *publicly released* Javanese hate speech dataset" sebagai fakta sekunder, bukan klaim utama.

**Rationale:** User pilih opsi "reframe ke pipeline+taksonomi" (paling defensible ke reviewer; klaim "pertama" rawan ditembak). Pilot #2 memberi bukti empiris untuk pilar 3.

**Konsekuensi:** PRD v0.3: G2 (NEIL → pipeline), G3 (from-scratch → code-mixed + publicly-released), G5 (Sinta 1 → Sinta 2 JINITA, sinkron D3). Paper introduction tetap cite story mahasiswa cheating sebagai motivasi pilar 1.

---

## D15 — Vendor mix final: 2-LLM deepseek+grok, Kimi dropped

**Date:** 2026-06-10
**Decision:** Pipeline cross-LLM consistency memakai **2 LLM: DeepSeek V4 Pro + Grok 4.3**. Kimi K2.6 **di-drop** dari pipeline (keputusan Bapak: "untuk kimi biarin, pakai yg ada aja").

**Rationale:**
1. **Operasional:** saldo Moonshot habis (run Kimi Pilot #3 v1 gagal 149/149 call, 429 insufficient balance).
2. **Empiris (lebih penting):** di n=149 Kimi = penyumbang noise — validity 73.8% (vs ds 95.3% / grok 100%), 126s/call (vs 7s grok), out-token 475K (~30× grok). Keunggulannya (pairwise ds–kimi 86.1%, drop-Grok α 0.722) tidak menebus ongkos praktis untuk bulk.
3. α tetap terukur dengan 2 rater; klaim "cross-LLM consistency" tetap valid (2 vendor independen).

**Konsekuensi:**
- Update D8 (validation strategy): consensus = deepseek+grok; baseline α pair ini di prompt v0 = **0.534** (bukan 0.587 3-LLM).
- Data Kimi v0 n=149 TETAP dipakai di paper sebagai **sensitivity analysis 3-vs-2 vendor** (tabel drop-1-vendor) — narasi seleksi vendor berbasis data = materi metodologi.
- Pilot #3+ eval cukup ds+grok (~50 mnt + ~$1.1/iter); tidak ada dependensi saldo Moonshot.

**See also:** [pilots.md Pilot #1b + #3](pilots.md), STATE.md Challenges Log (C-vendor + ops-resume), PRD §0 D15.

---

## D16 — Vendor mix final: 3-rater DeepSeek + Grok + qwen3:14b lokal

**Date:** 2026-06-11 (di-log retroaktif 2026-06-15)
**Decision:** Cross-LLM consistency memakai **3 rater**: DeepSeek V4 Pro + Grok 4.3 (cloud) + **qwen3:14b lokal** (Ollama, RTX 4080). **Memperluas** D15 (yang 2-LLM ds+grok) — qwen3 **ditambah** sebagai rater independen ke-3, bukan pengganti Grok.

**Rationale:**
1. Pilot #6 membuktikan qwen3:14b LOLOS sebagai rater (α(ds,qwen3) 0.660, CI overlap dengan ds+grok 0.763).
2. Rater ke-3 independen = triangulasi consensus lebih kuat (3 vendor, 2 keluarga arsitektur, 2 lokasi cloud+lokal).
3. qwen3 gratis + lokal → sebagian pipeline **reproducible tanpa API berbayar**; mengurangi risiko kredit habis (insiden Kimi D15 + xAI Pilot #5).
4. Cascade filter (Pilot #6b) pakai lokal untuk pre-screen murah, grok untuk verify (pool tetap grok-confirmed).

**Konsekuensi:**
- Consensus = majority vote 3 rater (≥2 label valid). Dataset Pilot #5 pakai aturan ini (331 consensus / 1 tie).
- qwen3 = rater paling bising (lone-dissenter 31/64 non-unanimous) → klaim α utama paper pakai **pasangan primer ds+grok** (held-out 0.670); 3-rater (held-out 0.565) dilaporkan sebagai consensus konservatif + bukti reproducibility.
- Data Kimi v0 (D15) tetap dipakai sebagai sensitivity 3-vs-2 vendor di paper.

**See also:** [pilots.md Pilot #5 + #6](pilots.md), [D15](#d15--vendor-mix-final-2-llm-deepseekgrok-kimi-dropped), STATE.md C8/C9.

---

## D17 — Metrik α dikanonikkan (Krippendorff coincidence-matrix) + verifikasi adversarial = SOP

**Date:** 2026-06-15
**Decision:** (1) `src/agreement.py krippendorff_alpha_nominal` diubah ke **bentuk kanonik coincidence-matrix** dengan bobot per-unit 1/(m_u−1) (sebelumnya "pooled pairs" tanpa bobot). (2) Sebelum angka analisis masuk paper/commit, jalankan **verifikasi adversarial** (code-audit + recompute independen).

**Rationale:**
- Temuan verifikasi Pilot #5: formula lama membiaskan Do saat coverage rater tak rata (unit 2 vs 3 rater). Identik untuk 2-rater (semua angka headline ds+grok TAK berubah); 3-rater bergeser (pilot01b 0.587→0.613, Pilot #5 held-out 0.558→0.565). Reviewer yang pakai library standar akan dapat angka kanonik → wajib konsisten. Divalidasi vs dataset rujukan Krippendorff (α=0.743).
- Verifikasi menangkap bug dedup yang **recompute independen sendiri lewatkan** (ia meniru urutan dedup yang sama) → butuh DUA jalur: code-audit (logika) + recompute (angka). Ini sendiri = materi metodologi paper ("rigor tanpa human gold").

**Konsekuensi:** `is_valid_json` kini wajib key 'hate' (refusal ≠ valid label; tak pengaruh α). pilot01b copy lokal disinkronkan. Semua α baru (Pilot #5+) kanonik. Angka 2-rater historis (0.763, 0.660, 0.747) tetap sah.

**See also:** STATE.md C9, `experiments/pilot05_bulk_labeling/report.md`, commit `fbd59a2`.

---

## D18 — Opsi A dieksekusi: perbesar pool via cascade (resolve D-OPEN-2)

**Date:** 2026-06-22
**Decision:** Pilih **perbesar pool via cascade filter (Pilot #6b)** daripada ship dataset 331 apa adanya. Dataset diperbesar **332 → 735 teks** (728 consensus). Vendor mix tetap 3-rater ds+grok+qwen3 (D16).

**Rationale:**
- Cascade (SEA-LION→qwen3 lokal pre-screen → grok verify) sudah dijalankan: pass1/pass2 lokal selesai, tapi pass3 grok verify **terblokir xAI 403** (kredit habis 2026-06-18) di 389/1687 → pool sempat mentok 431.
- Sesi 2026-06-22: Bapak konfirmasi kredit xAI terisi ($4.55). Live test grok ✅ → lanjutkan verify 1298 sisa. Confirm-rate grok di pass2-keeps = **25%** (1687→+304 keeps) → local pre-screen over-keep (temuan cascade-design untuk paper). **Dump haipradana habis** (12.7K terfilter penuh) → 735 ≈ ceiling sumber ini.
- Held-out validation justru **MENGUAT** di skala lebih besar: ds+grok held-out α **0.688** [0.614, 0.759] di 586 teks (vs Pilot #5 0.670 di held-out lebih kecil), CI lebih sempit → klaim anti-overfit lebih kuat. Worth it.

**Konsekuensi:** Dataset jadi 728 consensus (158 hate / 570 non-hate). SARA lebih kaya (tambah agama_kristen 18, suku_arab 11, agama_kepercayaan 12, hindu/rohingya/jepang). Tetap < gate D7 BERT (3K) → modeling perlu sumber tambahan ATAU framing dataset sebagai deliverable (bukan F1-chase). Biaya sesi ~$2.8 grok dari $4.55. Held-out α 3-rater 0.513 / full 0.545 (qwen3 tetap rater paling bising; ds+qwen3 0.462, grok+qwen3 0.438). Angka headline ds+grok diverifikasi recompute independen (cocok persis).

**See also:** [pilots.md Pilot #6b](pilots.md), STATE.md C10, `experiments/pilot05_bulk_labeling/report.md`.

---

## D19 — 🔄 PIVOT BESAR: Labeler → Generator

**Date:** 2026-06-23 (formalisasi + lock ke PRD 2026-06-29)
**Decision:** Arah inti proyek berubah dari **melabeli data Indonesia yang ada** (filter `haipradana` → label 3-LLM) ke **LLM sebagai GENERATOR** ujaran kebencian Jawa *fresh* register-stratified, divalidasi keasliannya oleh native. Pipeline baru: **GENERATE → consensus-QC → native authenticity check → dataset**.

**Rationale:**
- **Maksud asli ≠ yang dibangun.** Per Bapak (2026-06-23), niat sejak awal SELALU = generator. Istilah "annotation" di PRD/CLAUDE.md (di NLP = labeling) menyebabkan setiap sesi diam-diam membangun *labeler*. Drift ini tak pernah masuk source-of-truth → bertahan berbulan. Bapak kecewa saat sadar.
- **Bukti empiris human bottleneck di akuisisi, bukan labeling:** filter dump `haipradana` (8.269 tweet) → hanya **74 (0,9%) Jawa asli**, 62% Indonesia. Register krama/pasemon (carrier hate antar-priyayi, novelty inti) **uncollectable** dari sosmed — 157/158 hate nyata = ngoko. Data yang dibutuhkan tak bisa di-scrape; harus di-generate.
- Penemuan register-pragmatik (`experiments/register_probe/FINDINGS.md`) + LLM bisa generate krama otentik (native: "sangat bagus") membuat generator *feasible*, bukan sekadar diinginkan.

**Konsekuensi:**
- **Kerja lama di-repurpose, bukan dibuang:** taksonomi 4-dim + prompt v2 = otak generator; pipeline labeling 3-LLM (D16) = QC/detektor; dataset 728 = jangkar realisme + **bukti kelangkaan** (Motivasi paper: "0,9% yield → generation perlu").
- **Novelty pillars menggeser D14:** (1) register-pragmatik hate Jawa, (2) generator untuk register uncollectable, (3) detection blind-spot (pasemon lolos SEMUA detektor — cloud 11%, lokal 0%, di skala 36×5). Lihat `experiments/generation_pilot/RESULTS_probe.md`.
- **Peran native = authenticity referee**, bukan annotator (tetap konsisten zero-human-labeling; native hanya menilai keaslian sampel generated). Bottleneck aktif by design.
- PRD dikunci ke framing ini: **PRD §0.1** (2026-06-29, v0.4) = arah aktif; §4.2 NEIL + §5 Phases 2–4 = legacy.

**See also:** PRD §0.1, memory `generator-not-labeler-pivot`, `experiments/generation_pilot/README.md`, HANDOFF.md (sesi 3–5).

---

## D20 — Reframe paper: Generator → Diagnostic-suite + venue = JINITA saja

**Date:** 2026-07-06 (sesi 9, strategic review Fable 5 → eksekusi Sonnet)
**Decision:** (1) Paper direframe dari headline "Generation" ke **diagnostic-suite framing** (gaya HateCheck): generator = metode konstruksi stimulus, blind-spot deteksi = kontribusi utama. (2) Validator native ke-2/3 = **Yekti Asmoro Kanthi dan Daniel Rudiaman Sijabat** (dikonfirmasi penutur Jawa aktif). (3) **Venue target = JINITA Sinta 2 saja** — TIDAK mengejar Scopus/Q-tier untuk paper ini (paket eksperimen mahal seperti fine-tune IndoBERT/E5 tidak dikerjakan).

> **Koreksi (D21, 2026-07-07):** poin (2) salah untuk Daniel — ia **bukan penutur asli** Jawa (30 tahun resident Jawa Timur, fasih sbg bahasa tambahan). Yekti tetap penutur asli. Lihat D21 di bawah.

**Rationale:**
- Strategic review (`STRATEGY.md`, Fable 5, dijalankan sekali) mengidentifikasi 3 lubang validasi yang berisiko reject di venue tinggi: (R1) validator native n=1 (penulis sendiri menilai hasil sendiri), (R2) "blind-spot" hanya diuji LLM-judge dengan 1 prompt di atas data sintetis buatan DeepSeek sendiri (sirkular), (R3) framing dual-use ("uncollectable AND undetectable" terbaca sebagai resep evasion).
- Reframe (generator = metode, bukan headline) menutup R3 langsung via eksplisit dual-use statement (§4.8) tanpa perlu eksperimen mahal.
- Bapak pilih **paket minimum** (E1 validator + E7 anchor kelangkaan kedua + E9 lit-pass), BUKAN paket Scopus/Q (E2 detektor nyata + E3 anchor data real + E5 mitigasi fine-tune + E6 baseline manusia) — sesuai budget waktu weekend-only.

**Konsekuensi (dikerjakan sesi ini):**
- Paper `paper/draft_jinita.md` v4→v5: judul baru ("Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection"), abstract+contributions+conclusion direstrukturisasi, §4.8 Ethics dapat Dual-use statement baru, §4.7 Limitations #1 diupdate (validator ke-2/3 in-progress bukan kondisional). Taksonomi §2 + scarcity baseline §3.1 **tidak diubah** (sudah bagus).
- **E7 dikerjakan:** anchor kelangkaan kedua dari `D:\documents\twitter` (proyek sister Bapak, Digital Vitality Index) — 32-kota, ~1,42 juta tweet, Javanese 0,093% confirmed rate (tertinggi dari 10 bahasa daerah disurvei, tapi tetap <0,1%). Tabel 1 baru + referensi [8] (unpublished, disitasi dengan izin eksplisit Bapak — cek konflik publikasi terpisah SUDAH ditanyakan & disetujui).
- **E1 instrumen disiapkan:** `experiments/generation_pilot/build_multivalidator_forms.py` (form buta 2-kolom: OTENTIK + JELAS_HATE terpisah, per STRATEGY §6 poin 1) + `score_multivalidator.py` (α Krippendorff antar-rater, reuse `src/agreement.py`). **Pengisian form oleh Yekti/Daniel = langkah native, belum dieksekusi** — itu tugas Bapak/mereka, bukan otomatis.
  - **Percobaan pre-fill LLM ditolak (same day):** sempat dicoba isi draft Claude ke kedua form (atas instruksi Bapak) supaya Yekti/Daniel koreksi, bukan mulai kosong. Ditinjau → risiko anchoring bias merusak independensi yang justru mau diukur instrumen ini (pola sama dgn insiden mahasiswa back-translation, HARD RULE #2). **Bapak putuskan: batalkan, kedua form direset ke blank.** Detail: `STATE.md` Challenges Log C11.
- **Koreksi tak terkait ditemukan+diperbaiki:** nama universitas salah di paper+codebook — "Universitas Bina Husada Nusantara" (fabrikasi/salah ingat sesi lalu) → benar **"Universitas Bhinneka Nusantara"** (UBHINUS, dulu STIKI Malang). Lihat CLAUDE.md catatan afiliasi.
- Referensi [24] placeholder fabricated diganti sitasi HateCheck asli terverifikasi (Röttger et al., ACL-IJCNLP 2021, DOI dicek via ACL Anthology). Referensi [8] baru (DVI) disisipkan, [8]–[25] lama digeser [9]–[26].

**Ditunda (bukan ditolak, hanya di luar paket JINITA minimum):** E2 (detektor nyata: IndoBERT/Perspective/XLM-R), E3 (anchor data real krama-hate), E5 (eksperimen mitigasi fine-tune), E6 (baseline deteksi-manusia), E4 (perbesar suite), E8 (gradien collectability by register). Semua terdokumentasi di `STRATEGY.md` §4 kalau suatu saat mau naik ambisi ke Scopus/Q.

**See also:** `STRATEGY.md` (memo lengkap), memory `strategy-review-fable5-2026-07-06`, `experiments/generation_pilot/README.md` (update sesi 9).

---

## D21 — E1 hasil: IRR native rendah + koreksi kredensial Daniel

**Date:** 2026-07-07 (sesi 10)
**Decision:** Yekti dan Daniel mengisi `VALIDATION_FORM_yekti_FILLED.xlsx` / `VALIDATION_FORM_daniel_FILLED.xlsx` (108 baris, buta, independen). `score_multivalidator.py` dijalankan (di-repoint ke nama file `_FILLED`). Hasil dilaporkan apa adanya di paper, tidak dipoles.

**Hasil:**
- Rate otentik: **Mukhlis 55%** (baseline lama), **Yekti 91%**, **Daniel 45%**.
- Krippendorff's α (OTENTIK, pairwise): Mukhlis–Yekti **0.095** [-0.109, 0.293], Mukhlis–Daniel **0.779** [0.650, 0.889], Yekti–Daniel **-0.039** [-0.220, 0.146]. 3-rater α **0.336** [0.224, 0.449] — di bawah ambang konvensional 0.667 untuk kesimpulan tentatif.
- **Koreksi kredensial (dari Bapak, di tengah sesi):** Daniel Rudiaman Sijabat **bukan penutur asli** Jawa — tinggal 30 tahun di Jawa Timur, fasih Jawa sebagai bahasa tambahan, bukan L1. **Mukhlis dan Yekti tetap penutur asli**, dikonfirmasi ulang. Klaim "confirmed active Javanese speaker" untuk Daniel sejak D20 **salah**.

**Interpretasi:** ini bukan sekadar "butuh validator lebih banyak" — **dua penutur asli sungguhan (Mukhlis, Yekti) sendiri paling tidak sepakat** (α≈chance), sementara Daniel (non-native, resident lama) justru melacak Mukhlis dengan erat. Ini menunjukkan "otentik" sebagai binary refereeing task bukan construct ber-konsensus-tinggi bahkan antar native — bukan cuma masalah jumlah rater. Angka 55%/97%/11% (Table 2 paper) harus dibaca sebagai estimasi satu evaluator berkualitas, bukan ground truth ter-validasi inter-subjektif.

**Konsekuensi (dikerjakan sesi ini):**
- `paper/draft_jinita.md` §4.7 Limitation (1) ditulis ulang: melaporkan 3 rate + matriks α penuh + kredensial Daniel yang benar, tidak pool jadi satu angka. v5→v6 changelog appendix ditambahkan.
- PRD dapat entry **D21** (tabel Decisions Log) + koreksi inline di §0.2 poin 2.
- STATE.md Challenges Log dapat **C12**; Stage/Last update header diperbarui.
- HANDOFF.md dapat blok SESI 10 + koreksi inline di blok SESI 9.
- Koreksi ini TIDAK menghapus catatan lama (D20, dsb.) — ditandai sebagai koreksi dengan blockquote, mengikuti pola koreksi afiliasi UBHINUS sebelumnya (lihat CLAUDE.md).

**Follow-up diagnosis (same session, Bapak's hypothesis, verified against data):** Bapak proposed the low IRR isn't random noise — hate speech judgment is inherently subjective (e.g. "jancuk awakmu picek" = anger at an individual, not hate; "dasare wong meduro jorok-jorok" = hate despite no profanity, since it generalizes to a whole ethnic group), and validator environment (Bapak: homogeneous Javanese-majority; a relative in Surabaya: heterogeneous, frequent code-switching) may set different authenticity thresholds. Checked directly against the 39 Mukhlis-Yekti + 12 Mukhlis-Daniel disagreement rows — **strongly confirmed:**
- **Instrument artifact:** all 39 Mukhlis-Yekti disagreements run one direction (Mukhlis=not-authentic, Yekti=authentic); 19 of the 27 *krama_sarcastic* items (70% of that niche) are disagreement rows, and the niche accounts for 19/39 (49%) of all disagreements — either way, *krama_sarcastic* dominates. 34/39 have Yekti marking JELAS_HATE=0 — Mukhlis's original single-column form likely conflated "authentic Javanese" with "clearly reads as hate." Harmonizing (OTENTIK AND JELAS_HATE) raises Mukhlis-Yekti α from 0.095 to 0.519. Does NOT apply to Daniel (0.779→0.448, drops instead) — his disagreement pattern is different (non-native register doubt despite recognizing hate content).
- **Sociolinguistic environment:** 31/39 disagreement rows have Yekti's notes explicitly calling code-mixing with Indonesian "wajar" (normal) — exactly matching the homogeneous-vs-heterogeneous-environment hypothesis. Connected to two verified citations (web search + primary-source fetch, not guessed): Ravindranath & Cohn 2014 [25] (population size ≠ vitality, Javanese as the case study) and Smith-Hefner 2009 [26] (urbanization/class-linked krama attrition).

**Paper updated:** §1 Introduction (one sentence citing [25],[26]), §4.7 Limitation (1) substantially extended with the diagnosis + cross-reference to Limitation (4), Limitation (4) gets a one-sentence back-reference, References gains [25]/[26] (appended at list end, not renumbered — existing body citations were already not in strict first-appearance order, e.g. [16]/[20], so appending is lower-risk than a full renumber of an already lit-pass-verified list).

A related point Bapak raised (Chinese-Indonesian friends have a distinguishable "Chindo Javanese" dialect that native ears can perceive as different) is noted in Limitation (1) as an open question for future ethnolect-specific validation, not as a claim this paper makes — there is no data or community-specific validator to support more than that.

**See also:** `experiments/generation_pilot/multivalidator_result.md`, `paper/draft_jinita.md` §1 + §4.7 + v5→v6 changelog, memory `feedback-validator-independence-guard`, memory `e1-irr-result-daniel-credential-2026-07-07`.

---

## Open decisions

- **D-OPEN-1:** HKI batch placement di tridarma tracker UBHINUS — tunggu input user.
- **D-OPEN-3:** RESOLVED — Bapak pilih Opsi 1 (codebook v1.0 + draft paper JINITA, 2026-06-23). (D-OPEN-2 RESOLVED oleh D18.)
- **D-OPEN-4: RESOLVED (D21, 2026-07-07)** — Validasi keaslian native selesai untuk ketiga validator. Mukhlis 55%, Yekti 91%, Daniel 45%; α native-native (Mukhlis-Yekti) 0.095, 3-rater 0.336 — rendah, dilaporkan jujur di paper §4.7 sebagai temuan (bukan konfirmasi IRR bersih). Daniel dikoreksi: bukan penutur asli.
- **D-OPEN-5 (D20): RESOLVED** — Lit-pass referensi selesai (2026-07-06). 24 referensi final, semua tersitasi in-text (0 fabricated, 0 yatim). Dari 5 placeholder "(Authors TBD)": 2 fabricated diganti (Javanese NLP benchmark, sarcasm survey), 3 ternyata judul asli tinggal isi penulis (2× Pamungkas et al. — related work langsung relevan, ditambah eksplisit di §1; Törnberg). 2 referensi lama (Gwet, SEA-LION) di-drop karena tak pernah disitasi. Satu item ([4] WCSE 2021) masih perlu cek halaman manual (selisih publisher vs agregator) sebelum submit.

(Decisions yang sudah resolved tapi minor / default-approved tidak ditulis di sini supaya lean. Lihat [`PRD.md` §9](../PRD.md) untuk full open decisions list.)
