# Pilot #5 — Bulk Labeling Report (prompt v2, 3 rater: deepseek, grok, ollama:qwen3:14b)

**Pool:** 735 teks hot-Jawa | held-out 586 | prompt-iter 149

## Per-vendor metrics (pool penuh)

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate rate |
|---|---|---|---|---|---|---|
| deepseek | 735 | 0.7 | 96.5 | 15409 | $3.63 | 22% |
| grok | 735 | 0.1 | 99.9 | 5179 | $2.49 | 28% |
| ollama:qwen3:14b | 735 | 0.1 | 99.7 | 10869 | $0.00 | 14% |

**Total cost (termasuk porsi Pilot #3 yang di-merge):** $6.13

## Krippendorff's alpha (hate, 3 rater) — HELD-OUT VALIDATION

| Subset | n teks | alpha | 95% CI |
|---|---|---|---|
| **Held-out** (di luar pool iterasi prompt) | 586 | **0.513** | [0.450, 0.575] |
| Prompt-iter pool (pembanding; Pilot #3 ds+grok: 0.763) | 149 | **0.662** | [0.543, 0.764] |
| Full pool | 735 | **0.545** | [0.490, 0.602] |

(Catatan: alpha 3-rater di atas lebih rendah daripada pembanding ds+grok 0.763 karena rater ke-3 (qwen3 lokal) lebih bising — lihat sensitivity di bawah. Pembanding 0.763 = **2-rater ds+grok**, jadi tes overfit yang adil = baris ds+grok held-out di tabel berikut, BUKAN angka 3-rater.)

## Tes overfit ADIL — pasangan primer deepseek + grok (apples-to-apples vs Pilot #3 0.763)

| Subset | n teks | alpha | 95% CI |
|---|---|---|---|
| **Held-out** (di luar pool iterasi) | 586 | **0.688** | [0.614, 0.759] |
| Prompt-iter pool (= Pilot #3, harus ≈ 0.763) | 149 | **0.747** | [0.611, 0.861] |
| Full pool | 735 | **0.701** | [0.637, 0.765] |

(Held-out ds+grok ≥ ~0.6 dan CI overlap dengan iter-pool → prompt v2 GENERALIZES, bukan overfit. iter-pool ds+grok ≈ Pilot #3 0.763 [sedikit turun: 6 label deepseek yang dulu empty_response di Pilot #3 kini diperbaiki dari bulk & dimasukkan] = sanity-check merge/dedup benar.)

## Sensitivity rater: pairwise (held-out + full) + drop-1

| Rater set | subset | alpha | 95% CI |
|---|---|---|---|
| deepseek + grok | held-out | 0.688 | [0.614, 0.759] |
| deepseek + grok | full | 0.701 | [0.637, 0.765] |
| deepseek + ollama:qwen3:14b | held-out | 0.401 | [0.299, 0.496] |
| deepseek + ollama:qwen3:14b | full | 0.462 | [0.377, 0.549] |
| grok + ollama:qwen3:14b | held-out | 0.398 | [0.304, 0.485] |
| grok + ollama:qwen3:14b | full | 0.438 | [0.356, 0.519] |

## Consensus split → dataset (majority vote)

- **Consensus (majority hate):** 728 teks (99.0%) → `data/labeled/bulk_v2_consensus.jsonl`
  - hate=True: 158 | hate=False: 570
  - unanimous: 569 | majority non-unanimous: 159
  - severity-level agree DI ANTARA baris hate: 89/158 (baris non-hate 569/570 cuma sepakat BUK — bukan severity sungguhan)
- **Tie/invalid:** 7 teks → `data/labeled/bulk_v2_disagreement.jsonl` (bahan codebook + analisis)
  - breakdown: {'hate_tie': 7}

## Profil taksonomi (consensus hate=True)

- **severity** (vote 3 rater): {'sedang': 224, 'ringan': 133, 'BUK': 83, 'berat': 24, '?': 10}
- **register** (vote 3 rater): {'ngoko': 434, 'campur_kasar': 21, '?': 10, 'code_switched': 6, 'krama': 2, 'madya': 1}
- **form** (vote 3 rater): {'direct': 356, 'code_switched': 74, 'sarcastic': 29, '?': 10, 'idiomatic_pasemon': 7}
- **target_group** (top 15): {'gender_wanita': 111, 'tidak_ada': 83, 'politik_partai': 60, 'gender_lgbtq': 55, 'suku_tionghoa': 37, 'politik_tokoh': 31, 'agama_islam': 31, 'politik_ormas': 21, 'agama_kristen': 18, 'agama_kepercayaan': 12, 'suku_arab': 11, 'suku_rohingya': 3, 'agama_hindu': 3, 'kelas_kutha_ndeso': 2, 'suku_jepang': 2}
