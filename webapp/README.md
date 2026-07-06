# Demo UI — Generator & Detector (local only)

Web app buat didemokan (coauthor/reviewer), bukan produk publik. Reuses the same
prompts/clients as `experiments/generation_pilot/` — tidak ada logic baru di-duplikasi.

## Run

```
pip install -r requirements.txt      # nambah flask + openpyxl
python webapp/app.py
```

Buka `http://127.0.0.1:5000`.

## Isi

1. **Taksonomi** — 4 niche register x 9 target SARA (statis, dari `generate.py`).
2. **Generator (live)** — pilih niche/target/model -> panggil LLM sungguhan
   (`deepseek` cloud berbayar kecil; `gemma3:27b`/`qwen3:14b` via Ollama lokal, gratis
   tapi butuh Ollama jalan + model sudah di-pull).
3. **Detector (live)** — teks (dari Generator atau custom) -> jalankan sebagai
   hate-speech judge oleh 1+ LLM (prompt kultural v2), tampilkan verdict per detector +
   ringkasan evasion (blind-spot).
4. **Hasil Riset** — baca `experiments/generation_pilot/detect_report.md` +
   `validation_result.md` (hasil yang SUDAH divalidasi, statis) jadi heatmap/bar chart.

## Catatan

- Tab 2/3 memanggil API sungguhan (biaya kecil untuk deepseek/grok; qwen3/gemma3/gpt-oss
  lokal = gratis via Ollama `localhost:11434`).
- Tidak menyimpan teks yang di-generate/dites ke disk — hanya di memori browser selama
  sesi demo. Tetap ikuti etika `CLAUDE.md` §7: jangan screen-record/sebar teks ofensif
  yang muncul di layar.
- Jalankan di localhost saja; jangan expose ke jaringan publik.
