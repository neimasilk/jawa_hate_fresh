# Pilot #2 — LLM-as-Jawa-filter Report

**Sumber:** haipradana/indonesian-twitter-hate-speech-cleaned (raw text)
**Total diproses:** 250  |  **valid JSON:** 250  |  **invalid:** 0
**Filter LLM:** Grok 4.3, prompt jawa_filter_v0

## Distribusi kategori bahasa

| Kategori | N | % dari valid |
|---|---|---|
| jawa | 1 | 0.4% |
| campuran | 23 | 9.2% |
| indonesia | 219 | 87.6% |
| lainnya | 7 | 2.8% |

**Yield Jawa+campuran:** 24/250 = **9.6%**

## Cross-tab bahasa × label hate asli

| Kategori | hate | neutral |
|---|---|---|
| jawa | 0 | 1 |
| campuran | 9 | 14 |
| indonesia | 100 | 119 |
| lainnya | 0 | 7 |

**Subset panas (Jawa+campuran):** 24 teks, di antaranya **9 berlabel hate** (38%).
Disimpan ke `outputs/hot_jawa_subset.jsonl`.

## Contoh per kategori (max 4)

### jawa
- [neutral] _ngoko_ penanda=['Jancuk', 'jancuk']
  > Jancuk jancuk'

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
