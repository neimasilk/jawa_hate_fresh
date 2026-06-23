# Adversarial Audit — Findings, Action List & Response (2026-06-23)

Hasil audit multi-agent (8 reviewer adversarial → verifikasi → sintesis; 51 agen, recompute independen ke data nyata). Semua angka diverifikasi ulang oleh `experiments/audit_external/audit.py`. Dokumen ini = jawaban jujur + status tiap temuan.

## Verdict reviewer (apa adanya, tanpa sanjungan)

> **As-is: REJECT / major-revision berat untuk JINITA (SINTA-2), condong reject.** Komputasi sangat disiplin (semua α reproduce persis, formula kanonik), TAPI kontribusi **over-sold** di 3 titik beban: (1) `orig_label` manusia diabaikan padahal konsensus cuma setuju 54.5% (κ 0.19) dengannya; (2) headline reliabilitas 2-rater 0.688 ≠ reliabilitas label rilis 3-rater 0.513; (3) "generalizes not overfits" = fallacy CI-overlap (power ~27%). Plus: kebocoran nomor telepon, label hallucinated, leakage, Table 1 baseline conflated, "novelty" register yang nyaris tak muncul.

**Setelah perbaikan di bawah** → kandidat major-revision yang kredibel. Pengubah-permainan tunggal yang masih perlu: **spot-check pakar ~100 item** (butuh Bapak ~1 jam).

## Kekuatan nyata (terverifikasi, bukan basa-basi)
- Semua α headline reproduce ke 3 desimal dari implementasi from-scratch (0.688/0.701/0.513 dst). Tak ada statistik fabricated.
- 24 flip neutral→hate = slur Jawa/code-mixed **benar** yang dilewatkan anotator Indonesia (`sipit/aseng`, `banci/jablay`, `kafir`) → bukti empiris kuat (sebelumnya tak dipakai).
- Anonimisasi handle/URL bersih; kode α kanonik tervalidasi vs rujukan 0.743; 2 bug nyata ditemukan & diperbaiki sebelum rilis.
- Paper jujur soal beberapa batas (ngoko dominan, severity bising).

## Action list & status

| # | Prio | Temuan (terverifikasi) | Status |
|---|---|---|---|
| 1 | P0 | **`orig_label` diabaikan**: 54.5% setuju, κ 0.19, buang 307/441 hate-manusia | ✅ FIXED — Section 4.3 baru (confusion + κ + framing definitional narrowing + 24 flip benar) |
| 2 | P0 | **Headline 0.688 (2-rater) ≠ label rilis 3-rater 0.513** | ✅ FIXED — §4.2 pimpin 3-rater 0.513; ds+grok 0.688 sebagai batas atas |
| 3 | P0 | **Kebocoran PII**: nomor WA utuh (mau rilis publik) | ✅ FIXED — `clean_release.py` scrub 2 nomor → `*_clean.jsonl`; §4.10 diperbarui |
| 4 | P0 | **"Generalizes not overfits"** = fallacy CI-overlap, power ~27% | ✅ FIXED — diganti difference-CI [-0.09,+0.20] + catatan power; abstrak/§4.2/konklusi |
| 5 | P1 | **Table 1 baseline conflated** (v0 3-rater 0.587 vs 2-rater) | ✅ FIXED — v0=0.534, Δ=+0.23, semua sel ds+grok |
| 6 | P1 | **Directional bias** Grok over-label (McNemar p=1.5e-4), rater tak exchangeable | ✅ FIXED — §4.4 baru |
| 7 | P1 | **Token hallucinated** (`kaum_rhaim_anget`, `intra_jawa`) + sparsity ≤2 | ✅ FIXED — didokumentasi codebook §8.7 + §5 sparsity; normalisasi = TODO pipeline |
| 8 | P1 | **Count target tak reproducible** (campuran vote/union) | ✅ FIXED — `audit.py` jadi generation script; majority-of-3 di paper §4.1 + codebook §5 |
| 9 | P1 | **Dedup + leakage** (706/735 unik, 5 held-out bocor) | ✅ FIXED — dilaporkan §4.9 + codebook §8.4 (hapus sebelum hitung held-out) |
| 10 | P1 | **Klaim kausal n=2** "general dominates language-specific" | ✅ FIXED — §4.7 turun jadi "single observation, CI overlap, size confound" |
| 11 | P1 | **Register "novelty"** padahal krama-hate=0 | ✅ FIXED — judul tak lagi "register-aware"; §2.3/§4.5 = proposed/dormant |
| 12 | P2 | α salah metrik di skew → tambah raw agr + Gwet AC1 | ✅ FIXED — §4.2 Table 3 (raw 0.89, AC1 0.82) |
| 13 | P2 | **7 ties = artefak DeepSeek-null**, bukan kontes 3-arah | ✅ FIXED — codebook §6 reframe + arahkan ke 159 split 2-1 |
| 14 | P2 | Severity reliabilitas rendah tanpa penanda di JSONL | ⚠️ PARTIAL — didokumentasi; penanda inline field = TODO |
| 15 | P2 | Densitas Jawa rendah ("Javanese" overstated) | ⚠️ DISCLOSED — codebook §1 + §8; kuantifikasi langid proper = TODO |
| 16 | P3 | Soften adversarial-recompute + refusal (3.7% attrition) | ✅ FIXED — §4.8 + §3.4 |
| 17 | P3 | Citation-n codebook (586→561), "1/250" vs jawa-tag | ✅ FIXED — codebook §1/§7 |
| 18 | — | **Celah taksonomi**: hinaan warna kulit/fisik (`ireng jomok`) tak ada kategori | ✅ DOCUMENTED — codebook §8.3 + paper §4.9; tambah kategori `fisik_warnakulit` v1.1 |

