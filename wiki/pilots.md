# Pilots Index

_Last touched: 2026-05-07 saat wiki creation. Status hidup tiap pilot._

Cross-ref: [`STATE.md` Next milestones](../STATE.md), [`STATE.md` Challenges Log](../STATE.md), tiap pilot folder di [`experiments/`](../experiments/).

---

## Status overview

| Pilot | Topik | Status | Estimated cost | User effort | Folder |
|---|---|---|---|---|---|
| **#1** | LLM characterization (3 LLM × 100 sampel Jawa) | ✅ READY (blocker: install `datasets` + run) | ~$0.50 | 0 jam | [`pilot01_llm_characterization/`](../experiments/pilot01_llm_characterization/) |
| **#2** | LLM-as-Jawa-filter (vs langid baseline) | 📋 PLANNED | ~$0.30 | 0 jam | `pilot02_llm_jawa_filter/` |
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

**Blocker eksekusi:** install `datasets` + `pandas` package, lalu jalankan `run_pilot.py`.

```
.venv\Scripts\python.exe -m pip install datasets pandas
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\run_pilot.py
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\analyze.py
```

**Detail:** [`pilot01_llm_characterization/README.md`](../experiments/pilot01_llm_characterization/README.md).

---

## Pilot #2 — LLM-as-Jawa-filter

**Tujuan:** Test apakah LLM (atau salah satu dari 3 vendor) bisa filter Jawa-vs-non-Jawa lebih reliable dari langid pada raw dump.

**Motivasi:** langid Jawa false-positive tinggi (Jawa low-resource). Kalau LLM bisa filter accurate → pipeline cascade bisa pakai LLM untuk filter, bukan langid.

**Sample:** Mixed pool ~200 sampel dari OSCAR (`id` + `jv` + multilingual web crawl).

**Metric:** Akurasi LLM filter (binary Jawa-vs-non) vs ground truth (langid + manual validation kecil kalau perlu).

**Status:** PLANNED. Folder belum dibuat.

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
