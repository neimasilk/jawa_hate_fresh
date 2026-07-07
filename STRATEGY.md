# STRATEGY — Ujaran Kebencian Jawa (Strategic Review oleh Fable 5)

**Dokumen tipe:** Strategic memo (bukan eksekusi). Ditulis 2026-07-06 oleh Fable 5 sebagai *strategist* (satu kali, mahal). Eksekusi detail → serahkan ke Sonnet/Opus.
**Audience:** Bapak (Mukhlis) + sesi Claude Code berikutnya (executor).
**Scope:** Menilai posisi riset saat ini secara jujur, mendiagnosis kelemahan yang bisa menjatuhkan paper, dan menetapkan strategi + roadmap agar tembus **Scopus/Q-tier** (target) dengan **Sinta 2 / JINITA** sebagai lantai aman.
**Sumber:** seluruh repo (`paper/draft_jinita.md` v4, `experiments/register_probe/FINDINGS.md`, `experiments/generation_pilot/`, `data/labeled/` 728, `CODEBOOK.md`, PRD v0.4, STATE, wiki) + aset eksternal `D:\documents\twitter` (Digital Vitality Index).

> **Aturan main dokumen ini:** Ini memo strategi, bukan perintah. Setiap rekomendasi diberi label **[WAJIB]** / **[TINGGI]** / **[OPSIONAL]** dan estimasi effort + biaya + siapa eksekutornya. Keputusan yang hanya bisa diambil Bapak dikumpulkan di **§9**. Tidak melanggar HARD RULES CLAUDE.md — di mana ada gesekan (mis. "zero-human" vs multi-validator), gesekan itu **diangkat eksplisit**, tidak diselundupkan.

---

## 0. TL;DR — panggilan strategis dalam satu paragraf

Kerja tiga bulan terakhir menghasilkan **satu temuan yang benar-benar bernilai** dan **satu framing yang belum siap untuk venue tinggi**. Temuan bernilainya: *register kehormatan Jawa (unggah-ungguh) menyandi suhu + arah kebencian — benci panas→ngoko (berlimpah di korpus), benci dingin/ironis→krama (nyaris tak bisa dikoleksi), dan yang dingin-ironis itu lolos SEMUA detektor otomatis (4% vs ngoko 100%).* Itu temuan kelas jurnal bagus. Framing yang belum siap: **"kami membangun generator ujaran kebencian Jawa"** — ini punya tiga masalah yang, bila tidak diperbaiki, membuat paper ditolak di Scopus/Q-tier (dan berisiko bahkan di Sinta 2): **(1) validator native n=1** (penulis pertama sendiri), **(2) klaim "blind-spot" diuji hanya pada LLM-judge dengan satu prompt, di atas data sintetis buatan DeepSeek sendiri** (sirkularitas + validitas eksternal lemah), **(3) etika dual-use** — "generator yang bikin hate uncollectable DAN undetectable" terbaca sebagai alat serangan, bukan riset defensif.

**Rekomendasi inti (satu kalimat):** *Balik sudut pandang dari "generator" ke "diagnosis + perbaikan blind-spot deteksi berbasis register" (template HateCheck), tambahkan 2–3 validator native + baseline deteksi manusia + detektor nyata (bukan cuma LLM-judge) + satu eksperimen mitigasi (augmentasi menutup blind-spot).* Reframe ini sekaligus menyelesaikan ketiga masalah, menaikkan plafon venue dari Sinta 2 ke Scopus Q-tier/WOAH/LREC, dan mengubah paper dari "cara bikin hate tak terdeteksi" menjadi "cara membuat detektor melihat hate yang selama ini tak terlihat."

---

## 1. Penilaian jujur: apa yang kuat, apa yang rapuh

### 1.1 Yang genuinely kuat (jangan dikorbankan)

| # | Kekuatan | Kenapa bernilai |
|---|---|---|
| K1 | **Model register-pragmatik** (panas→ngoko / dingin·ironis·contempt→krama; 4 niche: ngoko_direct, krama_report, krama_sarcastic, krama_cold_contempt) | Novel, tidak ada di taksonomi hate manapun (Western/Indonesia). Grounded di intuisi native + tervalidasi. Ini **mahkota** paper. |
| K2 | **Detection blind-spot untuk implikatur (pasemon/ironi)** | Konkret, mengejutkan, dan *actionable* untuk desain moderasi. krama_sarcastic 4% vs ngoko 100%; krama_report tetap 78–89% → membuktikan yang membutakan = **implikatur, bukan kesopanan**. Ini pembeda halus yang membuat temuan kredibel. |
| K3 | **Bukti kelangkaan yang kuat + kini ganda** | 728 tweet berlabel → 0 konsensus krama-hate, 157/158 ngoko. **DAN** aset independen `D:\documents\twitter`: ~3,5 juta tweet di-scrape → hanya **1.321 (~0,09%)** terkonfirmasi Jawa (DVI). Dua sumber independen = argumen "collection paradox" kokoh. |
| K4 | **Higienis metodologis tinggi** | Krippendorff α kanonik (D17), held-out validation (anti-overfit, α 0.688), verifikasi adversarial multi-agent yang **menemukan 2 bug nyata**, PII scrub, semua run di-log. Ini reproducibility yang jarang di paper Sinta. Jual ini. |

### 1.2 Yang rapuh (bisa menjatuhkan paper — diurut by severity)

