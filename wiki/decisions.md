# Decisions Log

_Last touched: 2026-06-22 (D18 Opsi A dieksekusi — pool 332→735). Source-of-truth untuk decision rationale._

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

## Open decisions

- **D-OPEN-1:** HKI batch placement di tridarma tracker UBHINUS — tunggu input user.
- **D-OPEN-3:** Arah setelah pool 735: (a) codebook + draft paper metodologi (held-out + cascade findings = materi kuat), (b) cari sumber data tambahan untuk dekati gate BERT 3K, atau (c) modeling BERT di 728 + framing future-work. Tunggu keputusan Bapak. (D-OPEN-2 RESOLVED oleh D18.)

(Decisions yang sudah resolved tapi minor / default-approved tidak ditulis di sini supaya lean. Lihat [`PRD.md` §9](../PRD.md) untuk full open decisions list.)
