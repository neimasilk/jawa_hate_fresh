# Cultural Classification Prompt v1

**Status:** Pilot #3 iterasi #1 (dari v0).
**Task:** Klasifikasi ujaran kebencian Bahasa Jawa dengan kategori 4-dimensi + register-aware.
**Target LLMs:** DeepSeek V4 Pro, Grok 4.3, Kimi K2.6.

**Perubahan vs v0 (terfokus pada temuan disagreement C3 n=149):**
1. Definisi hate dipertegas: hate = serangan berbasis **identitas kelompok**; umpatan kasar / kritik kinerja pedas ≠ otomatis hate. (Sumber disagreement #1: Grok over-flag umpatan non-group sebagai hate "ringan".)
2. Kalimat system prompt v0 "ujaran kebencian bisa muncul lewat kekasaran leksikal" DIBUANG — itu mengajari over-flag. Diganti: penentu hate adalah ARAH ke identitas kelompok, bukan level kekasaran.
3. Contoh 1 v0 diperbaiki (umpatan personal "Dasar asu! Kowe ki pancen jancuk!" dilabeli hate:true berat dengan target tidak_ada — kontradiksi internal). Sekarang hate:false BUK.
4. Contoh pelanggaran unggah-ungguh (kowe+tindak) diganti contoh krama polite-violent yang group-directed (pelanggaran tata krama tanpa konten merendahkan kelompok = tidak sopan, bukan hate).
5. Aturan konsistensi: hate:false → severity WAJIB "BUK".

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
| v1 | 2026-06-10 | Definisi hate group-directed eksplisit; buang "kekasaran leksikal = hate" dari system prompt; fix Contoh 1 (umpatan personal → BUK); contoh krama polite-violent group-directed; kontras kritik-kinerja vs hate-politik; aturan hate:false→BUK | (pending Pilot #3 eval) |

## Open questions untuk validasi via eksperimen

- Apakah definisi eksplisit menaikkan α deepseek+grok (baseline v0: 0.534) dan menurunkan hate-rate Grok (baseline 77%)?
- Apakah ada teks yang justru flip ke arah salah (under-flag hate kelompok yang halus)?
- Pelanggaran unggah-ungguh murni (tanpa konten kelompok): dimensi terpisah di codebook? (v1 men-treat sebagai bukan-hate)
