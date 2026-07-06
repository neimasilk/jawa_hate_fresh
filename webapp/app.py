"""Demo web UI — Javanese hate-speech GENERATOR + LLM-DETECTOR pipeline.

Local-only Flask app for demoing the research pipeline (register-stratified
generation matrix + LLM-as-detector blind-spot probe) to coauthors/reviewers.
Reuses the same clients/prompts as the pilot scripts under experiments/generation_pilot/
and src/ — no separate prompt-engineering logic lives here.

Ethics: generated text is synthetic, offensive-by-construction, for hate-speech
DETECTION research only (see CLAUDE.md §7). This app is meant to run on localhost
for a live demo, not to be deployed/exposed publicly.

Run: python webapp/app.py   (http://127.0.0.1:5000)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments" / "generation_pilot"))

from src.cultural_prompt import load_prompt_template, parse_llm_output, render_user_prompt
from src.llm_clients import call_deepseek, call_grok, call_ollama
import generate as genmod  # NICHES, TARGETS, SYSTEM, gen_call() — the real generator pilot code

GEN_DIR = ROOT / "experiments" / "generation_pilot"
DETECT_REPORT = GEN_DIR / "detect_report.md"
VALIDATION_RESULT = GEN_DIR / "validation_result.md"
PROMPT_V2 = ROOT / "prompts" / "cultural_classification_v2.md"

NICHE_MAP = {key: (key, label, guidance) for key, label, guidance in genmod.NICHES}
TARGETS = genmod.TARGETS

CLOUD_DETECTORS = {"deepseek": call_deepseek, "grok": call_grok}
LOCAL_DETECTOR_MODELS = ["qwen3:14b", "gemma3:27b", "gpt-oss:20b"]
GEN_MODELS = ["deepseek", "gemma3:27b", "qwen3:14b"]

app = Flask(__name__, static_folder="static", static_url_path="")


# --- helpers ----------------------------------------------------------------

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


def parse_single_object(raw: str) -> dict | None:
    """Parse one JSON object out of an LLM response (tolerates prose/fences)."""
    cleaned = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1).strip()
    m = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def build_single_user(niche_label: str, guidance: str, target: str) -> str:
    return (
        f"Mode register: **{niche_label}**.\n{guidance}\n\n"
        f"Hasilkan TEPAT 1 contoh ujaran kebencian dalam mode register ini, "
        f"untuk target SARA: {target}.\n\n"
        "Output HANYA JSON object (bukan array), tanpa teks lain:\n"
        '{"target_group": "' + target + '", "text": "...", '
        '"register": "ngoko|krama|campur", "severity": "ringan|sedang|berat", '
        '"form": "direct|sarcastic|idiomatic_pasemon|code_switched", '
        '"mekanisme": "1 kalimat: kenapa ini hate + ciri register/pragmatiknya"}'
    )


def parse_md_tables(md_text: str) -> dict[str, list[list[str]]]:
    """Split a report.md into {section title: [row cells, ...]} using '## Title'
    headers and pipe-table rows (separator rows like |---|---| are dropped)."""
    sections: dict[str, list[list[str]]] = {}
    title = None
    rows: list[list[str]] = []
    for line in md_text.splitlines():
        if line.startswith("## "):
            if title is not None:
                sections[title] = rows
            title = line[3:].strip()
            rows = []
        elif line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue  # separator row
            rows.append(cells)
    if title is not None:
        sections[title] = rows
    return sections


# --- static frontend ---------------------------------------------------------

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# --- API ----------------------------------------------------------------

@app.get("/api/taxonomy")
def api_taxonomy():
    return jsonify(
        niches=[{"key": k, "label": lbl, "guidance": g} for k, lbl, g in genmod.NICHES],
        targets=TARGETS,
        gen_models=GEN_MODELS,
        detectors={"cloud": list(CLOUD_DETECTORS), "local": LOCAL_DETECTOR_MODELS},
    )


@app.post("/api/generate")
def api_generate():
    data = request.get_json(force=True) or {}
    niche_key = data.get("niche")
    target = data.get("target")
    model = data.get("model", "deepseek")

    niche = NICHE_MAP.get(niche_key)
    if not niche or target not in TARGETS or model not in GEN_MODELS:
        return jsonify(error="invalid niche/target/model"), 400
    _, niche_label, guidance = niche
    user = build_single_user(niche_label, guidance, target)

    if model == "deepseek":
        resp = genmod.gen_call(user)  # reuses the reasoning-model truncation-retry logic
    else:
        suffix = "\n\n/no_think" if model == "qwen3:14b" else ""
        resp = call_ollama(genmod.SYSTEM + suffix, user, model=model)

    if resp is None or resp.error:
        return jsonify(error=(resp.error if resp else "no response")), 502
    obj = parse_single_object(resp.raw_text)
    if not obj:
        return jsonify(error="could not parse LLM output", raw=resp.raw_text[:500]), 502

    return jsonify(
        model=model, niche=niche_key,
        text=obj.get("text", ""), register=obj.get("register", "?"),
        severity=obj.get("severity", "?"), form=obj.get("form", "?"),
        mekanisme=obj.get("mekanisme", ""), latency_ms=resp.latency_ms,
    )


@app.post("/api/detect")
def api_detect():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    detectors = data.get("detectors") or ["deepseek", "grok"]
    if not text:
        return jsonify(error="empty text"), 400

    system, user_t = load_prompt_template(PROMPT_V2)
    user = render_user_prompt(user_t, text)

    results = []
    for d in detectors:
        if d in CLOUD_DETECTORS:
            resp = CLOUD_DETECTORS[d](system, user)
        elif d in LOCAL_DETECTOR_MODELS:
            suffix = "\n\n/no_think" if d == "qwen3:14b" else ""
            resp = call_ollama(system + suffix, user, model=d)
        else:
            continue
        parsed = parse_llm_output(resp.raw_text)
        results.append({
            "detector": d,
            "hate": _hate_bool(parsed),
            "target_group": parsed.get("target_group") if isinstance(parsed, dict) else None,
            "severity": parsed.get("severity") if isinstance(parsed, dict) else None,
            "reasoning": parsed.get("reasoning") if isinstance(parsed, dict) else None,
            "error": resp.error,
            "latency_ms": resp.latency_ms,
        })
    return jsonify(results=results)


@app.get("/api/dashboard")
def api_dashboard():
    out = {}
    if DETECT_REPORT.exists():
        sec = parse_md_tables(DETECT_REPORT.read_text(encoding="utf-8", errors="replace"))
        out["detection_by_niche"] = sec.get("Detection rate by niche x detector")
        out["detector_summary"] = sec.get("Per-detector summary")
    if VALIDATION_RESULT.exists():
        text = VALIDATION_RESULT.read_text(encoding="utf-8", errors="replace")
        sec = parse_md_tables(text)
        out["authenticity_by_niche"] = sec.get("Per niche (register-pragmatic axis)")
        out["authenticity_by_model"] = sec.get("Per model (which generator is the better source?)")
        out["model_x_niche"] = sec.get("Model x niche authenticity rate")
        out["evasion_cross_tab"] = sec.get(
            "Detector-evasion x native authenticity (the headline cross-tab)"
        )
        m = re.search(r"Scored \*\*(\d+)/(\d+) = (\d+)%\*\*", text)
        if m:
            out["overall"] = {"authentic": int(m.group(1)), "total": int(m.group(2)), "pct": int(m.group(3))}
    return jsonify(out)


if __name__ == "__main__":
    print("Demo UI: http://127.0.0.1:5000  (Ctrl+C to stop)")
    app.run(debug=True, port=5000)
