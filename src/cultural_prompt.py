"""Loader cultural prompt template + parser output JSON."""
from __future__ import annotations

import json
import re
from pathlib import Path

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "cultural_classification_v0.md"

# Marker untuk extract sections dari markdown prompt file
SYSTEM_MARKER_START = "## System prompt"
USER_MARKER_START = "## User prompt template"
NEXT_SECTION_MARKER = "## Catatan iterasi"


def _extract_code_block(section: str) -> str:
    match = re.search(r"```\n(.*?)\n```", section, re.DOTALL)
    if not match:
        raise ValueError(f"No code block found in section:\n{section[:200]}")
    return match.group(1).strip()


def load_prompt_template(path: Path = PROMPT_PATH) -> tuple[str, str]:
    """Return (system, user_template). user_template berisi {TEXT_PLACEHOLDER}."""
    raw = path.read_text(encoding="utf-8")

    sys_start = raw.index(SYSTEM_MARKER_START)
    user_start = raw.index(USER_MARKER_START, sys_start)
    next_section = raw.index(NEXT_SECTION_MARKER, user_start)

    system_section = raw[sys_start:user_start]
    user_section = raw[user_start:next_section]

    system = _extract_code_block(system_section)
    user_template = _extract_code_block(user_section)

    if "{TEXT_PLACEHOLDER}" not in user_template:
        raise ValueError("User prompt missing {TEXT_PLACEHOLDER}")

    return system, user_template


def render_user_prompt(user_template: str, text: str) -> str:
    return user_template.replace("{TEXT_PLACEHOLDER}", text)


def parse_llm_output(raw_text: str) -> dict:
    """Coba parse output LLM jadi dict.

    LLM kadang wrap JSON dalam ```json ... ``` atau prefix narasi.
    Kembalikan dict dengan key '_parse_error' kalau gagal.
    """
    if not raw_text or not raw_text.strip():
        return {"_parse_error": "empty_response"}

    # Strip markdown fences kalau ada
    cleaned = raw_text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    # Find first { ... } block
    obj_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not obj_match:
        return {"_parse_error": "no_json_object", "_raw": raw_text[:500]}

    try:
        return json.loads(obj_match.group(0))
    except json.JSONDecodeError as e:
        return {"_parse_error": f"json_decode: {e}", "_raw": raw_text[:500]}
