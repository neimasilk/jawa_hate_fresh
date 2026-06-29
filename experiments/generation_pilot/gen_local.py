"""Multi-model generation — add the inter-model axis (FINDINGS §5).

Re-runs the SAME 4-niche x 9-target matrix from generate.py with free LOCAL models
(Ollama) so the paper can compare which generator produces authentic Javanese hate.
DeepSeek output lives in generated_pilot.jsonl; local output goes here, tagged by
model, into generated_multimodel.jsonl.

Why this matters: FINDINGS §2 claims LLMs can do authentic krama hate but default to
Central-Java prestige + "museum krama". Comparing a cloud reasoning model (DeepSeek)
vs a big local generalist (gemma3:27b) vs the production rater used as a generator
(qwen3:14b) tells us whether the capability is broad or DeepSeek-specific — and a weak
local result is itself a finding (the uncollectable register needs a strong model).

Resume-aware by (model, niche). Free (local). Run:
  python experiments/generation_pilot/gen_local.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import generate as G
from src.llm_clients import call_ollama

OUT = HERE / "generated_multimodel.jsonl"

# (model, needs /no_think). Both free on the local RTX 4080.
LOCAL_MODELS = [
    ("gemma3:27b", False),
    ("qwen3:14b", True),
]


def gen_call_ollama(user: str, model: str, no_think: bool):
    """Robust local call: retry once if content empty/truncated."""
    suffix = "\n\n/no_think" if no_think else ""
    last = None
    for _ in range(2):
        resp = call_ollama(G.SYSTEM + suffix, user, model=model)
        last = resp
        if resp.error:
            print(f"    ! error ({model}): {resp.error}")
            continue
        fr = resp.extra.get("finish_reason")
        if resp.raw_text.strip() and fr != "length":
            return resp
        print(f"    ~ empty/truncated ({model}, finish={fr}) -> retry")
    return last


def already_done() -> set[tuple[str, str]]:
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                done.add((r["model"], r["niche"]))
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main():
    done = already_done()
    if done:
        print(f"Resume: (model,niche) already present -> skip {len(done)}")
    new_rows = 0
    with OUT.open("a", encoding="utf-8") as f:
        for model, no_think in LOCAL_MODELS:
            for niche_key, niche_label, guidance in G.NICHES:
                if (model, niche_key) in done:
                    continue
                print(f"\n=== {model} | NICHE: {niche_key} ===")
                resp = gen_call_ollama(G.build_user(niche_key, niche_label, guidance), model, no_think)
                if resp is None or resp.error or not resp.raw_text.strip():
                    print(f"  FAILED {model}/{niche_key}: {resp.error if resp else 'no response'}")
                    continue
                items = G.parse_array(resp.raw_text)
                if not items:
                    print(f"  FAILED parse {model}/{niche_key}. Raw head:\n{resp.raw_text[:300]}")
                    continue
                for it in items:
                    row = {
                        "model": model,
                        "niche": niche_key,
                        "intended_target": it.get("target_group", "?"),
                        "text": it.get("text", ""),
                        "register": it.get("register", "?"),
                        "severity": it.get("severity", "?"),
                        "form": it.get("form", "?"),
                        "mekanisme": it.get("mekanisme", ""),
                    }
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                    f.flush()
                    new_rows += 1
                print(f"  +{len(items)} examples (latency {resp.latency_ms}ms, out_tok {resp.output_tokens})")
    print(f"\nDone. {new_rows} new rows -> {OUT.name}")


if __name__ == "__main__":
    main()