| # | Kelemahan | Severity | Kenapa mematikan | Penawar (lihat §4) |
|---|---|---|---|---|
| R1 | **Validator native n=1** (penulis pertama, sekaligus yang menilai keasliannya sendiri) | 🔴 FATAL untuk Q-tier | Semua klaim keaslian (97%, 55%, "authentic") bertumpu pada satu orang yang punya kepentingan. Tidak ada inter-rater reliability. Reviewer Scopus hampir pasti reject; reviewer Sinta 2 pun akan flag. Paper sendiri sudah mengaku ini limitasi #1. | E1: 2–3 validator native |
| R2 | **Blind-spot diuji hanya pada LLM-judge + prompt v2 yang sama**, di atas data sintetis buatan **DeepSeek sendiri** | 🔴 TINGGI | (a) Sirkularitas: DeepSeek generator=detektor gagal deteksi ironinya sendiri. (b) "5 detektor" sebetulnya 5 model × 1 prompt yang identik — bukan benchmark luas. (c) Validitas eksternal: apakah blind-spot properti *ironi Jawa* atau properti *gaya sintetis DeepSeek*? Tak terjawab. | E2: detektor nyata + E3: anchor data real |
| R3 | **Etika dual-use** — framing "uncollectable AND undetectable" | 🔴 TINGGI | Terbaca sebagai resep membuat hate tak terdeteksi. Ethics reviewer (wajib di Scopus/ACL-venue) bisa reject atas dasar ini saja. Juga risiko riil. | Reframe §3 + E5 mitigasi |
| R4 | **Skala kecil (108 contoh, 36 sel)** | 🟠 SEDANG | "Proof of concept" cukup untuk finding, tapi Q-tier mau *resource* yang usable atau *power* statistik. 108 terlalu tipis untuk klaim benchmark. | E4: perbesar + stratifikasi |
| R5 | **Ambiguitas ground-truth ironi** | 🟠 SEDANG (tersembunyi, berbahaya) | Contoh #21: native (Bapak sendiri) awalnya membaca sarkasme sebagai *pujian tulus*. Kalau native pun bisa salah baca ironi, apa dasar menyebut "miss" detektor sebagai *kegagalan*? Reviewer tajam akan tusuk di sini: mungkin ironinya memang genuinely ambiguous, bukan detektornya buta. | E6: baseline deteksi-manusia |
| R6 | **"Detektor" belum termasuk sistem deploy nyata** (IndoBERT fine-tuned, Perspective API, moderasi komersial) | 🟠 SEDANG | Klaim "seluruh ekosistem deteksi buta" hanya benar untuk LLM-judge. Jauh lebih kuat kalau IndoBERT fine-tuned + Perspective API juga miss. | E2 |
| R7 | **Generator bias (device formulaic)** | 🟡 RENDAH | DeepSeek pakai device berulang ("Mugi…enggal", "boten gadhah isin/unggah-ungguh"). Apakah representatif atau artefak distribusi LLM? Jujur diakui di limitasi, tapi memperlemah klaim "diversity". | E4 diversity-prompt |
| R8 | **Venue mismatch** — paper ditulis untuk JINITA, user kini mau Scopus/Q | 🟡 RENDAH | Bar rigor beda. Paper as-is tidak akan lolos Scopus Q3. Perlu keputusan sadar: naikkan kerja ke bar Q, atau terima Sinta 2. | §5 venue ladder |

**Kesimpulan penilaian:** Temuan (K1–K2) layak Q-tier. Bukti motivasi (K3) kuat. Tapi *eksekusi validasi* (R1, R2, R5, R6) masih di level workshop/Sinta. Gap-nya bukan ide — gap-nya **rigor validasi + framing etis**. Semua bisa ditutup dalam ~2–4 sesi weekend tanpa membongkar temuan.

---

## 2. Diagnosis akar: kenapa proyek ini "sulit" (dan kenapa itu justru asetnya)

Bapak menyebut dua tantangan. Keduanya bukan hambatan — keduanya adalah **subjek paper**. Strategist harus memastikan paper menjual keduanya sebagai temuan, bukan menyembunyikannya sebagai kendala.

**Tantangan 1 — orang Jawa pakai Indonesia di ruang publik.** Ini *diglosia digital*, dan Bapak sudah mengukurnya dua kali secara independen:
- `haipradana`: 8.269 tweet difilter → 74 (0,9%) Jawa.
- `D:\documents\twitter`: ~3,5 juta tweet → 1.321 (~0,09%) Jawa (DVI Javanese 0.093%, 84,3M penutur, indo_overlap 45%).

→ Ini bukan "gagal cari data". Ini **temuan kuantitatif tentang keterlihatan digital bahasa daerah** — dan `D:\documents\twitter` punya data pembanding lintas-bahasa (Madura 0,0008%, Sunda 0,018%, dst) yang membuat Javanese punya *baseline komparatif*. **Aset ini belum dipakai di paper. Pakai (E7).**

**Tantangan 2 — tingkatan bahasa (ngoko/madya/krama), hate krama sulit dicari.** Ini persis *collection paradox* yang jadi inti paper. Tapi ada nuansa yang belum digarap dan justru menguatkan:
- Paper sekarang meng-collapse **madya**. Intuisi Bapak ("madya masih bisa [dikoleksi]") adalah **hipotesis empiris yang berharga**: kemungkinan ada **gradien collectability by register** — ngoko (berlimpah) → madya (jarang) → krama (nol). Kalau ini terkuantifikasi, jadi sub-temuan rapi yang memperkuat argumen struktural (bukan sekadar "krama nol", tapi "keterlihatan menurun monoton dengan formalitas register"). **[OPSIONAL, tapi elegan — E8].**

**Insight strategis:** kedua "kesulitan" ini menyatu jadi satu tesis yang kuat: *NLP berbasis-korpus secara sistematis buta pada register yang tidak muncul di korpus — dan pada bahasa diglosik, seluruh register (krama) beserta modus pragmatiknya (pasemon) hilang. Jawa adalah studi kasus yang bisa diukur.* Itu tesis yang bisa dijual jauh di atas "deteksi hate Jawa".

---

## 3. Reframe strategis: dari "Generator" ke "Diagnose→Fix blind-spot" (template HateCheck)

Ini rekomendasi tunggal paling berdampak di dokumen ini. **Jangan buang kerjanya — putar sudut pandangnya.**

