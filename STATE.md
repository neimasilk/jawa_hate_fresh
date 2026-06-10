# STATE — Ujaran Kebencian Jawa (Fully LLM Pipeline)

**Stage:** Pilot #1, #2, #1b, #3 DONE → **Pilot #5 BULK BERJALAN** (filter full 12.7K → label v2 ds+grok → held-out α + consensus dataset). Pipeline idempotent: `scripts\run_bulk_pipeline.ps1`
**Last update:** 2026-06-10

---

## Status singkat

Sesi 2026-05-07 menghasilkan pivot framing besar (lihat [PRD.md §0](PRD.md) Decisions Log). Decisions pondasi sudah disepakati. Detail metodologis menunggu pilot eksperimen #1. Repo Git + struktur folder belum disetup (next action).

## Decisions yang sudah di-commit

Lihat [PRD.md §0 Decisions Log](PRD.md). Ringkas:
- Framing: **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** (fully automated, zero human in annotation + validation)
- Venue: JINITA Sinta 2
- Authorship: 3 (Mukhlis corresponding, Yekti, Daniel — all UBHINUS)
- Dialek: Jawa + turunan only; Sunda/Madura excluded sebagai sumber, tetap target group
- Data source: existing public dumps + LLM filter (live scraping dihindari)
- Validation: cross-LLM consistency + Krippendorff's α + adversarial perturbation + XAI
- Fallback ladder: zero human → minimal sanity check ~50 → pending

## Next milestones

1. **Setup repo Git + struktur folder** ✅ (done 2026-05-07)
2. **Pilot #1 — LLM characterization** ✅ DONE 2026-05-25
   - Gate GREEN (refusal 0.3%, JSON valid 94%, α=1.000) — **tapi α degenerate** (semua sampel BUK, sumber FineWeb2 nyaris tanpa hate). Lihat Challenges Log + `wiki/pilots.md`.
   - C2 ✅ (refusal bukan blocker), C1 sebagian ✅ (JSON valid), C3 ❌ belum terjawab (butuh sumber dengan hate asli).
3. **Pilot #2 — LLM-as-Jawa-filter** ✅ DONE 2026-05-25
   - Filter robust (100% valid), yield Jawa+campuran 9.6% (24/250, 9 hate). Code-mixed scope tervalidasi.
   - `hot_jawa_subset.jsonl` siap jadi input C3 re-test.
   - **Follow-up:** compare vs langid baseline (belum), scale filter untuk pool lebih besar.
3b. **Pilot #1b — C3 re-test** ✅ DONE 2026-06-08, **scale-up n=149 DONE 2026-06-10**
   - n=24: α=0.384 non-degenerate, gate YELLOW. Scale-up (filter N=2000 → pool 149 teks): **α=0.587 (CI [0.475, 0.698])** — C3 ROBUST, consensus moderat-baik dengan prompt v0.
   - Plot twist vendor: di n=149 **Grok = over-flagger** (umpatan kasar → hate ringan); drop-Grok α=0.722. Kimi tetap impraktis (126s/call, validity 73.8%). Disagreement #1 = boundary **profanity vs hate** → masalah definisi prompt, bukan vendor.
   - **NEXT:** Pilot #3 — pertegas definisi hate (group-directed) vs umpatan kasar di prompt, baru putuskan vendor mix bulk.
4. **Codebook v0 draft** (user effort ~3-5 jam, weekend session) — paralel dengan pilot
5. **Pilot #3 — Cultural prompt manual iteration** ✅ DONE 2026-06-10 (2 iterasi, ~$2.3)
   - Diagnosis v0: inkonsistensi internal prompt (system prompt "kekasaran leksikal = hate" + Contoh 1 melabeli umpatan personal sebagai hate berat) = root cause Grok over-flag.
   - **v1** (definisi hate group-directed, profanity≠hate): flip bersih (Grok 74 T→F, 0 F→T), hate-rate 77→28% / 55→15%, TAPI α flat 0.554 (prevalensi skewed → chance agreement naik). Residu: deepseek under-flag slur identitas ke individu.
   - **v2** (+ slur-identitas-ke-individu = hate, Contoh 9-10): **α ds+grok = 0.763 (CI [0.624, 0.879])**, Δ+0.229 vs v0. Disagreement 36→12. **KEEP — prompt kerja untuk bulk.**
   - Stop di v2: residu 12 = ambigu genuin (meta-komentar, kutipan hate, perbandingan positif); iterasi lanjut di pool sama = overfit risk. Validasi ulang di held-out saat bulk.
   - Infra: `experiments/pilot03_cultural_prompt/` + `src/agreement.py`. Vendor: ds+grok per D15 (Kimi dropped).
