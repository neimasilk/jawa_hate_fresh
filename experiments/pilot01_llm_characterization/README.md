# Pilot #1 — LLM Characterization

**Tujuan:** Karakterisasi 3 LLM (Claude Opus, GPT-4o, DeepSeek-V3) untuk task klasifikasi ujaran kebencian Bahasa Jawa.

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

Per sampel: ~700 token input × 3 LLM + ~150 token output × 3 LLM = ~2550 token total.
Untuk 100 sampel: ~255K token total.

| LLM | Pricing (in/out per 1M tok) | Cost 100 sampel |
|---|---|---|
| Claude Opus 4.7 | $15 / $75 | ~$2.20 |
| GPT-4o | $2.50 / $10 | ~$0.32 |
| DeepSeek-V3 | $0.27 / $1.10 | ~$0.03 |
| **Total** | | **~$2.55** |

(Harga indikatif; verify saat run.)
