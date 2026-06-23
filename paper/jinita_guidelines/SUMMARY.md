# JINITA — Ringkasan Petunjuk Penulisan + Checklist Kepatuhan

**Sumber (diunduh 2026-06-23, curl UA-browser; OJS memblokir bot biasa):**
- Author Guidelines / Submissions: `submissions.html`, `authorguidelines.html`
- Template resmi (Google Doc, ENG): `template.txt` — https://docs.google.com/document/d/1UAbWE80iRp5WlDkx9SMMdYKS5zndm3Oo
- Gen AI Policy: `gen_ai_policy.html` (turunan kebijakan Elsevier)
- Artikel sampel terbit: `sample_article.pdf`

---

## A. Persyaratan umum

| Item | Aturan JINITA | Status draft kita |
|---|---|---|
| Bahasa | **English** | ✅ Inggris |
| Panjang | min **6** hal, maks **12** (riset) / 16 (review). Guidelines web menyebut maks 20. | Target 8–12 hal |
| Manajemen referensi | Zotero/Mendeley/EndNote, **IEEE style** | ⚠️ konversi ke IEEE bernomor (done di draft v2) |
| Template | Wajib pakai **JINITA template (ENG)** (TNR 10pt, single space, A4) | ⚠️ format final saat pindah ke Word |
| Jumlah referensi | **min 20**, **≥80% jurnal terbit ≤5 tahun** | ⚠️ draft baru ~20 anchor; perlu lit-pass lengkapi DOI |

## B. Struktur manuskrip (IMRaD bernomor, ALLCAPS heading)

1. **Judul** — ≤ ~12 kata, **tanpa akronim/singkatan**, tanpa kata mubazir ("A Study of", "Analysis of"…). Boleh sebut metode **karena** paper ini mengembangkan metode baru.
2. **Abstract** — **150–250 kata**, **tanpa sitasi**, tanpa langkah prosedur. Wajib memuat: tujuan, desain riset, metodologi, hasil utama, kesimpulan, dan beda/manfaat vs metode lama.
3. **Keywords** — **maks 5**, ejaan American, hindari 'and'/'of', hindari jamak/istilah umum.
4. Bagian: **1. INTRODUCTION → [2. optional: proposed framework/theory] → METHOD → RESULTS AND DISCUSSION → CONCLUSION**. Subbagian 3.1, 3.1.1.
5. **ACKNOWLEDGEMENTS** sebelum **REFERENCES**.
6. Sitasi IEEE bernomor `[1]`, `[2]`; `Ref [16]` di awal kalimat; `et al.` untuk >3 penulis; referensi font 8pt.
7. Istilah bahasa asing **italic** (penting: kata Jawa `ngoko`, `krama`, `jancuk`, `pasemon` → italic).
8. Introduction 3–6 paragraf: latar, rumusan masalah, literatur relevan, pendekatan, kebaruan.

## C. Gen AI Policy (KRUSIAL untuk paper ini)

- **Wajib disclosure statement** saat submit untuk setiap penggunaan tool AI (atau sumber lain).
- Penulis **wajib verifikasi** akurasi output AI; **referensi hasil AI bisa salah/fabricated** → jangan percaya begitu saja. (→ kita TIDAK mengarang DOI; tandai yang perlu verifikasi.)
- Reviewer tidak boleh pakai AI (bukan urusan kita sebagai penulis).
- **Nuansa penting:** penggunaan LLM di paper kita ada **dua peran** — (1) LLM sebagai *metode anotasi* (inti riset, dijelaskan di METHOD, sah) dan (2) bantuan AI untuk *drafting* (didisclose di statement). Keduanya kompatibel dengan kebijakan.

## D. Lain-lain

- Submit blind review → siapkan versi **anonim** (tanpa nama/afiliasi) selain versi title-page.
- File: Word/RTF/ODT; single-space; 12pt (template body 10pt TNR); italics bukan underline; tabel/gambar inline.
- **APC** (mulai Vol 8 No 1): **Rp 1.500.000** (domestik) / **USD 100** (asing) — hanya jika diterima.
- Copyright jurnal: **CC BY 4.0** (≠ lisensi dataset kita CC BY-NC-SA — dua hal berbeda, tidak konflik).
- Kontak: faiz[at]pnc.ac.id.

## E. Penyesuaian yang sudah dilakukan ke draft (`draft_jinita.md` v2)

1. Judul dipersingkat, tanpa akronim.
2. Abstrak dipotong ke ≤250 kata, tanpa sitasi/placeholder.
3. 5 keywords sesuai aturan.
4. Restruktur ke IMRaD bernomor + bagian taksonomi sebagai "proposed framework" opsional.
5. Sitasi diubah ke IEEE bernomor `[n]`; daftar referensi IEEE ≥20 (anchor nyata; DOI sebagian perlu verifikasi lit-pass).
6. Ditambah: **Gen AI disclosure statement**, Ethics, Acknowledgements.
7. Istilah Jawa ditandai italic.

## F. Sisa TODO sebelum submit (butuh Bapak / lit-pass)

- [ ] Lengkapi & verifikasi **≥20 referensi** (DOI, vol/hal) — ≥80% jurnal ≤5 tahun. Anchor sudah nyata; perlu cek presisi.
- [ ] Pindahkan ke **Word template** JINITA (format kolom/font final).
- [ ] Modeling baseline (future work) — opsional kalau mau kuatkan Results.
- [ ] Versi blind (anonim) untuk submission.
- [ ] Isi Acknowledgements (sponsor/hibah, jika ada).
