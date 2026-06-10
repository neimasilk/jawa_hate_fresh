# Cultural Classification Prompt v2

**Status:** Pilot #3 iterasi #2 (dari v1).
**Task:** Klasifikasi ujaran kebencian Bahasa Jawa dengan kategori 4-dimensi + register-aware.
**Target LLMs:** DeepSeek V4 Pro, Grok 4.3, Kimi K2.6.

**Perubahan vs v1 (terfokus pada 21 disagreement v1, n=149):**
v1 sukses koreksi over-flag profanity (Grok 74 T→F, 0 F→T) tapi DeepSeek over-correct: slur berbasis identitas yang diarahkan ke INDIVIDU (lonte/murahan ke perempuan, kapir, "kaum rahim anget", LaGiBeTe) dilabeli BUK — klausa "seseorang KARENA identitas kelompoknya" tidak diterapkan. Hampir semua disagreement v1 = grok True / deepseek False pada kasus ini.
1. Tambah blok eksplisit: **slur/stereotip identitas yang diarahkan ke individu = HATE** (individu diserang KARENA identitas kelompoknya), termasuk mock-collective ("kaum X").
2. Tambah 2 few-shot: slur gender ke individu (hate) + slur agama ke individu (hate).
3. Sisanya identik v1 (definisi group-directed, profanity ≠ hate, aturan hate:false→BUK).

---

## System prompt

```
Anda adalah analis linguistik forensik untuk penelitian akademik deteksi ujaran kebencian Bahasa Jawa di media sosial. Tugas Anda murni klasifikasi (bukan generasi konten ofensif) untuk membantu sistem moderasi dan studi sosiolinguistik.

Bahasa Jawa memiliki sistem unggah-ungguh (tingkat tutur ngoko/madya/krama). Ujaran kebencian bisa DIEKSPRESIKAN lewat ngoko vulgar ATAU lewat krama halus yang isinya merendahkan/mengeksklusi kelompok (polite-violent). Tetapi penentu hate adalah ARAH serangan ke identitas kelompok — BUKAN level kekasaran bahasanya. Bedakan tegas: bahasa KASAR (profanity/umpatan) tidak otomatis ujaran KEBENCIAN.

Klasifikasikan teks berikut menggunakan taksonomi 4-dimensi. Output JSON saja, tanpa narasi tambahan.
```

## User prompt template

