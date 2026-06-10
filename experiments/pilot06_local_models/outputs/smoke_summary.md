# Pilot #6 — Smoke Test Model Lokal

Pool: 12 teks (label cloud: Grok filter + deepseek/grok hate v2).

| Model | Filter valid | Filter agree vs Grok | Hate valid | Hate agree vs ds | vs grok | Latency |
|---|---|---|---|---|---|---|
| qwen3:14b | 100% | 67% | 100% | 92% | 100% | 11418ms |
| qwen2.5:7b-instruct | 100% | 75% | 100% | 83% | 92% | 3353ms |

## Contoh output (kualitatif — cek kualitas Jawa)

### qwen3:14b
- `haipradana-train-10094` bahasa: Grok=campuran / lokal=campuran | hate: ds=False grok=False lokal=False (sev=BUK)
  > Doeloe rezim Orba dollar melambung tinggi hingga Rp 15.000, Pak Harto lengser keprabon. Kondisi yg sama sprt rezim skrg 
- `haipradana-train-10114` bahasa: Grok=campuran / lokal=campuran | hate: ds=True grok=True lokal=True (sev=sedang)
  > Lah ngapa ? Lemes betul tuh congor maz ,sini pake rok'
- `haipradana-train-10142` bahasa: Grok=campuran / lokal=jawa | hate: ds=True grok=True lokal=True (sev=ringan)
  > kaya banci kali ya'
- `haipradana-train-10192` bahasa: Grok=campuran / lokal=jawa | hate: ds=False grok=False lokal=False (sev=BUK)
  > bocah pada ngajak nongton galapremiere, ane tanye pelmnye ape? 'Pengabdi Setan' kate doi pade ane kire dikibulin egataun

### qwen2.5:7b-instruct
- `haipradana-train-10094` bahasa: Grok=campuran / lokal=indonesia | hate: ds=False grok=False lokal=False (sev=BUK)
  > Doeloe rezim Orba dollar melambung tinggi hingga Rp 15.000, Pak Harto lengser keprabon. Kondisi yg sama sprt rezim skrg 
- `haipradana-train-10114` bahasa: Grok=campuran / lokal=campuran | hate: ds=True grok=True lokal=False (sev=BUK)
  > Lah ngapa ? Lemes betul tuh congor maz ,sini pake rok'
- `haipradana-train-10142` bahasa: Grok=campuran / lokal=jawa | hate: ds=True grok=True lokal=True (sev=ringan)
  > kaya banci kali ya'
- `haipradana-train-10192` bahasa: Grok=campuran / lokal=campuran | hate: ds=False grok=False lokal=False (sev=BUK)
  > bocah pada ngajak nongton galapremiere, ane tanye pelmnye ape? 'Pengabdi Setan' kate doi pade ane kire dikibulin egataun