### 3.1 Masalah dengan framing "generation" saat ini
Judul v4: *"Register-Stratified Javanese Hate Speech Generation via LLMs."* Kata **"Generation"** sebagai headline memicu ketiga masalah sekaligus: dual-use (R3), tuntutan skala dataset (R4), dan menempatkan *generator quality* (yang bertumpu pada n=1 validator, R1) sebagai kontribusi utama.

### 3.2 Framing yang direkomendasikan
Jadikan **generation = metode konstruksi stimulus terkontrol** (bukan kontribusi utama), dan jadikan **karakterisasi + penutupan blind-spot deteksi = kontribusi utama**. Presedennya sudah mapan dan sangat disitasi:

- **HateCheck** (Röttger et al., ACL 2021) — *functional test suite* untuk detektor hate. Mereka **mengonstruksi** kalimat uji terkontrol (bukan koleksi), lalu mengukur di mana detektor gagal per fungsi. Konstruksi stimulus untuk audit = metode yang diterima, tidak dianggap "membuat hate". Ini payung etis + metodologis yang tepat.
- **CheckList** (Ribeiro et al., ACL 2020) — behavioral testing NLP via templated stimuli.

Analog langsung: **"JavaneseHateCheck: sebuah *register-aware diagnostic suite* untuk mengungkap blind-spot pragmatik pada deteksi ujaran kebencian bahasa diglosik."** Generator DeepSeek menjadi *stimulus constructor*, divalidasi native — persis peran yang sudah dilakukan.

### 3.3 Arc paper yang direkomendasikan (struktur pemenang: problem→diagnosis→mitigasi)
1. **Diglosia menyembunyikan satu register.** Benci dingin/ironis Jawa hidup di krama; krama absen dari korpus (kelangkaan, dua-anchor: haipradana 0,9% + twitter DVI 0,09%).
2. **Ini bukan sekadar gap data — ini gap deteksi.** Bangun *diagnostic suite* register-stratified (4 niche × N target), divalidasi **beberapa** native.
3. **Tunjukkan gap-nya = gap MANUSIA–MESIN.** Native mengenali ironi krama sebagai hate (~?%, ukur via E6); detektor — LLM-judge **dan** IndoBERT fine-tuned **dan** Perspective/API — hanya ~4%. *Gap manusia-mesin* = temuan yang tidak bisa dibantah "mungkin memang ambigu".
4. **Diagnosis kenapa:** implikatur (pasemon), bukan kesopanan permukaan (krama_report tetap tertangkap). Matriks register × modus-pragmatik.
5. **Mitigasi:** augmentasi register-stratified **menutup** X% gap saat fine-tune IndoBERT (E5). ← Ini yang mengubah generator dari liability jadi *alat defensif*.
6. **Rilis:** diagnostic suite + codebook + resep augmentasi, lisensi terbatas (norma HateHub/HateCheck).

### 3.4 Kenapa reframe ini menang di semua sumbu
- **Etika (R3):** kontribusi jadi *audit + perbaikan* detektor (defensif), bukan produksi hate. Mitigasi (langkah 5) membuat niat defensif tak terbantah.
- **Sirkularitas (R2):** ditutup langkah 3 (detektor nyata) + baseline manusia (langkah 3).
- **n=1 (R1):** beberapa native di langkah 2 + baseline manusia langkah 3.
- **Skala (R4):** sebagai *diagnostic suite* (bukan training set), 108→~200 stimulus terkontrol itu *cukup* dan sesuai norma (HateCheck ~3.700 tapi templated; skala kecil-terkontrol diterima untuk suite fungsional low-resource).
- **Impact:** naik dari "karakterisasi hate Jawa" ke "kelas kegagalan pragmatik pada NLP bahasa diglosik" — generalizable, lebih tinggi sitasi.

> **Catatan penting:** reframe ini **tidak membuang** paper v4. ~70% teks (taksonomi §2, method generation §3.2, scarcity §3.1) dipakai ulang. Yang berubah: judul, abstract, urutan kontribusi, penambahan §mitigasi + §baseline-manusia, dan pembingkaian etika. Executor cukup me-*restructure*, bukan menulis ulang.

---

## 4. Roadmap eksperimen berprioritas

Diurut by leverage (dampak-ke-plafon-venue ÷ effort). Kolom "Buka" = plafon venue yang dibuka eksperimen itu. Semua eksekusi → **Sonnet/Opus**, bukan Fable.

