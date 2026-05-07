# Pilot #4 — AutoResearch Loop untuk Cultural Prompt Engineering

**Status:** PLANNED — eksekusi setelah Pilot #1-3 selesai.

## Tujuan

Adopsi pattern Karpathy autoresearch (`~/Documents/autoresearch/`) untuk **autonomous prompt iteration**: agent semalaman iterate `prompts/cultural_classification_vN.md`, evaluasi tiap variant pada fixed 50-sample subset, keep/discard berdasarkan composite metric, log results + lesson.

Pattern Karpathy → adaptasi kita:

| Karpathy | Kita |
|---|---|
| Edit `train.py` (single file) | Edit `prompts/cultural_classification_vN.md` |
| Train 5 min per experiment | Eval 50-sample × 3 LLM (~3-5 min, ~$0.25/iter) |
| Metric: `val_bpb` (lower better) | Composite: refusal ↓ + JSON validity ↑ + inter-LLM α ↑ + class entropy diversity |
| `program.md` skill file | `program_prompt_research.md` dengan **kearifan lokal injection** |
| `NEVER STOP` loop | **Bounded loop** — guardrail max 50 iter × ~$0.25 = ~$12.5/run |
| `results.tsv` | `results.tsv` + kolom **lesson** (per HARD RULE "tantangan = kontribusi") |
| H100 single GPU | Tidak butuh GPU — pakai LLM API yang sudah verified (DeepSeek/Grok/Kimi) |

## Prereq sebelum eksekusi Pilot #4

- [ ] Pilot #1 (LLM characterization) selesai — baseline metric known
- [ ] Pilot #2 (LLM Jawa filter) selesai — pipeline filter ready
- [ ] Pilot #3 (manual prompt iteration v1, v2) — get baseline experience untuk metric calibration sebelum hand off ke agent
- [ ] `src/eval_prompt.py` ditulis — fixed 50-sample harness yang stable + reproducible
- [ ] Composite metric formula difinalkan (weights antar komponen)

## Komponen yang harus dibuat saat eksekusi

1. **`program_prompt_research.md`** — Instruksi agent (analog `program.md` Karpathy):
   - Setup: branch `autoresearch/<tag>`, baseline run pertama
   - Experimentation rules: edit ONLY `prompts/cultural_classification_vN.md`, jangan touch `eval_prompt.py`
   - **Cultural injection**: agent harus aware unggah-ungguh, pasemon, code-switching, taxonomy 4-dimensi; jangan generic hate detection
   - Loop: edit → commit → eval → grep composite metric → keep/discard
   - Logging: `results.tsv` per branch dengan kolom commit, composite, refusal, validity, alpha, entropy, **lesson**, description
   - Budget guardrail: stop kalau total cost > $12.5 atau iter > 50

2. **`src/eval_prompt.py`** — Eval harness:
   - Load fixed 50-sample subset (deterministic seed)
   - Call 3 LLMs (DeepSeek + Grok + Kimi) dengan prompt yang ditest
   - Compute composite metric + per-component breakdown
   - Output single line untuk grep (mis. `composite: 0.7234`)

3. **Baseline subset** — `experiments/pilot04_autoresearch_prompts/eval_subset.json`:
   - 50 sampel dari hasil Pilot #1 OSCAR pool (tidak overlap dengan Pilot #1's 100)
   - Stratified: 35 with-keyword + 15 no-keyword

## Composite metric (draft)

Formula tentative — finalkan di Pilot #3:

```
composite = w1 * (1 - refusal_rate)        # higher = better
          + w2 * json_validity_rate         # higher = better
          + w3 * inter_llm_alpha            # higher = better
          + w4 * class_entropy_normalized   # higher = better (avoid all-same labels)
```

Default weights: `w1=0.3, w2=0.2, w3=0.3, w4=0.2`. Tune setelah Pilot #1 hasil keluar.

## Risk + concern

- **Cost balon** kalau loop tidak bounded → wajib budget guardrail di program.md
- **Metric gaming**: agent bisa converge ke prompt yang reduce refusal tapi over-conservative klasifikasi (semua label "BUK" → high agreement palsu). Mitigasi: include class entropy term + sanity check sample manual
- **No human gold**: composite metric semuanya derivable dari LLM output sendiri = circular risk. Mitigasi: budget kecil ke human spot-check post-loop (kalau mau, optional)
- **Agent context drift**: long loop bisa lupa cultural context. Mitigasi: program.md harus self-contained + reload setiap iter

## Paper angle

Bisa dijadikan kontribusi metodologis sendiri: **"AutoResearch Pattern for Cultural Prompt Engineering in Low-Resource NLP"**. Karpathy's pattern (Mar 2026) belum diterapkan untuk cultural-aware prompt iteration di low-resource bahasa daerah. Adaptasi non-trivial: metric design, budget guardrail, cultural injection di program.md, gold-less validation challenge.

## Reference

Repo asli Karpathy: `~/Documents/autoresearch/` (cloned 2026-05-07).
- `README.md` — overview + design choices
- `program.md` — agent skill file template
- `prepare.py` — fixed eval harness contoh
- `train.py` — single-file modification target contoh
