# Pilots Index

_Last touched: 2026-05-07 saat wiki creation. Status hidup tiap pilot._

Cross-ref: [`STATE.md` Next milestones](../STATE.md), [`STATE.md` Challenges Log](../STATE.md), tiap pilot folder di [`experiments/`](../experiments/).

---

## Status overview

| Pilot | Topik | Status | Estimated cost | User effort | Folder |
|---|---|---|---|---|---|
| **#1** | LLM characterization (3 LLM × 100 sampel Jawa) | ✅ DONE 2026-05-25 — gate GREEN (lihat caveat) | $0.85 actual | 0 jam | [`pilot01_llm_characterization/`](../experiments/pilot01_llm_characterization/) |
| **#2** | LLM-as-Jawa-filter + ekstrak subset Jawa-panas | ✅ DONE 2026-05-25 — yield 9.6%, 24 hot (9 hate) | ~$0.05 | 0 jam | [`pilot02_llm_jawa_filter/`](../experiments/pilot02_llm_jawa_filter/) |
| **#1b** | C3 re-test (3 LLM × hot-Jawa) — memecah α degenerate | ✅ DONE 2026-06-10 — **scale-up n=149: α=0.587 (CI [0.48, 0.70]), gate YELLOW tipis** | $0.26 + $1.57 | 0 jam | [`pilot01b_c3_retest/`](../experiments/pilot01b_c3_retest/) |
| **#3** | Cultural prompt manual iteration | ✅ DONE 2026-06-10 — **v2: α ds+grok 0.534 → 0.763** dalam 2 iterasi | ~$2.3 actual | 0 jam | [`pilot03_cultural_prompt/`](../experiments/pilot03_cultural_prompt/) |
| **#4** | AutoResearch loop (Karpathy pattern) | 📋 PLANNED (mungkin tak perlu — Pilot #3 manual cuma butuh 2 iter) | ~$12.5/run (bounded) | 0 jam (overnight agent) | [`pilot04_autoresearch_prompts/`](../experiments/pilot04_autoresearch_prompts/) |
| **#5** | Bulk labeling produksi (filter full 12.7K → label v2 ds+grok → held-out α + dataset) | 🔄 RUNNING 2026-06-10 malam | ~$12-15 est | 0 jam (jaga mesin nyala) | [`pilot05_bulk_labeling/`](../experiments/pilot05_bulk_labeling/) |

---

## Pilot #1 — LLM characterization

**Tujuan:** Karakterisasi 3 LLM (DeepSeek V4 Pro, Grok 4.3, Kimi K2.6) untuk task klasifikasi ujaran kebencian Bahasa Jawa.

**Sample:** 100 dari OSCAR-2301 `jv` subset (streaming, 70% dengan keyword hint + 30% tanpa hint untuk diversity).

**Metrics:**
- Refusal rate per LLM
- JSON output validity rate per LLM
- Inter-LLM agreement: Krippendorff's α (binary hate label)
- Latency + token usage + cost
- Sample disagreements untuk inspeksi