## Butuh keputusan Bapak (TIDAK saya eksekusi sendiri)

| Item | Kenapa perlu Bapak | Dampak |
|---|---|---|
| **A. Spot-check pakar ~100 item** (fallback-ladder #2) | Bapak native expert; ~1 jam; stratifikasi pada ~331 disagreement LLM-vs-sumber | **Tertinggi.** Ubah κ 0.19 dari pembunuh → fitur ("LLM lebih benar di kasus divergen"). Tidak melanggar zero-human (spot-check ≠ anotasi penuh) |
| **B. Aturan label**: tetap 3-rater (headline 0.513) atau ganti ds+grok-only (headline 0.688, ubah 7 ties + 15 label hate) | Trade-off kejujuran vs angka | Saya sudah pilih opsi jujur (3-rater + ds+grok sebagai sensitivitas); konfirmasi atau ganti |
| **C. Anekdot mahasiswa nyontek** | Self-report n=1 tak terverifikasi tentang proyek sendiri → reviewer bisa anggap motivated reasoning / isu integritas | Demote jadi 1 kalimat ilustratif + sandar ke literatur (cost/scarcity) — butuh judgement coauthor |
| **D. Lit-pass referensi** | ≥20 ref IEEE, verifikasi DOI (jangan fabricate per Gen AI policy) | Anchor sudah nyata (23 ref); tinggal verifikasi |
| **E. Legal: lisensi `haipradana`** | Bolehkah turunan dirilis CC BY-NC-SA? | Potensi blocker rilis HKI/HF — perlu cek lisensi sumber |

## Eksperimen tambahan yang sudah dijalankan (di dalam review/audit)
- **External validity vs orig_label** → 54.5%, κ 0.19, 24 flip benar. (`audit.py §1`)
- **Difference-bootstrap power** overfitting → +0.058 [-0.09,+0.20], power ~27%. (`audit.py §3`)
- **Prevalence-robust** raw agr + AC1 per cell. (`audit.py §2`)
- **McNemar** directional bias. (`audit.py §4`)
- **Dedup + leakage** + off-taxonomy tokens + per-kategori reproducible. (`audit.py §5-7`)
- **FN-slur audit** → 11 kasus, 1 celah taksonomi nyata (skin-color). (`audit.py §9`)

## Artefak
- `experiments/audit_external/audit.py` — single source of truth angka (reproducible).
- `experiments/audit_external/clean_release.py` — scrub PII → `*_clean.jsonl` (rilis pakai versi clean).
- `paper/draft_jinita.md` v3 — semua koreksi terintegrasi.
- `codebook/CODEBOOK.md` v1.0a — idem.
