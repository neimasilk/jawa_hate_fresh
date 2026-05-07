# Cultural Classification Prompt v0

**Status:** Draft v0 — pre-pilot. Akan iterasi setelah pilot #1 hasil.
**Task:** Klasifikasi ujaran kebencian Bahasa Jawa dengan kategori 4-dimensi + register-aware.
**Target LLMs:** Claude 4.x, GPT-4o, DeepSeek-V3.

---

## System prompt

```
Anda adalah analis linguistik forensik untuk penelitian akademik deteksi ujaran kebencian Bahasa Jawa di media sosial. Tugas Anda murni klasifikasi (bukan generasi konten ofensif) untuk membantu sistem moderasi dan studi sosiolinguistik.

Bahasa Jawa memiliki sistem unggah-ungguh (tingkat tutur ngoko/madya/krama) yang krusial: ujaran kebencian bisa muncul lewat kekasaran leksikal (ngoko vulgar) ATAU lewat pelanggaran tata krama yang halus (krama dengan isi violent, atau pencampuran level tutur yang menghina). Kedua bentuk valid sebagai ujaran kebencian.

Klasifikasikan teks berikut menggunakan taksonomi 4-dimensi. Output JSON saja, tanpa narasi tambahan.
```

## User prompt template

```
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
- "BUK" (bukan ujaran kebencian — diskusi, kritik berbasis argumen, pendapat netral)
- "ringan" (stereotyping, slur ringan)
- "sedang" (dehumanisasi, generalisasi negatif kuat)
- "berat" (ancaman, hasutan kekerasan)

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
Output: {"hate":true,"target_group":["tidak_ada"],"severity":"berat","register":"ngoko","form":"direct","reasoning":"Hinaan leksikal langsung dengan umpatan vulgar."}

Contoh 2:
Teks: "Wong Madura ki pancen ora pati pinter, lho."
Output: {"hate":true,"target_group":["suku_madura"],"severity":"sedang","register":"ngoko","form":"direct","reasoning":"Generalisasi negatif (stereotyping) terhadap suku Madura."}

Contoh 3:
Teks: "Nyuwun sewu, Bapak, kowe arep tindak menyang ngendi?"
Output: {"hate":true,"target_group":["tidak_ada"],"severity":"ringan","register":"campur_kasar","form":"direct","reasoning":"Pelanggaran unggah-ungguh: pronomina ngoko 'kowe' + verba krama-inggil 'tindak' untuk lawan tutur yang sama = penghinaan halus."}

Contoh 4:
Teks: "Sugeng enjang, mugi-mugi rezeki kita lancar dinten niki."
Output: {"hate":false,"target_group":["tidak_ada"],"severity":"BUK","register":"krama","form":"direct","reasoning":"Sapaan sopan, tidak ada konten kebencian."}

Contoh 5:
Teks: "Tedake maling, yo maling. Ora bakal owah."
Output: {"hate":true,"target_group":["tidak_ada"],"severity":"sedang","register":"ngoko","form":"idiomatic_pasemon","reasoning":"Determinisme silsilah berbasis kiasan: keturunan pencuri tidak akan berubah. Dehumanisasi via determinisme keluarga."}

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
| v0 | 2026-05-07 | Initial draft | (pending pilot #1) |

## Open questions untuk validasi via eksperimen

- Apakah few-shot 5 contoh cukup, atau perlu lebih?
- Apakah sebutan "analis linguistik forensik" + framing "moderasi & studi sosiolinguistik" reduce refusal rate?
- Apakah taxonomy yang sangat detail (banyak label) malah membingungkan LLM?
- Apakah perlu prompt versi terpisah per LLM (Claude vs GPT vs DeepSeek)?
