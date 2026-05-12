# HANDOFF - Ujaran Kebencian Jawa

**Last updated:** 2026-05-12, setelah eksekusi awal Pilot #1.
**Tujuan:** sesi baru langsung tahu status terbaru, blocker, dan next action.

---

## TL;DR

Riset tetap pada framing **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"** untuk paper JINITA Sinta 2 + dataset/codebook HKI. Pilot #1 sudah dijalankan 300 call awal, tetapi hasil report pertama **belum valid sebagai keputusan metodologis** karena masalah teknis output kosong dari Kimi/DeepSeek akibat `finish_reason='length'`. Patch retry + token limit sudah dibuat; next action adalah **rerun resume Pilot #1 setelah patch**, lalu regenerate report.

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

Yang sudah selesai:
- Dependency `datasets` dan `pandas` sudah terpasang di `.venv`.
- OSCAR-2301 ternyata **gated** di Hugging Face, tidak bisa diakses tanpa autentikasi.
- Pilot #1 dipatch agar fallback ke `HuggingFaceFW/fineweb-2`, config `jav_Latn`.
- Sampel 100 teks berhasil dibuat di `experiments/pilot01_llm_characterization/outputs/pilot01_samples.json`.
- 300 call awal selesai, tersimpan di `outputs/pilot01_responses.jsonl`.
- `report.md` awal sudah dibuat.

Temuan penting:
- Log berisi 302 record, bukan 300, karena ada 2 duplikasi dari proses resume timeout.
- Tidak ada API error dan refusal rate 0%.
- Banyak output kosong dengan `finish_reason='length'`: Kimi 98 record, DeepSeek 5 record.
- Report awal memberi gate RED karena JSON validity rendah, tetapi ini **kemungkinan besar artefak `max_tokens` terlalu kecil**, bukan bukti LLM gagal memahami task.

Patch yang sudah dibuat tetapi belum rerun:
- `src/llm_clients.py`: `max_tokens` DeepSeek dinaikkan ke 2048, Kimi ke 4096.
- `experiments/pilot01_llm_characterization/run_pilot.py`: resume sekarang hanya menganggap record selesai kalau `raw_text` tidak kosong atau ada `error`; output kosong akan di-retry.
- `experiments/pilot01_llm_characterization/analyze.py`: deduplicate `(source_id, vendor)` dan print ASCII-safe untuk Windows console.

---

## Next Concrete Action

Jalankan ulang resume Pilot #1:

```powershell
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\run_pilot.py
.venv\Scripts\python.exe experiments\pilot01_llm_characterization\analyze.py
```

Ekspektasi:
- Skrip akan skip record yang sudah valid.
- Skrip akan retry record kosong, terutama Kimi dan sebagian DeepSeek.
- Setelah itu baca ulang `report.md`; baru tentukan GREEN/YELLOW/RED.

Kalau Kimi masih kosong setelah `max_tokens=4096`, next debug:
- cek apakah provider butuh parameter khusus untuk reasoning output,
- turunkan prompt verbosity khusus Kimi,
- atau jalankan Pilot #1 analysis sementara dengan DeepSeek + Grok saja sebagai diagnostic, bukan keputusan final.

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
