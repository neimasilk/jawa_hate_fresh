# Glossary

_Last touched: 2026-05-07 saat wiki creation. Definisi term yang sering muncul._

Cross-ref: [`PRD.md`](../PRD.md), [`Ujaran Kebencian Jawa_ Riset Mendalam_.md`](../Ujaran%20Kebencian%20Jawa_%20Riset%20Mendalam_.md) untuk konteks panjang.

---

## Bahasa Jawa & sosiolinguistik

### Unggah-ungguh basa
Sistem etiket bertutur Bahasa Jawa yang mengatur pilihan kata + gaya bahasa berdasarkan hubungan sosial penutur, lawan tutur, dan referen. **Bukan sekadar "sopan santun"** — sistem terstruktur kompleks. Termanifestasi dalam tingkatan tutur (speech levels) ngoko/madya/krama dengan sub-varian krama inggil/krama andhap.

Pelanggaran unggah-ungguh = bentuk hate speech struktural yang khas Jawa. Contoh: pronomina ngoko (`kowe`) + verba krama-inggil (`tindak`) untuk lawan tutur yang sama = penghinaan halus.

### Ngoko
Tingkatan tutur dasar/rendah, informal + lugas. Untuk teman sebaya, sangat akrab, atau status sosial lebih rendah. Contoh "makan" = `mangan`. Hate speech ngoko = direct, vulgar, mudah deteksi rule-based.

### Madya
Tingkatan tutur menengah antara ngoko dan krama. Semi-formal, dengan orang yang belum terlalu akrab. Hate speech madya = ambigu, mixed.

### Krama
Tingkatan tutur tinggi/formal, untuk menunjukkan rasa hormat. "Makan" = `nedha`. **Hate speech krama = polite-violent** (bahasa halus, isi keras). Carrier utama hate speech antar-priyayi/antar-tokoh. **Phenomenon yang tidak ada padanan English** — novelty kontribusi.

### Krama inggil
Sub-varian krama "ultra-hormat", untuk meninggikan lawan tutur atau orang ketiga. Tidak pernah digunakan untuk merujuk diri sendiri. "Pergi" = `tindak`. Salah pakai (untuk diri sendiri) = pelanggaran refleksif.

### Krama andhap
Sub-varian krama merendahkan diri, digunakan saat berbicara tentang/kepada orang yang sangat dihormati. Tidak pernah digunakan untuk orang lain.

### Pasemon
Kiasan / sindiran budaya Jawa. Form ujaran kebencian yang implisit dan kontekstual. Contoh: `Tedake maling, yo maling.` ("Keturunan pencuri, ya pencuri") — determinisme silsilah berbasis kiasan.

### Code-switching
Pencampuran bahasa dalam satu ujaran (Jawa-Indo, Jawa-Inggris, Jawa-Arab). Realitas sosmed Jawa real-world. Hate speech code-switched = sering, dataset translasi tidak menangkap.

### SARA
Suku, Agama, Ras, Antargolongan. Kategori yang dilindungi UU ITE Pasal 28(2). Target group dimensi taxonomy proyek ini.

---

## Methodology / framing

### NEIL
**Native-Expert-in-the-Loop.** Protocol awal yang ditulis di PRD §4.2 (sebelum pivot 2026-05-07). Single native domain expert (Bapak) sebagai final adjudicator + LLM ensemble silver labeler + intra-rater κ + external verifier subset + positionality.

