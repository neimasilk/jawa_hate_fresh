# Pilots Index

_Last touched: 2026-05-07 saat wiki creation. Status hidup tiap pilot._

Cross-ref: [`STATE.md` Next milestones](../STATE.md), [`STATE.md` Challenges Log](../STATE.md), tiap pilot folder di [`experiments/`](../experiments/).

---

## Status overview

| Pilot | Topik | Status | Estimated cost | User effort | Folder |
|---|---|---|---|---|---|
| **#1** | LLM characterization (3 LLM × 100 sampel Jawa) | ✅ DONE 2026-05-25 — gate GREEN (lihat caveat) | $0.85 actual | 0 jam | [`pilot01_llm_characterization/`](../experiments/pilot01_llm_characterization/) |
| **#2** | LLM-as-Jawa-filter + ekstrak subset Jawa-panas | ✅ DONE 2026-05-25 — yield 9.6%, 24 hot (9 hate) | ~$0.05 | 0 jam | [`pilot02_llm_jawa_filter/`](../experiments/pilot02_llm_jawa_filter/) |
| **#3** | Cultural prompt manual iteration v1, v2 (5-10 iter) | 📋 PLANNED | ~$2.50 | 0 jam (saya iterate) | `pilot03_cultural_prompt/` |
| **#4** | AutoResearch loop (Karpathy pattern) | 📋 PLANNED | ~$12.5/run (bounded) | 0 jam (overnight agent) | [`pilot04_autoresearch_prompts/`](../experiments/pilot04_autoresearch_prompts/) |

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

**Status:** ✅ DONE. Detail: [`pilot02_llm_jawa_filter/README.md`](../experiments/pilot02_llm_jawa_filter/README.md), report: [`report.md`](../experiments/pilot02_llm_jawa_filter/report.md).

---

## Pilot #3 — Cultural prompt manual iteration

**Tujuan:** Iterate prompt v0 → v1 → v2 secara manual (5-10 versi) untuk dapat baseline experience + finalize composite metric weights sebelum hand-off ke autonomous Pilot #4.

**Aktivitas saya iterate:**
- Coba variasi few-shot examples (tambah pasemon coverage, tambah krama violent example, dll)
- Variasi system prompt framing (forensik vs sosiolinguistik vs moderasi)
- Variasi schema output JSON

**Output:** Best v1/v2 + insight tentang composite metric weights yang sensible.

**Status:** PLANNED setelah Pilot #1.

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

## Future pilots (potential)

- **Pilot #5:** Bulk labeling 10K (atau gate 3K) pakai best-prompt dari Pilot #4
- **Pilot #6:** BERT/IndoBERT/XLM-R training di auto-labeled data
- **Pilot #7:** Adversarial perturbation testing untuk model robustness

(Update sesuai eksperimen progress + insight baru.)
