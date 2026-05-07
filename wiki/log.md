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

## Convention

- **INGEST:** Source baru di-process ke wiki. Touched = entity pages yang di-update.
- **QUERY:** User tanya, agent search wiki + synthesize. Touched = entity pages yang di-cite atau yang di-update kalau ada gap diisi.
- **LINT:** Health check. Touched = pages yang di-fix (kalau ada).
- Pre-wiki entries ditangkap retroactively saat creation, untuk historical context.
