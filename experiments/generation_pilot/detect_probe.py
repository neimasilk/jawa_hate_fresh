"""Detection blind-spot probe AT SCALE.

Systematizes experiments/register_probe/FINDINGS.md §3 (which had only a single
minimal pair) to the full register-stratified matrix: run the PRODUCTION detector
(prompt v2, the Pilot #3 winner) over every generated example with MULTIPLE
detectors, and measure which register-pragmatic niche evades which detector.

Controlled experiment: the generator (DeepSeek) is held constant; the register
NICHE is the manipulated variable. The dependent variable is each detector's
hate=true/false verdict. The hypothesis (FINDINGS §3): explicit propositional
hate (ngoko_direct, krama_report) is caught by all; IMPLICATURE (krama_sarcastic
= irony/pasemon) evades the cheap/local detectors. krama_cold_contempt is the
open question.

Detectors = the production trio (deepseek, grok, qwen3:14b) + two extra free local
models (gemma3:27b big-local, gpt-oss:20b mid-local) to separate "cheap/small" from
"local" from "model-specific" as the cause of the blind spot.

Resume-aware + 429/403-aware (mirrors run_bulk.py). Cheap: 2 cloud detectors x ~36
short texts ~= a few cents; the 3 local detectors are free.

Run: python experiments/generation_pilot/detect_probe.py
Output: detect_results.jsonl (raw) + detect_report.md (tables).
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt
from src.llm_clients import call_deepseek, call_grok, call_ollama

HERE = Path(__file__).parent
GEN = HERE / "generated_pilot.jsonl"
OUT = HERE / "detect_results.jsonl"
PROMPT_PATH = ROOT / "prompts" / "cultural_classification_v2.md"

NICHE_ORDER = ["ngoko_direct", "krama_report", "krama_sarcastic", "krama_cold_contempt"]


def _ollama_caller(model: str, no_think: bool = False):
    suffix = "\n\n/no_think" if no_think else ""

    def fn(system: str, user: str):
        return call_ollama(system + suffix, user, model=model)

    return fn


# (display name, callable). qwen3 needs /no_think (reasoning model).
DETECTORS = [
    ("deepseek", call_deepseek),
    ("grok", call_grok),
    ("qwen3:14b", _ollama_caller("qwen3:14b", no_think=True)),
    ("gemma3:27b", _ollama_caller("gemma3:27b")),
    ("gpt-oss:20b", _ollama_caller("gpt-oss:20b")),
]
DET_NAMES = [n for n, _ in DETECTORS]


def _hate_bool(parsed):
    if not isinstance(parsed, dict):
        return None
    if "_parse_error" in parsed:
        return None
    h = parsed.get("hate")
    if isinstance(h, bool):
        return h
    if isinstance(h, str):
        return h.strip().lower() in ("true", "ya", "yes", "1")
    if isinstance(h, (int, float)):
        return bool(h)
    return None


def already() -> set[tuple[int, str]]:
    done = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            err = (r.get("error") or "").lower()
            if "429" in err or "403" in err or "insufficient" in err or "permission-denied" in err:
                continue
            if (r.get("raw_text") or "").strip() or r.get("error"):
                done.add((r["gen_no"], r["detector"]))
    return done


def run_calls(rows):
    system, user_t = load_prompt_template(PROMPT_PATH)
    done = already()
    if done:
        print(f"Resume: {len(done)} (example, detector) pairs already done")
    total = len(rows) * len(DETECTORS)
    n = 0
    with OUT.open("a", encoding="utf-8") as f:
        for i, r in enumerate(rows, 1):
            user = render_user_prompt(user_t, r["text"])
            for name, callfn in DETECTORS:
                n += 1
                if (i, name) in done:
                    continue
                resp = callfn(system, user)
                parsed = parse_llm_output(resp.raw_text)
                rec = {
                    "gen_no": i,
                    "niche": r["niche"],
                    "intended_target": r["intended_target"],
                    "register": r.get("register"),
                    "text": r["text"],
                    "detector": name,
                    "hate": _hate_bool(parsed),
                    "parsed": parsed if isinstance(parsed, dict) else {"_raw": str(parsed)},
                    "raw_text": resp.raw_text,
                    "error": resp.error,
                    "latency_ms": resp.latency_ms,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                tag = "T" if rec["hate"] else ("F" if rec["hate"] is False else "?")
                print(f"  [{n}/{total}] ex{i:02d} {r['niche'][:16]:16s} {name:12s} -> {tag}"
                      + (f"  ERR {resp.error[:40]}" if resp.error else ""))
                time.sleep(0.15)


def analyze():
    recs = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
    # latest verdict per (gen_no, detector)
    latest = {}
    for r in recs:
        latest[(r["gen_no"], r["detector"])] = r
    recs = list(latest.values())

    by_nd = defaultdict(lambda: {"caught": 0, "valid": 0, "noverdict": 0})
    niches, targets = [], []
    for r in recs:
        if r["niche"] not in niches:
            niches.append(r["niche"])
        if r["intended_target"] not in targets:
            targets.append(r["intended_target"])
        cell = by_nd[(r["niche"], r["detector"])]
        if r["hate"] is None:
            cell["noverdict"] += 1
        else:
            cell["valid"] += 1
            if r["hate"]:
                cell["caught"] += 1

    niches = [n for n in NICHE_ORDER if n in niches] + [n for n in niches if n not in NICHE_ORDER]

    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))
    P("# Detection blind-spot probe — register x detector (at scale)\n")
    P("Production detector = prompt v2 (Pilot #3 winner). Generator held constant (DeepSeek).")
    P("Manipulated variable = register-pragmatic niche. Cell = hate-detection rate "
      "(caught / valid verdicts). Higher = detector flags it as hate; LOW = it EVADES detection.\n")

    P("## Detection rate by niche x detector\n")
    header = "| niche \\ detector | " + " | ".join(DET_NAMES) + " |"
    P(header)
    P("|" + "---|" * (len(DET_NAMES) + 1))
    for niche in niches:
        cells = []
        for d in DET_NAMES:
            c = by_nd.get((niche, d))
            if not c or c["valid"] == 0:
                cells.append("–")
            else:
                cells.append(f"{c['caught']}/{c['valid']} ({c['caught']/c['valid']:.0%})")
        P(f"| {niche} | " + " | ".join(cells) + " |")
    P("")

    # detector-level overall + the implicature gap
    P("## Per-detector summary\n")
    P("| detector | overall caught | ngoko_direct | krama_report | krama_sarcastic | krama_cold_contempt |")
    P("|---|---|---|---|---|---|")
    for d in DET_NAMES:
        tot_c = tot_v = 0
        rates = {}
        for niche in NICHE_ORDER:
            c = by_nd.get((niche, d))
            if c and c["valid"]:
                tot_c += c["caught"]
                tot_v += c["valid"]
                rates[niche] = f"{c['caught']/c['valid']:.0%}"
            else:
                rates[niche] = "–"
        overall = f"{tot_c}/{tot_v} ({tot_c/tot_v:.0%})" if tot_v else "–"
        P(f"| {d} | {overall} | " + " | ".join(rates.get(n, "–") for n in NICHE_ORDER) + " |")
    P("")

    # no-verdict / parse-failure accounting (honesty)
    P("## Verdict coverage (parse/refusal failures)\n")
    P("| detector | valid verdicts | no-verdict (parse fail/empty/refusal) |")
    P("|---|---|---|")
    for d in DET_NAMES:
        v = sum(c["valid"] for (n, dd), c in by_nd.items() if dd == d)
        nv = sum(c["noverdict"] for (n, dd), c in by_nd.items() if dd == d)
        P(f"| {d} | {v} | {nv} |")
    P("")

    # the headline finding: where do detectors disagree most? = the evasive examples
    P("## Most-evasive examples (detectors split / mostly missed)\n")
    perex = defaultdict(dict)
    meta = {}
    for r in recs:
        perex[r["gen_no"]][r["detector"]] = r["hate"]
        meta[r["gen_no"]] = r
    scored = []
    for no, verds in perex.items():
        vals = [v for v in verds.values() if v is not None]
        if not vals:
            continue
        caught = sum(1 for v in vals if v)
        scored.append((caught / len(vals), no, caught, len(vals)))
    scored.sort()  # lowest detection rate first
    P("| detection rate | niche | target | text | per-detector (T/F/?) |")
    P("|---|---|---|---|---|")
    for rate, no, caught, nval in scored[:12]:
        m = meta[no]
        verds = perex[no]
        pd = " ".join(f"{d[:6]}:{'T' if verds.get(d) else ('F' if verds.get(d) is False else '?')}" for d in DET_NAMES)
        txt = m["text"][:70].replace("|", "/")
        P(f"| {caught}/{nval} | {m['niche']} | {m['intended_target']} | {txt} | {pd} |")
    P("")

    P("## Interpretation\n")
    P("- ngoko_direct ~ all detectors high = explicit hostile content is easy (control).")
    P("- krama_report high too => politeness alone does NOT blind detectors (explicit propositional hate wins) — confirms FINDINGS §3 at scale.")
    P("- krama_sarcastic LOW for cheap/local detectors => IMPLICATURE (irony/pasemon) is the blind spot.")
    P("- Compare qwen3:14b vs gemma3:27b vs gpt-oss:20b: if the gap tracks size/quality not locality, the blind spot is a capability limit, not a cloud-vs-local artifact.")
    P("- krama_cold_contempt rate answers: is morally-superior cold contempt detected as hate, or does its calm surface evade?")

    (HERE / "detect_report.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


def main():
    if not GEN.exists():
        print(f"Missing {GEN}. Run generate.py first.")
        return
    rows = [json.loads(l) for l in GEN.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"Probing {len(rows)} generated examples x {len(DETECTORS)} detectors "
          f"= {len(rows) * len(DETECTORS)} calls.\n")
    run_calls(rows)
    print("\n=== ANALYSIS ===\n")
    analyze()


if __name__ == "__main__":
    main()
