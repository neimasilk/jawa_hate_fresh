# Wiki Schema — Cara LLM Agent Maintain Wiki Ini

**Pattern reference:** Karpathy LLM Wiki (Apr 2026) — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Tujuan:** User (Bapak Mukhlis) cukup baca `wiki/`. Agent (Claude Code di tiap sesi) yang maintain — update entity pages, cross-references, log, lint.

---

## 3-layer architecture proyek ini

| Layer | File / folder | Maintained by | Mutability |
|---|---|---|---|
| **Raw sources** | `PRD.md`, `Ujaran Kebencian Jawa_ Riset Mendalam_.md`, `experiments/*/outputs/`, `experiments/*/run.log`, hasil pilot raw | User curate + agent record | Append-only, jarang revisi |
| **Wiki** (this folder) | `wiki/index.md`, `wiki/log.md`, `wiki/decisions.md`, `wiki/pilots.md`, `wiki/glossary.md` | Agent | Live, di-edit setiap sesi sesuai kebutuhan |
| **Schema** | `CLAUDE.md` (hard rules + workflow), `wiki/SCHEMA.md` (file ini) | User edit, agent ikuti | Stabil, hanya berubah saat ada pivot besar |

**Catatan:** `STATE.md` dan `HANDOFF.md` adalah **bridging docs** antara raw sources dan wiki. Agent boleh refer dari wiki ke sini tanpa duplikasi.

---

## 3 operations

### 1. Ingest — saat ada raw source baru

Trigger: user attach file baru, eksperimen pilot selesai, decision baru di-commit, paper baru di-add ke literature, dll.

Steps agent:
1. Baca raw source baru
2. Identifikasi entity yang relevan (decision? pilot? glossary term?)
3. Update entity page yang relevant — APPEND atau REVISE, jangan rewrite total
4. Update `wiki/index.md` kalau ada entity baru
5. Log entry di `wiki/log.md` dengan format: `YYYY-MM-DD | INGEST | <source> | <entity-pages-touched> | <one-line summary>`
6. Cross-reference: kalau entity link ke entity lain, tambahkan link inline atau di "See also" section

### 2. Query — saat user tanya sesuatu

Steps agent:
1. Search `wiki/index.md` dulu untuk locate relevant entities
2. Read entity page → kalau jawab, jawab
3. Kalau wiki tidak cukup → fallback ke raw sources (`PRD.md`, `STATE.md`, log files)
4. **Kalau answer non-trivial dan reusable**: file balik ke wiki sebagai entity update + log entry
5. Format: agent jawab user, tapi sebut "(file ke `wiki/<entity>.md`)" supaya user tahu bahwa knowledge ditangkap

### 3. Lint — periodic health check

Trigger: setiap awal sesi yang panjang, atau saat user minta "cek konsistensi".

Steps agent:
1. **Contradictions:** apakah ada inkonsistensi antar files?
   - Mis. PRD §6 bilang Sinta 1 tapi CLAUDE.md HARD RULE #5 bilang Sinta 2 → flag
2. **Orphans:** apakah ada entity di `wiki/` yang tidak di-link dari `index.md`?
3. **Gaps:** apakah ada challenge di STATE.md "Challenges Log" yang belum ada entity di wiki?
4. **Stale memory:** apakah memory file masih akurat dengan current state?
5. Output: list singkat ke user (3-5 bullets max), atau auto-fix kalau trivial.

---

## Style guide untuk entity pages

- **Lean:** target max ~50-100 baris per entity. Kalau panjang, split.
- **Cross-reference inline:** pakai `[link](path)` ke entity lain atau raw source.
- **"See also" section** di bawah kalau ada > 2 cross-references.
- **Update timestamp** di top: `_Last touched: YYYY-MM-DD oleh sesi <topic>_`
- **Bahasa Indonesia** (sesuai user preference).
- **Status marker** kalau ada: `[active]`, `[archived]`, `[planned]`, `[deprecated]`.
- **Single source of truth principle:** tiap fact ada di SATU entity primary. Entity lain link ke sana, jangan duplikat.

---

## Naming convention

- File names: lowercase, underscore-separated, `.md` extension
- Entity pages: noun (mis. `decisions.md`, `pilots.md`, `glossary.md`), bukan kata kerja
- Special files: `index.md`, `log.md`, `SCHEMA.md` (uppercase intentional, schema = stable)
