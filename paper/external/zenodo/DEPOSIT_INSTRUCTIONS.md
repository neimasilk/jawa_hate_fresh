# Zenodo deposit — ✅ SELESAI 2026-07-27

> **Sudah terbit.** Record: <https://zenodo.org/records/21616875>
> **DOI versi 1.0.0 (dipakai di paper):** `10.5281/zenodo.21616875`
> **Concept DOI (selalu ke versi terbaru):** `10.5281/zenodo.21616874`
>
> Referensi [28] di naskah sudah memakai DOI versi. Dokumen di bawah disimpan sebagai
> catatan prosedur, kalau nanti perlu deposit versi baru.
>
> **Gotcha yang ditemukan saat pengisian:** field Description Zenodo memakai TinyMCE di
> dalam React — `setContent()` lewat API **tidak tersimpan** (hilang setelah reload).
> Yang berhasil: buka toolbar **Source code**, isi textarea dialognya, lalu Save. Radio
> DOI juga **reset ke "Yes, I already have one" setiap reload halaman**, jadi harus
> di-set ulang tepat sebelum Publish.

---

## Prosedur asli (arsip)

**Kenapa ini perlu:** Reviewer A (komentar 9) dan Reviewer B (komentar 21) sama-sama
menandai referensi DVI sebagai *"unpublished data"* — red flag SINTA 2, apalagi karena
dipakai menopang Table 1. Keputusan Bapak: deposit ke Zenodo supaya dapat DOI permanen.
Ini sekaligus mengeksekusi janji rilis artefak publik (keputusan D22 item 4).

**Yang di-deposit hanya angka agregat** — 10 baris × 4 kolom. Tidak ada teks tweet,
tidak ada user ID, tidak ada data pribadi. Aman dirilis.

---

## Langkah

1. Buka https://zenodo.org → login (bisa pakai akun GitHub/ORCID).
2. **New upload** → tipe **Dataset**.
3. Upload dua berkas dari folder ini:
   - `dvi_table1_snapshot.csv`
   - `README.md`
4. Isi metadata dari `zenodo_metadata.json` (title, description, keywords, license
   CC-BY-4.0, version 1.0.0, creator: Mukhlis Amien, Universitas Bhinneka Nusantara).
   Kalau Bapak punya ORCID, masukkan sekalian — memperkuat verifiabilitas.
5. **Publish.** Zenodo langsung menerbitkan DOI.
6. **Kirim DOI-nya ke saya.** Saya update referensi [28] di naskah dari bentuk
   sementara ke sitasi final, lalu rebuild docx.

## Setelah DOI ada, referensi [28] jadi:

```
[28] M. Amien, "Digital Vitality Index for Indonesian regional languages on Twitter:
     a lexicon-based confirmed-tweet measurement across 32 cities," dataset, Zenodo,
     2026, doi: 10.5281/zenodo.XXXXXXX.
```

## Catatan

- Zenodo memberi **dua** DOI: satu "concept DOI" (selalu menunjuk versi terbaru) dan
  satu DOI versi spesifik. Untuk sitasi paper, pakai **DOI versi spesifik** supaya
  yang disitasi persis angka yang ada di Table 1.
- Kalau nanti ada revisi data, Zenodo bikin versi baru tanpa mematikan DOI lama —
  sitasi di paper tetap valid.
- Lisensi CC-BY-4.0 dipilih supaya reviewer/pembaca bebas memverifikasi. Kalau Bapak
  mau lebih ketat, CC-BY-NC juga diterima Zenodo — tapi CC-BY lebih standar untuk
  data pendamping paper.