| ID | Eksperimen | Apa yang dibeli | Effort Bapak | Effort mesin | Biaya | Prioritas | Buka |
|---|---|---|---|---|---|---|---|
| **E1** | **2–3 validator native** menilai keaslian (comprehension rating, bukan anotasi). Idealnya Yekti/Daniel bila penutur Jawa; kalau tidak, 2 kolega native akademik. Hitung inter-rater α keaslian. | Menutup R1 (fatal). Mengubah 97%/55% dari klaim-1-orang → klaim ber-reliability. | Rekrut + koordinasi (~1–2 jam Bapak); tiap validator ~2 jam | Siapkan form + skor | ~$0 | 🔴 WAJIB | Sinta 2 solid + syarat perlu Q |
| **E2** | **Detektor nyata** selain LLM-judge: (a) IndoBERT/IndoRoBERTa hate fine-tuned publik, (b) Perspective API (dukung Indonesia), (c) 1 model toxicity multilingual (XLM-R). Jalankan di 36+ sel. | Menutup R2+R6. "Blind-spot" jadi lintas-arsitektur, bukan artefak 1 prompt. | 0 | Setup model + inference | ~$0 (Perspective gratis, IndoBERT lokal) | 🔴 WAJIB (untuk Q) | Q-tier |
| **E3** | **Anchor data REAL:** 5–15 contoh krama-sarcastic/cold-contempt hate asli (dari pengetahuan native, sastra/wayang, atau edge-case sosmed). Jalankan lewat detektor. | Menutup "apakah blind-spot cuma gaya DeepSeek?". Jembatan sintetis↔real. | Kurasi contoh (~1–2 jam, native-only) | Jalankan probe | ~$0 | 🔴 TINGGI | Q-tier |
| **E5** | **Eksperimen mitigasi:** fine-tune IndoBERT pada (728 real) vs (728 + generated krama), ukur apakah recall krama-ironi naik. | Mengubah generator→alat defensif (bunuh R3). Melengkapi arc problem→fix. Kontribusi paling "publishable". | 0 | Fine-tune ×2 + eval (GPU lokal RTX 4080) | ~$0 | 🔴 TINGGI | Q-tier / WOAH |
| **E6** | **Baseline deteksi-manusia:** minta 2–3 native (bisa sama dgn E1) menandai hate/non-hate pada sel yang sama dengan detektor. Bandingkan human recall vs machine recall. | Menutup R5. Mengubah "detektor miss" → "detektor miss yang MANUSIA tangkap" = gap manusia-mesin (temuan tak terbantah). | ~1 jam per native (gabung E1) | Skor + banding | ~$0 | 🟠 TINGGI | Q-tier |
| **E4** | **Perbesar + diversifikasi suite** ke ~150–200 stimulus: tambah target, diversity-prompt (lawan device formulaic R7), tambah axis regional (Arek vs Mataraman krama). | Menutup R4+R7. Suite lebih kredibel sebagai resource. | Validasi tambahan (skala dgn E1) | Generate + QC | ~beberapa sen DeepSeek | 🟡 SEDANG | Memperkuat Q |
| **E7** | **Integrasikan DVI `D:\documents\twitter`** sebagai anchor kelangkaan ke-2 + tabel komparatif lintas-bahasa. | Motivasi jadi kuantitatif + independen + komparatif. Murah, dampak tinggi ke §Intro. | Konfirmasi angka (~15 mnt) | Ekstrak + tulis | ~$0 | 🟠 TINGGI (murah) | Semua venue |
| **E8** | **Gradien collectability by register** — uji hipotesis Bapak "madya masih bisa": kuantifikasi yield hate per register (ngoko/madya/krama) di dump. | Sub-temuan struktural elegan (keterlihatan ∝ 1/formalitas). Menghidupkan madya yang kini di-collapse. | Nihil–kecil | Filter + hitung | ~$0–sen | 🟡 OPSIONAL | Memperkaya |
| **E9** | **Verifikasi ≥20 referensi** (DOI/vol/hal nyata) + Word template JINITA. | Sisa TODO existing. Wajib apa pun venue. | Review | Lit-pass | ~$0 | 🟠 WAJIB (pre-submit) | Semua |

### 4.1 Paket minimum per target venue

- **Untuk JINITA / Sinta 2 (lantai aman, ~1–2 sesi):** E1 (minimal 2 validator) + E7 + E9. Paper v4 sudah 90% jalan; ini menutup satu-satunya blocker fatal (R1) dan merapikan referensi. **Bisa submit dalam 2–4 minggu weekend.**
- **Untuk Scopus Q3/Q4 (target realistis, ~3–5 sesi):** tambah E2 + E3 + E6 + reframe §3. Ini paket "diagnosis kuat".
- **Untuk Scopus Q1/Q2 atau WOAH/LREC (stretch, ~5–8 sesi):** tambah E5 (mitigasi) + E4 (skala). Arc problem→diagnosis→fix penuh.

---

## 5. Strategi venue

### 5.1 Realita bar rigor
Paper as-is (n=1, LLM-judge-only, sintetis-only) = **workshop/Sinta level**. Ini bukan penghinaan — banyak paper Sinta 2 lolos dengan ini. Tapi Bapak minta Scopus/Q. Gap-nya = §4 paket menengah/stretch.

### 5.2 Ladder venue (rekomendasi: satu paper, bidik setinggi yang didukung kerja)
Dengan budget waktu Bapak (5–15 jam/bulan), **jangan pecah jadi 2 paper.** Satu paper kuat, dibidik ke plafon tertinggi yang paket eksperimennya sanggup didukung, dengan fallback ke bawah bila reject.

| Tier | Contoh venue | Syarat (paket §4.1) | Catatan |
|---|---|---|---|
| Lantai | **JINITA** (Sinta 2, target existing) | Minimum | KUM 25, APC ~Rp1,5jt. Aman. |
| Target | **Scopus Q3/Q4 IES/IAES**: ETASR, IJECE, TELKOMNIKA, Bulletin of EEI, IJ-AI (IAES) | Menengah | Cepat, Scopus-indexed, ramah topik NLP terapan Indonesia. APC bervariasi. |
| Stretch | **WOAH** (Workshop on Online Abuse and Harms, ACL) atau **LREC-COLING** | Stretch (butuh E5) | WOAH = rumah alami untuk audit/red-team detektor hate. LREC = rumah untuk resource+benchmark bahasa low-resource. Keduanya Scopus/ACL-Anthology, sitasi tinggi. **Kalau E5+E6 jadi, bidik sini dulu, fallback ke Q3.** |

**Rekomendasi konkret:** bidik **WOAH atau LREC** bila E5 (mitigasi) berhasil; kalau tidak sempat, **Scopus Q3 IAES/ETASR** dengan paket menengah; **JINITA** sebagai jaring pengaman final. Cek deadline WOAH/LREC berikutnya di awal — timing bisa menentukan urutan.

### 5.3 Anti-pattern venue (jangan)
- ❌ Jangan submit paralel ke JINITA **dan** Scopus (double-submission = pelanggaran etik).
- ❌ Jangan kejar Q1 murni-NLP (ACL/EMNLP main) — bar empiris (skala, baseline SOTA) di luar jangkauan waktu Bapak. WOAH (workshop) jauh lebih realistis dan tetap bergengsi.

---

## 6. Isu validitas yang harus ditutup sebelum klaim apa pun (untuk executor)

Ini catatan teknis untuk Sonnet/Opus. Setiap klaim di paper harus lulus ini:

