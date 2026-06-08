# Pilot #1b — C3 Re-test Report (3-LLM pada subset Jawa-panas)

**Pertanyaan C3:** apakah multi-LLM agreement bekerja pada hate Jawa ASLI?

**Input:** 24 teks `hot_jawa_subset.jsonl` (Pilot #2, haipradana code-mixed)
**Total records:** 72 | **Vendors:** deepseek, grok, kimi

## Per-vendor metrics

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | In tok | Out tok | Cost (USD) | Hate dist |
|---|---|---|---|---|---|---|---|---|
| deepseek | 24 | 8.3 | 91.7 | 23249 | 30272 | 26414 | $0.110 | 14T/6F |
| grok | 24 | 0.0 | 100.0 | 6464 | 32847 | 1588 | $0.045 | 20T/4F |
| kimi | 24 | 0.0 | 62.5 | 115163 | 31313 | 75726 | $0.100 | 7T/8F |

**Total cost:** $0.255

## Krippendorff's alpha (CORE metric C3)

- **Binary hate:** alpha = **0.384** (bootstrap 95% CI [0.009, 0.704], n_boot=2000)
- **Severity (4 kategori):** alpha = **0.376** (95% CI [0.101, 0.598])
- Label distribution (hate): {True: 41, False: 18} — non-degenerate, alpha bermakna

| Pair | N pairs | Agreement % |
|---|---|---|
| deepseek__grok | 20 | 80.0 |
| deepseek__kimi | 13 | 69.2 |
| grok__kimi | 15 | 66.7 |

### Sensitivitas: alpha hate setelah drop 1 vendor

| Drop | Keep | alpha | 95% CI | n pairable |
|---|---|---|---|---|
| deepseek | grok+kimi | 0.306 | [-0.250, 0.762] | 15 |
| grok | deepseek+kimi | 0.405 | [-0.188, 0.852] | 13 |
| kimi | deepseek+grok | 0.480 | [-0.079, 0.873] | 20 |

## Majority vote vs label asli haipradana

(orig_label = anotasi Indonesia-context, referensi sanity — BUKAN gold)

| orig_label | majority hate=True | majority hate=False |
|---|---|---|
| hate | 9 | 0 |
| neutral | 9 | 6 |

## Severity distribution per vendor

- **deepseek:** {'sedang': 3, 'ringan': 8, 'berat': 3, 'BUK': 6}
- **grok:** {'ringan': 11, 'berat': 5, 'sedang': 4, 'BUK': 4}
- **kimi:** {'ringan': 2, 'BUK': 8, 'berat': 3, 'sedang': 2}

## Disagreements (7 dari 24 teks)

- `haipradana-train-10298` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'ringan', 'kimi': 'BUK'}
  > Lebih geblek, kalo udah merit malah suka nelponin terus kak '
- `haipradana-train-2285` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'berat', 'grok': 'berat', 'kimi': 'BUK'}
  > ngewe napa'
- `haipradana-train-2288` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Kyulkyung visualnya edan.'
- `haipradana-train-3009` (orig: neutral) — hate: {'deepseek': True, 'grok': False, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'BUK', 'kimi': 'BUK'}
  > Sastra e karl mark. PENTOLAN komunis rusia.'
- `haipradana-train-3221` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Asw ini 1145 lho dan skrg ngantuk.'
- `haipradana-train-371` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > ... dan homo jadi mau tidak mau saya pun merasa harus membuktikan kalau saya tidak banci ke orang-orang namun sepertinya gagal karena banyak faktor apalagi dengan wajah saya yang bisa dibilang terlalu...
- `haipradana-train-7362` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'ringan', 'kimi': 'BUK'}
  > Wwkkw tae gua krn terlalu sering pake alesan mens jadi ditanya kok mens mulu sih'

## Decision gate C3

- Avg refusal rate: **2.8%** (target < 20%)
- Avg JSON validity: **84.7%** (target > 90%)
- Krippendorff's alpha (hate): **0.384** (target > 0.5) 

🟡 **YELLOW — alpha moderat. Inspeksi disagreement (boundary case atau noise?), pertimbangkan iterasi prompt (Pilot #3) sebelum scale-up.**

**Catatan n kecil:** 24 teks (9 hate orig). CI bootstrap di atas WAJIB dikutip bersama alpha. 
Hasil ini sinyal pertama C3, bukan angka final — konfirmasi di pool besar (scale filter Pilot #2) sebelum klaim paper.