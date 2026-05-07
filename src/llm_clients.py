"""LLM API client wrappers untuk pilot multi-LLM.

Tiga vendor: Anthropic (Claude), OpenAI (GPT-4o), DeepSeek (OpenAI-compatible API).
Semua mengembalikan tuple (raw_response_text, response_metadata) untuk logging penuh.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any

import anthropic
import openai
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMResponse:
    vendor: str
    model: str
    raw_text: str
    latency_ms: int
    input_tokens: int | None = None
    output_tokens: int | None = None
    error: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)


def call_claude(system: str, user: str, model: str = "claude-opus-4-7") -> LLMResponse:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.monotonic()
    try:
        msg = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        latency = int((time.monotonic() - t0) * 1000)
        text = msg.content[0].text if msg.content else ""
        return LLMResponse(
            vendor="anthropic",
            model=model,
            raw_text=text,
            latency_ms=latency,
            input_tokens=msg.usage.input_tokens,
            output_tokens=msg.usage.output_tokens,
            extra={"stop_reason": msg.stop_reason},
        )
    except Exception as e:
        return LLMResponse(
            vendor="anthropic",
            model=model,
            raw_text="",
            latency_ms=int((time.monotonic() - t0) * 1000),
            error=f"{type(e).__name__}: {e}",
        )


def call_openai(system: str, user: str, model: str = "gpt-4o") -> LLMResponse:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    t0 = time.monotonic()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=1024,
            temperature=0.0,
        )
        latency = int((time.monotonic() - t0) * 1000)
        text = resp.choices[0].message.content or ""
        return LLMResponse(
            vendor="openai",
            model=model,
            raw_text=text,
            latency_ms=latency,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
            extra={"finish_reason": resp.choices[0].finish_reason},
        )
    except Exception as e:
        return LLMResponse(
            vendor="openai",
            model=model,
            raw_text="",
            latency_ms=int((time.monotonic() - t0) * 1000),
            error=f"{type(e).__name__}: {e}",
        )


def call_deepseek(system: str, user: str, model: str = "deepseek-chat") -> LLMResponse:
    client = openai.OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
    )
    t0 = time.monotonic()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=1024,
            temperature=0.0,
        )
        latency = int((time.monotonic() - t0) * 1000)
        text = resp.choices[0].message.content or ""
        return LLMResponse(
            vendor="deepseek",
            model=model,
            raw_text=text,
            latency_ms=latency,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
            extra={"finish_reason": resp.choices[0].finish_reason},
        )
    except Exception as e:
        return LLMResponse(
            vendor="deepseek",
            model=model,
            raw_text="",
            latency_ms=int((time.monotonic() - t0) * 1000),
            error=f"{type(e).__name__}: {e}",
        )
