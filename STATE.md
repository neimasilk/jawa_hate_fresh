# STATE — Ujaran Kebencian Jawa (Fully LLM Pipeline)

**Stage:** Pre-eksperimen → Pilot #1 (LLM characterization)
**Last update:** 2026-05-07

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
2. **Pilot #1 — LLM characterization** (zero user effort, automated)
   - Sample ~100 candidate Jawa text dari OSCAR-2301 jv subset
   - Run **DeepSeek V4 Pro + Grok 4.3 + Kimi K2.6** dengan cultural prompt v0
   - Measure: refusal rate per LLM, inter-LLM agreement (Krippendorff's α), JSON validity, output quality, cost
   - Output: pilot report + decision gate GREEN/YELLOW/RED
3. **Pilot #2 — LLM-as-Jawa-filter** (zero user effort)
   - Test LLM accuracy untuk filter Jawa-vs-non-Jawa pada dump
   - Compare vs langid baseline
4. **Codebook v0 draft** (user effort ~3-5 jam, weekend session) — paralel dengan pilot
5. **Pilot #3 — Cultural prompt manual iteration** v1, v2 (~5-10 manual iter) untuk baseline experience + finalize composite metric weights
6. **Pilot #4 — AutoResearch loop (Karpathy pattern)** — automate pilot #3, scale ke 50+ variants overnight via agent autonomous loop. Bounded budget ~$12.5/run. Folder `experiments/pilot04_autoresearch_prompts/` sudah ada README + plan. Ref: `~/Documents/autoresearch/` (cloned). Potential paper angle: "AutoResearch Pattern for Cultural Prompt Engineering in Low-Resource NLP".

## Challenges Log

(Akan di-update setiap eksperimen. Format: tanggal, tantangan, hipotesis, eksperimen, hasil, lesson. Lessons-learned berpotensi jadi materi paper sendiri.)

| Tgl | Challenge | Hipotesis | Eksperimen | Hasil | Lesson |
|-----|-----------|-----------|------------|-------|--------|
| _-_ | _(belum ada eksperimen)_ | | | | |

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
| 2026-05-07 | Karpathy LLM Wiki adopted untuk dokumentasi (D12) | User minta evaluate gist Karpathy "LLM Wiki" (Apr 2026, https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Pattern: 3-layer (raw sources / wiki / schema) + 3 ops (ingest/query/lint) + LLM-maintained wiki untuk user-facing KB. **Adopt** — match dengan user preference "saya fokus melihat wiki, kamu yg mengatur". Lean implementation: 6 files di `wiki/` (SCHEMA, index, log, decisions, pilots, glossary). CLAUDE.md daily protocol updated untuk wiki di read order + maintenance section. HANDOFF.md updated untuk reflect wiki sebagai primary user-facing layer. Memory ref ditambah. |