1. **Keaslian ≠ "dikenali-sebagai-hate".** E1 mengukur *apakah ini Jawa krama otentik*. Blind-spot butuh subset di mana native sepakat (a) otentik **dan** (b) *jelas hate bagi native kompeten*. Baru "miss" detektor = kegagalan sejati. Pisahkan dua judgment ini di form (jangan gabung jadi satu kolom "OTENTIK").
2. **Sirkularitas generator-detektor** harus diungkap **dan** dijinakkan: laporkan blind-spot pada detektor yang **bukan** generator (Grok, gemma3, gpt-oss sudah; tambah IndoBERT/Perspective via E2). Klaim utama hanya boleh bersandar pada detektor non-generator + data ber-anchor-real (E3).
3. **Prompt-dependence:** karena 5 LLM-judge pakai prompt v2 identik, mereka **tidak independen**. Jangan sebut "5 detektor independen". Sebut jujur: "5 model di bawah satu protokol prompting + 3 detektor arsitektur berbeda (E2)".
4. **Label artifact:** prompt v2 mendefinisikan hate = "serangan ke identitas kelompok, profanity≠hate". Krama-ironi tak punya slur permukaan → detektor yang *patuh* prompt bisa benar-menurut-prompt menilai non-hate. Diskusikan: apakah blind-spot = kegagalan model atau *ketaksesuaian taksonomi permukaan-vs-pragmatik*? Ini justru memperdalam paper bila dibahas, bukan disembunyikan.
5. **DVI angka:** `detection_rate` DVI (0,093%) dan rasio mentah (1.321/3,5jt ≈ 0,037%) beda karena metode hitung. Kutip hati-hati ("~0,09% terkonfirmasi Jawa di scrape multi-kota"), jangan overclaim presisi. Verifikasi definisi kolom di `dvi_scores.csv` sebelum menulis angka.
6. **Madya (E8):** kalau digarap, jangan klaim melebihi data. "Yield hate madya < ngoko, > krama" butuh sampel cukup per sel.

---

## 7. Etika & dual-use (bukan formalitas — ini bisa menentukan accept/reject)

Sebagai riset deteksi (defensif, setara defensive-security), ini sah dan sudah dijalankan bertanggung jawab (data publik anonim, teks ofensif gitignored, rencana lisensi terbatas). Tapi strategist wajib menegaskan:

1. **Framing = penentu.** "Generator hate uncollectable+undetectable" (v4) → red flag. "Diagnostic suite untuk mengaudit + memperbaiki detektor" (§3) → kontribusi defensif standar. **Ubah framing, bukan sekadar tambah paragraf etika.**
2. **Eksperimen mitigasi (E5) = bukti niat.** Paper yang berakhir di "detektor buta" ambigu secara etis; paper yang berakhir di "…dan begini cara menutupnya" tak terbantah defensif. Ini alasan strategis (bukan cuma moral) untuk memprioritaskan E5.
3. **Rilis bertanggung jawab:** diagnostic set + resep augmentasi di bawah *gated/restricted access* (norma HateCheck/HateHub: request-based, no-redistribution, research-only). **Jangan** rilis prompt generator paling evasif secara terbuka. Nyatakan ini eksplisit di §Ethics + Data Availability.
4. **Dual-use statement eksplisit** di paper: akui potensi penyalahgunaan, jelaskan mitigasi (gated release, fokus defensif, tak ada model generator yang dirilis — hanya stimulus terkurasi + detektor). Reviewer Scopus/ACL mencari ini.

---

## 8. Risiko & mitigasi (risk register)

| Risiko | Kemungkinan | Dampak | Mitigasi |
|---|---|---|---|
| Yekti/Daniel **bukan** penutur Jawa aktif → E1 macet | Sedang | Tinggi (R1 tetap terbuka) | Rekrut 2 kolega native akademik (bukan mahasiswa dibayar-per-label — pelajaran insiden v1-v4). Bounded 2 jam, comprehension-only. Lihat §9-Q1. **RESOLVED sebagian (D21, 2026-07-07):** risiko ini materialisasi separuh — Daniel ternyata bukan penutur asli (30th resident Jatim), Yekti tetap native. E1 TIDAK macet (form terisi, α terhitung), tapi α native-native (Mukhlis-Yekti) rendah (0.095) — R1 tetap terbuka meski dengan alasan berbeda dari yang diantisipasi di sini (bukan "gagal rekrut", tapi "native pun tak sepakat"). Lihat `experiments/generation_pilot/multivalidator_result.md`. |
| E5 augmentasi **tidak** menutup blind-spot (recall tetap rendah) | Sedang | Sedang | Itu tetap temuan jujur & publishable ("augmentasi permukaan tak cukup untuk implikatur → butuh pendekatan pragmatik") — malah memperdalam paper. Tak ada downside fatal. |
| Perspective API tak dukung register Jawa dengan baik → hasil noisy | Sedang | Rendah | Itu *bagian dari temuan* (tool komersial buta pada Jawa). Laporkan apa adanya. |
| Reframe menunda submission JINITA | Rendah | Rendah | Jalur ganda-aman: submit paket-minimum ke JINITA lebih dulu **bukan** opsi (double-submit). Sebaliknya: putuskan venue di awal (§9-Q3), lalu satu jalur. |
| Waktu Bapak habis sebelum paket stretch selesai | Tinggi | Sedang | Paket berjenjang (§4.1): tiap tingkat = paper submittable. Selesaikan lantai dulu, naik bila waktu ada. Tak ada kerja terbuang. |
| Scope creep (madya E8, regional E4) menyedot waktu | Sedang | Sedang | Tandai OPSIONAL. Jangan sentuh sebelum WAJIB (E1/E2/E9) tuntas. |

---

## 9. Keputusan untuk Bapak (hanya Bapak yang bisa jawab)

Executor **tidak boleh** menebak ini — angkat ke Bapak di sesi berikut:

