# Pilot #5 — Bulk Labeling Report (prompt v2, 3 rater: deepseek, grok, ollama:qwen3:14b)

**Pool:** 332 teks hot-Jawa | held-out 183 | prompt-iter 149

## Per-vendor metrics (pool penuh)

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate rate |
|---|---|---|---|---|---|---|
| deepseek | 332 | 0.6 | 97.3 | 17152 | $1.62 | 20% |
| grok | 332 | 0.3 | 99.7 | 5630 | $1.13 | 30% |
| ollama:qwen3:14b | 332 | 0.0 | 99.7 | 11069 | $0.00 | 17% |

**Total cost (termasuk porsi Pilot #3 yang di-merge):** $2.75

## Krippendorff's alpha (hate, 3 rater) — HELD-OUT VALIDATION

| Subset | n teks | alpha | 95% CI |
|---|---|---|---|
| **Held-out** (di luar pool iterasi prompt) | 183 | **0.565** | [0.450, 0.669] |
| Prompt-iter pool (pembanding; Pilot #3 ds+grok: 0.763) | 149 | **0.662** | [0.543, 0.764] |
| Full pool | 332 | **0.610** | [0.527, 0.684] |

(Catatan: alpha 3-rater di atas lebih rendah daripada pembanding ds+grok 0.763 karena rater ke-3 (qwen3 lokal) lebih bising — lihat sensitivity di bawah. Pembanding 0.763 = **2-rater ds+grok**, jadi tes overfit yang adil = baris ds+grok held-out di tabel berikut, BUKAN angka 3-rater.)

## Tes overfit ADIL — pasangan primer deepseek + grok (apples-to-apples vs Pilot #3 0.763)

| Subset | n teks | alpha | 95% CI |
|---|---|---|---|
| **Held-out** (di luar pool iterasi) | 183 | **0.670** | [0.525, 0.792] |
| Prompt-iter pool (= Pilot #3, harus ≈ 0.763) | 149 | **0.747** | [0.611, 0.861] |
| Full pool | 332 | **0.706** | [0.610, 0.793] |

(Held-out ds+grok ≥ ~0.6 dan CI overlap dengan iter-pool → prompt v2 GENERALIZES, bukan overfit. iter-pool harus ≈ 0.763 = sanity-check bahwa merge/komputasi benar.)

## Sensitivity rater: pairwise (held-out + full) + drop-1

| Rater set | subset | alpha | 95% CI |
|---|---|---|---|
| deepseek + grok | held-out | 0.670 | [0.525, 0.792] |
| deepseek + grok | full | 0.706 | [0.610, 0.793] |
| deepseek + ollama:qwen3:14b | held-out | 0.439 | [0.250, 0.605] |
| deepseek + ollama:qwen3:14b | full | 0.552 | [0.426, 0.664] |
| grok + ollama:qwen3:14b | held-out | 0.508 | [0.355, 0.648] |
| grok + ollama:qwen3:14b | full | 0.537 | [0.426, 0.643] |

## Consensus split → dataset (majority vote)

- **Consensus (majority hate):** 331 teks (99.7%) → `data/labeled/bulk_v2_consensus.jsonl`
  - hate=True: 74 | hate=False: 257
  - unanimous: 265 | majority non-unanimous: 66
  - severity-level agree DI ANTARA baris hate: 41/74 (baris non-hate 257/257 cuma sepakat BUK — bukan severity sungguhan)
- **Tie/invalid:** 1 teks → `data/labeled/bulk_v2_disagreement.jsonl` (bahan codebook + analisis)
  - breakdown: {'hate_tie': 1}

## Profil taksonomi (consensus hate=True)

- **severity** (vote 3 rater): {'sedang': 98, 'ringan': 75, 'BUK': 31, 'berat': 12, '?': 6}
- **register** (vote 3 rater): {'ngoko': 197, 'campur_kasar': 13, '?': 6, 'code_switched': 5, 'krama': 1}
- **form** (vote 3 rater): {'direct': 164, 'code_switched': 39, 'sarcastic': 10, '?': 6, 'idiomatic_pasemon': 5}
- **target_group** (top 15): {'gender_wanita': 60, 'gender_lgbtq': 33, 'tidak_ada': 31, 'politik_partai': 20, 'suku_tionghoa': 18, 'agama_islam': 18, 'politik_tokoh': 16, 'politik_ormas': 8, 'agama_kepercayaan': 6, 'suku_arab': 6, 'agama_kristen': 5, 'agama_hindu': 3, 'intra_jawa_mataraman': 1, 'kelas_kutha_ndeso': 1}
