# Wiki Index — Ujaran Kebencian Jawa

_Last touched: 2026-06-22 (Opsi A/Pilot #6b selesai — pool 332→735, dataset 728 + D18)._

Catalog dari semua knowledge proyek. **Bapak baca dari sini — agent maintain seluruh konten.**

---

## Entity pages (wiki/)

| File | Topik | Status |
|---|---|---|
| [decisions.md](decisions.md) | Decisions log D1-D15 + rationale | [active] |
| [pilots.md](pilots.md) | Index Pilot #1-#4 + status + dependencies | [active] |
| [glossary.md](glossary.md) | Terms: NEIL, krama/ngoko, BPB, unggah-ungguh, BPE, dll | [active] |
| [SCHEMA.md](SCHEMA.md) | Cara agent maintain wiki ini (Karpathy pattern) | [stable] |
| [log.md](log.md) | Chronological log ingest/query/lint | [active] |

## Raw sources (proyek root)

| File | Konten | Akses |
|---|---|---|
| [`PRD.md`](../PRD.md) | Product Requirement Document — research design | §0 Decisions Log paling sering |
| [`STATE.md`](../STATE.md) | Live execution state, milestones, **Challenges Log**, sesi log | Update tiap sesi |
| [`CLAUDE.md`](../CLAUDE.md) | Hard rules + workflow untuk sesi Claude Code | Schema layer |
| [`HANDOFF.md`](../HANDOFF.md) | Quick context untuk sesi baru — TL;DR + read order | Pickup file |
| [`README.md`](../README.md) | Public-facing project description | Stable |
| [`Ujaran Kebencian Jawa_ Riset Mendalam_.md`](../Ujaran%20Kebencian%20Jawa_%20Riset%20Mendalam_.md) | Background literature paper draft (pre-pivot) — Tabel 1 taksonomi 7-kategori, Tabel 2 pre-trained models comparison | Background |

## Pipeline + code

| Path | Konten |
|---|---|
| [`prompts/cultural_classification_v0.md`](../prompts/cultural_classification_v0.md) | Prompt template Pilot #1, taxonomy 4-dimensi + 5 few-shot Jawa |
| [`src/llm_clients.py`](../src/llm_clients.py) | Wrapper DeepSeek + Grok + Kimi (semua OpenAI-compat) |
| [`src/cultural_prompt.py`](../src/cultural_prompt.py) | Loader prompt template + parser JSON output |
| [`src/agreement.py`](../src/agreement.py) | Metrik bersama: Krippendorff α kanonik (D17) + bootstrap CI + hate_units (dipakai Pilot #3/#5/#6) |
| [`prompts/cultural_classification_v2.md`](../prompts/cultural_classification_v2.md) | Prompt kerja produksi (pemenang Pilot #3, α ds+grok 0.763) |
| [`data/labeled/bulk_v2_consensus.jsonl`](../data/labeled/) | Dataset Pilot #6b (**728 teks**, 158 hate; diperbesar dari 331 Pilot #5; gitignored → rilis HF/Zenodo) |
| [`scripts/test_apis.py`](../scripts/test_apis.py) | Connectivity test 3 LLM (verified ✅ 3/3 per 2026-05-07) |
| [`experiments/pilot01_llm_characterization/`](../experiments/pilot01_llm_characterization/) | Pilot #1 ready to run (run_pilot.py + analyze.py) |
| [`experiments/pilot04_autoresearch_prompts/`](../experiments/pilot04_autoresearch_prompts/) | Pilot #4 plan (Karpathy autoresearch adaptation) |

## External refs

| Path | Konten |
|---|---|
| `~/Documents/autoresearch/` | Karpathy autoresearch repo (cloned, design ref untuk Pilot #4) |
| https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | LLM Wiki pattern (Karpathy Apr 2026) — adopted untuk dokumentasi ini |
| https://huggingface.co/datasets/oscar-corpus/OSCAR-2301 | Source data Pilot #1 (`jv` subset) |
| https://sinta.kemdiktisaintek.go.id/journals/profile/10719 | JINITA Sinta 2 profile (target venue) |

## Memory (Claude internal, user tidak perlu baca)

`~/.claude/projects/.../memory/` — feedback + project context yang Claude pakai cross-session. Bukan untuk user. Lihat di `MEMORY.md` di sana.

---

## Read order untuk sesi fresh Claude Code

1. `CLAUDE.md` (auto)
2. `HANDOFF.md` (quick TL;DR)
3. `wiki/index.md` ← anda di sini
4. `wiki/decisions.md` (D1-D9 rationale)
5. `wiki/pilots.md` (status pilot mana yang aktif)
6. `STATE.md` (Challenges Log + sesi log terakhir)

Detail dive ke `PRD.md §0` atau entity page tertentu hanya kalau diperlukan.