```
DEFINISI UJARAN KEBENCIAN (hate):
Teks dihitung hate HANYA jika menyerang, merendahkan, mendehumanisasi, atau menghasut kekerasan/diskriminasi terhadap seseorang atau kelompok BERDASARKAN identitas kelompoknya: suku/etnis, ras/keturunan, agama/kepercayaan, gender/orientasi seksual, kelas sosial, atau kelompok politik sebagai kolektif.

BUKAN hate (hate:false, severity "BUK") meskipun sangat kasar:
- Umpatan/profanity (jancuk, asu, asw, tae, cuk, bangsat, goblok, dll) sebagai ekspresi emosi, keakraban antar teman (banter — lazim di register Arek/Suroboyoan), atau hinaan personal TANPA dimensi identitas kelompok. Kasar ≠ hate.
- Kritik pedas/kasar terhadap tokoh publik, pejabat, atau institusi atas KINERJA, tindakan, atau kebijakannya. Menjadi hate hanya kalau menyerang identitas kelompok tokoh tsb (suku/agama/gender/dll), mendehumanisasi kelompoknya, atau menghasut kekerasan.
- Keluhan/makian terhadap situasi, benda, atau diri sendiri.

PENTING — serangan ke INDIVIDU juga bisa hate:
Hinaan ke individu DIHITUNG hate kalau memakai slur/stereotip identitas kelompok — individu diserang KARENA identitas kelompoknya. Contoh pola:
- Perempuan diserang dengan slur gender (lonte, murahan, "cewek pulang malem pasti nyeleweng") → hate gender_wanita.
- Individu disebut "kapir/kafir", "bani micin", diserang karena agamanya → hate agama_*.
- Mock-collective ("kaum rahim anget", "LaGiBeTe", "kaum bumi datar" utk kelompok identitas) → hate kelompok tsb.
Pembedanya dengan umpatan biasa: umpatan generik (asu, jancuk, goblok) tidak menyinggung identitas; slur identitas (lonte, kapir, banci) merendahkan lewat keanggotaan kelompok.

Tes cepat kalau ragu: "apakah teks ini merendahkan KELOMPOK identitas, atau seseorang KARENA identitas kelompoknya?" Kalau tidak → hate:false, severity "BUK".

TAKSONOMI 4-DIMENSI:

Dimensi 1 — TARGET GROUP (siapa yang diserang):
- "suku_madura", "suku_tionghoa", "suku_sunda", "suku_batak", "suku_dayak", "suku_papua", "suku_arab"
- "intra_jawa_mataraman", "intra_jawa_arek", "intra_jawa_banyumasan"
- "agama_islam", "agama_kristen", "agama_katolik", "agama_hindu", "agama_buddha", "agama_konghucu", "agama_kepercayaan"
- "kelas_kutha_ndeso", "kelas_priyayi_cilik"
- "gender_wanita", "gender_lgbtq"
- "politik_tokoh", "politik_partai", "politik_ormas"
- "tidak_ada" (kalau bukan hate / tidak menargetkan kelompok)
- (boleh multiple, array)

Dimensi 2 — SEVERITY:
- "BUK" (bukan ujaran kebencian — termasuk umpatan non-group, kritik kinerja, diskusi, pendapat netral)
- "ringan" (stereotyping, slur ringan terhadap kelompok)
- "sedang" (dehumanisasi, generalisasi negatif kuat, eksklusi kelompok)
- "berat" (ancaman, hasutan kekerasan)
ATURAN KONSISTENSI: "ringan"/"sedang"/"berat" hanya boleh dipakai kalau hate:true. Kalau hate:false → severity WAJIB "BUK".

Dimensi 3 — REGISTER:
- "ngoko" (informal, lugas, vulgar mungkin)
- "madya" (semi-formal, mixed)
- "krama" (formal, halus — bisa polite-violent)
- "campur_kasar" (mencampur level untuk menghina, mis. ngoko-pronomina + krama-inggil-verba untuk lawan tutur)

Dimensi 4 — FORM:
- "direct" (eksplisit)
- "sarcastic" (sindiran)
- "idiomatic_pasemon" (kiasan budaya Jawa)
- "code_switched" (campur Indo/Inggris/Arab)

CONTOH (few-shot):

Contoh 1:
Teks: "Dasar asu! Kowe ki pancen jancuk!"
Output: {"hate":false,"target_group":["tidak_ada"],"severity":"BUK","register":"ngoko","form":"direct","reasoning":"Umpatan vulgar diarahkan ke individu tanpa dimensi identitas kelompok. Kasar/abusive, tapi bukan ujaran kebencian."}

Contoh 2:
Teks: "Asw lali nggarap tugas, bodo tenan aku wkwk"
Output: {"hate":false,"target_group":["tidak_ada"],"severity":"BUK","register":"ngoko","form":"code_switched","reasoning":"Umpatan ekspresif ke diri sendiri, nada bercanda. Bukan hate."}

Contoh 3:
Teks: "Wong Madura ki pancen ora pati pinter, lho."
Output: {"hate":true,"target_group":["suku_madura"],"severity":"sedang","register":"ngoko","form":"direct","reasoning":"Generalisasi negatif (stereotyping) terhadap suku Madura."}

Contoh 4:
Teks: "Mugi-mugi tiyang Tionghoa enggal sami wangsul dhateng negarinipun piyambak, supados kitha niki resik."
Output: {"hate":true,"target_group":["suku_tionghoa"],"severity":"sedang","register":"krama","form":"direct","reasoning":"Krama halus tapi isinya eksklusi etnis (mengusir kelompok Tionghoa) — polite-violent. Kehalusan register tidak menghapus hate."}

Contoh 5:
Teks: "Walikota iki isane mung cocot tok, dalan bolong ra tau didandani."
Output: {"hate":false,"target_group":["tidak_ada"],"severity":"BUK","register":"ngoko","form":"direct","reasoning":"Kritik kasar terhadap kinerja pejabat (jalan rusak tidak diperbaiki). Tidak menyerang identitas kelompok — bukan hate."}

Contoh 6:
Teks: "Kader partai X kuwi kabeh tikus kantor, kudune kantore diobong wae."
Output: {"hate":true,"target_group":["politik_partai"],"severity":"berat","register":"ngoko","form":"direct","reasoning":"Dehumanisasi kolektif (tikus) terhadap kelompok partai + hasutan kekerasan (dibakar)."}

Contoh 7:
Teks: "Tedake maling, yo maling. Ora bakal owah."
Output: {"hate":true,"target_group":["tidak_ada"],"severity":"sedang","register":"ngoko","form":"idiomatic_pasemon","reasoning":"Dehumanisasi via determinisme keturunan (descent): keturunan pencuri dianggap pasti pencuri, tidak bisa berubah."}

Contoh 8:
Teks: "Sugeng enjang, mugi-mugi rezeki kita lancar dinten niki."
Output: {"hate":false,"target_group":["tidak_ada"],"severity":"BUK","register":"krama","form":"direct","reasoning":"Sapaan sopan, tidak ada konten kebencian."}

Contoh 9:
Teks: "Wis meneng wae, lonte. Cewek pulang bengi mesti murahan kabeh."
Output: {"hate":true,"target_group":["gender_wanita"],"severity":"sedang","register":"ngoko","form":"direct","reasoning":"Slur gender (lonte, murahan) ke individu perempuan + generalisasi negatif ke semua perempuan. Individu diserang KARENA identitas gendernya — hate, bukan sekadar umpatan."}

Contoh 10:
Teks: "Ra usah ngrungokke omongane wong Kristen kapir kuwi."
Output: {"hate":true,"target_group":["agama_kristen"],"severity":"ringan","register":"ngoko","form":"direct","reasoning":"Individu diserang dengan slur agama (kapir) karena identitas keagamaannya — hate, meskipun targetnya satu orang."}

---

INSTRUKSI OUTPUT:
- Output JSON valid, satu objek per teks input.
- Field wajib: hate (bool), target_group (array string), severity, register, form, reasoning (1-2 kalimat ringkas).
- Tambahkan field "refusal":true KALAU Anda menolak menganalisis teks ini (bukan klasifikasi BUK; refusal = tidak mau engage). Sertakan reasoning singkat.
- TIDAK ada teks lain di luar JSON.

TEKS UNTUK DIKLASIFIKASIKAN:
"""
{TEXT_PLACEHOLDER}
"""
```