- **Q1 — Validator native (E1):** Apakah Yekti/Daniel penutur Jawa aktif yang bisa menilai keaslian krama? Kalau tidak, apakah Bapak bersedia merekrut 2 kolega native akademik (bukan mahasiswa, comprehension-only ~2 jam)? *Ini membuka R1 yang fatal untuk Q-tier.* Catatan: ini rung-2 fallback ladder PRD (sanity check ~50 sampel), **bukan** pelanggaran zero-human — dan kategoris beda dari insiden mahasiswa nyontek (yang itu: labor bervolume, dibayar-per-label, tanpa stake; ini: rating komprehensi, peer akademik, ber-stake).
- **Q2 — Ambisi venue:** Scopus Q3 (realistis, paket menengah) atau stretch WOAH/LREC (butuh E5 mitigasi + GPU)? Ini menentukan berapa banyak §4 dikerjakan.
- **Q3 — Reframe:** Setuju putar dari "Generation" ke "Diagnostic/blind-spot + mitigasi" (§3)? Ini mengubah judul + urutan kontribusi paper v4.
- **Q4 — Mitigasi (E5):** Jalankan fine-tune IndoBERT (butuh ~beberapa jam GPU RTX 4080, gratis)? Ini pengunci framing defensif + pembuka WOAH.
- **Q5 — Aset twitter (E7):** Boleh integrasikan DVI `D:\documents\twitter` (proyek lain Bapak) ke paper ini sebagai anchor kelangkaan? (Cek: apakah ada rencana paper terpisah untuk DVI yang bisa bentrok/self-plagiarism.)
- **Q6 — §4.5 reframe (P0-3, ditambahkan 2026-07-07 sore, hasil audit ini sendiri). RESOLVED (2026-07-07, sama hari):** Bapak pilih opsi (c) — cek dulu apakah instrumen JELAS_HATE terlalu ketat, jangan langsung reframe dari angka mentah. Hasil cek (`analyze_disagreement.py` P0-3(d), keyword-coding CATATAN Yekti+Daniel per sel): dari 9 sel all-detector-evading, **5/9** (suku_tionghoa, agama_islam, agama_kristen, gender_lgbtq, suku_arab) genuinely "ironi samar/deniable/kebaca pujian tulus" menurut KEDUA validator — ini mendukung tesis blind-spot. **3/9** (semua target politik_kolektif) ditandai kedua validator sebagai "bukan hate identitas, cuma sinisme politik" — soal scope/construct-validity kategori target politik_kolektif, BUKAN soal buta-pragmatik. **1/9** (intra-jawa Arek vs Mataraman) ditandai "targete ora cetho" — soal target tak jelas dalam konstruksi stimulus. Jadi instrumen tidak "terlalu ketat" secara acak — ia menggabungkan 3 alasan berbeda jadi satu angka biner. Bapak setuju: §4.5 dipersempit ke 5/9 subset SARA yang genuinely ambiguous, 4 sel lain (politik+intra-jawa) jadi Limitation (6) baru soal construct-validity kategori target, bukan bagian klaim blind-spot utama. §4.5 dan §4.7 sudah ditulis ulang sesuai ini.

---

## 10. Handoff untuk executor (Sonnet/Opus) — urutan aksi konkret

Jangan mulai sebelum Bapak jawab §9 (khususnya Q1–Q3). Setelah itu, urutan by leverage:

1. **Baca** dokumen ini + `paper/draft_jinita.md` v4 + `FINDINGS.md`. **Jangan** ulang eksplorasi repo — inventaris lengkap ada di STATE + wiki.
2. **E7 (murah, kerjakan lebih dulu, tak butuh keputusan):** ekstrak angka DVI dari `D:\documents\twitter\datasets\dvi_scores.csv`, verifikasi definisi kolom, tulis paragraf anchor-kelangkaan-ke-2 + tabel komparatif lintas-bahasa untuk §1/§3.1. Ini menaikkan paper tanpa nunggu siapa pun.
3. **E1 (bila Bapak OK Q1):** bangun form validasi-keaslian **dua-kolom terpisah** ("otentik krama?" vs "jelas hate bagi native?"), sebar ke validator, skor inter-rater α. Reuse `score_validation.py`.
4. **E2 (bila target ≥Q, Q2):** setup IndoBERT hate publik + Perspective API + XLM-R toxicity, jalankan di 36 sel, tambahkan ke Table 3 sebagai kolom "detektor non-LLM-judge".
5. **E3:** minta Bapak kurasi 5–15 contoh krama-hate real, jalankan probe deteksi, tambahkan sebagai §"synthetic-real bridge".
6. **E6:** gabung ke E1 — native juga tandai hate/non-hate, hitung gap manusia-mesin.
7. **E5 (bila Q4 ya):** fine-tune IndoBERT (728) vs (728+generated), eval recall per-niche, tulis §Mitigasi.
8. **Reframe paper (bila Q3 ya):** judul → JavaneseHateCheck-style; restrukturisasi §3 (generation=metode), tambah §mitigasi + §baseline-manusia + §dual-use; **jangan tulis ulang** taksonomi/scarcity yang sudah bagus.
9. **E9:** lit-pass ≥20 ref (DOI nyata, jangan fabricate — Gen AI policy), Word template.
10. **Maintenance:** update PRD §0.1 (tambah D20 reframe bila Bapak setuju), `wiki/decisions.md`, `wiki/log.md`, STATE Challenges Log, HANDOFF next-action. Commit per milestone.

---

## 11. Satu halaman untuk Bapak (kalau cuma baca ini)

