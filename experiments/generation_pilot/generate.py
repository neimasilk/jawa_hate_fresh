"""Generation pilot (2026-06-23, redesigned 2026-06-29): LLM as Javanese hate GENERATOR.

This is the direction the author actually intended from the start (generator, not just
labeler). Generates realistic, REGISTER-STRATIFIED, culturally-grounded Javanese hate
speech for a hate-speech DETECTION research dataset (defensive/academic use), to be
validated for authenticity by the native-expert author.

Design = the matrix that experiments/register_probe/FINDINGS.md §5 asks for:
  NICHE (register-pragmatic mode) x TARGET (SARA group).
Each cell -> one authentic example. Covers the open question N3b-group:
"can authentic SARA-group krama cold-contempt be generated (not just interpersonal)?"

Why per-niche batched calls (not one mega-call): deepseek-v4-pro is a REASONING model.
A single call asking for 12 rich examples consumes the whole token budget on reasoning
and returns EMPTY content (proven 2026-06-29: small request -> 821 reasoning tokens +
valid content; 12-example request -> content empty). One call per register niche keeps
each call's load small and gives within-call diversity across targets.

Grounded in the register-pragmatic findings:
  - allow code-mixing (it is the social-media reality)
  - AVOID archaic/literary "museum krama" (prayogi/dedunung/kitha)
  - for krama, hate = COLD contempt / moral superiority / irony (not hot rage, not dictionary words)

Run: python experiments/generation_pilot/generate.py   (4 DeepSeek calls, a few cents)
Output: generated_pilot.jsonl (one row per generated example, with cell metadata).
Resume-aware: re-running skips niches already present in the output file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.llm_clients import _openai_compat_call

MODEL = "deepseek-v4-pro"
OUT = Path(__file__).parent / "generated_pilot.jsonl"

# --- The stratification matrix -------------------------------------------------

# SARA targets — chosen for cultural breadth (intra-Java, ethnic, religious, gender,
# political-collective). These are GROUP targets so every cell tests SARA-directed hate.
TARGETS = [
    "suku_madura",
    "suku_tionghoa",
    "suku_arab",
    "agama_islam",
    "agama_kristen",
    "gender_wanita",
    "gender_lgbtq",
    "politik_kolektif",
    "intra_jawa_arek_vs_mataraman",
]

# Register-pragmatic niches (FINDINGS.md §1). niche_key, label, guidance.
NICHES = [
    (
        "ngoko_direct",
        "ngoko langsung (panas/kasar)",
        "Serangan TERANG-TERANGAN dan panas dalam ngoko kasar. Umpatan vulgar Jawa boleh "
        "(jancuk, asu, bajingan, dll). Permukaan = isi: langsung menghina kelompok target.",
    ),
    (
        "krama_report",
        "krama ngrasani pihak-ketiga (N2)",
        "Register KRAMA yang sopan di permukaan, tetapi merendahkan kelompok yang TIDAK hadir "
        "(ngrasani / gosip pihak ketiga), sambil tetap hormat kepada lawan bicara. Kebenciannya "
        "ada di ISI proposisi, bukan di nada. Contoh pola: 'Mugi tiyang ... enggal ...'.",
    ),
    (
        "krama_sarcastic",
        "krama ironis / pasemon (N3a)",
        "Register KRAMA yang IRONIS: pujian atau penghormatan berlebihan yang sebenarnya "
        "menghina (mock-deference / pasemon / sindiran). Makna sebenarnya KEBALIKAN dari "
        "permukaannya. Inilah implikatur yang sulit dideteksi mesin.",
    ),
    (
        "krama_cold_contempt",
        "krama contempt-dingin ke KELOMPOK (N3b-group)",
        "Register KRAMA dingin: superioritas moral/hierarkis atas KELOMPOK target (bukan antar "
        "individu). Menuduh kelompok itu tak punya unggah-ungguh / isin / adab, dengan nada "
        "tenang merendahkan. INI yang diuji: bisakah cold-contempt krama diarahkan ke kelompok SARA.",
    ),
]

SYSTEM = (
    "Anda penutur asli Bahasa Jawa (multi-dialek) yang membantu penelitian akademik "
    "DETEKSI ujaran kebencian Bahasa Jawa. Tugas: menghasilkan contoh ujaran kebencian "
    "REALISTIS sebagai data latih untuk sistem moderasi/deteksi (tujuan defensif, bukan "
    "penyebaran). Buat seotentik mungkin seperti orang Jawa sungguhan di media sosial.\n"
    "ATURAN KEASLIAN (WAJIB):\n"
    "- Boleh code-mixing Jawa-Indonesia-Inggris-Arab (itu realita sosmed).\n"
    "- HINDARI kosakata krama sastrawi/kuno yang tak dipakai sehari-hari (mis. prayogi, "
    "dedunung, kitha, pawiyatan). Pakai Jawa HIDUP yang benar-benar dipakai orang.\n"
    "- Jangan default ke krama baku Jawa-Tengah saja; boleh rasa Jawa Timuran/Arek bila cocok.\n"
    "- Teks PENDEK seperti komentar sosmed (1-2 kalimat), bukan paragraf sastra."
)


def build_user(niche_key: str, niche_label: str, guidance: str) -> str:
    targets = "\n".join(f"  - {t}" for t in TARGETS)
    return (
        f"Mode register: **{niche_label}**.\n{guidance}\n\n"
        f"Hasilkan TEPAT {len(TARGETS)} contoh ujaran kebencian dalam mode register ini, "
        f"SATU contoh untuk masing-masing target SARA berikut:\n{targets}\n\n"
        "Setiap contoh harus benar-benar dalam mode register di atas (jangan tergelincir ke "
        "ngoko kalau diminta krama). Variasikan kata/idiom antar contoh.\n\n"
        "Output HANYA JSON array berisi objek, urut sesuai daftar target. Tiap objek:\n"
        '{"target_group": "<salah satu target di atas>", "text": "...", '
        '"register": "ngoko|krama|campur", "severity": "ringan|sedang|berat", '
        '"form": "direct|sarcastic|idiomatic_pasemon|code_switched", '
        '"mekanisme": "1 kalimat: kenapa ini hate + ciri register/pragmatiknya"}'
    )


def gen_call(user: str, tries=(12000, 20000, 30000)):
    """Robust call for a reasoning model: retry with a bigger token budget if the
    content comes back empty or got truncated (finish_reason='length')."""
    last = None
    for mt in tries:
        resp = _openai_compat_call(
            vendor="deepseek", model=MODEL,
            api_key_env="DEEPSEEK_API_KEY", base_url_env="DEEPSEEK_BASE_URL",
            base_url_default="https://api.deepseek.com/v1",
            system=SYSTEM, user=user, max_tokens=mt, temperature=0.8,
        )
        last = resp
        if resp.error:
            print(f"    ! error (max_tokens={mt}): {resp.error}")
            continue
        fr = resp.extra.get("finish_reason")
        if resp.raw_text.strip() and fr != "length":
            return resp
        print(f"    ~ empty/truncated (max_tokens={mt}, finish={fr}, "
              f"out_tok={resp.output_tokens}) -> retry bigger")
    return last


def parse_array(raw: str):
    m = re.search(r"\[.*\]", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    # fallback: collect individual objects
    items = []
    for om in re.finditer(r"\{[^{}]*\}", raw, re.DOTALL):
        try:
            items.append(json.loads(om.group(0)))
        except json.JSONDecodeError:
            continue
    return items


def already_done() -> set[str]:
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["niche"])
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main():
    done = already_done()
    if done:
        print(f"Resume: niches already present -> skip {sorted(done)}")
    all_rows = []
    with OUT.open("a", encoding="utf-8") as f:
        for niche_key, niche_label, guidance in NICHES:
            if niche_key in done:
                continue
            print(f"\n=== NICHE: {niche_key} ({niche_label}) ===")
            resp = gen_call(build_user(niche_key, niche_label, guidance))
            if resp is None or resp.error or not resp.raw_text.strip():
                print(f"  FAILED niche {niche_key}: "
                      f"{resp.error if resp else 'no response'}")
                continue
            items = parse_array(resp.raw_text)
            if not items:
                print(f"  FAILED parse for {niche_key}. Raw head:\n{resp.raw_text[:400]}")
                continue
            for it in items:
                row = {
                    "niche": niche_key,
                    "intended_target": it.get("target_group", "?"),
                    "text": it.get("text", ""),
                    "register": it.get("register", "?"),
                    "severity": it.get("severity", "?"),
                    "form": it.get("form", "?"),
                    "mekanisme": it.get("mekanisme", ""),
                    "model": MODEL,
                }
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                all_rows.append(row)
            print(f"  +{len(items)} examples "
                  f"(latency {resp.latency_ms}ms, out_tok {resp.output_tokens})")

    print(f"\nDone. Wrote {len(all_rows)} new rows this run -> {OUT.name}")
    for r in all_rows:
        print(f"\n[{r['niche']} | {r['intended_target']} | {r['register']}/{r['severity']}]")
        print(f"  TEKS: {r['text']}")
        print(f"  mek : {r['mekanisme']}")


if __name__ == "__main__":
    main()
