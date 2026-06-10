# Pilot #1b — C3 Re-test Report (3-LLM pada subset Jawa-panas)

**Pertanyaan C3:** apakah multi-LLM agreement bekerja pada hate Jawa ASLI?

**Input:** 149 teks `hot_jawa_subset.jsonl` (Pilot #2, haipradana code-mixed)
**Total records:** 447 | **Vendors:** deepseek, grok, kimi

## Per-vendor metrics

| Vendor | N | Refusal % | JSON Valid % | Latency mean (ms) | In tok | Out tok | Cost (USD) | Hate dist |
|---|---|---|---|---|---|---|---|---|
| deepseek | 149 | 4.7 | 95.3 | 29501 | 185769 | 159575 | $0.664 | 76T/61F |
| grok | 149 | 0.0 | 100.0 | 7194 | 204272 | 9765 | $0.280 | 115T/34F |
| kimi | 149 | 0.7 | 73.8 | 126285 | 193379 | 474894 | $0.628 | 55T/55F |

**Total cost:** $1.572

## Krippendorff's alpha (CORE metric C3)

- **Binary hate:** alpha = **0.587** (bootstrap 95% CI [0.475, 0.698], n_boot=2000)
- **Severity (4 kategori):** alpha = **0.480** (95% CI [0.387, 0.571])
- Label distribution (hate): {False: 150, True: 246} — non-degenerate, alpha bermakna

| Pair | N pairs | Agreement % |
|---|---|---|
| deepseek__grok | 137 | 78.8 |
| deepseek__kimi | 101 | 86.1 |
| grok__kimi | 110 | 77.3 |

### Sensitivitas: alpha hate setelah drop 1 vendor

| Drop | Keep | alpha | 95% CI | n pairable |
|---|---|---|---|---|
| deepseek | grok+kimi | 0.527 | [0.355, 0.685] | 110 |
| grok | deepseek+kimi | 0.722 | [0.580, 0.856] | 101 |
| kimi | deepseek+grok | 0.534 | [0.381, 0.674] | 137 |

## Majority vote vs label asli haipradana

(orig_label = anotasi Indonesia-context, referensi sanity — BUKAN gold)

| orig_label | majority hate=True | majority hate=False |
|---|---|---|
| hate | 66 | 14 |
| neutral | 31 | 38 |

## Severity distribution per vendor

- **deepseek:** {'sedang': 28, 'ringan': 25, 'berat': 23, 'BUK': 61}
- **grok:** {'ringan': 39, 'berat': 30, 'sedang': 46, 'BUK': 34}
- **kimi:** {'ringan': 22, 'BUK': 55, 'berat': 8, 'sedang': 25}

## Disagreements (36 dari 149 teks)

- `haipradana-train-10094` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang'}
  > Doeloe rezim Orba dollar melambung tinggi hingga Rp 15.000, Pak Harto lengser keprabon. Kondisi yg sama sprt rezim skrg ini, berani gak Jokowi lengser keprabon?'
- `haipradana-train-10213` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > pernah bilang mencla mencle nah Boss nya sendiri begitu URL
- `haipradana-train-10298` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'ringan', 'kimi': 'BUK'}
  > Lebih geblek, kalo udah merit malah suka nelponin terus kak '
- `haipradana-train-10622` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'BUK'}
  > Ketika cewek berbalas gombal di space iihhh murahan Genit Gathel Tapi cowok yang suka gombal sana sini dibilang wajar Okay siap
- `haipradana-train-10687` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > anda kalo merasa tersinggung jangan koar2 di twitter...laporin sana ke polri...paling juga ditolak...wong deliknya gak jelas kok agama yg mana....waktu ahok menista
- `haipradana-train-10701` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'ringan'}
  > Umat Islam jgn mau terprovokasi sm si Dede bajingan agama berubah ubah di sesuaikan dgn pesanan
- `haipradana-train-10967` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Inilah Mentri BUMN yg saenaknya dewe, miskin prestasi dan banyak conflict-of-interest. Gini kok dipertahankan Pres Jokowi, ada apa ???
- `haipradana-train-11393` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Prabowo ketularan mencla mencle Amien Rais. URL
- `haipradana-train-1258` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Berbagi gambar AI edisi Buaya Betina Mbak monggo jika berkenan disave Pak biasane yo seneng iki
- `haipradana-train-12662` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'BUK'}
  > duuuuhhhh, Jaya Suprana yang kristen saja mau berguru dengan beliau, lah yg ngaku muslim kok ora
- `haipradana-train-1483` (orig: neutral) — hate: {'grok': True, 'kimi': False} | severity: {'grok': 'ringan', 'kimi': 'BUK'}
  > mungkin ateis memercayai bahwa di tengah tengahnya surga dan neraka itu anget.'
- `haipradana-train-1840` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'berat', 'kimi': 'BUK'}
  > imejin gue sm jebi udh modar ketabrak meteor'
- `haipradana-train-2285` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'berat', 'grok': 'berat', 'kimi': 'BUK'}
  > ngewe napa'