**Status:** [deprecated] sejak [D1 framing pivot](decisions.md#d1--framing-pivot-ke-fully-automated-llm-pipeline). Pattern terminology ini tidak dipakai lagi. Section PRD §4.2 yang masih sebut NEIL = legacy.

### Fully Automated LLM Pipeline
Framing post-pivot (sejak [D1](decisions.md#d1--framing-pivot-ke-fully-automated-llm-pipeline)). Tagline: **"Eliminating Human Bottleneck in Low-Resource Hate Speech Annotation"**. Pipeline end-to-end tanpa human di annotation + validation.

### Composite metric (Pilot #4)
Multi-component metric untuk evaluasi prompt variants:
```
composite = w1 * (1 - refusal_rate)        # higher = better
          + w2 * json_validity_rate
          + w3 * inter_llm_alpha
          + w4 * class_entropy_normalized   # avoid all-same labels (gaming)
```
Default `w1=0.3, w2=0.2, w3=0.3, w4=0.2`. Tune setelah Pilot #1+#3.

### Krippendorff's α (alpha)
Statistic untuk mengukur agreement antar rater (atau dalam kita, antar-LLM). Range [-1, 1], 1 = perfect agreement, 0 = chance, <0 = systematic disagreement. Untuk binary nominal: `1 - (observed_disagreement / expected_disagreement)`.

Target Pilot #1: α > 0.5 (acceptable inter-LLM agreement).

### Cultural prompting
Prompt LLM dengan **explicit knowledge injection** tentang konteks budaya target — taxonomy, register awareness, few-shot examples dalam bahasa target, framing instruction yang sosiopragmatik. Lawan dari "generic hate speech detection" prompt (English-centric).

---

## Technical / NLP

### BERT
Bidirectional Encoder Representations from Transformers. Family of pre-trained encoder models. Project ini target fine-tune BERT family di hasil auto-labeled data: IndoBERT, XLM-R, DAPT RoBERTa Javanese (kalau bisa).

### IndoBERT
BERT yang specifically dilatih pada korpus Bahasa Indonesia (Indo4B). Bukan multilingual.

### XLM-R / XLM-RoBERTa
Multilingual encoder pre-trained di Common Crawl 100 bahasa. Stronger dari mBERT karena data lebih besar + bersih.

### IndoBERTweet
IndoBERT yang adapted untuk domain media sosial Twitter Indonesia. Vocabulary cover slang.

### IndoJavE
Pre-trained model yang explicitly handle code-switching Indonesia-Jawa-Inggris.

### BPE
Byte-Pair Encoding. Tokenization algorithm untuk subword units. Karpathy autoresearch pakai BPE 8192-vocab via `rustbpe` library.

### val_bpb
Validation Bits Per Byte. Karpathy autoresearch metric. Vocab-size-independent eval — sums per-token cross-entropy in nats / sums target byte lengths. Kita tidak pakai metric ini (kita classification, bukan LM pretraining), tapi pattern adopsi (single objective, fixed eval) inspirasi untuk composite metric.

### MTL
Multi-Task Learning. Riset mendalam pre-pivot mengusulkan MTL dengan auxiliary task = klasifikasi unggah-ungguh. **Status [deprecated/possible-future]:** PRD §4.3 setelah pivot tidak prioritas — mungkin masuk paper kedua atau section di paper utama kalau pilot sukses.

### XAI (LIME / SHAP)
Explainable AI techniques. LIME = Local Interpretable Model-Agnostic Explanations. SHAP = SHapley Additive exPlanations. Untuk validasi model "benar untuk alasan yang benar" — apakah BERT yang trained di auto-data benar-benar pakai unggah-ungguh signal atau spurious correlation.

---

## Research / venue

### Sinta
Science and Technology Index — sistem pemeringkatan jurnal Indonesia oleh Kemdikbud. Sinta 1 = peringkat tertinggi (skor 85-100), Sinta 6 = peringkat awal (30-40). Kita target Sinta 2 (skor 70-85), KUM first author = 25.

### JINTA
Wait — typo. Yang benar **JINITA**: Journal of Innovation Information Technology and Application, Politeknik Negeri Cilacap. Sinta 2 (berlaku hingga 2028). Venue utama paper kita ([D3](decisions.md#d3--venue-jinita-sinta-2)).

### KUM
Komponen Utama Mengajar/Meneliti — angka kredit untuk karir akademik dosen Indonesia. Project ini target total 55 KUM (paper Sinta 2: 25 + dataset HKI: 15 + codebook HKI: 15).

### HKI
Hak Kekayaan Intelektual. Project ini akan submit dataset + codebook sebagai HKI Karya Cipta (Basis Data + Buku/Spec).

---

## Documentation patterns

### LLM Wiki (Karpathy)
Pattern dari Karpathy gist Apr 2026 — LLM incrementally maintain persistent wiki, bukan retrieve raw on every query. 3-layer: raw sources (immutable) + wiki (LLM-maintained) + schema (CLAUDE.md). 3 ops: ingest, query, lint. **Pattern yang folder `wiki/` ini implement** ([D12](decisions.md#d12--adopsi-pattern-karpathy-llm-wiki-dokumentasi)).

### AutoResearch (Karpathy)
Pattern dari Karpathy repo Mar 2026 — agent autonomously iterate single file (`train.py`) overnight, fixed time budget, single metric, keep/discard via git. **Pattern untuk Pilot #4** ([D11](decisions.md#d11--adopsi-pattern-karpathy-autoresearch-pilot-4)).

---

## Vendor LLM

### DeepSeek V4 Pro
Flagship dari DeepSeek (Apr 2026). Model ID: `deepseek-v4-pro`. 1.6T total / 49B active params. OpenAI-compatible. Pricing tentative: ~$1.00/$3.00 per 1M tokens (in/out).

### Grok 4.3
Flagship dari xAI (Apr 2026). Model ID: `grok-4.3`. 1M context, multimodal, reasoning. OpenAI-compatible. Pricing: $1.25/$2.50 per 1M tokens.

### Kimi K2.6
Flagship open-source dari Moonshot AI (Apr 2026). Model ID: `kimi-k2.6`. 1T MoE / 32B active per token, 262K context. OpenAI-compatible. **Quirk: force `temperature=1.0`** (only value allowed). Pricing tentative: ~$0.30/$1.20 per 1M tokens.

---

## Data sources

### OSCAR
Open Super-large Crawled Aggregated coRpus. Multilingual web crawl. **OSCAR-2301** = versi terbaru, punya `jv` (Javanese) subset. Source data utama untuk Pilot #1.

### CC100
Multilingual corpus dari Common Crawl, 100+ bahasa termasuk Javanese (`jv` code). Recreated untuk pre-training XLM-R. Alternative source untuk Pilot #1/#2.

### Indonesian-hate-speech-superset
HuggingFace `manueltonneau/indonesian-hate-speech-superset` (14,306 posts). Indonesian hate speech aggregate, **tidak include Javanese explicit** tapi mungkin ada code-switched content. Optional fallback source.