**Decision gate** (otomatis di `analyze.py`):
- 🟢 GREEN — refusal <20% + validity >90% + α >0.5 → lanjut fully-LLM framing
- 🟡 YELLOW — marginal → iterasi prompt (Pilot #3)
- 🔴 RED — buruk → trigger fallback ladder ([D2](decisions.md#d2--fallback-ladder-kalau-pilot-gagal))

**Detail:** [`pilot01_llm_characterization/README.md`](../experiments/pilot01_llm_characterization/README.md). Report: [`report.md`](../experiments/pilot01_llm_characterization/report.md).

### Hasil (2026-05-25, deduped 100 sampel × 3 LLM)

| Vendor | Refusal | JSON Valid | Latency mean | Out tok | Cost |
|---|---|---|---|---|---|
| DeepSeek V4 Pro | 1.0% | 97% | 20s | 58K | $0.31 |
| Grok 4.3 | 0% | 100% | **11s** | 7K | $0.20 |
| Kimi K2.6 | 0% | 85% | **91s** | **260K** | $0.35 |

- **Gate GREEN:** refusal 0.3% (<20%), JSON valid 94% (>90%), α=1.000 (>0.5). Total cost $0.85, runtime 2j32m.
- **⚠️ CAVEAT — α=1.000 degenerate.** Ketiga LLM melabeli SEMUA 100 sampel `hate=false`/BUK. Agreement sempurna karena sumber FineWeb2 `jav_Latn` (fallback dari OSCAR gated) hampir tidak mengandung ujaran kebencian — mayoritas web/Wikipedia/promosi. Jadi **C3 (agreement pada konten hate asli) BELUM terjawab**; α ini tidak bisa dipakai untuk klaim multi-LLM consensus bekerja.
- **Terkonfirmasi real:** C2 (refusal bukan blocker ✅), C1 sebagian (LLM bisa hasilkan JSON taksonomi kultural valid ✅).
- **Vendor concern:** Kimi K2.6 reasoning model — 91s/call, 260K out-token, 11/100 masih kosong walau `max_tokens=4096`. Grok jauh lebih efisien. Relevan untuk seleksi vendor bulk pipeline (C-baru).
- **Implikasi next:** butuh sumber yang benar-benar mengandung hate Jawa untuk uji agreement bermakna → menyatu dengan masalah data sourcing (Pilot #2 filter + cari dump yang lebih "panas").

---

## Pilot #2 — LLM-as-Jawa-filter + ekstrak subset Jawa-panas

**Tujuan ganda:** (1) test apakah LLM bisa filter Jawa/code-mixed dari dump Indonesia; (2) **memecahkan blocker C3 Pilot #1** — ekstrak teks Jawa yang benar-benar mengandung hate (Pilot #1 α degenerate karena FineWeb2 nyaris tanpa hate).

**Motivasi:** langid Jawa false-positive tinggi (low-resource). Kalau LLM akurat → pipeline pakai LLM filter, bukan langid.

**Strategi data (keputusan 2026-05-25):** tidak ada korpus hate Jawa siap-unduh (UI/WCSE 2021 hanya di paper). Maka **filter dump hate Indonesia (`haipradana`) → ekstrak subset Jawa/code-mixed**, RAW TEXT saja (label asli tak dipakai sbg label pipeline), dan **terima code-mixed sebagai scope sah**. Konsisten dengan metodologi fully-LLM + public dumps. ⚠️ Implikasi novelty di-flag (lihat README Pilot #2 + perlu update PRD).

**Setup:** 250 sampel (seed 42) dari haipradana, anonimisasi, filter via Grok 4.3 (`prompts/jawa_filter_v0.md`). Smoke test 4 contoh ✅ (jawa/krama/campuran/indonesia terbedakan benar, tidak tertipu kata gaul).

**Output:** distribusi bahasa, yield Jawa+campuran, cross-tab × hate, `outputs/hot_jawa_subset.jsonl`.

### Hasil (2026-05-25, 250 sampel)

- **Filter robust:** 100% JSON valid (250/250). Kategori `lainnya` (2.8%) tepat menangkap Sunda/Melayu/Portugis → filter tidak asal-asalan.
- **Distribusi:** jawa 0.4% (1) · campuran 9.2% (23) · indonesia 87.6% (219) · lainnya 2.8% (7).
- **Yield Jawa+campuran = 9.6%** (24/250). Di antaranya **9 hate** (38%). → densitas hot-Jawa ≈ 3.6% dari dump Indonesia.
- **Temuan kunci:** Jawa "murni" nyaris nol (1 teks, "jancuk jancuk"); hate Jawa sosmed **didominasi code-mixed** → **memvalidasi keputusan menerima code-mixed sebagai scope** secara empiris.
- Subset panas tersimpan: `outputs/hot_jawa_subset.jsonl` (24 teks).

**Implikasi:** 24 teks (9 hate) cukup untuk C3 re-test PERTAMA (non-degenerate, α akan punya variasi label), tapi tipis untuk angka robust. Untuk pool lebih besar: scale filter ke lebih banyak baris haipradana (~12.7K → estimasi ~460 hot-Jawa).

### Scale-up (2026-06-08, N=2000)

Filter diperluas 250 → 2000 tweet haipradana. Pool hot-Jawa **24 → 149 teks (80 hate orig, 54%)**. Yield Jawa+campuran 7.5% — konsisten dengan 9.6% awal. `hot_jawa_subset.jsonl` ditulis ulang berisi 149 teks → input C3 scale-up Pilot #1b.

**Status:** ✅ DONE. Detail: [`pilot02_llm_jawa_filter/README.md`](../experiments/pilot02_llm_jawa_filter/README.md), report: [`report.md`](../experiments/pilot02_llm_jawa_filter/report.md).

---

## Pilot #1b — C3 re-test (multi-LLM agreement pada hate Jawa asli)

**Tujuan:** Memecahkan blocker C3 dari Pilot #1 (α=1.000 degenerate karena FineWeb2 nyaris tanpa hate). Re-test 3-LLM dengan prompt v0 **sama** di `hot_jawa_subset.jsonl` (Pilot #2: 24 teks Jawa code-mixed, 9 berlabel hate asli). Prompt sengaja sama → beda hasil atribusi ke **DATA**, bukan prompt.

### Hasil (2026-06-08, 24 teks × 3 LLM, $0.26)

| Vendor | Refusal | JSON Valid | Latency mean | Hate dist |
|---|---|---|---|---|
| DeepSeek V4 Pro | 8.3% | 91.7% | 23s | 14T/6F |
| Grok 4.3 | 0% | 100% | **6s** | 20T/4F |
| Kimi K2.6 | 0% | **62.5%** | **115s** | 7T/8F |

- **Krippendorff's α (binary hate) = 0.384** (bootstrap 95% CI [0.01, 0.70]); severity α = 0.376. **NON-DEGENERATE** (41T/18F) → α bermakna, beda fundamental dari Pilot #1.
- **Pairwise:** deepseek–grok **80%**, deepseek–kimi 69%, grok–kimi 67%.
- **Sensitivitas drop-1-vendor:** drop Kimi → α **0.480** (keep deepseek+grok); drop Grok → 0.405; drop DeepSeek → 0.306. Kimi = penurun α terbesar.
- **Gate YELLOW** (refusal 2.8% ✅, validity 84.7% 🟡 ditarik turun Kimi, α 0.384 < 0.5).
- **Majority vs label haipradana:** 9/9 teks ber-orig-label `hate` → majority hate=True (recall 100% pada hate eksplisit); 9/15 `neutral` → majority hate=True (LLM lebih sensitif ke umpatan Jawa `asu/ngewe/tae` daripada anotasi Indonesia-context haipradana — bisa sinyal kultural, bisa over-flag; perlu inspeksi).

**Lesson (materi paper):**
1. **C3 terjawab: multi-LLM consensus bekerja MODERAT pada hate Jawa asli**, bukan degenerate. α 0.38–0.48 tergantung vendor mix.
2. **Kimi K2.6 = sumber noise utama** (validity 62.5% karena reasoning-model empty, 5/7 disagreement = Kimi dissenter melabeli BUK). Menguatkan temuan vendor Pilot #1 → pertimbangkan **2-LLM deepseek+grok** untuk bulk (lebih murah, agreement 80%).
3. **CI sangat lebar (n=24)** → angka belum robust. Masalah = ukuran sampel, bukan prompt. **Scale-up filter pool besar wajib sebelum klaim paper.**

### Scale-up n=149 (2026-06-08 → 06-10, $1.57, prompt v0 sama)

| Vendor | Refusal | JSON Valid | Latency mean | Hate dist | Cost |
|---|---|---|---|---|---|
| DeepSeek V4 Pro | 4.7% | 95.3% | 30s | 76T/61F | $0.66 |
| Grok 4.3 | 0% | 100% | **7s** | **115T/34F** | $0.28 |
| Kimi K2.6 | 0.7% | **73.8%** | **126s** | 55T/55F | $0.63 |

- **α hate = 0.587** (bootstrap 95% CI **[0.475, 0.698]**) — naik dari 0.384 (n=24), CI jauh lebih sempit dan seluruhnya ≈ di atas 0.5-batas-bawah. **Angka C3 robust.** Severity α = 0.480 (CI [0.387, 0.571]).
- **Pairwise:** deepseek–kimi **86.1%** (tertinggi!), deepseek–grok 78.8%, grok–kimi 77.3%.
- **Drop-1-vendor:** drop **Grok** → α **0.722** (CI [0.580, 0.856]) — tertinggi; drop Kimi → 0.534; drop DeepSeek → 0.527.
- **Gate YELLOW tipis:** α ✅ 0.587 > 0.5, refusal ✅ 1.8%, validity ❌ 89.7% < 90% — satu-satunya yang gagal, murni diseret Kimi (73.8%); deepseek+grok saja = 97.7%.
- **PLOT TWIST vendor vs n=24:** di n=24 Kimi tampak noise utama; di n=149 **Grok = outlier over-flagger** (77% teks dilabel hate vs deepseek 51% / kimi 50%). Pola di 36 disagreement: mayoritas = **Grok sendirian melabeli hate `ringan`/`sedang` pada umpatan kasar non-group-directed** (asw, bodo anjir, mencla-mencle, kritik politik kasar). Kimi tetap impraktis untuk bulk (126s/call, validity 73.8%, out-tok 475K).
- **Majority vs orig haipradana:** 66/80 orig-`hate` → majority True (82.5%); **31/69 orig-`neutral` → majority True (45%)** — LLM menangkap umpatan Jawa (`ngewe`, `wasu`, `budek`, `tae`) yang dilewatkan anotasi Indonesia-context. Sinyal kultural kuat untuk paper, tapi sebagian besar kasus ini = profanity, bukan group-directed hate → tergantung definisi taksonomi.

**Lesson scale-up (materi paper):**
1. **C3 ROBUST: α 0.587 dengan CI sempit** — consensus moderat-baik dengan prompt v0 tanpa iterasi apapun.
2. **Boundary "profanity vs hate" = sumber disagreement #1**, bukan vendor capability. Grok memperlakukan umpatan kasar sebagai hate ringan; deepseek/kimi tidak. Ini **masalah definisi di prompt** → perbaikan paling menjanjikan ada di **Pilot #3** (pertegas definisi hate = group/identity-directed, umpatan kasar ≠ otomatis hate), bukan ganti vendor.
3. **Tidak ada 2-LLM combo yang menang semua aspek:** deepseek+kimi α tertinggi (0.722) tapi Kimi lambat+invalid; deepseek+grok cepat+murah+validity 97.7% tapi α 0.534. Rekomendasi: **iterasi prompt dulu (Pilot #3), baru putuskan vendor mix** — kalau definisi hate dipertegas, α deepseek+grok kemungkinan naik signifikan.

**Status:** ✅ DONE (termasuk scale-up). Detail: [`pilot01b_c3_retest/README.md`](../experiments/pilot01b_c3_retest/README.md), report: [`report.md`](../experiments/pilot01b_c3_retest/report.md).

---

## Pilot #3 — Cultural prompt manual iteration

**Tujuan:** angkat α dengan memperbaiki PROMPT, berdasarkan diagnosis disagreement C3 n=149. Baseline v0: α 3-LLM **0.587**, α deepseek+grok **0.534**. Protokol lengkap: [`pilot03_cultural_prompt/README.md`](../experiments/pilot03_cultural_prompt/README.md).

**Diagnosis v0 (temuan kunci, materi paper):** root cause Grok over-flag ada di **prompt v0 sendiri** — system prompt menyebut "ujaran kebencian bisa muncul lewat kekasaran leksikal" dan Contoh 1 few-shot melabeli umpatan personal murni (`Dasar asu! Kowe ki pancen jancuk!`, target `tidak_ada`) sebagai `hate:true, berat` (kontradiksi internal: hate tanpa target group). Grok mengikuti literal; deepseek/kimi mengabaikan → split sistematis di boundary profanity-vs-hate. **Inkonsistensi internal prompt = sumber inter-LLM disagreement yang terukur.**

**v1 (2026-06-10):** definisi hate group/identity-directed eksplisit + tes cepat "merendahkan kelompok identitas?"; buang kalimat "kekasaran leksikal"; fix Contoh 1 (umpatan personal → BUK); contoh krama polite-violent group-directed (ganti contoh unggah-ungguh murni); kontras kritik-kinerja-pejabat (BUK) vs dehumanisasi+hasutan partai (berat); aturan hate:false → severity BUK. 8 few-shot, semua sintetis (tanpa kontaminasi pool eval).

**Eval per versi:** pool sama 149 teks (`run_eval.py` parametrized `P3_PROMPT_VERSION`/`P3_VENDORS`, resume-aware); `analyze.py` komparatif vs baseline v0: Δα per vendor-set, **flip table per vendor (T→F vs F→T)**, hate-rate shift, disagreement listing. Keep/discard threshold Δα ±0.05. Metrik bersama di `src/agreement.py`.

### Hasil (2026-06-10, 2 iterasi × 298 call ds+grok, ~$2.3 — vendor per D15)

| Versi | Perubahan kunci | α ds+grok | Disagreement | Hate rate (ds / grok) |
|---|---|---|---|---|
| v0 (baseline) | — | 0.534 [0.381, 0.674] | 36 | 55% / 77% |
| v1 | definisi group-directed; profanity ≠ hate | 0.554 [0.382, 0.713] | 21 | 15% / 28% |
| **v2** | + slur identitas ke individu = hate | **0.763 [0.624, 0.879]** | **12** | 19% / 31% |

- **v1:** koreksi kualitatif sukses besar (flip Grok 74 T→F / **0 F→T**, raw agreement ~79→86%) tapi **α flat** — prevalensi jadi skewed → chance agreement naik → α terkoreksi keras. **Lesson metodologis (paper): α bisa flat walau label membaik; selalu baca flip table + raw agreement bareng α.** Residu v1: deepseek under-flag slur identitas ke individu (lonte/kapir/kaum-rahim-anget/LaGiBeTe).
- **v2:** blok "slur identitas ke individu = hate" + Contoh 9 (slur gender) & 10 (slur agama) → **Δα +0.229 vs v0**. Flip sehat (F→T: ds 1, grok 2).
- **Stop di v2 (anti-overfit):** residu 12 disagreement = ambigu genuin (meta-komentar ttg diskriminasi, kutipan hate, perbandingan positif antar-etnis) → bahan codebook + held-out validation saat bulk, BUKAN target prompt berikutnya.
- Insiden operasional: saldo Kimi habis di run v1 (149 error 429) → D15 drop Kimi; resume logic di-patch (429 ≠ done).

**Status:** ✅ DONE. **Prompt kerja bulk = `prompts/cultural_classification_v2.md`**, vendor = deepseek+grok. Report: [`report_v1.md`](../experiments/pilot03_cultural_prompt/report_v1.md), [`report_v2.md`](../experiments/pilot03_cultural_prompt/report_v2.md).

---

## Pilot #4 — AutoResearch loop

**Tujuan:** Autonomous prompt iteration via Karpathy autoresearch pattern adaptation. Agent overnight iterate prompt variants, log keep/discard berdasarkan composite metric.

**Pattern adaptation:**

| Karpathy autoresearch | Adaptasi kita |
|---|---|
| Edit `train.py` (single file) | Edit `prompts/cultural_classification_vN.md` |
| Train 5 min/experiment | Eval 50-sample × 3 LLM (~3-5 min, ~$0.25/iter) |
| `val_bpb` metric | Composite (refusal + validity + α + entropy) |
| `program.md` skill | `program_prompt_research.md` + cultural injection |
| `NEVER STOP` loop | Bounded ~$12.5/run, max 50 iter |
| H100 single GPU | LLM API |
| `results.tsv` | `results.tsv` + kolom `lesson` |

**Reference:** Karpathy autoresearch repo cloned di `~/Documents/autoresearch/` ([D11](decisions.md#d11--adopsi-pattern-karpathy-autoresearch-pilot-4)).

**Paper angle:** "AutoResearch Pattern for Cultural Prompt Engineering in Low-Resource NLP" — bisa jadi kontribusi metodologis sendiri atau section di paper utama.

**Status:** PLANNED. Folder + README detail sudah ada di [`pilot04_autoresearch_prompts/README.md`](../experiments/pilot04_autoresearch_prompts/README.md). Eksekusi setelah Pilot #1-3 baseline jelas.

---

## Pilot #5 — Bulk labeling (produksi pertama)

**Tujuan:** dataset berlabel pertama via pipeline penuh + **held-out validation** α prompt v2 (anti-overfit terhadap pool iterasi 149).

**Pipeline (launched 2026-06-10 malam):** filter full haipradana 12.7K (Grok; resume dari 2K lama → ~10.7K call baru, est 8-15 jam) → regenerate `hot_jawa_subset.jsonl` (~950 est) → label prompt v2 × deepseek+grok (149 lama di-merge dari Pilot #3; ~800 teks baru, est ~6 jam, ~$8) → analisis.

**Output:** α held-out vs prompt-iter vs full; `data/labeled/bulk_v2_consensus.jsonl` (label final = kedua vendor agree; severity hanya kalau sama persis); `bulk_v2_disagreement.jsonl` (bahan codebook); profil taksonomi (severity/register/form/target_group).

**Interpretasi:** α held-out ≈ 0.763 → v2 generalizes ✅; jauh < 0.6 → indikasi overfit, re-iterasi di pool campuran.

**Ketahanan:** semua step resume-aware + 429-aware; rantai idempotent `scripts/run_bulk_pipeline.ps1` (jalankan ulang kapan pun). Panduan user: HANDOFF §Panduan Bapak.

**Status:** 🔄 RUNNING (step 1 filter). Detail: [`pilot05_bulk_labeling/README.md`](../experiments/pilot05_bulk_labeling/README.md).

---

## Future pilots (potential)

- **Pilot #6:** BERT/IndoBERT/XLM-R training di auto-labeled data
- **Pilot #7:** Adversarial perturbation testing untuk model robustness

(Update sesuai eksperimen progress + insight baru.)
