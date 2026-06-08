# Pilot #2 — LLM-as-Jawa-filter Report

**Sumber:** haipradana/indonesian-twitter-hate-speech-cleaned (raw text)
**Total diproses:** 2000  |  **valid JSON:** 1999  |  **invalid:** 1
**Filter LLM:** Grok 4.3, prompt jawa_filter_v0

## Distribusi kategori bahasa

| Kategori | N | % dari valid |
|---|---|---|
| jawa | 15 | 0.8% |
| campuran | 134 | 6.7% |
| indonesia | 1800 | 90.0% |
| lainnya | 50 | 2.5% |

**Yield Jawa+campuran:** 149/1999 = **7.5%**

## Cross-tab bahasa × label hate asli

| Kategori | hate | neutral |
|---|---|---|
| jawa | 6 | 9 |
| campuran | 74 | 60 |
| indonesia | 897 | 903 |
| lainnya | 7 | 43 |

**Subset panas (Jawa+campuran):** 149 teks, di antaranya **80 berlabel hate** (54%).
Disimpan ke `outputs/hot_jawa_subset.jsonl`.

## Contoh per kategori (max 4)

### jawa
- [neutral] _ngoko_ penanda=['Jancuk', 'jancuk']
  > Jancuk jancuk'
- [neutral] _ngoko_ penanda=['cangkem', 'po', 'silit', 'angel', "ki'"]
  > Wasuuu, cangkem po silit kok angel dicekel ki'
- [neutral] _ngoko_ penanda=['yen', 'gawe', 'ning', 'ana', 'nyong', 'digawe bae', 'temboke']
  > Pimen yen gawe ning slawi perek hotel grand dian nah ana toko matrial kue gone nyong, digawe bae pimen 2x9 m temboke wkwk'
- [hate] _ngoko_ penanda=['jomok']
  > Jomok

### campuran
- [hate] _ngoko_ penanda=['kaya']
  > kaya banci kali ya'
- [neutral] _ngoko_ penanda=['geblek', 'merit', 'nelponin']
  > Lebih geblek, kalo udah merit malah suka nelponin terus kak '
- [neutral] _ngoko_ penanda=['camken']
  > Jika engkau TIDAK menjalankan perintah ini seumur hidup mu bisa dipastikan MATI mu dalam keadaan MURTAD dan Kafir camken Dari sini semua orang tahu Kenapa merek
- [hate] _ngoko_ penanda=['cocot']
  > Ha ha ha ha ha ....calon presiden ..cuma jago cocot ha ha ha ...ngurusi DKI kagak becus ha ha ha ha'

### indonesia
- [hate] _tidak_ada_ penanda=[]
  > Kelakuan LGBT kaum pelangi anak adopsi jadi pemuas napsu iblis mereka Na uzubillahiminzalik
- [neutral] _tidak_ada_ penanda=[]
  > Kristen woles aja prof.. Dri timur sampe barat namanya beda2, menyesuaikan tiap daerah termasuk tata cara beribadah nya.. Tetapi masalah keyakinan semua sama.. 
- [hate] _tidak_ada_ penanda=[]
  > kafir haram jadi pemimpin nyet'
- [neutral] _tidak_ada_ penanda=[]
  > Yang paling malesin setelah jatoh dari motor itu bukan ngebenerin motornya, tapi punya koreng di lutut yang which is literally pas udah kering bakal susah jalan

### lainnya
- [neutral] _tidak_ada_ penanda=[]
  > Mereun dititah ku si Gunawan sia asri ngaku kunyuk jadi aing nu keuna kehed.'
- [neutral] _tidak_ada_ penanda=[]
  > MSNAKDNSKDNSKDNDJFN MUITO BOM'
- [neutral] _tidak_ada_ penanda=[]
  > Tadi video call dgn sofiya and guest what kiteorg pki baju and seluar yg sama without discussing. '
- [neutral] _tidak_ada_ penanda=[]
  > Presiden PAS Datuk Seri Abdul Hadi Awang tidak akan mempertahankan kerusi Dewan Undangan Negeri DUN Rhu Rendang, sebaliknya hanya akan bertanding kerusi Parlime
