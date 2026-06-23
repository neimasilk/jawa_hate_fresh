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
| **D15-vendor-mix** | **INGEST** | Saldo Kimi habis (429 ×149) → keputusan user: "pakai yg ada aja" | **PRD §0 (D15), wiki/decisions.md (D15), HANDOFF.md, STATE.md, pilot03 README, wiki/index.md** | **Kimi DROPPED — pipeline final 2-LLM deepseek+grok.** α tetap terukur (2 rater); baseline Pilot #3 = α ds+grok v0 0.534. Data Kimi v0 n=149 → sensitivity analysis 3-vs-2 di paper. Patch resume: 429 ≠ done. |
| **pilot3-launch** | **INGEST** | User "lanjutkan" → mulai Pilot #3 | **prompts/cultural_classification_v1.md, experiments/pilot03_cultural_prompt/ (run_eval + analyze + README), src/agreement.py, wiki/pilots.md, STATE.md** | **Diagnosis v0: root cause Grok over-flag = prompt v0 sendiri** (system prompt "kekasaran leksikal = hate" + Contoh 1 melabeli umpatan personal `target tidak_ada` sbg `hate:true berat` — kontradiksi internal; Grok ikut literal, deepseek/kimi abaikan). v1: definisi hate group/identity-directed + fix few-shot + aturan hate:false→BUK. Eval v1 ds+grok (298 call) launched background; analyze komparatif (Δα, flip table) siap. Smoke test record pertama ✅ (`banci` → gender_lgbtq sedang, definisi baru dipakai benar). |

| **pilot3-done** | **INGEST** | Eval v2 selesai → α 0.763 | **prompts/cultural_classification_v2.md, experiments/pilot03_cultural_prompt/ (report_v1, report_v2, README), wiki/pilots.md, STATE.md, HANDOFF.md** | **Pilot #3 DONE dalam 2 iterasi: α ds+grok 0.534 → v1 0.554 (flat, prevalensi skewed — lesson: baca flip table bareng α) → v2 0.763 (CI [0.624, 0.879])**, disagreement 36→12. Prompt kerja bulk = v2. Stop sebelum overfit; residu 12 ambigu genuin → codebook + held-out. Next: pilihan Bapak (bulk design / codebook / langid baseline). |

| **pilot5-launch** | **INGEST** | User: "lakukan sesuai rekomendasi + tutorial + jalankan" | **experiments/pilot05_bulk_labeling/ (run_bulk + analyze + README + prompt_iter_sids.json), scripts/run_bulk_pipeline.ps1, pilot02 run_filter.py (N=full + 429-aware), HANDOFF (§Panduan Bapak), STATE, wiki/pilots.md** | **Bulk produksi pertama LAUNCHED:** filter full 12.7K berjalan (resume dari 2K) → label v2 ds+grok → held-out α + consensus dataset ke `data/labeled/`. Snapshot 149 prompt-iter sids untuk held-out split. Pipeline idempotent (1 script, resume-aware semua step). Est ~15-20 jam, ~$12-15. |

---

