# Wiki Log

Chronological log dari ingest / query / lint operations di wiki.

Format: `YYYY-MM-DD | OP | sumber/trigger | entities-touched | summary`

---

## 2026-05-07

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| post-pivot | INGEST | User pivot decision (NEIL → Fully LLM) | (pre-wiki) PRD §0, CLAUDE.md, STATE.md, memory/ | Decisions D1-D9 ditangkap di PRD §0 sebelum wiki ada |
| pilot-prep | INGEST | Setup repo + Pilot #1 prep | (pre-wiki) requirements.txt, src/, prompts/, experiments/pilot01_*/ | Pipeline scaffolding |
| handoff | INGEST | User minta handoff doc | (pre-wiki) HANDOFF.md created | Quick-pickup untuk sesi fresh |
| vendor-pivot | INGEST | User attach `.env.txt` dengan 3 keys (DeepSeek/xAI/Kimi) | (pre-wiki) llm_clients.py, .env.example, scripts/test_apis.py | Connectivity 3/3 ✅ |
| pilot4-plan | INGEST | User minta evaluate Karpathy autoresearch | (pre-wiki) experiments/pilot04_autoresearch_prompts/ + memory ref | Pilot #4 plan |
| **wiki-creation** | **INGEST** | User minta evaluate Karpathy LLM Wiki + adopt | **wiki/SCHEMA.md, wiki/index.md, wiki/decisions.md, wiki/pilots.md, wiki/glossary.md, wiki/log.md (file ini)** | Wiki created, 6 files, lean version. D12 ditambah. CLAUDE.md daily protocol akan di-update untuk include wiki/. |
| session-end | INGEST | User: "buat handoff document, kemudian kita cukup hari ni, sampai ketemu di sesi baru yg bersih" | HANDOFF.md (TL;DR + status final + quick action menu + cara user mulai sesi baru) | Sesi 2026-05-07 selesai. Final repo state: `d22172f` (atau commit setelah HANDOFF update). Pilot #1 ready to run di sesi berikutnya — tinggal `pip install datasets pandas` + jalankan. |

---

## 2026-05-25

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan?" pada fresh office machine | HANDOFF.md, STATE.md, wiki/index.md (read) | Pickup: Pilot #1 patch committed tapi rerun belum dijalankan. Blocker: fresh machine tanpa `.env`/`.venv`. |
| setup | INGEST | Fresh office machine | .venv rebuilt, .env disediakan user (3 keys) | venv + deps reinstall; connectivity 3/3 ✅. Data/kode/output sudah dari Git. |
| **pilot1-rerun** | **INGEST** | Rerun resume Pilot #1 setelah patch max_tokens | **experiments/pilot01_*/outputs/, report.md, wiki/pilots.md, STATE.md, HANDOFF.md** | Rerun 2j32m. Kimi empty turun 98→11, DeepSeek 5→0. **Gate GREEN** (refusal 0.3%, valid 94%, α=1.000) **tapi α degenerate** (semua sampel BUK; FineWeb2 nyaris tanpa hate). C2 ✅, C1 sebagian ✅, C3 belum terjawab. Kimi mahal/lambat. |
| data-strategy | INGEST | User "cari sumber data panas" + survei HF/web | wiki/pilots.md #2, README pilot02 | Tak ada korpus hate Jawa siap-unduh. Keputusan: filter dump hate Indonesia → subset Jawa/code-mixed, terima code-mixed scope. Flag novelty (dataset Jawa sudah ada) untuk PRD. |
| **pilot2-done** | **INGEST** | Pilot #2 LLM-as-Jawa-filter (Grok, 250 tweet haipradana) | **prompts/jawa_filter_v0.md, experiments/pilot02_*/, wiki/pilots.md, STATE.md, HANDOFF.md** | Filter 100% valid; yield Jawa+campuran 9.6% (24, 9 hate); `lainnya` tepat tangkap Sunda/Melayu/Portugis. Jawa murni ~nol → code-mixed scope tervalidasi. `hot_jawa_subset.jsonl` siap untuk C3 re-test. |

---