- `haipradana-train-2288` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Kyulkyung visualnya edan.'
- `haipradana-train-2395` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'BUK'}
  > Duh kok kesannya insensitive gt yaaa sis gr gr bom tempo hari asosiasi cadar makin negatif, eh saiki ketambahan iki
- `haipradana-train-2726` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > MALEN JEMPOL GWA PEGEL NGE SWITCH ACC KAMPANG ON D YG SATU LAGI AJA NDE'
- `haipradana-train-3009` (orig: neutral) — hate: {'deepseek': True, 'grok': False, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'BUK', 'kimi': 'BUK'}
  > Sastra e karl mark. PENTOLAN komunis rusia.'
- `haipradana-train-3221` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Asw ini 1145 lho dan skrg ngantuk.'
- `haipradana-train-3610` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > bodo anjir ngapa uangnya kek gitu si wkwkw'
- `haipradana-train-371` (orig: neutral) — hate: {'deepseek': False, 'grok': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan'}
  > ... dan homo jadi mau tidak mau saya pun merasa harus membuktikan kalau saya tidak banci ke orang-orang namun sepertinya gagal karena banyak faktor apalagi dengan wajah saya yang bisa dibilang terlalu...
- `haipradana-train-3877` (orig: hate) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'berat', 'grok': 'sedang', 'kimi': 'BUK'}
  > klu KPK di bubarkan.. Kita sebagai rakyat wajibkudu bubarkan wakil rakyatDPR
- `haipradana-train-4015` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'ringan'}
  > Aku ra usah tak tutupi wis budek o mba, wkwkwk'
- `haipradana-train-4586` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Lbih baik gtu dri pd munafik, sok mlu tapi mau'
- `haipradana-train-4810` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'berat', 'kimi': 'sedang'}
  > Wasuuu, cangkem po silit kok angel dicekel ki'
- `haipradana-train-566` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Detik detik Presiden Indonesia, eh Gubernur Indonesia ? pak bertemu dengan Presiden Turki Tanpa teks, tanpa bingung lgsg nyrocos ngomong nampak sangat Akrab sekali. Beda dengan si itu... Ah sudahlah g...
- `haipradana-train-6327` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'BUK'}
  > Benerin sinyal dulu cuk !! Udah 2 minggu sinyalmu kaya bangke. BUSUK'
- `haipradana-train-6551` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > Bila mok antek tok. Bila mok kurus tok.'
- `haipradana-train-6556` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'sedang'}
  > Anak awak Rahim anget juga diajak ngobrol ma sopir travel aja lgsg nyaman
- `haipradana-train-6829` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'ringan'}
  > Dear driver lo ada yang tukeran orang buat anter gw, gw sih gak masalah asal pinter gak dongo muter2 cari rumah gw. Ini udah pake driver pengganti dongo buang waktu gw bgt buat nunggu. Taik'
- `haipradana-train-6910` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'berat', 'kimi': 'ringan'}
  > ios asw napada '
- `haipradana-train-7362` (orig: neutral) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'ringan', 'grok': 'ringan', 'kimi': 'BUK'}
  > Wwkkw tae gua krn terlalu sering pake alesan mens jadi ditanya kok mens mulu sih'
- `haipradana-train-7654` (orig: hate) — hate: {'deepseek': True, 'grok': True, 'kimi': False} | severity: {'deepseek': 'sedang', 'grok': 'ringan', 'kimi': 'BUK'}
  > Ha ha ha ha ha ....calon presiden ..cuma jago cocot ha ha ha ...ngurusi DKI kagak becus ha ha ha ha'
- `haipradana-train-8606` (orig: neutral) — hate: {'deepseek': False, 'grok': False, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'BUK', 'kimi': 'ringan'}
  > Itu lagi ngomong bacot dalem ati'
- `haipradana-train-8651` (orig: neutral) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'ringan', 'kimi': 'BUK'}
  > asw gua ketawa'
- `haipradana-train-9179` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': True} | severity: {'deepseek': 'BUK', 'grok': 'berat', 'kimi': 'ringan'}
  > Hahaha payah tai kotok!'
- `haipradana-train-9922` (orig: hate) — hate: {'deepseek': False, 'grok': True, 'kimi': False} | severity: {'deepseek': 'BUK', 'grok': 'sedang', 'kimi': 'BUK'}
  > Yg paling mirisnya, mereka tuh cowo bertiga anj anj anj anj anj! COWO LOH! Sanggup ya mulutnya ngerumpi terus gbisa diam kaya congor bebek. Sampe film nya habis anjiiirr! Kesal ke ubun ubun dah ketaha...

## Decision gate C3

- Avg refusal rate: **1.8%** (target < 20%)
- Avg JSON validity: **89.7%** (target > 90%)
- Krippendorff's alpha (hate): **0.587** (target > 0.5) 

🟡 **YELLOW — alpha moderat. Inspeksi disagreement (boundary case atau noise?), pertimbangkan iterasi prompt (Pilot #3) sebelum scale-up.**

**Catatan:** n=149 teks. CI bootstrap di atas WAJIB dikutip bersama alpha.