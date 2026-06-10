# Pilot #3 — Prompt v2 vs v0 (pool n=149)

**Baseline v0:** Pilot #1b scale-up (α full-3LLM = 0.587). **Vendors v2:** deepseek, grok

## Per-vendor metrics (v2)

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate dist | Hate rate v0 → vN |
|---|---|---|---|---|---|---|---|
| deepseek | 149 | 0.0 | 94.0 | 18725 | $0.744 | 27T/113F | 55% → **19%** |
| grok | 149 | 0.0 | 100.0 | 7189 | $0.506 | 46T/103F | 77% → **31%** |

**Total cost v2:** $1.250

## Krippendorff's alpha (hate) — vN vs v0, pool sama

| Vendor set | α v0 | 95% CI | α v2 | 95% CI | Δ |
|---|---|---|---|---|---|
| deepseek+grok | 0.534 | [0.381, 0.674] | **0.763** | [0.624, 0.879] | +0.229 |

## Flip label per vendor (v0 → v2)

| Vendor | T→F | F→T | tetap | unpairable |
|---|---|---|---|---|
| deepseek | 47 | 1 | 84 | 17 |
| grok | 71 | 2 | 76 | 0 |

(T→F diharapkan dominan di Grok kalau definisi profanity-vs-hate bekerja; F→T besar = red flag under/over-correction.)

## Majority vote vs label asli haipradana (v2)

| orig_label | majority hate=True | majority hate=False |
|---|---|---|
| hate | 37 | 43 |
| neutral | 9 | 60 |

## Disagreements v2 (12 dari 149 teks)

- `haipradana-train-10622` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Ketika cewek berbalas gombal di space iihhh murahan Genit Gathel Tapi cowok yang suka gombal sana sini dibilang wajar Okay siap
- `haipradana-train-10829` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Liat ae spa cewek sendiri jadi kayak pick me girl
- `haipradana-train-1258` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Berbagi gambar AI edisi Buaya Betina Mbak monggo jika berkenan disave Pak biasane yo seneng iki
- `haipradana-train-12582` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Mungkin masih banyak masyarakat tionghoa yg lebih pancasialis dr pada wong jowo cm nggak terekpos aja, contoh nyata pak kwik ekonom dan ustadz felix siauw '
- `haipradana-train-12662` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > duuuuhhhh, Jaya Suprana yang kristen saja mau berguru dengan beliau, lah yg ngaku muslim kok ora
- `haipradana-train-1483` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > mungkin ateis memercayai bahwa di tengah tengahnya surga dan neraka itu anget.'
- `haipradana-train-1721` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Gus Mus alimnya kayak gini kok ya ada yg berani fitnah toh Kebencianku sama buzzer2 politik wes sampe pada klimaksnya I m done Dugaanku selama ini mgkn gak sepenuhnya salah Jangan2 selama ini mereka c...
- `haipradana-train-2613` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Jomok
- `haipradana-train-3877` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > klu KPK di bubarkan.. Kita sebagai rakyat wajibkudu bubarkan wakil rakyatDPR
- `haipradana-train-4629` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Jidatnya Gosong ,gaya Islami tp Mentalnya Bajingan,pedagang Agama,calo ibadah Uang org mau ibadah di embat,ini lbh busuk dan'
- `haipradana-train-7423` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Asw untung gapernah ewe ewe anak wong Tapi koyok e enak ki tapi ojo mbokyo koe dadi wong lanang ki seng Apikk suu saake kaum betina Mesakno lhurr mosok bar di ewe mbok tingalno kan saake
- `haipradana-train-827` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > "teko o rek!" mksdnya bukan arek, tapi perek'

## Kesimpulan iterasi

- α(deepseek+grok): v0 0.534 → v2 **0.763** (CI [0.624, 0.879])
- ✅ **v2 NAIK signifikan** — keep, jadikan baseline iterasi berikut.