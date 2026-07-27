# Syarat "author dengan afiliasi internasional" — sudah terpenuhi di naskah

**Status: kemungkinan besar ini masalah METADATA OJS, bukan masalah kekurangan penulis.**

## Bukti

Naskah yang Bapak submit (`paper/JUTIF_Amien_Kanthi_Sijabat_2026 fixed.docx`) **sudah memuat
penulis keempat dengan afiliasi internasional**:

> Mukhlis Amien\*¹, Yekti Asmoro Kanthi², Daniel Rudiaman Sijabat³, **Roby Firnando Yusuf⁴**
> ⁴Software Engineering, Jeonbuk National University, South Korea

Tapi email keputusan editor dibuka dengan **hanya tiga nama**:

> "Mukhlis Amien, Yekti Asmoro Kanthi, Daniel Rudiaman Sijabat:"

Sapaan itu dibangkitkan otomatis oleh OJS dari **metadata submission**, bukan dari isi berkas.
Dan catatan sesi 13 mencatat bahwa saat submit, yang dimasukkan ke metadata OJS memang
**3 penulis** (Mukhlis, Yekti, Daniel) — Roby tidak ikut didaftarkan.

**Kesimpulan:** editor membaca daftar penulis dari metadata (3 orang, semua Indonesia), lalu
memicu butir standar *"please add an additional author with an international affiliation"*.
Editor kemungkinan besar belum melihat bahwa di dalam berkas naskah penulis keempatnya sudah ada.

## Yang perlu dilakukan (bukan cari penulis baru)

1. **Tambahkan Roby Firnando Yusuf sebagai contributor di metadata OJS** submission #6393.
   Di author dashboard → tab *Metadata* / *Contributors* → *Add Contributor*.
   Isi: nama, email, afiliasi **Jeonbuk National University, South Korea**, negara South Korea,
   ORCID kalau ada. Urutan penulis: keempat.
2. **Sebutkan di response letter** bahwa penulis dengan afiliasi internasional sudah ada di
   naskah sejak submission awal, dan metadata sudah disamakan. (Sudah saya tulis di
   `JUTIF_R1_response.md` butir E10.)
3. Data Roby yang saya perlukan kalau Bapak mau saya rapikan lebih lanjut: **email** dan
   **ORCID** — dua hal itu belum ada di naskah.

## Catatan kecil yang sudah saya perbaiki

Di berkas yang disubmit, baris afiliasi tertulis menempel tanpa koma:
`4Software EngineeringJeonbuk National University, South Korea`.
Di berkas revisi sudah jadi `⁴Software Engineering, Jeonbuk National University, South Korea`.

## Kalau ternyata editor memang minta penulis KELIMA

Kalau setelah metadata dibetulkan editor masih meminta tambahan penulis internasional,
baru pakai jalur undangan. Prinsipnya: **minta kontribusi nyata, bukan sekadar izin pakai nama.**
Paper ini justru sedang menonjolkan integritas metodologis (limitasi 6 poin, IRR rendah
dilaporkan apa adanya) — gift authorship akan kontradiktif, dan melanggar norma ICMJE/COPE.

Peran yang realistis dan genuinely menambah nilai:

1. **Validasi silang taksonomi register-pragmatik** ke bahasa diglosik lain (Korea/Jepang
   punya sistem honorifik) — langsung memperkuat klaim generalisasi yang sekarang masih
   normatif di §4.5 dan Conclusion.
2. **Review independen desain detection probe** — apakah ada confound yang terlewat
   (Limitasi 5 soal shared-prompt sudah disinggung Reviewer B).
3. **Framing lintas-bahasa di Discussion** terhadap literatur moderasi multibahasa.

Draft email undangan (bahasa Inggris) tersedia di riwayat git commit `590e55f` file ini,
kalau sewaktu-waktu diperlukan.
