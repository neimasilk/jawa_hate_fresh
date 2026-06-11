# Pilot #6b — Validasi filter lokal vs Grok

Sampel stratified n=300 (150 keep / 150 drop), seed 42. no_think=True.

| Model | JSON valid | keep-recall | drop-agree | latency med |
|---|---|---|---|---|
| aisingapore/Llama-SEA-LION-v3.5-8B-R:q5_k_m | 300/300 | 76% (n=150) | 65% (n=150) | 3.5s |
| qwen3:14b | 300/300 | 77% (n=150) | 75% (n=150) | 10.5s |

**Interpretasi:** keep-recall rendah = pool hilang (false negative, tidak terpulihkan); drop-agree rendah = pool kotor (false positive, termitigasi verifikasi Grok murah di tahap keep). Pilih model dengan keep-recall tertinggi; latency tie-breaker.