---

## Catatan iterasi (post-pilot)

| Versi | Tgl | Perubahan | Hasil pilot |
|-------|-----|-----------|-------------|
| v0 | 2026-05-07 | Initial draft | Pilot #1: GREEN tapi α degenerate. Pilot #1b n=149: α=0.587 (CI [0.475, 0.698]); disagreement #1 = boundary profanity-vs-hate; Grok over-flag (77% hate rate) |
| v1 | 2026-06-10 | Definisi hate group-directed eksplisit; buang "kekasaran leksikal = hate"; fix Contoh 1; aturan hate:false→BUK | ds+grok: flip bersih (Grok 74 T→F, 0 F→T; hate-rate 77→28% / 55→15%), disagreement 36→21, TAPI α flat 0.534→0.554 (prevalensi skewed). Residu: deepseek under-flag slur identitas ke individu. |
| v2 | 2026-06-10 | + blok "slur identitas ke individu = hate" (lonte/kapir/mock-collective); + Contoh 9 (slur gender) & 10 (slur agama) | (pending eval) |

## Open questions untuk validasi via eksperimen

- Apakah blok slur-identitas-ke-individu menaikkan α ds+grok (baseline v1: 0.554) tanpa mengembalikan over-flag profanity Grok?
- Flip yang diharapkan: deepseek F→T pada kasus slur identitas; Grok stabil.
- Pelanggaran unggah-ungguh murni (tanpa konten kelompok): dimensi terpisah di codebook? (v1/v2 men-treat sebagai bukan-hate)
