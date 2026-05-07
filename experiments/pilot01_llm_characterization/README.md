# Pilot #1 — LLM Characterization

**Tujuan:** Karakterisasi 3 LLM (DeepSeek V4 Pro, Grok 4.3, Kimi K2.6) untuk task klasifikasi ujaran kebencian Bahasa Jawa. Semua OpenAI-compatible API.

**Output yang ingin diukur:**
1. **Refusal rate** per LLM — seberapa sering LLM menolak engage dengan konten hate speech (over-cautious safety)
2. **Output validity** per LLM — seberapa sering output JSON parseable dengan field lengkap
3. **Inter-LLM agreement** — Krippendorff's α (untuk severity, register; nominal untuk hate/non-hate)
4. **Latency + token usage + biaya** per LLM
5. **Qualitative observations** — pola error, kata yang trigger refusal, dll

**Sample size:** 100 sampel dari OSCAR-2301 `jv` subset (random + light keyword pre-filter untuk variety).

**Decision gate (post-pilot):**
- Refusal rate < 20% + JSON validity > 90% + α > 0.5 → **lanjut fully-LLM framing**
- Marginal di salah satu metric → iterasi prompt (pilot #3) sebelum scale
- Buruk di semua → trigger fallback ladder (sanity check 50 sampel atau pending)

## File

- `run_pilot.py` — main script: load 100 sampel → call 3 LLMs × cultural prompt → log raw + parsed → save
- `analyze.py` — compute metrics dari log (refusal, validity, agreement, cost)
- `report.md` — pilot report (di-generate setelah analyze.py jalan)
- `outputs/` — raw LLM responses (JSON Lines, per-sample × per-vendor)

## Cara jalan

```
# 1. Pastikan .env sudah ada API keys (lihat .env.example di root)
# 2. Install deps
pip install -r requirements.txt

# 3. Run pilot (estimasi: ~5-10 menit, ~$1-2 cost)
python experiments/pilot01_llm_characterization/run_pilot.py

# 4. Analyze
python experiments/pilot01_llm_characterization/analyze.py
```

## Estimasi cost

Per sampel: ~700 token input × 3 LLM + ~200-400 token output × 3 LLM (output bervariasi karena reasoning models).
Untuk 100 sampel: ~210K input + ~60-120K output total.

| LLM | Pricing (in/out per 1M tok, **tentative**) | Cost 100 sampel (rough) |
|---|---|---|
| DeepSeek V4 Pro | $1.00 / $3.00 | ~$0.20 |
| Grok 4.3 | $1.25 / $2.50 | ~$0.20 |
| Kimi K2.6 | $0.30 / $1.20 | ~$0.07 |
| **Total** | | **~$0.50** |

(DeepSeek V4 + Kimi pricing placeholder — verify post-run dari actual usage. Grok verified per xAI Apr 2026.)

## Connectivity test (pre-pilot)

Per 2026-05-07: ketiga API verified alive (`scripts/test_apis.py`):
- DeepSeek V4 Pro: ~12s latency, paham Jawa krama
- Grok 4.3: ~17s latency, paham Jawa krama
- Kimi K2.6: ~7s latency, paham Jawa krama (note: Kimi force `temperature=1.0`)
