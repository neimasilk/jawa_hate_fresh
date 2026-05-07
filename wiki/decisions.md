# Decisions Log

_Last touched: 2026-05-07 saat wiki creation. Source-of-truth untuk decision rationale._

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

## Open decisions

- **D-OPEN-1:** HKI batch placement di tridarma tracker UBHINUS — tunggu input user.

(Decisions yang sudah resolved tapi minor / default-approved tidak ditulis di sini supaya lean. Lihat [`PRD.md` §9](../PRD.md) untuk full open decisions list.)
