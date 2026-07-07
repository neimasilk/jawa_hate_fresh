# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-07-07 (sesi 10, lanjutan) — **✅ Audit Fable P0 (STRATEGY §12) SELESAI: bug angka diperbaiki, diagnosis E1 direproduksi dari script, dan §4.5 direframe (klaim dipersempit ke 5/9 subset SARA setelah cek instrumen atas permintaan Bapak).** Sebelumnya sesi 10 awal: E1 hasil masuk — IRR native rendah (α 0.336, di bawah ambang) + koreksi kredensial Daniel (bukan penutur asli). Sebelumnya: Reframe paper (D20), sesi 9; Demo webapp commit `5b4e5a0` (sesi 8); Paper v4 + validasi native (sesi 7).

**🆕 SESI 10 (2026-07-07) — E1 hasil: IRR native rendah + koreksi kredensial Daniel:**

- Bapak serahkan `VALIDATION_FORM_yekti_FILLED.xlsx` + `VALIDATION_FORM_daniel_FILLED.xlsx` (108 baris masing-masing, terisi buta, independen). `score_multivalidator.py` di-repoint ke nama file `_FILLED` (script semula expect nama tanpa suffix) lalu dijalankan — pertama kali dengan data nyata (sebelumnya cuma pernah jalan di draft LLM yang ditolak, C11).
- **Hasil:** rate otentik Mukhlis 55%, Yekti 91%, Daniel 45%. Pairwise Krippendorff's α: Mukhlis-Yekti **0.095** (~chance), Mukhlis-Daniel 0.779, Yekti-Daniel **-0.039** (di bawah chance), 3-rater 0.336 (di bawah ambang konvensional 0.667). **Ini TIDAK menutup Limitation #1 sebagai konfirmasi bersih** — sebaliknya, dua penutur asli sungguhan (Mukhlis, Yekti) paling tidak sepakat satu sama lain.
- **Koreksi tak terduga (dari Bapak, di tengah sesi):** Daniel Rudiaman Sijabat **bukan penutur asli Jawa** — tinggal 30 tahun di Jawa Timur, fasih Jawa sebagai bahasa tambahan, bukan L1. **Yekti tetap penutur asli**, dikonfirmasi ulang oleh Bapak. Klaim "confirmed active Javanese speaker" untuk Daniel yang dipakai sejak D20 (PRD/HANDOFF/wiki/STRATEGY) **salah** — dikoreksi di semua dokumen (ditandai sebagai koreksi, bukan diam-diam ditimpa).
- **Paper diupdate:** `paper/draft_jinita.md` §4.7 Limitation (1) ditulis ulang — melaporkan angka asli + kredensial Daniel yang benar + interpretasi jujur (authenticity = construct rendah-konsensus bahkan antar native, bukan sekadar butuh lebih banyak validator). v5→v6 changelog appendix ditambahkan.
- **Maintenance:** PRD dapat **D21** (Decisions Log + koreksi inline di §0.2 poin 2). STATE Challenges Log dapat **C12**. wiki/decisions.md, wiki/index.md, STRATEGY.md, `experiments/generation_pilot/README.md` dikoreksi paralel.
- **Diagnosis lanjutan (Bapak, sesi sama):** bukan puas dengan "α rendah", Bapak berhipotesis disagreement Mukhlis-Yekti punya pola, bukan noise — (a) hate speech itu subyektif (contoh Bapak: "jancuk awakmu picek" = marah biasa BUKAN hate; "dasare wong meduro jorok-jorok" = hate walau tanpa kata kotor), (b) lingkungan homogen (Bapak) vs heterogen/code-switching (saudara di Surabaya) mungkin bikin standar "otentik" beda. **Dicek langsung ke data (39 baris disagreement Mukhlis-Yekti + 12 Mukhlis-Daniel) — TERKONFIRMASI KUAT:** (1) semua 39 disagreement 1 arah, 19/39 (49%) dari seluruh disagreement (juga 19/27=70% dari niche itu sendiri — dua penyebut berbeda, lihat STRATEGY.md P0-1), 34/39 Yekti tandai JELAS_HATE=0 → form 1-kolom Mukhlis kemungkinan conflate "otentik" dgn "jelas hate"; harmonized alpha naik 0.095→0.519 (TIDAK berlaku utk Daniel: 0.779→0.448, pola beda — non-native ragu register meski paham konten hate). (2) 31/39 catatan Yekti eksplisit sebut "Campur" (kode-campur Indonesia) sbg wajar baginya — match persis hipotesis lingkungan heterogen vs homogen Bapak. **2 sitasi baru diverifikasi (web search + fetch, bukan tebakan):** Ravindranath & Cohn 2014 [25] ("population besar ≠ vitalitas", Javanese jadi contoh kasus), Smith-Hefner 2009 [26] (krama attrition terkait urbanisasi/kelas). **Paper diupdate:** §1 (1 kalimat baru), §4.7 Limitation (1) diperluas dgn diagnosis penuh + cross-ref ke (4), Limitation (4) dapat 1 kalimat cross-ref balik, References +2 (append di akhir, tidak renumber existing — list body citations sudah tidak strict appearance-order sejak awal). Poin Bapak soal dialek Jawa-Chindo (penutur Jawa asli bisa rasakan beda dialek Chindo) dicatat sbg open question validasi ethnolect-spesifik di Limitation (1), bukan klaim baru (belum ada data/validator dari komunitas itu).
- **🧭 REVIEW FABLE (sesi 10, sore):** Bapak minta Fable audit hasil sesi ini → temuan: 1 bug angka SUDAH masuk paper ("70% (19/27)" salah denominator — yang benar 19/39=49% dari disagreement, atau 19/27=70% dari niche), angka diagnosis belum reproducible (melanggar SOP D17 — dihitung ad-hoc, tidak ada script), analisis JELAS_HATE×machine_caught (E6-lite, data sudah ada!) belum dijalankan padahal bisa mengubah klaim §4.5, dan klaim "DeepSeek 97%" belum diuji multi-rater. **Rencana perbaikan lengkap + guard rails: `STRATEGY.md` §12** (P0 blocking sebelum Word template; P1 struktur+commit; P2 pending keputusan Bapak).
- **⏭️ Next action (per STRATEGY §12):** (1) **P0-1..P0-4** — fix bug 70%, tulis `analyze_disagreement.py` + verifikasi jalur kedua, analisis JELAS_HATE×machine_caught (gate ke Bapak kalau hasil melemahkan §4.5), tabel model×validator; (2) **P1-7 commit+push segera** (kerja sesi 9+10 belum di-commit — HARD RULE #6; cek .gitignore untuk form _FILLED berisi teks ofensif dulu); (3) P1-5/6 restrukturisasi Limitation(1)→Results + fix "documented"; (4) baru cek ref [4] + Word template JINITA. **Tidak ada langkah native tersisa** kecuali P2-8 opsional (Bapak 30 menit, re-jawab 39 baris disagreement 2-kolom).

**🆕 SESI 10 (lanjutan, 2026-07-07) — P0 dikerjakan, §4.5 di-gate ke Bapak:**

- **P0-1 ✅** bug denominator "70% (19/27)" diperbaiki di paper §4.7 + STATE C13 + HANDOFF (blok di atas) + wiki/decisions.md D21 + memory `e1-irr-result-daniel-credential-2026-07-07` — semua sekarang bilang eksplisit: 19/27=70% dari niche krama_sarcastic ITU SENDIRI, 19/39=49% dari SELURUH disagreement (dua pertanyaan beda, sebelumnya ketuker).
- **P0-2 ✅** `experiments/generation_pilot/analyze_disagreement.py` ditulis (baru, di-commit) — mereproduksi SEMUA angka diagnosis C13/D21 (39/12 disagreement, arah, per-niche, JELAS_HATE distribusi, 31 catatan code-switch bersarang penuh di 34 baris JELAS_HATE=0, harmonized α) dari script, bukan lagi dari sesi Bash ad-hoc. Diverifikasi jalur kedua (formula closed-form alpha 2-rater independen, ditulis terpisah dari `src/agreement.py`) — cocok dalam rounding (0.519 vs 0.517, 0.448 vs 0.446). Output: `disagreement_analysis.md` (committed, aman — tidak ada teks ofensif verbatim, cuma statistik+catatan singkat Yekti/Daniel).
- **P0-4 ✅** tabel model×validator baru: DeepSeek 97%/100%/97% (Mukhlis/Yekti/Daniel), ranking deepseek>gemma3>qwen3 bertahan di ketiganya walau angka absolut beda (Yekti lebih lenient di semua model). 1 kalimat ditambah ke paper §4.1 sebagai bukti robustness klaim generator utama.
- **P0-3 ✅ RESOLVED — §4.5 direframe dengan persetujuan Bapak.** Analisis JELAS_HATE×machine_caught pada 36 sel DeepSeek: dari **9 sel yang lolos SEMUA 5 detektor**, **0/9 ditandai JELAS_HATE=1 oleh Yekti, dan 0/9 oleh Daniel**. Digate ke Bapak (AskUserQuestion) — Bapak pilih "cek dulu apakah instrumen JELAS_HATE terlalu ketat" sebelum reframe apa pun. Keyword-coding CATATAN kedua validator per sel (bukan treat 0/9 sbg angka datar) menemukan: **5/9** (suku_tionghoa, agama_islam, agama_kristen, gender_lgbtq, suku_arab) genuinely "ironi samar/deniable/kebaca pujian tulus" menurut KEDUA validator = mendukung tesis blind-spot; **3/9** (semua target politik_kolektif) = kedua validator bilang "bukan hate identitas, sinisme politik" = soal scope/construct-validity kategori target, BUKAN buta-pragmatik; **1/9** (intra-jawa Arek vs Mataraman) = "targete ora cetho" = target tak jelas dlm konstruksi stimulus. Instrumen tidak "terlalu ketat" secara acak — ia menggabungkan 3 pertanyaan beda jadi 1 flag biner. Draft §4.5 (klaim dipersempit ke 5/9 subset SARA) + Limitation (6) baru (soal politik_kolektif + target-ambiguity) diajukan ke Bapak via AskUserQuestion dengan preview lengkap teks — **disetujui apa adanya**, langsung diterapkan ke paper. Detail lengkap: `experiments/generation_pilot/disagreement_analysis.md` bagian P0-3(b)+(d), `STRATEGY.md` §9 Q6 (resolved).
- **Semua P0 (P0-1 s.d. P0-4) SELESAI.** Belum dikerjakan: P1-5/6 (restrukturisasi Limitation(1)→Results section baru, fix kata "documented" di §4.7 soal Chindo), P2 (opsional, pending Bapak — re-jawab 39 baris 2-kolom). P1-7 (commit+push) sudah jalan sebelumnya sesi ini; commit lanjutan untuk §4.5/Limitation(6) menyusul. Next: lanjut P1-5/6, atau cek ref [4] manual + Word template JINITA kalau Bapak mau stop restrukturisasi lebih lanjut.

---

> **🧭 STRATEGIC REVIEW (2026-07-06, Fable 5) → `STRATEGY.md`.** Bapak minta review strategis (sekali, mahal) untuk naikkan target ke Scopus/Q. Temuan: register-pragmatik + blind-spot pasemon kuat & layak Q-tier, TAPI validasinya rapuh (validator n=1, blind-spot cuma diuji LLM-judge, framing dual-use). **Keputusan Bapak (sesi 9, sudah dieksekusi — lihat blok di bawah): reframe ✅, validator=Yekti/Daniel ✅, tapi venue=JINITA Sinta 2 SAJA** (bukan Scopus/Q — paket mahal E2/E3/E5/E6 di `STRATEGY.md` §4 DITUNDA, bukan ditolak, kalau suatu saat mau naik ambisi). Baca `STRATEGY.md` kalau mau detail lengkap roadmap yang tak dikerjakan.

**🆕 SESI 9 (2026-07-06) — Reframe paper (D20) + E1/E7/E9:**

- **Konteks:** lanjutan langsung dari strategic review Fable 5 di sesi yang sama (Sonnet sbg executor). 4 pertanyaan gerbang ditanya via AskUserQuestion sebelum eksekusi (tidak menebak keputusan Bapak): reframe? validator siapa? venue apa? boleh pakai data twitter?
- **Keputusan Bapak:** reframe ✅ | validator = **Yekti/Daniel** (penutur Jawa aktif, dikonfirmasi) | **venue = JINITA Sinta 2 saja** (bukan Scopus/Q) | data twitter DVI boleh dipakai ✅.
  > **Koreksi (sesi 10, 2026-07-07):** "dikonfirmasi penutur Jawa aktif" ternyata salah untuk **Daniel** — ia **bukan penutur asli**, tinggal 30 tahun di Jawa Timur, fasih sebagai bahasa tambahan. Yekti tetap penutur asli. Lihat blok SESI 10 di atas.
- **E7 (anchor kelangkaan kedua):** diverifikasi metodologi `D:\documents\twitter` (`compute_dvi.py`/`clean_analysis.py` — lexicon match ≥2 distinctive-word/tweet, N=1.419.641 tweet dedup 32-kota). Javanese = **0,093% confirmed rate** (1.321 tweet), **tertinggi dari 10 bahasa daerah disurvei** tapi tetap <0,1% — anchor kelangkaan independen kedua (beda metode + beda populasi dasar dari haipradana 0,9%). Ditambahkan ke `paper/draft_jinita.md` §1 sebagai Tabel 1 + referensi [8] baru (sitasi "unpublished data, cited with permission" — proyek sister Bapak, konflik publikasi sudah dicek & disetujui).
- **Reframe paper v4→v5:** judul baru *"Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection"* (blind-spot = headline, generator = metode konstruksi stimulus). Abstract ditulis ulang (247 kata, sesuai limit ≤250). Contributions diurut ulang (blind-spot proof dulu, taksonomi menjelaskan kenapa, generator distatement eksplisit "bukan tujuan"). §4.8 Ethics dapat **Dual-use statement** baru (3 mitigasi: tidak merilis generator repurposable, restricted/gated license ala HateCheck, framing vulnerability-disclosure). §4.7 Limitations #1 diupdate (validator ke-2/3 in-progress, bukan kondisional). **Taksonomi §2 + scarcity baseline §3.1 TIDAK disentuh** (instruksi eksplisit Bapak: jangan tulis ulang yang sudah bagus). Referensi [24] (placeholder fabricated "Authors TBD") diganti sitasi HateCheck asli (Röttger et al., ACL-IJCNLP 2021, DOI diverifikasi via ACL Anthology). Changelog v4→v5 lengkap di lampiran paper.
- **E1 (instrumen validator ke-2/3):** `experiments/generation_pilot/build_multivalidator_forms.py` (form BUTA per-validator dari `_key.csv`, TIDAK menimpa form Bapak yang sudah terisi) + `score_multivalidator.py` (α Krippendorff antar-rater, reuse `src/agreement.py` — smoke-tested). **Desain form ditingkatkan:** 2 kolom terpisah OTENTIK (sama seperti form Bapak, utk komparabilitas) + JELAS_HATE (BARU — memisahkan "apakah ini Jawa asli" dari "apakah ini jelas hate", supaya kasus seperti #21 di paper — sarkasme terbaca pujian tulus — tidak lagi ambigu). Dijalankan sukses → `VALIDATION_FORM_yekti.xlsx` + `VALIDATION_FORM_daniel.xlsx` (108 baris, 27 PRIORITAS, kosong).
  - **Percobaan pre-fill LLM ditolak (same day, C11):** sempat dicoba pre-fill kedua form dengan draft Claude (atas instruksi Bapak, supaya Yekti/Daniel koreksi bukan mulai kosong) + `score_multivalidator.py` dijalankan pada draft itu. Ditinjau → **berisiko anchoring bias** yang merusak independensi yang justru mau diukur instrumen ini (lihat `STATE.md` C11). **Bapak putuskan: batalkan, kedua form di-reset ke blank** (`*_BLANK_BACKUP.xlsx`). `_fill_llm_draft.py` masih ada di repo tapi JANGAN dijalankan ulang di form ini — itu catatan pendekatan yang ditolak, bukan langkah aktif. `multivalidator_result.md` sudah update ke status RESET.
  - **Pengisian oleh Yekti/Daniel (blank) = LANGKAH NATIVE BERIKUTNYA, belum dilakukan** (di luar scope agent — beri file + instruksi di sheet "Petunjuk").
- **E9 (lit-pass) SELESAI:** agent verifikasi 19 referensi via WebSearch (ACL Anthology/arXiv/Crossref/IEEE Xplore/DBLP) selesai. Hasil: dari 5 placeholder "(Authors TBD)", cuma 2 benar-benar fabricated ([3] Javanese NLP benchmark, [25 lama] sarcasm survey — diganti paper nyata); 3 lainnya ternyata judul asli tapi penulis belum diisi (Pamungkas et al. ×2 soal GPT-augmentation Indonesian hate speech — ternyata related work yang SANGAT relevan, sekarang disitat eksplisit di §1). 9 referensi lain dikoreksi detail (salah venue/halaman/penulis — kasus terparah: Møller et al. "Information 2023" ternyata venue+1 penulis fabricated, versi asli = ACL Findings EACL 2024). **2 referensi di-drop** (Gwet, SEA-LION) karena ternyata TIDAK PERNAH disitasi di teks — masalah lebih mendasar dari sekadar akurasi: **10 referensi lain yang tadinya "yatim" (ada di daftar pustaka tapi tak pernah dirujuk) sekarang diberi sitasi in-text nyata** di titik yang relevan. Final: 24 referensi, semua tersitasi (diverifikasi via cross-check grep), DOI/arXiv ID lengkap. Satu item ([4], halaman WCSE 2021) masih perlu cek manual manual (selisih publisher vs agregator).
- **Koreksi tak terduga (dari user, di tengah sesi):** nama universitas salah tertulis di `paper/draft_jinita.md` + `codebook/CODEBOOK.md` — **"Universitas Bina Husada Nusantara" (SALAH, fabrikasi sesi lampau) → "Universitas Bhinneka Nusantara" (BENAR)**. UBHINUS = akronim **U**niversitas **BHI**nneka **NUS**antara (universitas baru, dulu STIKI Malang). `README.md` ternyata sudah benar dari awal — hanya paper+codebook yang salah. Catatan afiliasi ditambahkan ke `CLAUDE.md` supaya kesalahan ini tidak terulang di sesi mendatang.
- **Maintenance:** D20 dicatat formal di `wiki/decisions.md` + PRD v0.4→v0.5 (§0.2 baru).
- **⏭️ Next action (lit-pass sudah selesai, tinggal):** (1) **serahkan `VALIDATION_FORM_yekti.xlsx`/`VALIDATION_FORM_daniel.xlsx` ke Yekti/Daniel** (langkah native, satu-satunya yang tersisa dan tak bisa diotomasi — instruksikan mereka isi BUTA, tanpa diskusi dulu dengan Bapak atau satu sama lain, ~1-2 jam); (2) setelah kedua form terisi, jalankan `score_multivalidator.py` untuk α inter-rater; (3) cek manual halaman referensi [4] (WCSE 2021, selisih publisher 65–69 vs agregator 461–465); (4) baru pindah ke Word template JINITA untuk submission final.

---

**🆕 SESI 8 (2026-07-06) — Demo webapp di-commit + didokumentasikan:**

- Sesi dibuka dengan `webapp/` (Flask, ~800 baris: `app.py` + `static/{index.html,app.js,style.css}` + README) **staged tapi belum di-commit dan tidak tercatat di HANDOFF/STATE/wiki manapun** — kemungkinan sisa sesi sebelumnya yang belum sempat di-wrap-up. Ditinjau (baca app.py+README, smoke-test import + jalankan server lokal, cek endpoint `/api/taxonomy` + `/api/dashboard` return data benar termasuk angka validasi 97%/56%/11%), lalu **commit `5b4e5a0`**.
- **Isi webapp** (lihat `webapp/README.md`): 4 tab — (1) Taksonomi statis (4 niche × 9 target), (2) Generator live (panggil DeepSeek/gemma3/qwen3 sungguhan, reuse `generate.py`), (3) Detector live (LLM sbg hate-speech judge pakai prompt v2, reuse `src/cultural_prompt.py`), (4) Dashboard baca `detect_report.md` + `validation_result.md` statis jadi heatmap/bar chart. Localhost-only (`python webapp/app.py` → `127.0.0.1:5000`), tidak untuk deploy publik; tidak menyimpan teks ke disk.
- **Tidak mengubah arah riset** — murni tooling demo untuk presentasi ke coauthor/reviewer, dibangun di atas kode yang sudah ada (tidak ada logic baru).
- **⏭️ Next action tidak berubah** dari sesi 7: **lit-pass referensi** (verifikasi ≥20 ref IEEE, DOI/vol/hal nyata) atau inter-rater ke-2 (Yekti/Daniel).

---

**🆕 SESI 7 (2026-06-30) — Validasi native + Paper v4:**

### A. Validasi native (SELESAI)
- `VALIDATION_FORM.xlsx` diisi LLM (108 baris), **lalu dikoreksi native Bapak** → hasil final:
  - **DeepSeek 35/36 (97%)** — 1 gugur: no.21 krama_sarcastic/agama_islam dibaca sebagai pujian tulus, bukan sarkasme
  - **Gemma3 20/36 (56%)** — krama_sarcastic gagal semua (bocor Bahasa Indonesia); krama_cold_contempt sebagian salah register (ngoko)
  - **Qwen3 4/36 (11%)** — krama semua gagal; kata `kacandran` = halusinasi (bukan Jawa); cold_contempt = Indonesia murni
  - **Total: 59/108 = 55%** otentik. File: `experiments/generation_pilot/validation_result.md`
- **Koreksi native kunci:** `kacandran`=halusinasi; no.21=pujian tulus (0); `ngentu`=vulgar valid (1); `naté`/`saestu`/`estri` = kata Jawa valid dengan è-pepet (bukan encoding rusak)
- **Cross-tab evasion×native:** item yang lolos detektor = otentik native → krama_sarcastic DeepSeek = *uncollectable AND undetectable hate* (klaim paper terkonfirmasi)

### B. Paper v4 — generator framing (SELESAI, `paper/draft_jinita.md`)
- **Judul baru:** "Register-Stratified Javanese Hate Speech Generation via Large Language Models"
- **Kontribusi utama berubah:** 4-niche × 9-target matrix + detection blind-spot proof (bukan 728 labeled texts + α)
- **Struktur baru:** §1 Intro (collection paradox) → §2 Register-pragmatic taxonomy (4 niches Table) → §3 Method (labeling=scarcity baseline; generation=main) → §4 Results (Table 1 per-model, Table 2 per-niche, Table 3 detection 5-detector) → §5 Conclusion
- **Headline numbers di paper:** DeepSeek 97%; krama_sarcastic 30% authentic / 4% detection rate; ngoko_direct 81% authentic / 100% detection rate; 9/36 cells evade ALL 5 detectors
- **25 referensi** (4 baru vs v3; ~15 masih butuh verifikasi DOI/vol/hal)
- **Change log appendix** (hapus sebelum submit)

**🆕 SESI 6 (2026-06-29) — lock PRD (zero native input):**
- Form `VALIDATION_FORM.xlsx` **belum diisi** → native validation = bottleneck (tugas Bapak, irreducible). Tak ada kerja otomatis sesi 5 yang tersisa.
- Kerjakan **Next Action #2** yang tak butuh native: **kunci PRD ke generator** (HARD RULE #1). Pivot D19 selama 3 sesi cuma di HANDOFF/STATE/memory — **tak pernah masuk PRD** → risiko drift ke-3. Sekarang: **PRD v0.4 §0.1** (PIVOT block = arah aktif) + D16–D19 di Decisions Log + Goals G2/G3 re-anchor ke *generation* + §4.2 NEIL/§5 Phases 2–4 ditandai legacy. `wiki/decisions.md` D19 formal + D-OPEN-4.

---


**🆕 SESI 5 (2026-06-29) — systematize otomatis (ultracode workflow):**
- **Logika:** validasi native = bottleneck (by design). Daripada nunggu Bapak, ubah jadi **2 hasil paper otomatis + tugas native lebih tajam**. Semua nol-human, ~beberapa sen DeepSeek + lokal gratis.
- **🎯 Detection blind-spot probe AT SCALE** (`experiments/generation_pilot/detect_probe.py`, 36 sel × 5 detektor, 0 parse-fail, recompute independen cocok persis). **TEMUAN HEADLINE + koreksi:** krama_sarcastic (ironi/pasemon) **lolos SEMUA detektor** (ds 11%, grok 11%, qwen3/gemma3/gpt-oss 0%; total 2/45 verdict hate). ngoko_direct 100% semua (kontrol). krama_report 78–89% cloud → kesopanan saja TIDAK membutakan. **Klaim minimal-pair FINDINGS §3 ("cuma qwen3 yang gagal, cloud nangkap") = KELIRU** — di skala, blind-spot implikatur near-universal, cloud pun gagal. 9 sel lolos 0/5 (7 sarkastik + krama_report/cold_contempt × politik).
- **📊 Multi-model gen** (`gen_local.py`): qwen3:14b **bocor ke Bahasa Indonesia** di niche krama (gagal generate register uncollectable); DeepSeek + gemma3:27b = Jawa otentik. Kapabilitas generasi model-dependent (cermin hasil deteksi).
- **🤖 QC judge-panel 4-agen** (workflow, 115K tok): 0 museum-krama / 0 indo-leak (advisory, non-native), flag #21 (santri sarkastik baca sincere-blessing) + #26 (Arek lemah) + 12 formulaic clone (Mugi…enggal / ingkang sampun paring / lacks-isin).
- **Form di-rebuild** (`rebuild_form.py`): **108 contoh** (deepseek/gemma3/qwen3 ×36) + **27 PRIORITAS** (baris kuning: detector-evasive ATAU judge-flagged + 1 slice per model×niche). `score_validation.py` di-upgrade (header-based; breakdown per-model, model×niche, cross-tab evasi×native).
- **⏭️ LANGKAH PERTAMA sesi berikut = TETAP validasi native**, tapi kini jauh lebih informatif: Bapak isi `VALIDATION_FORM.xlsx` **baris PRIORITAS (kuning) DULU** (kolom OTENTIK 1/0 + MASALAH) → `python experiments/generation_pilot/score_validation.py`. Kolom konteks H (machine_caught) + I (auto_concern) bantu menilai.
- **Sintesis committed:** `experiments/generation_pilot/RESULTS_probe.md` (tabel + interpretasi, TANPA verbatim ofensif). Teks ofensif (detect_results/generated_multimodel/detect_report/judge_panel/xlsx) gitignored per policy.
- **Caveat jujur:** ds+qwen3 = generator SEKALIGUS detektor → DeepSeek gagal deteksi ironi yang ia sendiri generate (11%) = temuan, bukan confound. Judge-panel non-native = advisory; keaslian final tetap native.

**🆕 SESI 4 (2026-06-29) — generator pilot tuntas dijalankan:**
- **Bug empty-content di-root-cause + diperbaiki:** deepseek-v4-pro reasoning model; minta 12 contoh sekaligus → reasoning makan semua token, content kosong. Request kecil sebenarnya berhasil. **Bukan kegagalan task.**
- **`generate.py` di-redesign** jadi **matriks stratifikasi 4 niche register × 9 target SARA** (per-niche batched, retry-on-truncation, resume-aware) → fix bug + sekaligus bikin tabel yang diminta FINDINGS §5.
- **Hasil: 35/36 contoh hate Jawa fresh** ter-generate (~beberapa sen). 0 museum-krama. **N3b krama cold-contempt ke KELOMPOK SARA BERHASIL** (jawab open-question; device berulang = tuduh kelompok tak punya isin/unggah-ungguh — native nilai otentik vs formulaic).
- **Pipeline lengkap siap:** `generate.py` → `review_generated.py` (auto-triage + `VALIDATION_FORM.xlsx`) → **[isi native]** → `score_validation.py`.
- **⏭️ LANGKAH PERTAMA sesi berikut = VALIDASI NATIVE:** Bapak isi `experiments/generation_pilot/VALIDATION_FORM.xlsx` kolom G (OTENTIK? 1/0) + H (MASALAH), lalu `python experiments/generation_pilot/score_validation.py`. Ini bottleneck inti (by design — native = authenticity referee).
- Detail: `experiments/generation_pilot/README.md`. Teks ofensif sintetis gitignored (policy mirror expert_spotcheck); scripts+README di-commit (`7d09765`).
- **Sisa kecil:** 1 cell drop (`krama_sarcastic × suku_arab`) saat retry → matriks 35/36. Bisa diisi ulang (perlu regen niche `krama_sarcastic`), atau biarkan; tidak menghalangi validasi.
- **Roadmap setelah validasi native** (saya bisa otomatisasi): (1) **multi-model** generator (DeepSeek vs lokal vs Grok) = perbandingan antar-model; (2) **judge ke-2** (Yekti/Daniel kalau penutur Jawa) = reliabilitas inter-rater keaslian; (3) **axis regional** (apakah LLM default krama Jawa-Tengah & hapus Arek/Jatim). Semua = tabel paper.
- **Caveat jujur untuk validasi:** generator pakai **device berulang** (cold-contempt → tuduh kelompok tak punya isin/unggah-ungguh; krama_report → semua buka "Mugi tiyang … enggal …"). Polanya otentik, tapi **otentik-kaya vs formulaic** = justru yang Bapak nilai.

---

### Konteks pivot (sesi 3, tetap berlaku) — **🔄 PIVOT BESAR: LABELER → GENERATOR.**

**Inti pivot (BACA INI DULU):** Seluruh kerja lama = **LLM melabeli data Indonesia yang ADA** (`haipradana/indonesian-twitter-hate-speech-cleaned`, HF publik) yang difilter buat cari Jawa. Tapi yield Jawa cuma **0,9%** (8.269 tweet difilter → 74 "jawa", 62% Indonesia). **Maksud asli Bapak SELALU = GENERATOR** (bikin hate Jawa *fresh* pakai LLM), bukan filter+label. Niat itu tak pernah masuk PRD ("annotation"=labeling) → drift. Bapak kecewa sadar ini. **KEPUTUSAN: pivot ke LLM-as-GENERATOR.**

**Arah baru:** GENERATE (LLM, prompt kultural) → consensus-label + spot-check native (QC) → dataset. **Kerja lama ganti peran (TIDAK dibuang):** taksonomi + prompt v2 = otak generator; pipeline labeling 3-LLM = QC; dataset 728 = jangkar realisme + **bukti kelangkaan** (section Motivasi paper: "collection gagal, 0,9% yield → generation perlu").

**Novelty inti yang ketemu sesi ini:** **register-pragmatik hate Jawa** (`experiments/register_probe/FINDINGS.md`) — register menyandi SUHU benci (panas→ngoko, dingin/contempt/ironis→krama); LLM TERNYATA bisa generate krama otentik (DeepSeek dinilai Bapak "sangat bagus"); blind-spot deteksi = **ironi/pasemon**, bukan kesopanan (qwen3 lolos krama sarkastik).

**⏭️ LANGKAH PERTAMA sesi berikut:** ~~jalankan generator~~ **SUDAH DIJALANKAN sesi 4** (35 contoh, lihat blok sesi 4 di atas). Langkah pertama sekarang = **validasi native** (`VALIDATION_FORM.xlsx`).

**💰 Budget:** DeepSeek balance **~$2.2** (sesi 4 generator pakai cuma ~beberapa sen; murah, PILIH ini buat generate). xAI/Grok mahal/terbatas — stop dipakai buat filter.

**Catatan:** audit sesi 2 (paper v3 + codebook v1.0a + `paper/AUDIT_RESPONSE.md`) tetap valid sebagai perbaikan kejujuran lapisan-labeling. 5 keputusan audit (A-E) kini SUBORDINAT ke pivot generator. Tidak ada run in-flight.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

**Cara mulai:** cukup bilang **"lanjut"**. Agent: baca CLAUDE.md → HANDOFF.md (ini) → wiki/index.md → STATE.md, lalu kerjakan "Next Concrete Action" di bawah.

---

## ✅ OPSI A / PILOT #6b SELESAI (2026-06-22): pool diperbesar 332 → 735

Cascade filter (SEA-LION→qwen3 lokal pre-screen → grok verify) dijalankan tuntas. Sempat terblokir xAI **403 kredit habis** (2026-06-18) di pass3 verify (pool mentok 431); resume 2026-06-22 setelah Bapak konfirmasi kredit terisi ($4.55) + live grok test ✅. `scripts/run_cascade_remaining_pipeline.ps1` jalan sampai selesai (verify 1298 sisa → regenerate pool → label 3-rater → analyze).

**Hasil kunci:**
- **Pool 332 → 735** (held-out 586 | prompt-iter 149). Grok confirm-rate di pass2-keeps cuma **25.4%** (1687→+304) → local pre-screen over-keep (temuan cascade-design). **Dump 12.7K habis → 735 ≈ ceiling** sumber ini (estimasi ~950 optimis).
- **Held-out validation MENGUAT:** ds+grok held-out α **0.688** [0.614, 0.759] di 586 teks (vs Pilot #5 0.670 di held-out lebih kecil, CI lebih sempit), full 0.701, iter 0.747 → prompt v2 generalizes robust. 3-rater held-out 0.513 / full 0.545 (qwen3 tetap rater paling bising: ds+qwen3 0.462, grok+qwen3 0.438). **Pakai ds+grok untuk klaim utama.** Angka diverifikasi **recompute independen** (cocok persis).
- **Dataset (`data/labeled/`, gitignored):** `bulk_v2_consensus.jsonl` **728 teks** (158 hate / 570 non-hate, ~22% stabil; unanimous 569) + `bulk_v2_disagreement.jsonl` 7 ties. Dataset 331 lama di-backup `_backup_pilot05_3rater_20260622_*`.
- **SARA lebih kaya:** gender_wanita 111, politik 112, gender_lgbtq 55, tionghoa 37, islam 31, **+ kristen 18, arab 11, kepercayaan 12, hindu 3, rohingya 3**. Register ngoko dominan; form direct/code_switched/sarcastic/pasemon.
- Biaya sesi ~$2.8 grok (verify + label) dari $4.55. **⚠️ 728 < gate D7 BERT (3K)** → lihat Next Action (D-OPEN-3).

---

## ✅ PILOT #5 SELESAI (2026-06-15): dataset berlabel pertama + held-out validation

Pipeline produksi penuh dijalankan sampai tuntas (3-rater **ds + grok + qwen3-lokal** = D16) di pool **332 teks hot-Jawa**. `analyze.py` menghasilkan dataset + report + validasi anti-overfit.

**HELD-OUT VALIDATION (klaim kunci paper — prompt v2 tidak overfit ke pool iterasi 149):**
- Tes ADIL same-rater-set ds+grok: **held-out α = 0.670 [0.525, 0.792]** vs iter-pool **0.747** → di atas ambang 0.6 + CI overlap = **GENERALIZES ✅**.
- α 3-rater (ds+grok+qwen3): held-out 0.565, full 0.610. Lebih rendah karena **qwen3 = rater paling bising** (lone-dissenter 31/64 baris non-unanimous; konsisten Pilot #6). Pakai angka ds+grok untuk klaim utama, qwen3 = rater ke-3 gratis/reproducible.

**DATASET v1** (`data/labeled/`, gitignored → rilis HF/Zenodo nanti):
- `bulk_v2_consensus.jsonl`: **331 teks** (74 hate / 257 non-hate, ~22% hate stabil held-out vs iter) — majority-vote ≥2 rater valid.
- `bulk_v2_disagreement.jsonl`: **1 tie** (sid 3009, "komunis Rusia" — borderline politis) = bahan codebook.
- Target group teratas: gender_wanita 60, gender_lgbtq 33, politik 44, suku_tionghoa 18, agama_islam 18. Severity sepakat hanya 41/74 baris hate → **label inti tetap binary**, severity noisier.

**⚠️ Ukuran:** 331 label (74 hate) = bukti pipeline solid + held-out valid, TAPI jauh di bawah target D7 (10K, gate 3K) untuk training BERT. Pool perlu diperbesar (lihat Next Action).

**Verifikasi adversarial (materi paper metodologi):** sebelum commit, analisis di-audit multi-agent + recompute independen. Menemukan **2 bug nyata** yang sudah diperbaiki: (1) dedup load-order (record stale menimpa label valid → consensus 330/2 jadi 331/1, ds+grok iter 0.763→0.747); (2) formula α non-kanonik (diperbaiki ke coincidence-matrix Krippendorff, validasi vs dataset rujukan 0.743). Lesson: recompute independen *meniru* bug yang sama → hanya **code-audit** yang menangkapnya. Detail: `experiments/pilot05_bulk_labeling/report.md` + commit `fbd59a2`/`2ac5db3`.

---

## ✅ D16 (2026-06-11): vendor mix final = 3-rater ds + grok + qwen3-lokal

Setelah Pilot #6, Bapak putuskan pakai **3 rater**: deepseek + grok (cloud) + qwen3:14b (lokal gratis). Bukan ganti Grok, tapi **tambah** qwen3 sebagai rater independen ke-3 → triangulasi lebih kuat + sebagian reproducible tanpa API berbayar. Cascade filter (Pilot #6b) dibangun untuk perbesar pool murah: lokal pre-screen → grok verify (pool tetap grok-confirmed). Catatan: kredit xAI sudah terisi (labeling pool 332 cloud sukses 0 error).

---

## ✅ PILOT #6 SELESAI (2026-06-11): lokal bisa gantikan Grok

Validasi penuh di pool 149 (prompt v2, pembanding α ds+grok = 0.763):

| Rater ke-2 vs deepseek | JSON valid | Pairwise | α | 95% CI | Biaya |
|---|---|---|---|---|---|
| grok (pembanding) | — | — | 0.763 | [0.624, 0.879] | $ mahal |
| **qwen3:14b /no_think** | 100% | 90% | **0.660** | [0.480, 0.807] | **gratis** |
| SEA-LION v3.5-8B-R | 100% | 80% | 0.422 | [0.238, 0.581] | gratis |

- **qwen3 LOLOS** — CI overlap kuat dengan 0.763. **deepseek(murah) + qwen3(gratis) = consensus viable tanpa xAI.**
- **SEA-LION GAGAL** gate consensus (noise dua arah: 18 over-flag + 10 miss). Temuan paper menarik: model Jawa-native ≠ otomatis rater lebih baik. Masih kandidat untuk tugas FILTER (2.2s/call).
- Infra bulk SIAP untuk lokal: `run_filter.py` (`FILTER_VENDOR="ollama"`) & `run_bulk.py` (`BULK_VENDORS="deepseek,ollama"`) sudah diparametrize; 2.225 record error 403 (xAI habis) sekarang dihitung transient → rerun otomatis retry.

**Pending keputusan Bapak (satu-satunya blocker):** vendor mix final — lihat Next Concrete Action.

---

## ✅ D15 (2026-06-10): KIMI DROPPED — pipeline = 2-LLM deepseek+grok

Saldo Moonshot habis (run Kimi v1 gagal 149/149, 429) → keputusan Bapak: **biarkan, pakai yang ada** = deepseek+grok. Empiris mendukung (Kimi validity 73.8%, 126s/call). α tetap terukur (2 rater); data Kimi v0 n=149 tetap dipakai di paper sebagai sensitivity analysis 3-vs-2 vendor. **Baseline pembanding Pilot #3 sekarang: α ds+grok v0 = 0.534.** Detail: `wiki/decisions.md` D15.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI.

**🔆 STATUS TERKINI (2026-07-06, sesi 9):** **PAPER v5 (reframe, D20) + lit-pass SELESAI** — diagnostic-suite framing, venue dikunci **JINITA Sinta 2 saja** (bukan Scopus/Q, lihat `STRATEGY.md`). Judul baru + abstract/contributions/conclusion direstrukturisasi + Dual-use statement baru; taksonomi §2/scarcity §3.1 tidak berubah. Anchor kelangkaan kedua (data twitter DVI) masuk sebagai Tabel 1. Referensi: 24 total, semua terverifikasi + tersitasi in-text (0 fabricated, 0 yatim). Validasi native Mukhlis tetap: 59/108=55% otentik (DeepSeek 97%). Detection blind-spot proof: krama_sarcastic 4% detection rate vs ngoko_direct 100%. **⏭️ NEXT = (1) serahkan form validator ke Yekti/Daniel** (`VALIDATION_FORM_yekti.xlsx`/`_daniel.xlsx`, instrumen sudah siap — satu-satunya langkah tersisa yang butuh manusia), (2) `score_multivalidator.py` setelah terisi, (3) cek manual halaman ref [4], (4) Word template JINITA. Tidak ada run in-flight. Budget DeepSeek ~$2.2 (murah untuk regen kalau perlu).

**✅ NOVELTY REFRAME (D14, 2026-06-08):** keputusan Bapak — klaim "dataset pertama/from-scratch" **DITINGGALKAN** (dataset hate Jawa sudah ada: UI/WCSE 2021, tak di-release). Novelty utama sekarang 3 pilar: (1) **pipeline fully-automated zero-human**, (2) **taksonomi kultural 4-dimensi register-aware**, (3) **code-mixed realism**. PRD sudah di-update ke v0.3 (D13 retroaktif + D14, Goals G2/G3/G5 sinkron). Dataset tetap deliverable ("first *publicly released*" = fakta sekunder, bukan klaim utama).

**✅ C3 SCALE-UP SELESAI (2026-06-10, n=149, $1.57) — C3 ROBUST:**
- **α hate = 0.587** (bootstrap 95% CI **[0.475, 0.698]**) — naik dari 0.384 (n=24), CI jauh lebih sempit. **Multi-LLM consensus bekerja moderat-baik pada hate Jawa asli dengan prompt v0 tanpa iterasi.** Severity α = 0.480.
- **Gate YELLOW tipis:** α ✅, refusal 1.8% ✅; hanya validity 89.7% < 90% ❌ — murni diseret Kimi (73.8%); deepseek+grok saja 97.7%.
- **PLOT TWIST vendor:** di n=24 Kimi tampak noise utama; di n=149 **Grok = over-flagger** (115T/34F = 77% hate rate; umpatan kasar non-group → hate "ringan"). **Drop Grok → α 0.722** (tertinggi); drop Kimi → 0.534. Pairwise tertinggi justru deepseek–kimi 86.1%. Kimi tetap impraktis bulk (126s/call, validity 73.8%).
- **Disagreement #1 (36/149) = boundary profanity vs hate** — masalah DEFINISI di prompt, bukan capability vendor → **arah Pilot #3 jelas: pertegas hate = group/identity-directed, umpatan kasar ≠ otomatis hate.**
- **Sinyal kultural (materi paper):** 31/69 teks orig-`neutral` haipradana → LLM majority hate=True (LLM tangkap umpatan Jawa `ngewe/wasu/budek/tae` yang dilewatkan anotasi Indonesia-context).
- Report lengkap: `experiments/pilot01b_c3_retest/report.md`.

**Filter scale-up (selesai sebelumnya):** N=250→2000 tweet haipradana. Pool hot-Jawa **24 → 149 teks (80 hate, 54%)**. Yield 7.5%.

**✅ PILOT #1b n=24 (konteks):** α=0.384 non-degenerate (CI [0.01, 0.70]) — sinyal pertama C3, sudah digantikan angka n=149 di atas.

**Konteks lama (tetap berlaku):**
- **Pilot #1** gate GREEN tapi α degenerate (FineWeb2 nyaris tanpa hate) → sudah dipecahkan Pilot #1b.
- **Pilot #2** (LLM-as-Jawa-filter, Grok): Jawa murni ~nol → code-mixed scope tervalidasi empiris.

---

## Baca Dulu

1. `CLAUDE.md` - hard rules dan daily protocol.
2. `wiki/index.md` - user-facing knowledge base.
3. `wiki/decisions.md` - D1-D12 decision history.
4. `wiki/pilots.md` - status pilot.
5. `STATE.md` - live state dan challenges log.
6. `experiments/pilot01_llm_characterization/report.md` - report awal, tapi baca dengan catatan teknis di bawah.

---

## Status Terbaru

Pilot #1 SELESAI (2026-05-25, di komputer kantor baru). Report final di `experiments/pilot01_llm_characterization/report.md`.

Hasil deduped (100 sampel × 3 LLM):
- DeepSeek: refusal 1%, JSON valid 97%, 20s/call, $0.31
- Grok: refusal 0%, JSON valid 100%, 11s/call, $0.20 (paling efisien)
- Kimi: refusal 0%, JSON valid 85%, **91s/call, 260K out-tok, $0.35** (reasoning model, mahal+lambat, 11/100 masih kosong walau max_tokens=4096)
- Total cost $0.85, runtime 2j32m.

Gate GREEN: refusal 0.3% (<20%), JSON valid 94% (>90%), α=1.000 (>0.5).

**⚠️ CAVEAT KRITIS — jangan dibaca bulat-bulat:**
- α=1.000 itu **degenerate**: ketiga LLM melabeli SEMUA 100 sampel `hate=false`/BUK. Setuju sempurna karena sumber FineWeb2 `jav_Latn` (fallback dari OSCAR yang gated) nyaris tidak mengandung hate — mayoritas teks web/Wikipedia/promosi.
- Yang terkonfirmasi real: C2 (refusal bukan blocker) + C1 sebagian (LLM bisa hasilkan JSON taksonomi valid).
- Yang BELUM terjawab: C3 (apakah multi-LLM consensus bekerja pada hate ASLI). α ini tidak bisa dipakai untuk klaim consensus.

Patch yang sudah final dan ter-commit:
- `src/llm_clients.py`: max_tokens DeepSeek 2048, Kimi 4096.
- `run_pilot.py`: resume retry record kosong (done = ada raw_text atau error).
- `analyze.py`: dedup `(source_id, vendor)` keep-last (retry menang), print ASCII-safe.

Catatan dedup: rerun meng-APPEND record baru (responses.jsonl punya 300 unik tapi ~106 baris duplikat untuk Kimi/DeepSeek yang di-retry). `analyze.py` dedup keep-last sudah benar memilih retry yang valid.

---

## Next Concrete Action (urutan)

Konteks: **REFRAME ke Diagnostic-suite (D20, 2026-07-06 sesi 9), venue = JINITA saja.** Lihat status atas + `STRATEGY.md`. Urutan:

1. ✅ **GENERATOR + SYSTEMATIZE + VALIDASI NATIVE + PAPER v4 — SEMUA SELESAI (sesi 4–7).** Validasi final 59/108=55% (DeepSeek 97%).
2. ✅ **Kunci PRD ke framing generator — SELESAI (sesi 6).**
3. ✅ **Sistematisasi generasi — SUDAH (sesi 5).**
4. ✅ **Strategic review + reframe paper (D20) — SELESAI (sesi 9).** Paper v5: diagnostic-suite framing, Dual-use statement, Tabel 1 anchor kelangkaan kedua (data twitter). Detail lengkap di blok SESI 9 di atas.
5. **⏭️ LANGKAH AKTIF #1 — Selesaikan lit-pass referensi.** Agent verifikasi 19 referensi `[verify]`/"(Authors TBD)" sudah dikirim (background, sesi 9); cek hasilnya, update daftar pustaka `paper/draft_jinita.md` §REFERENCES dengan sitasi terverifikasi (jangan fabricate — beberapa placeholder mungkin perlu diganti/dihapus kalau tak ada padanan nyata).
6. **⏭️ LANGKAH AKTIF #2 — Serahkan form validator ke Yekti/Daniel** (langkah native, TIDAK bisa diotomasi): `experiments/generation_pilot/VALIDATION_FORM_yekti.xlsx` + `VALIDATION_FORM_daniel.xlsx` sudah siap (instruksi di sheet "Petunjuk" masing-masing). Minta mereka isi BUTA (tanpa lihat jawaban Bapak atau diskusi satu sama lain dulu) — 2 kolom: OTENTIK + JELAS_HATE, ~1-2 jam. Setelah terisi: `python experiments/generation_pilot/score_multivalidator.py` → α inter-rater.
7. Setelah #5 dan #6: pindah paper ke **Word template JINITA** untuk submission final + review Yekti/Daniel atas isi paper (bukan cuma form validasi).
8. (Ditunda, bukan prioritas — hanya kalau Bapak mau naik ambisi venue nanti) E2/E3/E5/E6 di `STRATEGY.md` §4: detektor nyata (IndoBERT/Perspective), anchor data real krama-hate, eksperimen mitigasi fine-tune, baseline deteksi-manusia.

**Catatan paper:** novelty inti = register-pragmatik (`experiments/register_probe/FINDINGS.md`) + generator-untuk-uncollectable + bukti kelangkaan (kini 2 anchor independen) + detection blind-spot (kini headline paper, bukan sekadar hasil). Paper-labeling lama (audit sesi 2) jadi bahan pendukung.

---

### Keputusan audit sesi 2 (kini subordinat ke pivot — `paper/AUDIT_RESPONSE.md`):
1. **(TERTINGGI) Spot-check pakar ~100 item** — Bapak native, ~1 jam, stratifikasi pada disagreement LLM-vs-sumber. Ubah κ0.19 dari pembunuh → fitur. Tidak melanggar zero-human. **Ini pengubah accept/reject.**
2. **Aturan label**: konfirmasi tetap 3-rater (headline 0.513, sudah saya pilih jujur) atau ganti ds+grok-only (0.688).
3. **Anekdot mahasiswa nyontek**: demote jadi 1 kalimat? (judgement coauthor — isu integritas).
4. **Lit-pass referensi** (≥20 IEEE, verifikasi DOI).
5. **Legal lisensi `haipradana`** (boleh rilis turunan CC BY-NC-SA?) — potensi blocker rilis.

Lalu: pindah paper ke Word template JINITA + review Yekti/Daniel.

---

### Konteks lama (D-OPEN-3, masih berlaku)

**D-OPEN-3 SELESAI — Bapak pilih Opsi 1 (codebook + draft paper).** Keduanya dibuat 2026-06-23. Petunjuk JINITA sudah di-download + paper disesuaikan ke template. **Tidak ada run in-flight, tidak butuh saldo.**

**Sudah jadi:**
- `codebook/CODEBOOK.md` v1.0 — taksonomi 4-dimensi grounded di dataset 728, 7 boundary cases dengan adjudikasi, distribusi empiris, limitasi jujur (termasuk temuan register krama langka 157/158 ngoko).
- `paper/draft_jinita.md` v2 — draft Inggris, **conform template JINITA**: judul ≤12 kata tanpa akronim, abstrak ≤250 kata tanpa sitasi, 5 keywords, IMRaD bernomor (1 INTRO / 2 TAXONOMY / 3 METHOD / 4 RESULTS&DISCUSSION / 5 CONCLUSION), sitasi IEEE `[n]`, ≥20 referensi anchor, **Gen AI disclosure**, Ethics, Acknowledgements.
- `paper/jinita_guidelines/` — petunjuk JINITA terunduh (`submissions.html`, `template.txt`, `gen_ai_policy.html`) + `SUMMARY.md` (checklist kepatuhan + sisa TODO).

**Sisa TODO (untuk sesi berikut / review Bapak):**
1. **Lit-pass referensi:** lengkapi & verifikasi ≥20 referensi IEEE (DOI/vol/hal), ≥80% jurnal ≤5 tahun. Anchor sudah nyata (Ibrohim&Budi 2019, Putri/Ibrohim/Budi Javanese-Sunda = kemungkinan "UI 2021" yang kita rujuk, NusaCrowd, Gilardi PNAS, dll); tinggal verifikasi presisi (jangan fabricate — per Gen AI policy).
2. **Pindah ke Word template** JINITA (TNR 10pt, A4, kolom) untuk submission final.
3. **Review Bapak + coauthor** (Yekti, Daniel) atas isi codebook + paper.
4. Opsional: modeling baseline (IndoBERT/XLM-R) sebagai karakterisasi dataset (future-work, bisa kuatkan Results) — butuh GPU lokal gratis.
5. Versi blind (anonim) untuk peer review.

**Catatan teknis:** dataset final `data/labeled/bulk_v2_consensus.jsonl` (728) + `_disagreement.jsonl` (7). Pool `experiments/pilot02_llm_jawa_filter/outputs/hot_jawa_subset.jsonl` (735). Report `experiments/pilot05_bulk_labeling/report.md`. Backup dataset 331 lama: `data/labeled/_backup_pilot05_3rater_20260622_*`. APC JINITA Rp1.5jt/$100 (hanya jika diterima).

---

## 📖 PANDUAN BAPAK

**Status:** paper v5 + lit-pass SELESAI (sesi 9, 2026-07-06). Tidak ada run in-flight, tidak butuh saldo. **Satu-satunya langkah tersisa butuh Bapak** (bukan Claude Code) — lihat tutorial di bawah.

### ⏭️ Yang perlu Bapak lakukan sekarang: serahkan form validasi ke Yekti & Daniel

Validasi Bapak sendiri (n=1, first author) **sudah selesai** — tercatat di `VALIDATION_FORM.xlsx` (59/108=55% otentik, dikoreksi 2026-06-30). Yang dibutuhkan sekarang adalah validasi ke-2/ke-3 dari Yekti dan Daniel supaya angka keaslian punya *inter-rater reliability* (bukan cuma klaim 1 orang) — ini syarat minimum untuk paper naik dari sekadar "kredibel" ke "robust secara metodologis".

1. **Ambil 2 file** dari `experiments/generation_pilot/`:
   - `VALIDATION_FORM_yekti.xlsx` → untuk Yekti Asmoro Kanthi
   - `VALIDATION_FORM_daniel.xlsx` → untuk Daniel Rudiaman Sijabat
2. **Kirim satu file ke satu orang** (email/WA) — jangan ditukar.
3. **Minta mereka baca sheet "Petunjuk"** di dalam file (sudah ada instruksi lengkap), intinya:
   - 108 baris teks; baris kuning (PRIORITAS, 27 baris) diisi dulu kalau waktu terbatas.
   - Isi 2 kolom judgment: **OTENTIK?** (1/0 — terdengar Jawa asli pada register yang dimaksud?) dan **JELAS_HATE?** (1/0 — terpisah dari OTENTIK, apakah jelas menyerang identitas kelompok?). Boleh beda arah (otentik tapi bukan hate, atau sebaliknya) — itu memang yang mau diukur.
   - Kolom `machine_caught`/`auto_concern` cuma info bantu, bukan jawaban benar.
   - Estimasi waktu: 1–2 jam per orang.
4. **Poin krusial: mereka isi BUTA** — tanpa lihat jawaban Bapak, dan tanpa diskusi satu sama lain sebelum keduanya selesai. Kalau tidak, hasilnya tidak bisa dipakai mengukur konsistensi antar-penutur.
5. **Setelah kedua form kembali terisi**, taruh lagi di folder yang sama (nama file jangan diubah) dan bilang ke Claude Code — akan dijalankan `score_multivalidator.py` untuk hitung α Krippendorff antar-rater.

### Sisa kecil lain (opsional, tidak menghalangi)
- Cek manual halaman referensi [4] di `paper/draft_jinita.md` (WCSE 2021 — publisher bilang pp. 65–69, satu agregator bilang pp. 461–465).
- Setelah validator ke-2/3 selesai: pindah paper ke Word template JINITA untuk submission final.

*(Catatan teknis fase data-collection lama — pengecekan progres pilot filter/labeling background — sudah tidak relevan di fase saat ini (paper-writing); diarsipkan dari sini. Semua pipeline generation/labeling sudah tuntas, tidak ada run in-flight.)*

---

## Konteks Keputusan Final

- Proyek lama v1-v4 **jangan dipakai** sebagai baseline, warm-start, atau data training. Alasan: dataset lama mayoritas hasil back-translation mahasiswa, bukan ujaran Jawa natural.
- Human annotation bukan default. Fallback maksimal adalah sanity check kecil oleh Bapak jika pilot benar-benar gagal.
- Data source default adalah public dumps, bukan live scraping.
- Scope bahasa sumber: Jawa dan turunannya; Sunda/Madura bukan sumber, tetapi bisa menjadi target group dalam ujaran Jawa.
- Vendor Pilot #1: DeepSeek V4 Pro, Grok 4.3, Kimi K2.6.

---

## Catatan Teknis

- `.env.txt` dipakai untuk API keys dan gitignored.
- Kimi hanya menerima `temperature=1.0`; sudah di-handle.
- FineWeb2 `jav_Latn` publik dan berhasil streaming, tapi contoh awal banyak teks web/Wikipedia/promosi. Ini mungkin membuat hate rate sangat rendah; jangan simpulkan kualitas hate detection hanya dari distribusi BUK di fallback source.
- Runtime aktual lebih lama dari estimasi awal: sekitar 2 jam total karena Kimi lambat. Rerun resume seharusnya lebih pendek, tetapi tetap bisa puluhan menit.
- Worktree saat handoff belum clean: ada patch di `src/llm_clients.py`, `run_pilot.py`, `analyze.py`, plus `outputs/` dan `report.md`.

---

## User Communication

Bahasa Indonesia, ringkas. User prefer eksperimen kecil daripada blueprint panjang. Jangan re-litigate decisions final kecuali diminta. Jika ada hasil buruk, dokumentasikan sebagai lesson learned, bukan disembunyikan.