6. **Pilot #5 — Bulk labeling (produksi pertama)** 🔄 STARTED 2026-06-10 malam
   - Pipeline: filter full haipradana 12.7K (Grok, resume dari 2K lama) → pool hot-Jawa ~950 est → label prompt v2 × ds+grok (149 lama di-merge dari Pilot #3) → analisis.
   - Deliverable: **held-out validation α** (anti-overfit), `data/labeled/bulk_v2_consensus.jsonl` (dataset v1), `bulk_v2_disagreement.jsonl` (bahan codebook), profil taksonomi.
   - Infra: `experiments/pilot05_bulk_labeling/` + `scripts/run_bulk_pipeline.ps1` (rantai 4 step idempotent). Est total ~15-20 jam, ~$12-15.
7. **Pilot #4 — AutoResearch loop (Karpathy pattern)** — automate pilot #3, scale ke 50+ variants overnight via agent autonomous loop. Bounded budget ~$12.5/run. Folder `experiments/pilot04_autoresearch_prompts/` sudah ada README + plan. Ref: `~/Documents/autoresearch/` (cloned). Potential paper angle: "AutoResearch Pattern for Cultural Prompt Engineering in Low-Resource NLP". (Catatan: hasil manual Pilot #3 — 2 iterasi cukup — bisa mengubah perlunya pilot ini.)

## Challenges Log

(Akan di-update setiap eksperimen. Format: tanggal, tantangan, hipotesis, eksperimen, hasil, lesson. Lessons-learned berpotensi jadi materi paper sendiri.)

| Tgl | Challenge | Hipotesis | Eksperimen | Hasil | Lesson |
|-----|-----------|-----------|------------|-------|--------|
| 2026-05-12 | Output LLM kosong massal (Kimi 98, DeepSeek 5) | `max_tokens` terlalu kecil, habis untuk reasoning token | Naikkan max_tokens (DeepSeek 2048, Kimi 4096) + resume retry record kosong | Kimi kosong turun 98→11, DeepSeek 5→0 | Reasoning model (Kimi K2.6) butuh token budget besar; validity rendah bisa artefak teknis, bukan kegagalan task. Selalu cek `finish_reason` sebelum simpulkan gate. |
| 2026-05-25 (C2) | Refusal rate LLM untuk konten hate | Safety alignment mungkin over-cautious tolak | Pilot #1, 100 sampel × 3 LLM | Refusal 0.3% (DeepSeek 1, lainnya 0) | Refusal **bukan blocker** untuk fully-LLM framing. (Catatan: sampel nyaris tanpa hate, jadi belum diuji pada konten ekstrem.) |
| 2026-05-25 (C1) | LLM bisa hasilkan output taksonomi kultural valid? | LLM paham schema 4-dimensi Jawa | Pilot #1, JSON validity | Valid 94% rata (Grok 100, DeepSeek 97, Kimi 85) | LLM bisa hasilkan JSON taksonomi valid. Kualitas nuansa register belum diuji (tidak ada hate sample). |
| 2026-05-25 (C3) | Inter-LLM agreement realistic atau noise? | α tinggi = consensus bekerja | Pilot #1, Krippendorff's α binary hate | α=1.000 — **TAPI degenerate**: semua 100 sampel dilabeli BUK | **α tidak bermakna** karena sumber (FineWeb2 jav_Latn) nyaris tanpa hate. C3 BELUM terjawab. Butuh sumber dengan hate Jawa asli untuk uji agreement sungguhan. |
| 2026-05-25 (C-vendor) | Efisiensi vendor untuk bulk pipeline | Semua 3 vendor setara | Pilot #1 latency + token + cost | Kimi 91s/call, 260K out-tok, 11% kosong; Grok 11s/7K-tok | Kimi K2.6 reasoning model mahal+lambat utk bulk. Grok paling efisien. Pertimbangkan drop/limit Kimi di pipeline besar, atau pakai hanya untuk triangulasi sampel. |
| 2026-05-25 (C4) | LLM bisa filter Jawa/code-mixed dari dump Indonesia? | LLM lebih reliable dari langid (Jawa low-resource) | Pilot #2: Grok filter 250 tweet haipradana | 100% JSON valid; yield Jawa+campuran 9.6% (24/250, 9 hate); `lainnya` tepat tangkap Sunda/Melayu/Portugis | LLM filter Jawa **bekerja & presisi** (tidak tertipu kata gaul, pisahkan bahasa lain). Tapi densitas hot-Jawa di dump Indonesia rendah (~3.6%) → butuh filter banyak baris untuk pool besar. |
| 2026-05-25 (C-scope) | Apakah "Jawa murni" realistis sebagai scope? | Ada cukup hate Jawa murni | Pilot #2 distribusi register | Jawa murni nyaris nol (1/250, "jancuk jancuk"); hate Jawa didominasi code-mixed | **Code-mixed = realita** hate Jawa sosmed. Keputusan menerima code-mixed sebagai scope tervalidasi empiris. Insisting "ngoko/krama murni" akan bias jauh dari realita. |
| 2026-06-08 (C3 re-test) | Multi-LLM agreement bekerja pada hate Jawa ASLI? (memecah α degenerate Pilot #1) | α non-degenerate akan ukur consensus sungguhan | Pilot #1b: 3-LLM (prompt v0 sama) di `hot_jawa_subset.jsonl` (24 teks, 9 hate orig) | **α hate = 0.384** (CI [0.01, 0.70]), severity 0.376. **Non-degenerate** (41T/18F). Pairwise deepseek-grok **80%**, dengan Kimi turun ke 67-69%. Drop Kimi → α 0.48. Gate **YELLOW**. | **C3 terjawab: consensus bekerja MODERAT, bukan degenerate.** Kimi = sumber noise utama (validity 62.5%, 5/7 disagreement = Kimi dissenter BUK). **CI sangat lebar (n=24)** → angka belum robust, WAJIB scale-up sebelum klaim. Sinyal: 2-LLM deepseek+grok mungkin cukup untuk bulk (lebih murah, agreement lebih tinggi). |
| 2026-06-10 (C5 prompt iter) | α moderat (0.534 ds+grok) — prompt issue atau task ambiguity? | Disagreement #1 = boundary profanity-vs-hate = definisi prompt, bisa diperbaiki | Pilot #3: v1 (definisi group-directed) lalu v2 (+slur identitas ke individu), eval pool sama n=149 | v1: koreksi kualitatif sukses (flip Grok 74 T→F / 0 F→T) tapi α flat 0.554 (prevalensi skewed). v2: **α 0.763 (CI [0.624, 0.879])**, disagreement 36→12 | **2 koreksi definisi prinsipil mengangkat α +0.23 tanpa ganti vendor/model.** Lesson metodologis: (1) α bisa flat walau label membaik (chance agreement naik saat prevalensi skewed) — selalu baca flip table + raw agreement bareng α; (2) kontradiksi internal few-shot = sumber disagreement terukur; (3) stop iterasi sebelum overfit ke pool eval — residu ambigu genuin masuk codebook, bukan prompt. |
| 2026-06-10 (ops-resume) | Saldo Kimi habis di tengah Pilot #3 → 149 call error 429, dan resume logic menganggap error = done (rerun akan skip) | Error kuota ≠ error permanen, harus dibedakan di resume | Bersihkan record error + patch `already_processed` (429/insufficient balance tidak dihitung done) | Rerun setelah top-up akan retry otomatis | **Resume design harus bedakan error transient (kuota/jaringan) vs permanen.** Juga: cek saldo vendor sebelum run besar. Resolusi: D15 — Kimi di-drop, pipeline 2-LLM ds+grok. |
| 2026-06-10 (C3 scale-up) | α n=24 belum robust (CI [0.01, 0.70]) — naikkan n | CI lebar = masalah n, bukan prompt; α akan stabil di n besar | Pilot #1b scale-up: filter N=2000 → pool 149 teks (80 hate orig) × 3 LLM, prompt v0 sama, $1.57 | **α hate = 0.587** (CI **[0.475, 0.698]**), severity 0.480. Gate YELLOW tipis (hanya validity 89.7% < 90%, diseret Kimi 73.8%). Pairwise deepseek-kimi 86.1% tertinggi. **Drop Grok → α 0.722**; drop Kimi → 0.534. Majority: 31/69 orig-neutral → hate True. | **C3 ROBUST: consensus moderat-baik (α 0.587) dengan prompt v0 tanpa iterasi.** Plot twist: **Grok = over-flagger** (umpatan kasar non-group → hate ringan; 77% teks dilabel hate), bukan Kimi yang noise utama spt n=24 — kesimpulan vendor dari n kecil bisa terbalik. Disagreement #1 = **boundary profanity vs hate = masalah DEFINISI prompt** → Pilot #3 pertegas hate = group/identity-directed. LLM tangkap umpatan Jawa yg dilewatkan anotasi Indonesia-context (sinyal kultural, materi paper). |

### Challenge yang sudah diidentifikasi (belum di-eksperimen)

- **C1:** LLM Jawa quality (ngoko/krama, pasemon, code-switching) — apakah cukup untuk klasifikasi nuansa register? Pilot #1 akan jawab.
- **C2:** LLM refusal rate untuk hate speech content (over-cautious safety alignment). Pilot #1 akan ukur per-vendor.
- **C3:** Inter-LLM agreement realistic atau noise — kalau α antar-LLM rendah, multi-LLM consensus tidak bekerja.
- **C4:** LLM filter Jawa vs langid — false positive rate (Jawa low-resource di langid). Pilot #2.
- **C5:** Cultural prompt engineering — apa yang work / tidak. Iterative.
- **C6:** Coverage target group — bias toward Mataraman (data dump dominan), under-represent Madura/Tionghoa/dll target group.
- **C7:** Validation tanpa human gold — methodology defensibility ke reviewer Sinta 2.

## Slip / drift watch

Plan PRD §5 menyebut Fase 1 (Taxonomy 1 bulan) → Fase 6 (Paper). Dengan pivot fully-LLM, banyak Fase compress ke automation. Realistic timeline:
- Pilot phase (#1-3): 2-4 minggu
- Bulk pipeline run + iteration: 4-6 minggu
- Modeling + eval: 2-3 minggu
- Paper writing (Bapak driver review, saya draft): 6-10 minggu
- **Total: ~4-6 bulan realistic**

User time budget: ~5-15 jam/bulan, weekend only. Bottleneck = paper writing review (15-25 jam total) + decision sessions (~5 jam). Annotation effort: zero (kecuali fallback aktif).

## Sesi log

| Tgl | Sesi | Output |
|-----|------|--------|
| 2026-05-07 | Konsep + decision pivot | PRD §0 Decisions Log added; CLAUDE.md HARD RULES updated; STATE.md created; memory seeded |
| 2026-05-07 | Setup repo + pilot #1 prep | Repo init + push GitHub (`neimasilk/jawa_hate_fresh`); requirements.txt + .env.example; src/llm_clients.py + cultural_prompt.py; prompts/cultural_classification_v0.md (5 few-shot); experiments/pilot01_llm_characterization/{run_pilot.py, analyze.py, README.md}. Sumber data: OSCAR-2301 jv subset (streaming, 100 sampel dengan light keyword pre-filter). **Blocker eksekusi: API keys belum ada (lihat .env.example).** |
| 2026-05-07 | HANDOFF.md created | Dokumen pickup untuk sesi baru: TL;DR, read order, konteks penting (mahasiswa cheating story, framing pivot), status, blocker, user comm notes, gotchas. CLAUDE.md daily protocol updated untuk reference HANDOFF.md. |
| 2026-05-07 | Vendor pivot + connectivity test | User pilih 3 LLM baru: **DeepSeek V4 Pro + Grok 4.3 + Kimi K2.6** (semua OpenAI-compat). Drop Claude+GPT-4o. Update llm_clients.py + .env.example + requirements.txt (drop anthropic). `.env.txt` Bapak gunakan (Windows-style); load_dotenv try .env then .env.txt. Created scripts/test_apis.py. **Test result: 3/3 ✅** — semua paham Jawa krama. Kimi force `temperature=1.0` (fixed via override). venv `.venv/` dibuat dengan openai 2.35.1 + python-dotenv + tqdm. **Pilot #1 ready to run** — tinggal install `datasets` package + jalankan `run_pilot.py`. |
| 2026-05-07 | Karpathy autoresearch reference + Pilot #4 planned | Cloned `karpathy/autoresearch` ke `~/Documents/autoresearch/` (sister dir). Pattern review: single-file edit + fixed eval budget + composite metric + autonomous loop overnight + git commit/reset per iter. **Adopsi sebagai Pilot #4** ("AutoResearch Loop untuk Cultural Prompt Engineering"). Adaptasi: edit `prompts/cultural_classification_vN.md` (bukan train.py), eval 50-sample × 3 LLM (bukan train 5min), composite metric (refusal+validity+α+entropy, bukan val_bpb), bounded loop ~$12.5/run (bukan NEVER STOP), `program_prompt_research.md` dengan kearifan lokal injection. Folder `experiments/pilot04_autoresearch_prompts/` + README dibuat dengan plan + risk + paper angle. Eksekusi setelah Pilot #1-3 baseline jelas. |
| 2026-05-25 | Pilot #2 (LLM-as-Jawa-filter) + keputusan strategi data | Survei: tak ada korpus hate Jawa siap-unduh (UI/WCSE 2021 cuma di paper). Keputusan: filter dump hate Indonesia (haipradana) → ekstrak subset Jawa/code-mixed, terima code-mixed sebagai scope. Buat prompts/jawa_filter_v0.md + pilot02 run_filter.py/analyze.py/README (smoke test 4/4 ✅). Run 250 tweet via Grok: 100% valid, yield 9.6% (24 hot, 9 hate), `lainnya` tepat tangkap Sunda/Melayu/Portugis. Jawa murni nyaris nol → code-mixed scope tervalidasi. `hot_jawa_subset.jsonl` siap untuk C3 re-test. **Flag novelty (dataset Jawa sudah ada → reframe from-scratch) diangkat ke user, PRD belum diubah.** |
| 2026-05-25 | Setup ulang di komputer kantor baru + rerun Pilot #1 | Fresh machine: rebuild `.venv` (datasets/openai/pandas/dotenv/tqdm), user sediakan `.env` (3 keys), connectivity 3/3 ✅. Rerun resume Pilot #1 setelah patch max_tokens (2j32m): Kimi empty 98→11, DeepSeek 5→0. Regenerate report → **gate GREEN tapi α degenerate** (semua BUK; FineWeb2 jav_Latn nyaris tanpa hate). Update Challenges Log (C1/C2/C3/C-vendor), wiki/pilots.md, wiki/log.md, HANDOFF.md. Lesson: validity rendah awal = artefak token, bukan kegagalan task; multi-LLM α belum tervalidasi tanpa hate sample. |
| 2026-06-08 | Novelty reframe (D14) + Pilot #1b C3 re-test | User decision: reframe novelty (drop klaim "dataset pertama" → pipeline zero-human + taksonomi register-aware + code-mixed). PRD v0.3 (D13 retroaktif + D14, G2/G3/G5 sinkron), wiki/decisions.md, index.md updated. Buat `experiments/pilot01b_c3_retest/` (run_c3 + analyze + README), jalankan 24 teks × 3 LLM ($0.26, ~50 mnt). **α hate=0.384 non-degenerate, gate YELLOW** → C3 terjawab (consensus moderat). Kimi noise utama (validity 62.5%, drop→α 0.48). CI lebar (n kecil) → scale-up wajib. Memory: machine-context-neima. |
| 2026-06-10 | Pilot #3 prompt iteration (sesi sama, lanjutan) | Diagnosis v0 (kontradiksi internal few-shot) → v1 (profanity≠hate: flip bersih tapi α flat 0.554) → v2 (+slur identitas ke individu: **α 0.763**, disagreement 36→12). Insiden saldo Kimi habis → **D15 vendor mix final ds+grok**. Prompt kerja bulk = v2. Infra pilot03 + src/agreement.py. Total ~$2.3. |
| 2026-06-10 | C3 scale-up selesai + analisis n=149 | Run background 447/447 call selesai ($1.57). `analyze.py` → **α=0.587 (CI [0.475, 0.698])**, C3 ROBUST. Temuan baru: Grok over-flagger (drop-Grok α=0.722), boundary profanity-vs-hate = disagreement utama → arah Pilot #3 jelas (pertegas definisi hate group-directed di prompt). Fix stale n=24 footer di analyze.py. Update STATE/HANDOFF/wiki/pilots + commit. |
| 2026-05-07 | Karpathy LLM Wiki adopted untuk dokumentasi (D12) | User minta evaluate gist Karpathy "LLM Wiki" (Apr 2026, https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Pattern: 3-layer (raw sources / wiki / schema) + 3 ops (ingest/query/lint) + LLM-maintained wiki untuk user-facing KB. **Adopt** — match dengan user preference "saya fokus melihat wiki, kamu yg mengatur". Lean implementation: 6 files di `wiki/` (SCHEMA, index, log, decisions, pilots, glossary). CLAUDE.md daily protocol updated untuk wiki di read order + maintenance section. HANDOFF.md updated untuk reflect wiki sebagai primary user-facing layer. Memory ref ditambah. |