## 2026-06-08

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan" | CLAUDE.md, HANDOFF.md, wiki/index.md, STATE.md (read) | Pickup: Next Concrete Action = Opsi A (C3 re-test di hot_jawa_subset 24 teks). Connectivity 3/3 ✅, run launched background. |
| **novelty-reframe** | **INGEST** | User decision: reframe novelty (opsi recommended) | **PRD.md (v0.3: D13+D14 di §0, G2/G3/G5 sinkron), wiki/decisions.md (D13 retroaktif + D14), wiki/index.md** | D14: klaim "dataset pertama" ditinggalkan → novelty = pipeline zero-human + taksonomi register-aware + code-mixed realism. D13 (data strategy 2026-05-25) dinomori retroaktif. |
| pilot1b-launch | INGEST | C3 re-test (Opsi A HANDOFF) | experiments/pilot01b_c3_retest/ (run_c3.py + analyze.py + README) | Runner baru: 24 teks × 3 LLM, prompt v0 sama (atribusi beda hasil ke DATA), + α severity + bootstrap CI + majority-vs-orig_label. |
| **pilot1b-done** | **INGEST** | Run C3 selesai (72 call, $0.26, ~50 mnt) | **experiments/pilot01b_c3_retest/report.md + outputs/, STATE.md, HANDOFF.md, wiki/pilots.md** | **α hate=0.384 NON-DEGENERATE** (CI [0.01,0.70]), severity 0.376. Pairwise deepseek-grok 80%. Kimi noise utama (validity 62.5%, drop→α 0.48). Gate YELLOW. C3 terjawab (consensus moderat). Tambah sensitivitas drop-1-vendor ke analyze.py. Next: scale filter pool besar untuk CI sempit. |

---

## 2026-06-10

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan" | CLAUDE.md, HANDOFF.md, wiki/index.md, STATE.md (read) | Pickup: cek C3 scale-up (launched background 06-08, ~53% saat handoff) → ternyata SELESAI (447/447 record unik). |
| **pilot1b-scaleup-done** | **INGEST** | C3 scale-up selesai (447 call, n=149, $1.57) | **experiments/pilot01b_c3_retest/report.md + outputs/, analyze.py (fix stale n=24 footer), STATE.md, HANDOFF.md, wiki/pilots.md** | **α hate=0.587 (CI [0.475, 0.698]) — C3 ROBUST**, severity α 0.480. Gate YELLOW tipis (hanya validity 89.7%<90, diseret Kimi 73.8%). **Plot twist: Grok = over-flagger** (drop-Grok α=0.722; umpatan kasar non-group → hate "ringan"); pairwise tertinggi deepseek–kimi 86.1%. Disagreement #1 (36/149) = boundary profanity-vs-hate → **arah Pilot #3: pertegas definisi hate group-directed**. 31/69 orig-neutral → majority hate=True (sinyal kultural, materi paper). Keputusan vendor mix bulk ditunda sampai sesudah Pilot #3. |
| **pilot3-launch** | **INGEST** | User "lanjutkan" → mulai Pilot #3 | **prompts/cultural_classification_v1.md, experiments/pilot03_cultural_prompt/ (run_eval + analyze + README), src/agreement.py, wiki/pilots.md, STATE.md** | **Diagnosis v0: root cause Grok over-flag = prompt v0 sendiri** (system prompt "kekasaran leksikal = hate" + Contoh 1 melabeli umpatan personal `target tidak_ada` sbg `hate:true berat` — kontradiksi internal; Grok ikut literal, deepseek/kimi abaikan). v1: definisi hate group/identity-directed + fix few-shot + aturan hate:false→BUK. Eval v1 ds+grok (298 call) launched background; analyze komparatif (Δα, flip table) siap. Smoke test record pertama ✅ (`banci` → gender_lgbtq sedang, definisi baru dipakai benar). |

---

## Convention

- **INGEST:** Source baru di-process ke wiki. Touched = entity pages yang di-update.
- **QUERY:** User tanya, agent search wiki + synthesize. Touched = entity pages yang di-cite atau yang di-update kalau ada gap diisi.
- **LINT:** Health check. Touched = pages yang di-fix (kalau ada).
- Pre-wiki entries ditangkap retroactively saat creation, untuk historical context.
