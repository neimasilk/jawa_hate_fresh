"""Register blind-spot probe (2026-06-23).

Tests whether our zero-human LLM labeling pipeline (DeepSeek + Grok + qwen3, prompt v2)
detects POLITE-SURFACE Javanese hate (krama) as well as it detects coarse (ngoko) hate.

Minimal pair: the SAME hateful meaning (Madurese are coarse / should be excluded),
rendered in three register-pragmatic configurations identified with the native expert:
  - ngoko direct          (coarse, surface=hostile)      -> control, should be caught
  - krama third-party      (polite to listener, derogates absent group)
  - krama sarcastic        (mock-praise; surface looks like PRAISE) -> the hard case

If the krama variants get hate=false while ngoko gets hate=true, the pipeline has a
register blind spot exactly at the culturally-unique Javanese phenomenon.

Run: python experiments/register_probe/blindspot_test.py
(Uses DeepSeek + Grok API + local qwen3. ~9 calls, a few cents.)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.cultural_prompt import load_prompt_template, render_user_prompt, parse_llm_output
from src.llm_clients import call_deepseek, call_grok, call_ollama

PROMPT_V2 = ROOT / "prompts" / "cultural_classification_v2.md"

# Same hateful proposition, three register-pragmatic renderings (target: suku_madura)
STIMULI = {
    "ngoko_direct": "Wong Madura kuwi kabeh watake kasar, ora usah manggon nang kuthaku, gawe rusuh wae.",
    "krama_report": ("Mbok bilih langkung prayogi menawi tiyang Madura menika boten sami dedunung "
                     "wonten ing kitha kula, awit watakipun asring kasar saha asring damel resahing "
                     "masarakat ingkang sampun ayem tentrem."),
    "krama_sarkastik": ("Inggih, tiyang Madura menika pancen kawentar gagah prakosa, ngantos "
                        "sabendinten mesthi mbekta clurit kangge njagi paseduluran. Sae sanget, ta."),
    # 3 contoh DeepSeek yang dinilai native-expert "sangat bagus" (interpersonal cold-contempt, no group)
    "ds_coldcontempt_1": "Panjenengan punika tiyang ingkang boten gadhah unggah-ungguh.",
    "ds_coldcontempt_2": "Kula mboten sami kaliyan panjenengan ingkang asor.",
    "ds_coldcontempt_3": "Menapa panjenengan mboten gadhah isin?",
}

VENDORS = [("deepseek", call_deepseek), ("grok", call_grok), ("qwen3", call_ollama)]


def main():
    system, user_t = load_prompt_template(PROMPT_V2)
    print(f"{'stimulus':<16} {'vendor':<9} {'hate':<6} {'severity':<8} reasoning")
    print("-" * 100)
    for key, text in STIMULI.items():
        for vname, fn in VENDORS:
            try:
                resp = fn(system, render_user_prompt(user_t, text))
                if resp.error:
                    print(f"{key:<16} {vname:<9} ERROR {resp.error[:40]}")
                    continue
                p = parse_llm_output(resp.raw_text)
                hate = p.get("hate")
                sev = p.get("severity", "?")
                reason = (p.get("reasoning") or "")[:70]
                print(f"{key:<16} {vname:<9} {str(hate):<6} {str(sev):<8} {reason}")
            except Exception as e:
                print(f"{key:<16} {vname:<9} EXC {str(e)[:50]}")
        print()


if __name__ == "__main__":
    main()
