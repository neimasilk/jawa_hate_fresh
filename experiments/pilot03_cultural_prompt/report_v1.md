# Pilot #3 — Prompt v1 vs v0 (pool n=149)

**Baseline v0:** Pilot #1b scale-up (α full-3LLM = 0.587). **Vendors v1:** deepseek, grok

## Per-vendor metrics (v1)

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | Cost (USD) | Hate dist | Hate rate v0 → vN |
|---|---|---|---|---|---|---|---|
| deepseek | 149 | 0.7 | 97.3 | 18684 | $0.666 | 22T/122F | 55% → **15%** |
| grok | 149 | 0.0 | 100.0 | 5118 | $0.424 | 41T/108F | 77% → **28%** |

**Total cost v1:** $1.091

## Krippendorff's alpha (hate) — vN vs v0, pool sama

| Vendor set | α v0 | 95% CI | α v1 | 95% CI | Δ |
|---|---|---|---|---|---|
| deepseek+grok | 0.534 | [0.381, 0.674] | **0.554** | [0.382, 0.713] | +0.019 |

## Flip label per vendor (v0 → v1)

| Vendor | T→F | F→T | tetap | unpairable |
|---|---|---|---|---|
| deepseek | 54 | 1 | 77 | 17 |
| grok | 74 | 0 | 75 | 0 |

(T→F diharapkan dominan di Grok kalau definisi profanity-vs-hate bekerja; F→T besar = red flag under/over-correction.)

## Majority vote vs label asli haipradana (v1)

| orig_label | majority hate=True | majority hate=False |
|---|---|---|
| hate | 36 | 44 |
| neutral | 8 | 61 |

## Disagreements v1 (21 dari 149 teks)

- `haipradana-train-10253` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > ebong dungu akut. Woii itu pesan berita saat trf . Diinput manual bong...Makanya jgn norak2 bgt, kelamaan dikolam sik'
- `haipradana-train-10829` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Liat ae spa cewek sendiri jadi kayak pick me girl
- `haipradana-train-11555` (orig: hate) — hate: {'deepseek': True, 'grok': False} | severity: {'deepseek': 'ringan', 'grok': 'BUK'}
  > Pret.. kampret , Tak dukung 2019 ganti presiden.. tp.presidenmu sapa ??? Rocky gerung kapir thaa ???'
- `haipradana-train-12022` (orig: hate) — hate: {'deepseek': True, 'grok': False} | severity: {'deepseek': 'sedang', 'grok': 'BUK'}
  > Pak sbelum berani umumkan Muhammad Nabi Gadungan, Anda hrs dorong KPAI mlarang anak mengaji
- `haipradana-train-1258` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Berbagi gambar AI edisi Buaya Betina Mbak monggo jika berkenan disave Pak biasane yo seneng iki
- `haipradana-train-12662` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > duuuuhhhh, Jaya Suprana yang kristen saja mau berguru dengan beliau, lah yg ngaku muslim kok ora
- `haipradana-train-1483` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > mungkin ateis memercayai bahwa di tengah tengahnya surga dan neraka itu anget.'
- `haipradana-train-2613` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Jomok
- `haipradana-train-2680` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Azu tenan soh orang2 kek.gini nih...bani.micin...'
- `haipradana-train-3093` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > awas guys ada pelakor mba mba feb undip 22 demennya ngelonte sm pacar org korbannya ga satu doang
- `haipradana-train-3333` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'berat'}
  > Jika engkau TIDAK menjalankan perintah ini seumur hidup mu bisa dipastikan MATI mu dalam keadaan MURTAD dan Kafir camken Dari sini semua orang tahu Kenapa mereka pengen nya BERANTEM terus
- `haipradana-train-3877` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'berat'}
  > klu KPK di bubarkan.. Kita sebagai rakyat wajibkudu bubarkan wakil rakyatDPR
- `haipradana-train-4600` (orig: hate) — hate: {'deepseek': True, 'grok': False} | severity: {'deepseek': 'sedang', 'grok': 'BUK'}
  > Dengan ideologi pancasila saja kalian tidak bisa berbagi toleransi antar umat beragama apalagi dengan ideologi khilafuck yg kalian banggakan tak terbayang bagaimana nasib kaum minoritas jadi manusia i...
- `haipradana-train-4629` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Jidatnya Gosong ,gaya Islami tp Mentalnya Bajingan,pedagang Agama,calo ibadah Uang org mau ibadah di embat,ini lbh busuk dan'
- `haipradana-train-4859` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > Ga mikir keluarga korban bom ukhti2 otaknya di dengkul.. kok KZL ya?'
- `haipradana-train-6000` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > askrl kaum rahim anget
- `haipradana-train-7423` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Asw untung gapernah ewe ewe anak wong Tapi koyok e enak ki tapi ojo mbokyo koe dadi wong lanang ki seng Apikk suu saake kaum betina Mesakno lhurr mosok bar di ewe mbok tingalno kan saake
- `haipradana-train-922` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Pengajian dibubarkan LaGiBeTe dibelain Disitu saya pengen nglempar bakiak
- `haipradana-train-9318` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > cwk pratama arhan kena serang kaum rahim anget sit
- `haipradana-train-9537` (orig: hate) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > sampe segitunya jadi penjilat, ngakunya muslim, agamanya di hinaampdi nista si BTP cangkem mingkem, ahok akan selalu di kenang oleh kaum penjilat kek elo.'
- `haipradana-train-955` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > cewe pulang malem pasti cewe gabener pasti murahan pasti nyeleweng lah ini srikandi srikandinya pulang malem bahkan pagi buat bikin mobil balap formula student listrik piye ga bahaya ta Happy belated ...

## Kesimpulan iterasi

- α(deepseek+grok): v0 0.534 → v1 **0.554** (CI [0.382, 0.713])
- 🟡 **v1 ≈ v0** — cek flip table & disagreement: mungkin perbaikan kualitatif tanpa α naik.