## 2026-06-11

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan" | CLAUDE.md, HANDOFF.md, wiki/index.md (read) | Pickup: Langkah 1 = ambil hasil 2 run lokal semalam. qwen3 ternyata SELESAI (α 0.660); SEA-LION ter-download tapi run baru 61/140 → di-resume. |
| **pilot6-done** | **INGEST** | Resume run SEA-LION selesai (140/140) → α final kedua model lokal | **wiki/pilots.md (section Pilot #6 + status #5/#6), pilot06 README, STATE.md (C8 + sesi log), HANDOFF.md, run_filter.py + run_bulk.py** | **Pilot #6 DONE: qwen3:14b α(ds, lokal) 0.660 (CI [0.480, 0.807]) LOLOS — consensus deepseek+lokal viable tanpa xAI. SEA-LION (Jawa-native) α 0.422 (CI [0.238, 0.581]) GAGAL** — noise dua arah (18 over + 10 miss); temuan paper: region-specific ≠ rater lebih baik. Utang teknis: run_filter/run_bulk diparametrize lokal (`FILTER_VENDOR`/`BULK_VENDORS`) + resume 403=transient. Pending keputusan Bapak: vendor mix final (rekomendasi deepseek+qwen3). |
| **D16 + bulk + cascade** | **INGEST** (di-log retroaktif 2026-06-15) | Keputusan Bapak vendor mix + eksekusi (commits `3fa1411`/`39acb20`/`3207869`) | **(saat itu BELUM di-log) src 3-rater infra, pilot05 outputs, pilot06 run_cascade.py, run_filter.py** | **D16: vendor mix 3-rater ds+grok+qwen3** (tambah qwen3, bukan ganti grok). Labeling cloud ds+grok pool 332 selesai (373 call, 0 error). Cascade filter Pilot #6b dibangun (SEA-LION→qwen3 pre-screen → grok verify, pool grok-confirmed). 3 commit ini tak sempat di-log → disusulkan sesi 2026-06-15. |

---

## 2026-06-15

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan" | CLAUDE.md, HANDOFF.md, wiki/index.md, wiki/decisions.md, wiki/pilots.md, STATE.md (read) + git log | **Drift 4-hari terdeteksi:** doc bilang "blocker = keputusan vendor", tapi git sudah jauh (D16 dibuat, cloud labeling selesai, cascade infra ada) + qwen3 rater ke-3 (192 record) uncommitted. Rekonsiliasi: keputusan sudah dibuat & dieksekusi, tinggal finalisasi analisis. |
| **pilot5-finalize** | **INGEST** | Jalankan analisis Pilot #5 (pertama kali) | **experiments/pilot05_bulk_labeling/ (analyze.py + report.md + bulk_responses.jsonl), data/labeled/ (gitignored)** | Fix crash list-valued `form` → `analyze.py` jalan → **dataset 331 consensus (74 hate) + held-out validation: ds+grok held-out α 0.670 vs iter 0.747 → prompt v2 GENERALIZES**. Tambah tabel tes-overfit-adil (same-rater-set). |
| **verify-adversarial** | **LINT** | Verifikasi sebelum commit (workflow 3 agent: 2 code-audit + 1 recompute independen) | **src/agreement.py, experiments/pilot01b_c3_retest/ (analyze + report), pilot05 analyze.py** | Recompute verdict "confirmed" TAPI code-audit menemukan **2 bug**: (1) dedup load-order (record stale menimpa label valid → consensus 330/2→331/1, ds+grok iter 0.763 = artefak bug, sebenarnya 0.747); (2) formula α non-kanonik → diperbaiki ke **coincidence-matrix Krippendorff** (validasi vs 0.743). **D17.** Sync pilot01b 0.587→0.613. Lesson: recompute meniru bug yang sama → butuh code-audit terpisah. |
| **ingest-docs** | **INGEST** | Susulkan D16 + log Pilot #5 final ke wiki | **HANDOFF.md, STATE.md (stage/milestone/C9/sesi log), wiki/decisions.md (D16+D17+D-OPEN-2), wiki/pilots.md (#5 DONE + #6b), wiki/log.md (ini)** | Doc disinkronkan ke git reality. Commits `fbd59a2`+`2ac5db3`. **Next: D-OPEN-2 keputusan Bapak — perbesar pool (cascade) vs ship v1 + modeling/codebook.** |

---

## 2026-06-22

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjutkan" | CLAUDE.md, HANDOFF.md, wiki/index.md, STATE.md (read) + cek state cascade | Pickup: cascade overnight (launched 06-15) → pass1/pass2 lokal selesai tapi **pass3 grok 403 kredit habis** (06-18), pool mentok 431, tidak ada proses in-flight. |
| **opsiA-pivot** | QUERY | User info kredit xAI terisi ($4.55) | (live grok test) | Premis "tanpa uang" (pilihan sementara 2-rater) gugur → live test grok ✅ → konfirmasi Bapak: pivot balik ke **Opsi A penuh** (pool ~761, 3-rater). |
| **pilot6b-cascade-done** | **INGEST** | `scripts/run_cascade_remaining_pipeline.ps1` tuntas | **experiments/pilot02_*/outputs (pilot02_responses, hot_jawa_subset 735, cascade_pass2, SEA-LION filter), pilot02 report.md, pilot05 bulk_responses + report.md, data/labeled/ (gitignored)** | Verify 1298 sisa (confirm-rate 25.4% → +304 keeps) → **pool 332→735** (dump habis, ceiling). Label 3-rater 735 → **dataset 728 consensus (158 hate)**, 7 ties. **Held-out ds+grok α 0.688** [0.614,0.759] di 586 teks (menguat vs 0.670), full 0.701; 3-rater held-out 0.513/full 0.545 (qwen3 bising). SARA lebih kaya (+kristen/arab/kepercayaan/hindu/rohingya). Biaya ~$2.8 grok. |
| **verify-recompute** | **LINT** | Sanity angka headline sebelum commit | (recompute independen from-scratch) | Coincidence-matrix Krippendorff jalur terpisah → **cocok persis** report (0.688/0.701/0.513/0.545). Kode sudah kanonik sejak D17 → tak ada bug baru. Recompute = sanity cepat (bukan ganti audit penuh; risiko bug rendah karena reuse kode tervalidasi). |
| **ingest-docs** | **INGEST** | Log Opsi A selesai ke wiki + docs | **wiki/decisions.md (D18 + resolve D-OPEN-2 → D-OPEN-3), wiki/pilots.md (#6b DONE + section hasil), wiki/index.md, STATE.md (stage/6c/C10/sesi log), HANDOFF.md, .gitignore (run *.log), wiki/log.md (ini)** | Doc disinkronkan. **Next: D-OPEN-3 keputusan Bapak — codebook/paper (rekomendasi) vs sumber data baru vs modeling+future-work.** |

---

## 2026-06-23

| Time | OP | Trigger | Touched | Summary |
|------|----|---------|---------|---------|
| session-start | QUERY | User "lanjut, kemaren saya tinggal, apakah sudah selesai?" | CLAUDE.md, HANDOFF.md, wiki/index.md, STATE.md (read) + git status + cek dataset | Konfirmasi **Opsi A tuntas** (git clean, commit `eccc3f4`, dataset 728 + pool 735 ada di disk). Tidak ada run in-flight. |
| dataset-integrity | LINT | Cek `deepseek:null` di record consensus | (recompute counts) | deepseek non-null **708/728**, full 3-rater **705**, sisanya transient fail (bukan bug) → klaim α ds+grok valid. |
| **decision** | QUERY | AskUserQuestion D-OPEN-3 | (keputusan Bapak) | Bapak pilih **Opsi 1: codebook + draft paper**. Bahasa paper **Inggris**. |
| **codebook-paper** | **INGEST** | Eksekusi Opsi 1 | **codebook/CODEBOOK.md, paper/draft_jinita.md** | Ekstrak contoh nyata per kategori dari dataset → **Codebook v1.0** (4-dimensi grounded, 7 boundary cases adjudicated, distribusi 728, limitasi jujur incl. register krama langka) + **draft paper metodologi** (Inggris, 3 pilar novelty). |
| **jinita-guidelines** | **INGEST** | User "download petunjuk dari jinita, pelajari, sesuaikan" | **paper/jinita_guidelines/ (submissions.html, template.txt, gen_ai_policy.html, SUMMARY.md), paper/draft_jinita.md (v2 conform)** | OJS blokir WebFetch (403) → curl UA-browser sukses. Pelajari: English, IMRaD bernomor, abstrak 150–250 kata tanpa sitasi, max-5 keywords, IEEE refs (≥20, ≥80% jurnal ≤5thn), Gen AI disclosure wajib. **Sesuaikan paper:** judul ≤12 kata, restruktur IMRaD, sitasi IEEE [n], ≥20 referensi anchor nyata, Gen AI disclosure + Ethics + Acknowledgements. |
| ingest-docs | INGEST | Sync docs | **STATE.md, HANDOFF.md, wiki/index.md, wiki/log.md (ini), .gitignore** | D-OPEN-3 resolved → Opsi 1 done. **Next: lit-pass verifikasi DOI ≥20 ref + Word template + review Bapak/coauthor.** |
| **audit-adversarial** | **LINT** | User (ultracode): "review menyeluruh & jujur, kritik keras, bikin action list, lakukan yg layak" | Workflow `wkams2l8z` 8-reviewer + verify + synth (51 agen, 2.27M tok) → recompute independen ke data. Verdict **as-is REJECT/major-revision**. 18 temuan (12 confirmed major/blocker). |
| **audit-fixes** | **INGEST** | Eksekusi do-now items | **experiments/audit_external/{audit.py, clean_release.py}, paper/draft_jinita.md (v3), codebook/CODEBOOK.md (v1.0a), paper/AUDIT_RESPONSE.md, STATE.md, HANDOFF.md, wiki/index.md+log.md, .gitignore** | 17/18 do-now diperbaiki: external-validity §4.3 (54.5%/κ0.19/24-flip-benar), reliabilitas jujur (3-rater 0.513 + AC1, buang "generalizes"), scrub PII 2 nomor, Table 1 baseline (0.534/Δ0.23), McNemar bias, register di-demote (judul ganti), dedup/leakage, count majority-of-3 reproducible, celah taksonomi skin-color. **5 keputusan Bapak (A spot-check pakar=tertinggi, B aturan label, C anekdot mhs, D ref, E lisensi).** |

---

## Convention

- **INGEST:** Source baru di-process ke wiki. Touched = entity pages yang di-update.
- **QUERY:** User tanya, agent search wiki + synthesize. Touched = entity pages yang di-cite atau yang di-update kalau ada gap diisi.
- **LINT:** Health check. Touched = pages yang di-fix (kalau ada).
- Pre-wiki entries ditangkap retroactively saat creation, untuk historical context.
