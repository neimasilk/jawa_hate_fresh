# Pilot #6 — Model Lokal (Ollama) sebagai Pengganti Vendor Cloud

**Motivasi:** kredit xAI/Grok mahal (filter 12.7K ≈ $14). Model lokal di RTX 4080 (16GB) = gratis setelah setup, dan vendor independen yang sah untuk cross-LLM consensus. **Bonus paper:** memakai model open region-specific Jawa (SEA-LION) memperkuat narasi cultural grounding + reproducibility (siapa pun bisa jalankan tanpa biaya API).

## Kandidat (muat di RTX 4080 16GB)

| Model | Ukuran (Q5) | Catatan |
|---|---|---|
| **SEA-LION v3.5-8B-R** (AI Singapore) | 5.7GB | Instruction-tuned **Jawa & Sunda eksplisit**, hybrid reasoning, 128k ctx, TIDAK safety-aligned (nol refusal — bagus utk hate). Standout kultural. |
| **Qwen3 14B** | 9.3GB | Generalis kuat, JSON andal, multilingual. Pembanding kapabilitas. |
| Gemma 4 26B MoE / gemma3:27b | 17GB | Paling capable tapi mepet/luber → lambat. Cadangan. |

## Strategi (hemat maksimal)

- **Filter (12.7K call, tugas mudah = deteksi bahasa)** → paling cocok di-offload ke lokal (SEA-LION Jawa-native). Hemat ~$9.50 Grok. Tidak mengganggu α consensus (filter divalidasi terpisah).
- **Labeling/consensus** → model lokal yang IKUT consensus WAJIB re-validasi α (v2 0.763 = deepseek+grok). Opsi: tetap cloud, ATAU tambah lokal sbg rater ke-3 (triangulasi lokal+cloud).

## smoke_test.py

Uji cepat ~12 teks berlabel cloud, 2 tugas (filter + hate v2), metrik: JSON valid %, agreement vs Grok (filter) & vs deepseek/grok (hate), latency, contoh output (kualitas Jawa kualitatif).

```
$env:SMOKE_MODELS="aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m,qwen3:14b"
.venv\Scripts\python experiments\pilot06_local_models\smoke_test.py
```
→ `outputs/smoke_summary.md` + log per model.

## Gate keputusan

- **Filter:** JSON valid >90% + agree vs Grok >80% → lokal layak ganti Grok di filter.
- **Hate (kalau mau masuk consensus):** JSON valid >90% + agreement masuk akal → lanjut re-validasi α penuh di pool 149.

## Hasil smoke test (12 teks, 2026-06-10)

| Model | Filter valid | Filter agree (keep) | Hate valid | Hate vs ds | vs grok | Latency |
|---|---|---|---|---|---|---|
| qwen3:14b (thinking) | 100% | 67% | 100% | 83% | 92% | 60.7s |
| **qwen3:14b (/no_think)** | 100% | 67% | 100% | **92%** | **100%** | **11.4s** |
| qwen2.5:7b-instruct | 100% | 75% | 100% | 83% | 92% | **3.4s** |

**Temuan:**
- **Hate classification (consensus-critical): local KUAT.** qwen3 no_think reproduksi aturan v2 tepat (`banci`→gender_lgbtq, slur identitas). JSON 100% valid.
- **Filter: local lebih ceroboh.** qwen2.5 lewatkan penanda Jawa nyata (`lengser keprabon`, `wong`), `penanda_jawa` banyak halusinasi. Kategori bahasa mostly benar tapi ~25% borderline akan ke-drop. Untuk filter, kualitas < Grok.
- **`/no_think` wajib** untuk reasoning model (qwen3 61s→11s). qwen2.5 (non-reasoning) tercepat 3.4s.

## Validasi consensus (149 pool)

`run_local_consensus.py`: jalankan model lokal prompt v2 di 149 pool → α(deepseek, lokal) vs pembanding α(deepseek, grok)=0.763. Pakai ulang label deepseek v2 yang ada → cuma butuh run lokal (gratis).

## Status

| Tahap | Status |
|---|---|
| `call_ollama` + `/no_think` support | ✅ |
| Smoke test qwen3 + qwen2.5 | ✅ — local kuat di hate, ceroboh di filter |
| Validasi α(deepseek, qwen3-local) di 149 | 🔄 running |
| Pull SEA-LION v3.5-8B-R | 🔄 downloading (lambat) |
| Validasi α SEA-LION | ⏳ tunggu pull |
| Keputusan vendor mix final | ⏳ tunggu α |
