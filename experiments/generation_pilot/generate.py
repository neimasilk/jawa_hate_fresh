"""Generation pilot (2026-06-23): LLM as Javanese hate-speech GENERATOR.

This is the direction the author actually intended from the start (generator, not just
labeler). Generates realistic, register-stratified, culturally-grounded Javanese hate
speech for a hate-speech DETECTION research dataset (defensive/academic use), to be
validated for authenticity by the native-expert author.

Grounded in the register-pragmatic findings (experiments/register_probe/FINDINGS.md):
  - allow code-mixing (it is the social-media reality)
  - AVOID archaic/literary "museum krama" (prayogi/dedunung/kitha)
  - for krama, hate = COLD contempt / moral superiority / sarcasm (not hot rage, not dictionary words)

Run: python experiments/generation_pilot/generate.py   (one DeepSeek call, a few cents)
Output: prints generated examples + writes generated_pilot.jsonl for native validation.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.llm_clients import call_deepseek, _openai_compat_call

N = 12

SYSTEM = (
    "Anda penutur asli Bahasa Jawa (multi-dialek) yang membantu penelitian akademik "
    "DETEKSI ujaran kebencian Bahasa Jawa. Tugas: menghasilkan contoh ujaran kebencian "
    "REALISTIS sebagai data latih untuk sistem moderasi/deteksi (tujuan defensif, bukan "
    "penyebaran). Buat seotentik mungkin seperti orang Jawa sungguhan di media sosial.\n"
    "ATURAN KEASLIAN:\n"
    "- Boleh code-mixing Jawa-Indonesia-Inggris-Arab (itu realita sosmed).\n"
    "- HINDARI kosakata krama sastrawi/kuno yang tak dipakai sehari-hari (mis. prayogi, "
    "dedunung, kitha). Pakai Jawa HIDUP.\n"
    "- Untuk register krama: kebencian muncul sebagai CONTEMPT DINGIN / superioritas moral / "
    "sindiran halus (pasemon) — BUKAN amukan, BUKAN kata kamus kuno.\n"
    "- Untuk ngoko: boleh kasar/langsung/vulgar (umpatan).\n"
    "- Hate = menyerang kelompok identitas (SARA): suku/etnis, agama, gender/orientasi, politik kolektif."
)

USER = (
    f"Hasilkan {N} contoh ujaran kebencian Bahasa Jawa, BERAGAM. Variasikan:\n"
    "- target SARA: suku_madura, suku_tionghoa, suku_arab, agama_islam, agama_kristen, "
    "gender_wanita, gender_lgbtq, politik_partai, intra_jawa_arek/mataraman.\n"
    "- register: 'ngoko' (langsung/kasar), 'krama' (cold-contempt/sarkastik), 'campur_kasar'.\n"
    "- form: direct, sarcastic, idiomatic_pasemon, code_switched.\n"
    "Sertakan minimal 4 contoh register krama (mode contempt/sarkastik, otentik bukan museum).\n\n"
    "Output HANYA JSON array. Tiap objek:\n"
    '{"text": "...", "target_group": ["..."], "register": "...", "severity": "ringan|sedang|berat", '
    '"form": "...", "mekanisme": "1 kalimat: kenapa ini hate + ciri register-nya"}'
)


def main():
    # NB: deepseek-v4-pro is a REASONING model — with max_tokens=2048 (the call_deepseek
    # default) all tokens were consumed by reasoning and content came back EMPTY
    # (output_tokens=2048, len=0). Use a large budget so the answer survives.
    resp = _openai_compat_call(
        vendor="deepseek", model="deepseek-v4-pro",
        api_key_env="DEEPSEEK_API_KEY", base_url_env="DEEPSEEK_BASE_URL",
        base_url_default="https://api.deepseek.com/v1",
        system=SYSTEM, user=USER, max_tokens=8192,
    )
    if resp.error:
        print("ERROR:", resp.error)
        return
    raw = resp.raw_text
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if not m:
        print("No JSON array found. Raw:\n", raw[:1000])
        return
    try:
        items = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        print("JSON parse error:", e, "\nRaw:\n", raw[:1000])
        return

    out = Path(__file__).parent / "generated_pilot.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"Generated {len(items)} examples (deepseek). -> {out.name}\n")
    for i, it in enumerate(items, 1):
        print(f"{i}. [{it.get('register','?')}/{','.join(it.get('target_group',[]))}/{it.get('severity','?')}]")
        print(f"   TEKS: {it.get('text','')}")
        print(f"   mekanisme: {it.get('mekanisme','')}\n")


if __name__ == "__main__":
    main()
