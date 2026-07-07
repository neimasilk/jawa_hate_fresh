# Codebook Taksonomi Ujaran Kebencian Bahasa Jawa

**Versi:** 1.0a (2026-06-23, dikoreksi pasca audit adversarial — lihat §9 Changelog)
**Penyusun:** Mukhlis Amien, Yekti Asmoro Kanthi, Daniel Rudiaman Sijabat (Universitas Bhinneka Nusantara)
**Status:** Supplementary untuk paper JINITA + deliverable HKI (Karya Tulis/Spesifikasi)
**Lisensi:** CC BY-NC-SA 4.0
**Dataset rujukan:** `bulk_v2_consensus.jsonl` (728 teks, 158 hate / 570 non-hate)
**Pelabelan:** Fully-automated 3-rater LLM consensus (DeepSeek V4 Pro + Grok 4.3 + qwen3:14b lokal), prompt `cultural_classification_v2`, zero anotasi manual.

---

## 0. Cara membaca codebook ini

Codebook ini adalah **manual operasional** untuk mengklasifikasikan teks Bahasa Jawa (termasuk *code-mixed* Jawa–Indonesia–Inggris–Arab) ke dalam taksonomi ujaran kebencian 4-dimensi. Dokumen ini dipakai dua hal:

1. **Spesifikasi anotasi** — definisi, aturan keputusan, dan contoh batas (*boundary cases*) yang dipakai untuk mengarahkan rater (di sini: rater LLM via prompt). Setiap aturan di sini punya padanan eksplisit di prompt produksi `prompts/cultural_classification_v2.md`.
2. **Dokumentasi dataset** — penjelasan label untuk pengguna dataset yang dirilis (Hugging Face/Zenodo).

**Prinsip inti yang harus dipegang sebelum apa pun:** penentu ujaran kebencian adalah **ARAH serangan ke identitas kelompok**, BUKAN tingkat kekasaran bahasa. Bahasa Jawa kaya umpatan (*pisuhan*: `asu`, `jancuk`, `cuk`, `tae`, `bangsat`) yang dalam register Arek/Suroboyoan justru penanda keakraban. Kekasaran ≠ kebencian. Ini sumber kesalahan paling umum dan menjadi fokus utama codebook (§2, §6).

---

## 1. Ruang lingkup

| Aspek | Keputusan | Rujukan |
|---|---|---|
| Bahasa sumber | Jawa + turunan (Mataraman, Arek, Banyumasan, dll). *Code-mixed* dengan Indonesia/Inggris/Arab **diterima** karena merupakan realita sosmed Jawa. | D5, D13 |
| Bahasa lain sebagai sumber | Sunda, Madura, Melayu **bukan** sumber. Tetapi Sunda/Madura/Tionghoa/dll tetap bisa menjadi **target** ujaran. | D5 |
| Unit analisis | Satu posting/komentar (teks pendek sosmed), sudah dianonimisasi (username, mention, URL dihapus/diganti placeholder). | Etika §7 PRD |
| Platform sumber | Dump publik berbahasa Indonesia (`haipradana`) difilter LLM untuk subset Jawa/code-mixed. Bukan *live scraping*. | D6, D13 |

