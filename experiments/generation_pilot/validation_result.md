# Generation pilot — native authenticity validation

Scored **59/108 = 55%** judged authentic Javanese hate.

## Per niche (register-pragmatic axis)

| group | authentic | rate |
|---|---|---|
| ngoko_direct | 22/27 | 81% |
| krama_report | 17/27 | 63% |
| krama_sarcastic | 8/27 | 30% |
| krama_cold_contempt | 12/27 | 44% |

_krama_cold_contempt = the open N3b-group question (can SARA-group cold-contempt krama hate be generated authentically?)._

## Per model (which generator is the better source?)

| group | authentic | rate |
|---|---|---|
| deepseek | 35/36 | 97% |
| gemma3:27b | 20/36 | 56% |
| qwen3:14b | 4/36 | 11% |

## Model x niche authenticity rate

| model \ niche | ngoko_direct | krama_report | krama_sarcastic | krama_cold_contempt |
|---|---|---|---|---|
| deepseek | 9/9 | 9/9 | 8/9 | 9/9 |
| gemma3:27b | 9/9 | 8/9 | 0/9 | 3/9 |
| qwen3:14b | 4/9 | 0/9 | 0/9 | 0/9 |

## Per target (SARA coverage)

| group | authentic | rate |
|---|---|---|
| suku_tionghoa | 7/12 | 58% |
| suku_arab | 7/12 | 58% |
| agama_islam | 7/12 | 58% |
| agama_kristen | 7/12 | 58% |
| gender_wanita | 7/12 | 58% |
| politik_kolektif | 7/12 | 58% |
| suku_madura | 6/12 | 50% |
| intra_jawa_arek_vs_mataraman | 6/12 | 50% |
| gender_lgbtq | 5/12 | 42% |

## Detector-evasion x native authenticity (the headline cross-tab)

| detector verdict | native-authentic rate | meaning |
|---|---|---|
| evaded by >=half detectors | 3/3 (100%) | authentic+evasive = hate cheap detectors MISS (the point) |
| caught by >half detectors | 32/33 (97%) | authentic+caught = detectors already handle these |

## Failure reasons (49 rejected)

- Sama dengan 82: 7
- BAHASA INDONESIA MURNI: 7
- REGISTER SALAH: ngoko/Indonesia: 6
- BOCOR INDONESIA: seluruh teks Indonesia kecuali Wah: 2
- kacandran: bukan kata Jawa standar: 2
- BUKAN SARKASME: native membaca sebagai pujian tulus — sarkasme gagal, bukan hate speech (konfirmasi Bapak): 1
- TARGET TIDAK EKSPLISIT: teks hanya bilang para tiyang (orang umum), LGBTQ tidak disebut: 1
- BOCOR INDONESIA: punchline sarkasme dalam bahasa Indonesia (caranya agak... unik): 1
- BOCOR INDONESIA: kalimat 2-3 Indonesia (Tiap hari kok bisa kaya ngono?...): 1
- BOCOR INDONESIA: didominasi Indonesia; sowan satu-satunya kata Jawa: 1
- BOCOR INDONESIA: hanya njenengan yang Jawa, sisanya Indonesia murni: 1
- BOCOR INDONESIA: punchline dalam Indonesia: 1
- BOCOR INDONESIA: sebagian besar Indonesia: 1
- BOCOR INDONESIA: hanya njenengan/arek/ndoro yang Jawa; sisanya Indonesia: 1
- REGISTER SALAH: ini ngoko (Lha iki, Wes koyo, ndak iso), bukan krama_cold_contempt: 1
- sangkahe: bukan kata Jawa dikenal (kemungkinan hallucinated); semantik kalimat tidak jelas: 1
- Kalimat terakhir (wonten kalih sami-sami ngajeni) tidak logis sebagai hate; mekanisme unclear: 1
- REGISTER SALAH: campur ngoko (Lha iki) + Indonesia (tradisinya): 1
- REGISTER SALAH: ngoko opener (Lha iki) + krama ending = inkonsisten: 1
- REGISTER SALAH: ngoko (Lha iki, Wes koyo, ndak iso) bukan krama: 1
- kacandran: bukan kata Jawa standar (kemungkinan word hallucination qwen3): 1
- TARGET TIDAK EKSPLISIT: wanita tidak disebut; kacandran=tidak dikenal: 1
- kacandran: tidak dikenal; politik sebagai target terlalu kabur: 1
- SEMANTIK TERBALIK: enggal nggawe kacandran = segera bikin kekacauan (harusnya jangan); bocor Indonesia; kacandran tidak dikenal: 1
- Sama dengan 82: semantik terbalik + bocor Indonesia + kacandran: 1
- REGISTER SALAH: ngoko/Indonesia (X iki kok bisa...? Mungkin...nggak ngerti Y) bukan krama_sarcastic: 1
- REGISTER SALAH: ngoko/Indonesia, template identik 91: 1
- REGISTER SALAH: ngoko/Indonesia; logika aneh (hak wanita kok jadi alat hina?): 1
- BAHASA INDONESIA MURNI: tuh nggak pernah... selalu... = bukan Jawa sama sekali: 1
- BAHASA INDONESIA MURNI; nama partai X = placeholder tidak spesifik: 1