- **Temuan Bapak bagus** — register Jawa menyandi suhu benci, dan benci-ironis-krama lolos semua detektor. Itu layak jurnal bagus. **Jangan ragu soal nilai idenya.**
- **Yang belum siap = validasinya, bukan idenya.** Tiga lubang: cuma Bapak sendiri yang menilai keaslian (n=1), "detektor" baru LLM diberi-prompt (belum detektor nyata), dan datanya sintetis buatan DeepSeek sendiri. Ketiganya bisa ditutup tanpa membongkar temuan.
- **Ubah cerita paper:** dari *"kami bikin generator hate Jawa"* → *"kami temukan detektor buta pada hate halus-ironis Jawa, lalu kami perbaiki"*. Cerita kedua lebih kuat, lebih aman secara etika, dan tembus venue lebih tinggi. Kerjanya 70% sama, tinggal diputar.
- **Langkah pertama paling penting:** cari **2–3 penutur Jawa** (Yekti/Daniel atau kolega) untuk ikut menilai — 2 jam per orang, sekadar baca-dan-nilai, bukan anotasi. Ini membuka pintu ke Scopus. Ini beda total dari mahasiswa nyontek dulu (peer akademik, tanpa tekanan volume).
- **Target realistis:** Scopus Q3 (IAES/ETASR) kalau tambah detektor nyata + validator; **WOAH/LREC** (lebih bergengsi) kalau sempat eksperimen "augmentasi menutup blind-spot" di GPU lokal. **JINITA tetap jaring pengaman.**
- **Aset yang belum Bapak pakai:** data scraping `D:\documents\twitter` (3,5 juta tweet → 0,09% Jawa) adalah bukti kelangkaan terkuat yang Bapak punya, dan belum masuk paper. Murah dimasukkan, dampak besar.

---

## 12. Review Fable — sesi 10 (2026-07-07): audit hasil E1 + rencana perbaikan (eksekutor: Sonnet)

**Konteks yang direview:** E1 selesai (Yekti 91% / Mukhlis 55% / Daniel 45%; α M-Y 0.095, M-D 0.779, Y-D −0.039, 3-rater 0.336; Daniel dikoreksi bukan native), diagnosis disagreement (artefak instrumen 1-kolom + code-switching/lingkungan; harmonized α 0.095→0.519), edit paper §1 + §4.7 + refs [25][26].

**Verdict:** Kejujuran dan arah diagnosis BENAR dan berharga — jangan dibongkar. Tapi ada 1 error angka yang sudah masuk paper, angka-angka diagnosis belum memenuhi SOP dua-jalur proyek ini sendiri (D17/C9), dan ada analisis wajib yang belum dijalankan padahal datanya sudah ada — dengan potensi mengubah klaim §4.5. **Paper TIDAK BOLEH lanjut ke Word template sebelum P0 tuntas.** Commit/push justru harus segera (jangan tunggu P0).

> **Progress (Sonnet, 2026-07-07, same day):** P0-1 ✅ fixed (paper + STATE + HANDOFF + wiki/decisions + memory, all corrected to "19/39=49% of all disagreements, 19/27=70% of the niche itself"). P0-2 ✅ `experiments/generation_pilot/analyze_disagreement.py` written + run, second verification pathway (closed-form alpha) matched within rounding — see script docstring. P0-4 ✅ DeepSeek ranks #1 for all three validators, one sentence added to §4.1. P0-3 ✅ **RESOLVED (Q6 below).** Raw result: 0/9 of the all-detector-evading cells are rated JELAS_HATE=1 by either Yekti or Daniel. Bapak asked to check *why* before reframing (didn't accept the raw number at face value) — breakdown found 5/9 genuine irony/deniability (supports the thesis), 3/9 a *politik_kolektif* scope issue, 1/9 a target-clarity construction issue (see `disagreement_analysis.md` P0-3(d)). Bapak approved narrowing §4.5's claim to the 5/9 SARA-target subset + new Limitation (6) for the other 4 — both written.

### P0 — blocking (kerjakan berurutan, ~1 sesi Sonnet)

**P0-1. Fix bug denominator "70% (19/27)".**
19/27=70% adalah proporsi item krama-sarcastic yang jadi disagreement; proporsi disagreement yang krama-sarcastic = 19/39 = 49%. Kalimat paper §4.7(1) "70% (19/27) concentrate in the krama-sarcastic niche" salah dan menyebar ke: STATE.md C13, wiki/decisions.md D21 follow-up, HANDOFF.md blok sesi 10, memory `e1-irr-result-daniel-credential-2026-07-07`. Tulis presisi di semua tempat, mis.: "19 of the 27 krama-sarcastic items (70% of that niche) were disagreement rows; the niche accounts for 19/39 (49%) of all disagreements." **Selesai bila:** grep "19/27" dan "70%" di repo hanya muncul dengan frasa yang benar.

**P0-2. Reproducibility: `experiments/generation_pilot/analyze_disagreement.py`.**
Reproduksi SEMUA angka diagnosis yang sekarang dikutip paper dari sesi Bash ad-hoc: n disagreement per pasangan (39, 12), arah (39×(M=0,Y=1); Daniel 11×(1,0)+1×(0,1)), per-niche, count catatan "campur" (31 — dan VERIFIKASI klaim nesting "31 ⊆ 34 baris JELAS_HATE=0" yang sekarang tersirat di paper), JELAS_HATE distribusi (34/5), harmonized α (M-Y 0.519, M-D 0.448; tambah Y-D harmonized untuk kelengkapan), pola Daniel 9/12. Reuse `src/agreement.py`. Output → `disagreement_analysis.md` (committed). Lalu **jalur verifikasi kedua** per D17: recount independen dengan implementasi berbeda (bukan menjalankan ulang script yang sama). Angka di paper harus match output script; kalau ada selisih, paper ikut script, bukan sebaliknya.