**Catatan empiris penting (jujur):** Jawa **leksikal-murni** (ngoko/krama tanpa campuran sama sekali) nyaris nol di sosmed (1/250 pada Pilot #2). Ujaran kebencian Jawa real **didominasi code-mixed**. (Catatan: field `filter_bahasa="jawa"` ~10% di dataset berarti "Jawa-dominan", bukan murni leksikal — tidak kontradiksi dengan 1/250.) Codebook ini sengaja **tidak** memaksakan kemurnian leksikal. **Peringatan kejujuran (temuan audit):** ~90% record + 95% record hate ber-`filter_bahasa="campuran"`, dan banyak di antaranya didominasi Indonesia dengan sedikit penanda Jawa → framing paling akurat = **"Indonesia code-mixed dengan Jawa"**, bukan "Jawa murni". Kuantifikasi densitas Jawa dengan langid proper sebelum klaim angka di paper.

---

## 2. Definisi inti: apa itu ujaran kebencian (hate)

> **Hate = teks yang menyerang, merendahkan, mendehumanisasi, atau menghasut kekerasan/diskriminasi terhadap seseorang atau kelompok BERDASARKAN identitas kelompoknya:** suku/etnis, ras/keturunan, agama/kepercayaan, gender/orientasi seksual, kelas sosial, atau kelompok politik sebagai kolektif.

### 2.1 BUKAN hate (label `hate:false`, severity `BUK`) — meskipun sangat kasar

1. **Umpatan/profanity** (`jancuk`, `asu`, `tae`, `cuk`, `bangsat`, `goblok`) sebagai ekspresi emosi, keakraban antar teman (*banter*), atau hinaan personal **tanpa dimensi identitas kelompok**.
2. **Kritik pedas/kasar** terhadap tokoh publik/pejabat/institusi atas **kinerja/tindakan/kebijakan**-nya. Menjadi hate hanya kalau menyerang identitas kelompok (suku/agama/gender/dll) tokoh tersebut.
3. **Keluhan/makian** terhadap situasi, benda, atau diri sendiri.

Contoh nyata `BUK` dari dataset (semua kasar, tak satu pun hate):
- `"Weh gimana ini, bisa gawat citranya ASU...."` — umpatan ekspresif, tanpa target kelompok.
- `"Nganjing2in seneng. Dianjingin marah. Tolol."` — komentar perilaku, bukan identitas.
- `"ngakakakakaka bete banget asu"` — penanda emosi/keakraban.
- `"Bukannya teraweh malah nyebar spoiler anjir anjir jancuk lah"` — makian situasi.

### 2.2 Serangan ke INDIVIDU juga bisa hate

Hinaan ke satu orang **dihitung hate** kalau memakai **slur/stereotip identitas kelompok** — individu diserang KARENA keanggotaan kelompoknya:

- Perempuan diserang slur gender (`lonte`, `murahan`, `rahim anget`) → hate `gender_wanita`.
- Individu disebut `kapir/kafir`, `bani micin`, diserang karena agamanya → hate `agama_*`.
- *Mock-collective* (`kaum rahim anget`, `LaGiBeTe`, `bani onta`) untuk kelompok identitas → hate kelompok tsb.

**Pembeda kunci:** umpatan generik (`asu`, `jancuk`, `goblok`) tidak menyinggung identitas; slur identitas (`lonte`, `kapir`, `banci`, `maho`) merendahkan lewat **keanggotaan kelompok**.

### 2.3 Tes cepat (decision rule utama)

> **"Apakah teks ini merendahkan KELOMPOK identitas, atau seseorang KARENA identitas kelompoknya?"**
> Jika **tidak** → `hate:false`, severity `BUK`, target `tidak_ada`.

```
                  ┌─────────────────────────────────────────┐
   Teks masuk ──► │ Ada serangan/rendahan/hasutan?           │── tidak ──► BUK
                  └───────────────┬─────────────────────────┘
                                  │ ya
                                  ▼
                  ┌─────────────────────────────────────────┐
                  │ Sasarannya identitas KELOMPOK            │── tidak ──► BUK
                  │ (atau individu KARENA identitas kel.)?   │  (umpatan/kritik kinerja)
                  └───────────────┬─────────────────────────┘
                                  │ ya
                                  ▼
                              hate:true ──► tentukan 4 dimensi (§3)
```

---

## 3. Empat dimensi taksonomi

Setiap teks `hate:true` dilabeli pada 4 dimensi. Teks `hate:false` selalu: `target_group=["tidak_ada"]`, `severity="BUK"` (register & form tetap dapat dicatat).

### Dimensi 1 — TARGET GROUP (siapa yang diserang)

Array string (boleh multi-target). Kategori:

| Klaster | Kategori |
|---|---|
| Suku/etnis | `suku_madura`, `suku_tionghoa`, `suku_sunda`, `suku_batak`, `suku_dayak`, `suku_papua`, `suku_arab`, `suku_rohingya`, `suku_jepang` |
| Intra-Jawa | `intra_jawa_mataraman`, `intra_jawa_arek`, `intra_jawa_banyumasan` |
| Agama/kepercayaan | `agama_islam`, `agama_kristen`, `agama_katolik`, `agama_hindu`, `agama_buddha`, `agama_konghucu`, `agama_kepercayaan` |
| Kelas/region | `kelas_kutha_ndeso`, `kelas_priyayi_cilik` |
| Gender/seksualitas | `gender_wanita`, `gender_lgbtq` |
| Politik | `politik_tokoh`, `politik_partai`, `politik_ormas` |
| (bukan hate) | `tidak_ada` |

**Contoh nyata per kategori (dari dataset, sudah dianonimisasi):**

| Kategori | Contoh teks | Catatan |
|---|---|---|
| `suku_tionghoa` | `"Usir aja nih cina satu. ... cina udh numpang di negeri ini"` | Eksklusi etnis + "numpang" |
| `suku_tionghoa` | `"maaf sipit mtmu ku skip"` | Slur fisik (`sipit`) |
| `gender_wanita` | `"rahim anget"` / `"penyebab rahim anget"` | *Mock-collective* fandom, slur gender |
| `gender_lgbtq` | `"Dasar ckck maho"`, `"kaya banci kali ya"` | Slur orientasi (`maho`, `banci`) |
| `suku_arab` | `"para bani Onta"`, `"Bani pinggiran koreng"` | *Mock-collective* etnis Arab |
| `agama_islam` | `"Lagu2an Banserep Pekok"`, `"ukhti2 otaknya di dengkul"` | Hinaan ke kelompok keislaman |
| `agama_kristen` | `"wes lemu, ireng, kafir sisan asu"` | Slur agama (`kafir`) ke individu |
| `politik_partai` | `"Hajar ndan.. ganyang PKI"` | Hasutan + slur politik (`PKI`) |
| `politik_tokoh` | `"Cebong dongo"` | Slur politik (`cebong`) |
| `agama_kepercayaan` | `"Liat aja kelakuan nya masih barbar ... nyajen ... ngasepin kuburan"` | Dehumanisasi praktik kepercayaan |

> **Catatan distribusi (lihat §5):** target paling sering = `gender_wanita` (49), lalu politik (`partai` 20 + `tokoh` 17 + `ormas` 9), `gender_lgbtq` (19), `suku_tionghoa` (15), `agama_islam` (15). Suku Madura/Sunda/Batak/Dayak/Papua hampir tak muncul di dump ini — **bias sumber** (lihat §8 Limitasi).

### Dimensi 2 — SEVERITY (tingkat keparahan)

| Nilai | Definisi | Contoh |
|---|---|---|
| `BUK` | Bukan ujaran kebencian (wajib jika `hate:false`) | umpatan non-kelompok, kritik kinerja |
| `ringan` | *Stereotyping*, slur ringan terhadap kelompok | `"maaf sipit mtmu ku skip"` |
| `sedang` | Dehumanisasi, generalisasi negatif kuat, eksklusi kelompok | `"CINA ASU"`, `"Usir aja nih cina"` |
| `berat` | Ancaman, hasutan kekerasan | `"Hajar ndan.. ganyang PKI"`, `"Dimampusin aja"` |

**ATURAN KONSISTENSI:** `ringan/sedang/berat` hanya valid jika `hate:true`. Jika `hate:false` → severity WAJIB `BUK`.

> **Peringatan reliabilitas (penting):** severity adalah dimensi **paling bising**. Antar-rater hanya sepakat severity pada **89/158** baris hate. **Label inti dataset = binary `hate`**; gunakan severity sebagai sinyal kasar (ordinal), bukan ground-truth presisi. Lihat §7.

### Dimensi 3 — REGISTER (tingkat tutur)

| Nilai | Karakter |
|---|---|
| `ngoko` | Informal, lugas, mungkin vulgar |
| `madya` | Semi-formal, campuran |
| `krama` | Formal-halus — bisa *polite-violent* (halus tapi isinya mengeksklusi) |
| `campur_kasar` | Mencampur level untuk menghina (mis. pronomina ngoko + verba krama-inggil ke lawan tutur) |

**Konsep novelty — *polite-violent krama*:** ujaran kebencian yang dibungkus krama halus. Contoh teoretis (dari few-shot prompt):
> `"Mugi-mugi tiyang Tionghoa enggal sami wangsul dhateng negarinipun piyambak, supados kitha niki resik."` — krama sopan, tapi isinya mengusir etnis Tionghoa. Kehalusan tidak menghapus hate.

> **TEMUAN EMPIRIS JUJUR (materi paper):** dalam dataset sosmed ini, register hate **157/158 = ngoko**; krama-hate murni **nol**, `campur_kasar` hanya 1. *Polite-violent krama* adalah fenomena linguistik **nyata** tetapi **langka di sosmed** — ia carrier hate antar-priyayi/formal, bukan di kolom komentar. Maka kontribusi dimensi register **bukan** "krama-hate sering", melainkan: (a) taksonomi yang **register-aware** mampu menangkapnya bila muncul, dan (b) konfirmasi empiris bahwa hate sosmed Jawa = **ngoko + code-mixing**, bukan krama. Klaim ini didokumentasikan apa adanya, tidak di-*oversell*.

### Dimensi 4 — FORM (bentuk penyampaian)

| Nilai | Definisi | Contoh dataset |
|---|---|---|
| `direct` | Eksplisit (141, majority-of-3) | `"CINA ASU"` |
| `sarcastic` | Sindiran (4) | `"Nang grejo 20 taun raiku gk onok kris10 e blas wkwkwk"` |
| `idiomatic_pasemon` | Kiasan budaya Jawa (1) | `"Tedake maling, yo maling. Ora bakal owah."` (determinisme keturunan) |
| `code_switched` | Campur Indo/Inggris/Arab (4) | `"Kiro2 akad nggowo outfit ngene ... ketok kyok kris10"` |

> Catatan: `direct` mendominasi. `code_switched` sebagai *form* under-counted karena hampir semua teks sudah code-mixed di level leksikal; rater menandai `code_switched` hanya saat percampuran menonjol secara struktural.

---

## 4. Prosedur pelabelan (ringkas, untuk reproduktibilitas)

1. Baca teks utuh (termasuk emoji/tertawa `wkwk` yang sering menandakan *banter* → indikasi `BUK`).
2. Terapkan **tes cepat §2.3**. Jika lolos sebagai non-hate → `hate:false`, `tidak_ada`, `BUK`. Selesai.
3. Jika hate → tentukan `target_group` (boleh multi), `severity`, `register`, `form`.
4. Tulis `reasoning` 1–2 kalimat yang menyebut **mekanisme** (slur identitas? eksklusi? hasutan? dehumanisasi?).
5. Output JSON valid; tambahkan `refusal:true` hanya jika menolak menganalisis (bukan klasifikasi BUK).

Format output per teks:
```json
{"hate": true, "target_group": ["gender_wanita"], "severity": "sedang",
 "register": "ngoko", "form": "direct",
 "reasoning": "Slur gender ke individu + generalisasi ke semua perempuan."}
```

---

## 5. Distribusi empiris dataset rilis (728 teks)

| Ukuran | Nilai |
|---|---|
| Total teks consensus | 728 |
| hate / non-hate | 158 (21.7%) / 570 |
| Unanimous (3 rater sepakat) | 569 |
| Ties (1-1, masuk file disagreement) | 7 |
| Rater | DeepSeek (708 vote) + Grok (727) + qwen3:14b (726) |

> **Aturan hitung (penting untuk reproduksi):** angka di bawah = **majority-of-3** — sebuah kategori dihitung untuk satu teks hate jika muncul di **≥2 vote valid** teks itu (prinsip sama dengan label biner), diregenerasi oleh `audit.py`. Draf awal memakai penjumlahan vote per-vendor (mis. gender_lgbtq "55") yang menggelembungkan angka — **angka majority di sini menggantikannya.**

**Target group (hate, majority-of-3):** `gender_wanita` 46 · `politik_partai` 19 · `gender_lgbtq` 18 · `suku_tionghoa` 14 · `agama_islam` 8 · `politik_tokoh` 8 · `politik_ormas` 7 · `agama_kristen` 7 · `suku_arab` 3 · `agama_kepercayaan` 3 · sisanya (`suku_rohingya`, `suku_jepang`, `intra_jawa_arek`, `agama_hindu`) = 1.
> **Sparsity:** ≥9 kategori taksonomi punya 0 instance; 4 kategori ber-instance ≤2 → **analisis per-kategori tak bisa** untuk kategori ini (bias sumber tunggal, lihat §8).

**Register (hate):** `ngoko` 157 · `campur_kasar` 1 · krama 0 (157/158 ngoko).
**Form (hate, majority-of-3):** `direct` 141 · `code_switched` 4 · `sarcastic` 4 · `idiomatic_pasemon` 1 · (8 tanpa mayoritas).
**Severity (hate):** `sedang` (terbanyak) · `ringan` · `berat` (sedikit). Severity-agree hanya **89/158** (56%); 69/158 tanpa severity unanimous → **field severity diberi penanda low-reliability**, label inti tetap biner.

---

## 6. Boundary cases & adjudikasi (kasus paling sulit)

Kasus berikut dari `bulk_v2_disagreement.jsonl` (7 "ties"). **Koreksi penting (audit 2026-06-23):** ke-7 ini ties hanya karena **DeepSeek dropout** (vote null) sehingga voting tinggal 2 rater yang pecah 1-1 — **bukan** kasus 3-arah terkontes. Jadi treat sebagai *ilustrasi batas Grok-vs-qwen3*, bukan "kasus tersulit dataset". Untuk analisis boundary yang sebenarnya, sampel dari **159 split mayoritas 2-1** di dalam file consensus (di mana label diputuskan tipis). Pola di 7 ties ini: Grok melabeli slur identitas sebagai hate; qwen3 membacanya sebagai umpatan generik/faktual.

| # | Teks (ringkas) | Grok | qwen3 | Adjudikasi codebook |
|---|---|---|---|---|
| B1 | `"...ke kafir... Jakarta keren ... yg skrng kerja nda becus"` | hate `agama_kristen` (`kafir`) | BUK (kritik kinerja) | **Ambigu.** `kafir` di sini menyebut pengganti pejabat, bercampur kritik kinerja. **Default: hate ringan** bila slur agama (`kafir`) dipakai sebagai label merendahkan, sesuai §2.2 — *meski* dibungkus kritik kinerja. |
| B2 | `"...wkwkw maho dong gua"` | hate `gender_lgbtq` (`maho`) | BUK (bercanda) | **Borderline.** Slur (`maho`) dipakai bercanda ke diri sendiri/teman. Aturan: slur identitas **tetap** hate ringan walau nada *banter* — normalisasi slur = bahaya. **Default: hate ringan.** (Catatan: ini titik di mana rater paling sering pecah.) |
| B3 | `"Sastra e karl mark. PENTOLAN komunis rusia."` | hate `politik_tokoh` | BUK (faktual) | **BUK.** Pernyataan deskriptif tentang tokoh; tak ada serangan/rendahan. qwen3 benar. Label "komunis" deskriptif ≠ hate kecuali dipakai untuk merendahkan kolektif. |
| B4 | `"...Badjingan lu akun2 homok yg nyerang dia ... anjing akun gede"` | hate `gender_lgbtq` (`homok`) | BUK (umpatan ke individu) | **Hate ringan.** `homok` = slur orientasi diarahkan ke kelompok ("akun2 homok"). §2.2 berlaku. Grok benar. |
| B5 | `"Yg voting malingsia siapa cok jancok PKI"` | hate `politik_partai` (`PKI`) | BUK (umpatan) | **Hate ringan.** `PKI` sebagai slur politik kolektif. Tapi `jancok` di sini umpatan generik → bukan penentu. Grok benar pada dimensi PKI. |
| B6 | `"Cowo suka nganggep cewek murahan ... apa beda nya dengan cowok..."` | BUK (kritik *double standard*) | hate `gender_wanita` (`murahan`) | **BUK (cenderung).** Teks justru **mengkritik** pelabelan "murahan", bukan melontarkannya. `murahan` dikutip, bukan diafirmasi → konteks meta. Grok benar. **Lesson: deteksi *kutipan/kritik-atas-slur* vs *pemakaian-slur* adalah batas tersulit.** |
| B7 | `"...sobat menyan ... masih barbar ... Bubarin pengajian nyajen ... we are different breed"` | hate `agama_kepercayaan` | BUK (kritik umum) | **Hate sedang.** Dehumanisasi (`barbar`, `terbelakang`, `different breed`) + hasutan bubarkan praktik kepercayaan (`nyajen`, `ngasepin kuburan`). Grok benar. |

**Lesson metodologis lintas-kasus (materi paper §Discussion):**
1. **Slur identitas dalam nada bercanda** (B2) = titik pecah utama rater. Keputusan codebook: *banter* tidak menghapus status slur identitas (default hate ringan), demi tidak menormalisasi slur.
2. **Use vs mention** (B6): teks yang **mengutip/mengkritik** slur ≠ teks yang **memakai** slur. Batas tersulit; rater LLM belum andal membedakannya.
3. **Slur + kritik kinerja tercampur** (B1): kehadiran kritik kebijakan tidak otomatis menetralkan slur identitas.

---

## 7. Catatan protokol pelabelan (zero-human)

- Label dihasilkan **tanpa anotasi manusia** — 3 rater LLM (DeepSeek + Grok cloud, qwen3:14b lokal/gratis), label final = *majority vote*. (Catatan: rater TIDAK sepenuhnya independen — mereka berbagi data pretraining, dan Grok over-label sementara qwen3 under-label; lihat audit §4.4 paper.)
- Validasi reliabilitas memakai **Krippendorff's α** (bentuk kanonik *coincidence-matrix*). Karena label rilis = **3-rater majority**, reliabilitas yang berlaku untuk dataset = **α 3-rater 0.513 held-out / 0.545 full** ("moderat"). Pasangan dua-model-cloud DeepSeek+Grok lebih tinggi (**α 0.688** held-out, raw agreement 0.886, Gwet AC1 0.820) tetapi hanya subset dari aturan label → dilaporkan sebagai batas atas, **bukan** angka headline. qwen3 = rater ke-3 paling bising (α pasangan 0.40) tapi gratis/reproducible.
- **PENTING (validitas ≠ reliabilitas):** α hanya mengukur kesepakatan antar-LLM, bukan kebenaran. Vs label manusia sumber, konsensus hanya setuju 54.5% (κ 0.19) karena taksonomi ini sengaja **mempersempit** hate ke group-directed (buang profanity). Klaim validitas perlu **spot-check pakar ~100 item** (belum dilakukan).
- **Severity** noisier daripada `hate` biner → label inti = biner. Angka diregenerasi reproducible oleh `experiments/audit_external/audit.py`. Verifikasi adversarial menemukan 2 bug (diperbaiki) + audit lanjutan (2026-06-23) menemukan over-claim yang sudah dikoreksi di paper v3.

---

## 8. Limitasi & catatan kultural (transparansi)

1. **Validitas belum teruji (limitasi utama).** Semua angka = reliabilitas antar-LLM, BUKAN kebenaran. Vs label manusia sumber: setuju 54.5%, κ 0.19; konsensus membuang 307/441 (70%) hate-manusia. Sebagian besar = **penyempitan definisi yang disengaja** (profanity non-grup → BUK) dan **24 flip neutral→hate = slur Jawa benar yang dilewatkan anotator** (`sipit/aseng`, `banci/jablay`, `kafir`). Tapi tetap perlu **spot-check pakar ~100 item** untuk klaim validitas.
2. **Bias sumber.** Dump tunggal (`haipradana`) → target condong ke **gender + politik + Tionghoa/Islam**; Madura/Sunda/Batak/Dayak/Papua & register krama **kosong/under-represented**. ≥9 kategori 0 instance, 4 kategori ≤2. Penambahan sumber = *future work*.
3. **Celah taksonomi (temuan audit).** Hinaan **warna kulit/fisik** tak punya kategori target → mis. `"bacot lo ireng jomok"` (orig=hate) di-skip jadi BUK. **v1.1 perlu kategori `fisik_warnakulit`/physical-trait.**
4. **Near-duplicate + leakage.** 706/735 teks unik (149/158 hate unik); 5 teks held-out duplikat pool iterasi (~1% leakage) → dihapus sebelum hitung held-out. Pakai N-unik-hate ≈149 untuk klaim yang bergantung ukuran.
5. **Register krama langka** di sosmed (§3 Dim-3) — dimensi register = *capability*, bukan demonstrasi.
6. **Use-vs-mention** (B6) belum tertangani — slur yang dikutip/dikritik bisa salah-label hate.
7. **Token off-taksonomi.** Vote mentah memuat `kaum_rhaim_anget` (1), `intra_jawa` (terpotong), `suku_jepang`/`suku_rohingya` (di luar daftar prompt walau grup nyata) → pipeline perlu langkah validasi token ke daftar kanonik.
8. **Kepercayaan vs antisemitisme** (`"Zionis"` → `agama_kepercayaan`) — kategori politik-agama global belum rapi; sub-kategori di v1.1.

---

## 9. Changelog

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 2026-06-23 | Codebook formal pertama. Diturunkan dari prompt produksi `cultural_classification_v2` (pemenang Pilot #3, α ds+grok 0.763 di pool tuning) + profil empiris dataset 728 (Pilot #6b) + 7 boundary cases. |
| 1.0a | 2026-06-23 | Koreksi pasca audit adversarial: angka target/form ke aturan majority-of-3 reproducible (`audit.py`); reliabilitas jujur (3-rater 0.513 label / ds+grok 0.688 batas atas, buang klaim "generalizes"); reframe 7 ties (artefak DeepSeek-null); tambah validitas eksternal vs `orig_label` (54.5%, κ 0.19) + celah taksonomi skin-color + dedup/leakage + sparsity. |

**TODO v1.1:** kategori target `fisik_warnakulit`; sub-kategori politik-agama global (Zionis dll); langkah validasi token off-taksonomi; spot-check pakar ~100 item.

**Provenance prompt → codebook:** definisi §2 = blok DEFINISI prompt v2; aturan §2.2 = blok "slur identitas ke individu = hate" (ditambahkan v1→v2, menaikkan α ds+grok **+0.23**: 0.534→0.763); contoh few-shot 1–10 prompt = sumber contoh kanonik (contoh krama §3 Dim-3 adalah few-shot **konstruksi**, bukan dari data). Setiap aturan codebook punya jejak ke keputusan pilot (lihat `wiki/decisions.md`, `wiki/pilots.md`).