Rejected items:
- [deepseek/krama_sarcastic/agama_islam] BUKAN SARKASME: native membaca sebagai pujian tulus — sarkasme gagal, bukan hate speech (konfirmasi Bapak) — 0/5 detected; ironi tidak tersampaikan ke native speaker
- [gemma3:27b/krama_report/gender_lgbtq] TARGET TIDAK EKSPLISIT: teks hanya bilang para tiyang (orang umum), LGBTQ tidak disebut
- [gemma3:27b/krama_sarcastic/suku_madura] BOCOR INDONESIA: punchline sarkasme dalam bahasa Indonesia (caranya agak... unik)
- [gemma3:27b/krama_sarcastic/suku_tionghoa] BOCOR INDONESIA: kalimat 2-3 Indonesia (Tiap hari kok bisa kaya ngono?...)
- [gemma3:27b/krama_sarcastic/suku_arab] BOCOR INDONESIA: didominasi Indonesia; sowan satu-satunya kata Jawa
- [gemma3:27b/krama_sarcastic/agama_islam] BOCOR INDONESIA: hanya njenengan yang Jawa, sisanya Indonesia murni
- [gemma3:27b/krama_sarcastic/agama_kristen] BOCOR INDONESIA: seluruh teks Indonesia kecuali Wah
- [gemma3:27b/krama_sarcastic/gender_wanita] BOCOR INDONESIA: punchline dalam Indonesia
- [gemma3:27b/krama_sarcastic/gender_lgbtq] BOCOR INDONESIA: seluruh teks Indonesia kecuali Wah
- [gemma3:27b/krama_sarcastic/politik_kolektif] BOCOR INDONESIA: sebagian besar Indonesia
- [gemma3:27b/krama_sarcastic/intra_jawa_arek_vs_mataraman] BOCOR INDONESIA: hanya njenengan/arek/ndoro yang Jawa; sisanya Indonesia
- [gemma3:27b/krama_cold_contempt/suku_madura] REGISTER SALAH: ini ngoko (Lha iki, Wes koyo, ndak iso), bukan krama_cold_contempt
- [gemma3:27b/krama_cold_contempt/suku_tionghoa] sangkahe: bukan kata Jawa dikenal (kemungkinan hallucinated); semantik kalimat tidak jelas
- [gemma3:27b/krama_cold_contempt/suku_arab] Kalimat terakhir (wonten kalih sami-sami ngajeni) tidak logis sebagai hate; mekanisme unclear
- [gemma3:27b/krama_cold_contempt/agama_kristen] REGISTER SALAH: campur ngoko (Lha iki) + Indonesia (tradisinya)
- [gemma3:27b/krama_cold_contempt/gender_lgbtq] REGISTER SALAH: ngoko opener (Lha iki) + krama ending = inkonsisten
- [gemma3:27b/krama_cold_contempt/intra_jawa_arek_vs_mataraman] REGISTER SALAH: ngoko (Lha iki, Wes koyo, ndak iso) bukan krama
- [qwen3:14b/ngoko_direct/suku_madura] kacandran: bukan kata Jawa standar (kemungkinan word hallucination qwen3)
- [qwen3:14b/ngoko_direct/gender_wanita] TARGET TIDAK EKSPLISIT: wanita tidak disebut; kacandran=tidak dikenal
- [qwen3:14b/ngoko_direct/gender_lgbtq] kacandran: bukan kata Jawa standar — LGBTQ disebutkan eksplisit — kalau kacandran valid, bisa jadi 1
- [qwen3:14b/ngoko_direct/politik_kolektif] kacandran: tidak dikenal; politik sebagai target terlalu kabur
- [qwen3:14b/ngoko_direct/intra_jawa_arek_vs_mataraman] kacandran: bukan kata Jawa standar
- [qwen3:14b/krama_report/suku_madura] SEMANTIK TERBALIK: enggal nggawe kacandran = segera bikin kekacauan (harusnya jangan); bocor Indonesia; kacandran tidak dikenal
- [qwen3:14b/krama_report/suku_tionghoa] Sama dengan 82: semantik terbalik + bocor Indonesia + kacandran
- [qwen3:14b/krama_report/suku_arab] Sama dengan 82
- [qwen3:14b/krama_report/agama_islam] Sama dengan 82
- [qwen3:14b/krama_report/agama_kristen] Sama dengan 82
- [qwen3:14b/krama_report/gender_wanita] Sama dengan 82
- [qwen3:14b/krama_report/gender_lgbtq] Sama dengan 82
- [qwen3:14b/krama_report/politik_kolektif] Sama dengan 82
- [qwen3:14b/krama_report/intra_jawa_arek_vs_mataraman] Sama dengan 82
- [qwen3:14b/krama_sarcastic/suku_madura] REGISTER SALAH: ngoko/Indonesia (X iki kok bisa...? Mungkin...nggak ngerti Y) bukan krama_sarcastic
- [qwen3:14b/krama_sarcastic/suku_tionghoa] REGISTER SALAH: ngoko/Indonesia, template identik 91
- [qwen3:14b/krama_sarcastic/suku_arab] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_sarcastic/agama_islam] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_sarcastic/agama_kristen] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_sarcastic/gender_wanita] REGISTER SALAH: ngoko/Indonesia; logika aneh (hak wanita kok jadi alat hina?)
- [qwen3:14b/krama_sarcastic/gender_lgbtq] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_sarcastic/politik_kolektif] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_sarcastic/intra_jawa_arek_vs_mataraman] REGISTER SALAH: ngoko/Indonesia
- [qwen3:14b/krama_cold_contempt/suku_madura] BAHASA INDONESIA MURNI: tuh nggak pernah... selalu... = bukan Jawa sama sekali
- [qwen3:14b/krama_cold_contempt/suku_tionghoa] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/suku_arab] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/agama_islam] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/agama_kristen] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/gender_wanita] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/gender_lgbtq] BAHASA INDONESIA MURNI
- [qwen3:14b/krama_cold_contempt/politik_kolektif] BAHASA INDONESIA MURNI; nama partai X = placeholder tidak spesifik
- [qwen3:14b/krama_cold_contempt/intra_jawa_arek_vs_mataraman] BAHASA INDONESIA MURNI

## QC judge panel vs native verdict

- 29 judge-flagged; 1 natively rejected (precision 3%).
- of 49 native rejections, 1 were judge-flagged (recall 2%).

## PRIORITAS subset: 20/27 = 74% authentic

## Interpretation guide
- High overall rate => LLM is a viable generator for a register-stratified Javanese hate set.
- krama_cold_contempt authentic => N3b-group is generable (the uncollectable register synthesized + native-validated).
- Best model x niche cell => preferred generator per register.
- Evasive AND authentic => genuinely hard hate the cheap detectors miss = the dataset's reason to exist.
- Low judge recall => non-native auto-checks miss native-only judgments => confirms the irreducible native-referee role.
eree role.