**P0-3. Analisis JELAS_HATE × machine_caught (E6-lite — datanya SUDAH ADA, gratis).**
Ini analisis paling penting yang belum dilakukan: (a) rate JELAS_HATE per niche per validator (Yekti, Daniel); (b) khusus 36 sel DeepSeek yang diuji detektor: cross-tab JELAS_HATE vs machine_caught, dan khusus 9 sel yang lolos SEMUA 5 detektor — berapa yang manusia tandai jelas-hate?; (c) α Yekti-Daniel pada kolom JELAS_HATE (belum pernah dihitung; bisa jadi lebih tinggi ATAU lebih rendah dari OTENTIK — dua-duanya informatif). **Risiko/peluang:** kalau native juga tidak jelas membaca pasemon sebagai hate, klaim §4.5 "the hate that detectors miss is real Javanese hate" harus dinuansir. Framing jujur yang tersedia bila itu terjadi: *deniability pasemon membutakan manusia dan mesin — justru itu mekanisme sosialnya, konsisten dengan contoh #21 dan literatur sarcasm-detection [23]*. **Jangan tulis narasi sebelum angka keluar; kalau hasilnya tipe yang melemahkan, gate ke Bapak (AskUserQuestion) sebelum rewrite §4.5.**

**P0-4. Tabel authenticity per-model × per-validator.**
Apakah "DeepSeek 97%" (Table 2) bertahan menurut Yekti dan Daniel? Hitung 3×3 (model × validator). Kalau DeepSeek ranking-1 di ketiganya → tambah 1 kalimat robustness di §4.1 (klaim headline selamat dari multi-rater scrutiny — gratis dan kuat). Kalau tidak → abstract/§4.1/§5 wajib di-soften. Saat ini abstract & §5 masih menyebut 97%/55% tanpa kualifikasi apa pun.

### P1 — struktur & kebersihan (~1 sesi Sonnet)

**P1-5. Restrukturisasi: diagnosis keluar dari Limitations.**
Limitation (1) sekarang ~700 kata — hasil empiris riil terkubur di section disclaimer, limitasi lain jadi tampak kerdil, reviewer membaca sebagai defensive burying. Pindahkan hasil multi-validator + diagnosis ke subsection Results baru (mis. "§4.6 Multi-validator authenticity: instrument and sociolinguistic effects", renumber §4.6–4.8 lama) dengan 1 tabel kecil (rate per validator; α pairwise mentah + harmonized). Limitation (1) susut ke 4–6 kalimat yang merujuk ke subsection itu. Sekalian: §3.3 (metode) tambah deskripsi pass ke-2/3 (blind, instrumen 2-kolom, kredensial Daniel akurat); abstract +1 kalimat range multi-rater — **awas limit 250 kata (sekarang 247), harus trim di tempat lain**; tambah 1 kalimat alternatif "rater leniency" untuk Yekti + kenapa catatan diskriminatifnya (JELAS_HATE cuma 51/108, notes niche-spesifik) menunjukkan threshold genuine, bukan rubber-stamp — preempt reviewer.

**P1-6. Fix overclaim kecil:** "its own **documented** Javanese sociolect" (Chindo, §4.7) — sumbernya anekdot Bapak, bukan literatur. Ganti "reported"/"anecdotally reported". Proyek ini zero-tolerance fabrikasi; kata "documented" tanpa sitasi = pelanggaran kecil tapi tipikal yang dicari reviewer.

**P1-7. Commit + push SEKARANG (jangan tunggu P0).**
Kerja sesi 9 (reframe v5, STRATEGY.md, E7, E1-instrumen, lit-pass) + sesi 10 (hasil E1, D21, diagnosis) SEMUANYA belum di-commit — pelanggaran HARD RULE #6 yang sedang berjalan (ingat insiden petir 2026-04-29). Sebelum commit: **cek .gitignore untuk `VALIDATION_FORM*_FILLED.xlsx`** — kolom TEKS berisi teks ofensif sintetis; policy existing = teks sintetis TIDAK di-push publik. Kalau form kena ignore, pertimbangkan commit agregat skor tanpa TEKS (mis. CSV kolom no/niche/OTENTIK/JELAS_HATE/MASALAH) supaya `analyze_disagreement.py` reproducible dari repo. Konsistenkan dengan policy `expert_spotcheck`.

### P2 — opsional / pending keputusan Bapak

**P2-8. (Butuh Bapak ~30 menit, opsional tapi menguatkan.)** Harmonized-α saat ini berdiri di atas ASUMSI bahwa kolom tunggal Mukhlis = konjungsi (otentik AND jelas-hate). Cara mengubah asumsi jadi pengukuran: Mukhlis re-jawab HANYA 39 baris disagreement dengan instrumen 2-kolom. Non-blind (Bapak sudah lihat hasil) — jujur dilaporkan sebagai *post-hoc decomposition of the original conflated judgment*, bukan IRR baru. Kalau hasilnya cocok dengan transformasi AND → klaim artefak instrumen jadi terukur, bukan konjektur. **Keputusan Bapak: mau atau tidak.**

**P2-9. Pra-submission (saat pindah Word template):** renumber referensi ke urutan sitasi IEEE murni (termasuk [25][26] yang sekarang di-append di akhir), + cek manual halaman ref [4] (WCSE 2021).

### JANGAN (guard rails untuk eksekutor)

- ❌ Jangan minta Yekti/Daniel re-rate atau "klarifikasi" jawaban mereka — kontaminasi + biaya waktu; data mereka final.
- ❌ Jangan tambah eksperimen baru di luar daftar ini (venue tetap JINITA, scope terkunci D20/D21).
- ❌ Jangan tulis narasi §4.5 baru sebelum P0-3 selesai dihitung dan (bila melemahkan) di-gate ke Bapak.
- ❌ Jangan hapus/haluskan angka α rendah di manapun — 0.095 tetap dilaporkan; diagnosis adalah *penjelasan*, bukan pengganti.

**Estimasi:** P0 ≈ 1 sesi Sonnet (murni komputasi + edit terarah), P1 ≈ 1 sesi, P2-8 ≈ 30 menit Bapak + 30 menit skor.

---

*Ditulis sekali oleh Fable 5 sebagai strategist. Eksekusi → Sonnet/Opus. Semua keputusan arah → Bapak (§9). Dokumen ini bukan pengganti PRD (source of truth) — ini rekomendasi; bila Bapak setujui, executor melebur poin relevannya ke PRD/wiki via D20.*
