# HANDOFF — Untuk sesi Claude Code yang fresh

**Tujuan:** Agar sesi baru langsung paham konteks tanpa user perlu re-explain.
**Last updated:** 2026-05-07 (akhir sesi pertama, sebelum pause untuk besok)

---

## TL;DR (3 baris)

Riset deteksi ujaran kebencian Bahasa Jawa, framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** = core novelty. Repo `neimasilk/jawa_hate_fresh` @ commit `d22172f` (atau lebih baru). Setup lengkap: dokumentasi terstruktur via Karpathy LLM Wiki pattern (`wiki/` folder), 4 pilot planned (#1 ready, #4 = adopsi Karpathy autoresearch). **Next concrete action: install `datasets pandas` + run Pilot #1 (~5-10 min, ~$0.50).**

---

## Baca dalam urutan ini

1. **`CLAUDE.md`** — Hard rules + workflow. Sudah di-update post-pivot.
2. **`wiki/index.md`** — **PRIMARY USER-FACING KNOWLEDGE BASE** (Karpathy LLM Wiki pattern, [D12](../wiki/decisions.md#d12--adopsi-pattern-karpathy-llm-wiki-dokumentasi)). User fokus baca dari sini. Catalog all entity pages + raw sources.
3. **`wiki/decisions.md`** — D1-D12 dengan rationale. Source-of-truth untuk decision history.
4. **`wiki/pilots.md`** — Status Pilot #1-#4 + dependencies + commands.
5. **`wiki/glossary.md`** — Term definitions (NEIL, krama/ngoko, BPB, unggah-ungguh, vendor LLM, dll).
6. **`wiki/SCHEMA.md`** — Cara agent maintain wiki (ingest/query/lint workflow). **Wajib baca SEKALI** kalau sesi pertama setelah wiki creation.
7. **`STATE.md`** — Live execution state, Challenges Log (C1-C7), sesi log.
8. **`PRD.md` §0 Decisions Log** — Kanonik untuk D1-D9 (D10-D12 ditambah di wiki). §1-§11 banyak legacy.
9. **`prompts/cultural_classification_v0.md`** — Prompt template Pilot #1.
10. **`experiments/pilot01_*/README.md`** + **`pilot04_*/README.md`** — Spec per pilot.
11. **`Ujaran Kebencian Jawa_ Riset Mendalam_.md`** — Background pre-pivot (taksonomi 7-kategori, pre-trained models survey).
12. **External:** `~/Documents/autoresearch/` (Karpathy repo, design ref Pilot #4).

Memory di `~/.claude/projects/.../memory/MEMORY.md` auto-loaded — berisi feedback tentang user preferences + project context.

---

## Konteks penting yang TIDAK obvious dari file-file di atas

### Story motivasi (jangan dilupakan)

Mahasiswa annotator di proyek lama v1-v4 **"curang" dengan back-translate English/Indo → Jawa**, hanya sedikit yg dianotasi asli. Mahasiswa sudah lulus, tidak available untuk fix. Dataset v1-v4 = mayoritas terjemahan, tidak menangkap realitas SARA Jawa. **Story ini = motivation utama untuk fully-LLM framing**, dan akan di-cite (anonimized) di paper introduction sebagai concrete failure mode dari "default" multi-annotator approach.

### Framing pivot dari NEIL → Fully LLM

CLAUDE.md/PRD awal punya "NEIL (Native-Expert-in-the-Loop)" sebagai kontribusi metodologis. Setelah diskusi 2026-05-07, framing pivot ke **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"**. NEIL term tidak dipakai lagi. Sebagian PRD section yang masih sebut NEIL = legacy, akan di-rewrite post-pilot.

### Venue: Sinta 2, BUKAN Sinta 1

CLAUDE.md/PRD awal target Sinta 1. User pilih **JINITA Sinta 2** (Politeknik Negeri Cilacap). KUM first author 25, bukan 40. Sudah di-update di CLAUDE.md HARD RULE #5.

### Decisions tentative vs final

Per HARD RULE baru di CLAUDE.md ("Riset = coba-coba"): decisions methodologis bisa berubah berdasarkan eksperimen. Detail blueprint a priori = minimum. Pilot dulu, blueprint setelahnya. **Dokumentasi tantangan + lessons-learned sambil jalan = potential kontribusi paper sendiri** — jangan sembunyikan "kegagalan" pilot.

---

## Status final 2026-05-07

**Yang sudah jadi:**
- Repo Git + GitHub `neimasilk/jawa_hate_fresh` (latest: `d22172f`, branch `main`)
- Dokumentasi lengkap: `CLAUDE.md`, `PRD.md` (§0 Decisions Log), `STATE.md`, `HANDOFF.md`, **`wiki/`** (6 files: SCHEMA, index, log, decisions, pilots, glossary)
- Folder structure: `data/{raw,intermediate,labeled,golden}/`, `src/`, `prompts/`, `notebooks/`, `logs/`, `notes/`, `experiments/{pilot01,02,03,04}/`
- Code: `src/llm_clients.py` (3 vendor wrappers OpenAI-compat), `src/cultural_prompt.py`, `scripts/test_apis.py`
- Prompt: `prompts/cultural_classification_v0.md` (4-dim taxonomy + 5 few-shot Jawa)
- Pilot #1: `experiments/pilot01_llm_characterization/` lengkap (run_pilot.py + analyze.py + README)
- Pilot #4: `experiments/pilot04_autoresearch_prompts/README.md` (plan, akan eksekusi setelah Pilot #1-3)
- API keys: `.env.txt` (gitignored) — DeepSeek + xAI + Kimi, **connectivity 3/3 ✅**
- Python venv: `.venv/` dengan `openai 2.35.1`, `python-dotenv`, `tqdm`
- Memory: 9 file di `~/.claude/projects/.../memory/`

**Yang siap di-eksekusi (tinggal jalankan):**
```
# Install datasets package (one-time, ~30 detik):
.venv\Scripts\python.exe -m pip install datasets pandas

# Run pilot #1 (~5-10 menit, ~$0.50):
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\run_pilot.py

# Analyze (output: report.md dengan decision gate GREEN/YELLOW/RED):
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\analyze.py
```

**Yang masih open:**
- HKI batch placement di tridarma tracker UBHINUS — minor, bisa nanti
- Pilot #2/#3 folder belum dibuat (akan dibuat saat eksekusi)

---

## Pilot #1 dalam satu paragraf

Sample 100 teks Jawa dari OSCAR-2301 `jv` subset (streaming, dengan light keyword pre-filter untuk diversity 70% with-hint + 30% no-hint). Klasifikasi via 3 LLM (DeepSeek V4 Pro, Grok 4.3, Kimi K2.6 — semua OpenAI-compat) pakai cultural prompt v0. Log raw + parsed ke JSONL (resume-on-crash). Analyze → metrics: refusal rate, JSON validity, Krippendorff's α (binary hate), pairwise agreement, cost. **Decision gate** (otomatis di analyze.py): GREEN (refusal <20% + validity >90% + α >0.5) → lanjut fully-LLM; YELLOW → iterasi prompt (pilot #3); RED → fallback ladder (sanity check 50 / pending). Estimasi cost ~$0.50, runtime ~5-10 menit.

---

## User communication notes (penting!)

- **Bahasa: Indonesian.** User dosen native Jawa, bicara Indonesia.
- **Ringkas.** User pernah eksplisit bilang "saya ga baca semua yg kamu tulis". Default max 8-15 baris. Pakai bullet/tabel.
- **Bottleneck constraint.** Weekend only, ~5-15 jam/bulan. Jangan minta input panjang. Tawarkan default + biarkan user revise.
- **Empirical over theoretical.** User prefer pilot eksperimen kecil daripada diskusi blueprint detail. Saat ada konflik blueprint vs realitas → realitas menang.
- **Decisions yang sudah final** ada di PRD §0 + memory. Jangan re-litigate kecuali user eksplisit minta.
- **Risiko: jangan tergoda over-engineering.** Riset, bukan production. Pipeline minimal yang work > pipeline canggih yang macet.

---

## Common gotchas

| Gotcha | Solusi |
|---|---|
| Git config kosong di laptop ini → commit error "Author identity unknown" | Sudah di-set global per 2026-05-07 (Mukhlis Amien / amien@stiki.ac.id). Verify dengan `git config --global --list`. |
| `.env.example` ke-ignore by `.env.*` pattern | Sudah di-fix dengan `!.env.example` exception di `.gitignore`. |
| Bapak pakai `.env.txt` (Windows-friendly), bukan `.env` | `src/llm_clients.py` `load_dotenv()` try `.env` dulu, fallback `.env.txt`. Kedua di-gitignore via `.env.*` pattern. |
| Kimi K2.6 reject `temperature=0.0` | Kimi force temperature=1. Sudah di-handle di `call_kimi()` (override). Determinism diandalkan dari few-shot + structured output. |
| OSCAR-2301 streaming butuh `trust_remote_code=True` | Sudah di-set di `run_pilot.py`. |
| Tidak ada Javanese-specific hate speech dataset publik | Confirm. Pakai OSCAR jv + LLM filtering sebagai source default. Fallback: `manueltonneau/indonesian-hate-speech-superset` filter for code-switched Javanese content. |
| Riset mendalam Bagian 4.1 sebut "3 anotator + Cohen's κ" | **DIABAIKAN** — bertentangan dengan framing fully-LLM. Story mahasiswa cheating = case-in-point kenapa multi-annotator manual high-risk. |

---

## Quick action menu untuk fresh session

| Kalau user bilang... | Lakukan... |
|---|---|
| "Lanjut" / "Run pilot 1" | Install `datasets pandas` di venv (kalau belum) → jalankan `run_pilot.py` → `analyze.py` → diskusi hasil dengan user |
| "Apa progress?" | Baca `wiki/index.md` → `wiki/pilots.md` → `STATE.md` Challenges Log + sesi log |
| "Update wiki" | Identifikasi entity yg perlu update → edit + log entry di `wiki/log.md` |
| "Cek konsistensi" / "Lint" | Run lint workflow per `wiki/SCHEMA.md` — cek kontradiksi PRD vs CLAUDE vs wiki, orphan pages, gaps di STATE Challenges |
| "Update PRD/decision" | Update `wiki/decisions.md` (entity primary) + `PRD.md §0` (canonical) + log entry di `wiki/log.md` |
| "Bikin pilot baru (#5/#6/dll)" | Update `wiki/pilots.md` future section → bikin folder `experiments/pilot0X_*/` + README. Pattern di pilot01 atau pilot04 |
| "Bahas ulang scope/venue/dialek" | Cek `wiki/decisions.md` untuk D-entry yg sudah ada. Kalau user mau revisi, update D-entry + bilang konsekuensi + log |

## Cara user mulai sesi baru (untuk Bapak)

1. Buka folder ini di Claude Code
2. Sesi Claude Code otomatis baca `CLAUDE.md`
3. Berdasarkan daily protocol di `CLAUDE.md`, agent akan baca: HANDOFF.md → `wiki/index.md` → entity pages relevan → STATE.md → tanya Bapak
4. Bapak cukup kasih instruksi singkat. Misalnya:
   - **"Lanjut pilot 1"** — agent install deps + run + analyze
   - **"Cek wiki konsisten"** — agent jalankan lint workflow
   - **"Diskusi codebook v1"** — agent buka prompts + diskusi
   - **"Cek hasil pilot kemarin"** — agent baca latest pilot output

---

**Catatan untuk diri sendiri (sesi mendatang):** Jangan re-explain semua dari awal. Asumsi user sudah paham proyek-nya. Tanya yang spesifik perlu sekarang. Kalau ada konflik dengan dokumentasi (CLAUDE/PRD/STATE), update dokumentasi-nya — jangan diam-diam menyimpang.
