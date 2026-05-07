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

1. **Setup repo Git + struktur folder** (zero user effort, Claude execute)
2. **Pilot #1 — LLM characterization** (zero user effort, automated)
   - Sample ~100 candidate Jawa text dari existing dump
   - Run Claude + GPT-4o + DeepSeek dengan cultural prompt
   - Measure: refusal rate per LLM, inter-LLM agreement, output quality
   - Output: pilot report → decide go/no-go fully-LLM framing
3. **Pilot #2 — LLM-as-Jawa-filter** (zero user effort)
   - Test LLM accuracy untuk filter Jawa-vs-non-Jawa pada dump
   - Compare vs langid baseline
4. **Codebook v0 draft** (user effort ~3-5 jam, weekend session) — paralel dengan pilot
5. **Pilot #3 — Cultural prompt engineering iteration** berdasarkan hasil #1+#2

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
