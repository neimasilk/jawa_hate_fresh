# HANDOFF — Untuk sesi Claude Code yang fresh

**Tujuan:** Agar sesi baru langsung paham konteks tanpa user perlu re-explain.
**Last updated:** 2026-05-07 (akhir sesi setup awal)

---

## TL;DR (3 baris)

Riset deteksi ujaran kebencian Bahasa Jawa, framing **fully automated LLM pipeline** sebagai novelty (zero human in annotation + validation, fallback ladder kalau pilot gagal). Repo `neimasilk/jawa_hate_fresh` di GitHub. **Pre-eksperimen → Pilot #1 ready, blocker: API keys belum di-set di `.env`.**

---

## Baca dalam urutan ini

1. **`CLAUDE.md`** — Hard rules + workflow. Sudah di-update post-pivot.
2. **`PRD.md` §0 Decisions Log** — D1-D9 keputusan yang sudah final. Sisanya (§1-§11) banyak yang **legacy/superseded** — akan di-rewrite setelah pilot.
3. **`STATE.md`** — Status, milestones, **Challenges Log** (C1-C7 sudah teridentifikasi sebelum eksperimen), sesi log.
4. **`prompts/cultural_classification_v0.md`** — Prompt template untuk pilot #1, dengan few-shot Jawa.
5. **`experiments/pilot01_llm_characterization/README.md`** — Spec pilot pertama + decision gate.
6. **`experiments/pilot04_autoresearch_prompts/README.md`** — Plan untuk autoresearch loop (Karpathy pattern adaptation), eksekusi setelah Pilot #1-3.
7. **`Ujaran Kebencian Jawa_ Riset Mendalam_.md`** — Background riset (pre-pivot, baca kalau butuh konteks taksonomi 7-kategori atau survei pre-trained models).
8. **External ref:** `~/Documents/autoresearch/` (Karpathy repo, cloned sebagai design reference Pilot #4).

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

## Status hari ini (2026-05-07)

**Sudah selesai:**
- Repo Git init + push ke GitHub `neimasilk/jawa_hate_fresh`
- CLAUDE.md + PRD.md + STATE.md updated
- Folder structure: `data/{raw,intermediate,labeled,golden}/`, `src/`, `notebooks/`, `prompts/`, `logs/`, `notes/`, `experiments/{pilot01,02,03}/`
- `requirements.txt` + `.env.example`
- `src/llm_clients.py` (Anthropic / OpenAI / DeepSeek wrappers, returning unified `LLMResponse`)
- `src/cultural_prompt.py` (load template + parse JSON output)
- `prompts/cultural_classification_v0.md` (4-dimensi taxonomy + 5 few-shot Jawa)
- `experiments/pilot01_llm_characterization/{run_pilot.py, analyze.py, README.md}`

**Status:** API keys sudah di `.env.txt` (3 vendor: DeepSeek + xAI + Kimi). Connectivity test ✅ 3/3 passed. venv `.venv/` sudah ada dengan openai+dotenv+tqdm.

**Untuk jalankan pilot #1 penuh, masih perlu:**
- Install `datasets` package: `.venv/Scripts/python.exe -m pip install datasets pandas`
- Jalankan: `.venv/Scripts/python.exe experiments/pilot01_llm_characterization/run_pilot.py`
- Lalu: `.venv/Scripts/python.exe experiments/pilot01_llm_characterization/analyze.py`

Estimasi cost ~$0.50 untuk 100 sampel (cheap karena 3 vendor relatif murah).

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
| "Lanjut pilot" | Cek `.env` ada → jalankan `python experiments/pilot01_llm_characterization/run_pilot.py` |
| "Apa progress?" | Baca STATE.md sesi log + Challenges Log |
| "Update PRD" | Spesifik section mana — jangan rewrite blanket |
| "Bahas ulang scope/venue/dialek" | Cek PRD §0 Decisions Log. Kalau user mau revisi, update D-entry + bilang konsekuensi |
| "Bikin pilot baru" | Folder template di `experiments/pilot0X_*/` — copy structure pilot01 |

---

**Catatan untuk diri sendiri (sesi mendatang):** Jangan re-explain semua dari awal. Asumsi user sudah paham proyek-nya. Tanya yang spesifik perlu sekarang. Kalau ada konflik dengan dokumentasi (CLAUDE/PRD/STATE), update dokumentasi-nya — jangan diam-diam menyimpang.
