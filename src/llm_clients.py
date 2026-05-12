"""LLM API client wrappers untuk pilot multi-LLM.

Tiga vendor (semua OpenAI-compatible API):
  - DeepSeek V4 Pro / Flash      — https://api.deepseek.com/v1
  - xAI Grok 4.3                  — https://api.x.ai/v1
  - Moonshot Kimi K2.6            — https://api.moonshot.ai/v1

load_dotenv() coba .env dulu, lalu .env.txt sebagai fallback (Windows convention).
Semua function mengembalikan LLMResponse untuk logging seragam.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import openai
from dotenv import load_dotenv

# Load .env atau .env.txt (Windows-friendly)
_ROOT = Path(__file__).resolve().parents[1]
for envfile in (".env", ".env.txt"):
    p = _ROOT / envfile
    if p.exists():
        load_dotenv(p)
        break


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


def _openai_compat_call(
    vendor: str,
    model: str,
    api_key_env: str,
    base_url_env: str,
    base_url_default: str,
    system: str,
    user: str,
    max_tokens: int = 1024,
    temperature: float = 0.0,
) -> LLMResponse:
    api_key = os.environ.get(api_key_env)
    if not api_key:
        return LLMResponse(
            vendor=vendor,
            model=model,
            raw_text="",
            latency_ms=0,
            error=f"missing env var {api_key_env}",
        )

    client = openai.OpenAI(
        api_key=api_key,
        base_url=os.environ.get(base_url_env, base_url_default),
    )
    t0 = time.monotonic()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        latency = int((time.monotonic() - t0) * 1000)
        text = resp.choices[0].message.content or ""
        usage = resp.usage
        return LLMResponse(
            vendor=vendor,
            model=model,
            raw_text=text,
            latency_ms=latency,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            extra={"finish_reason": resp.choices[0].finish_reason},
        )
    except Exception as e:
        return LLMResponse(
            vendor=vendor,
            model=model,
            raw_text="",
            latency_ms=int((time.monotonic() - t0) * 1000),
            error=f"{type(e).__name__}: {e}",
        )


def call_deepseek(system: str, user: str, model: str = "deepseek-v4-pro") -> LLMResponse:
    return _openai_compat_call(
        vendor="deepseek",
        model=model,
        api_key_env="DEEPSEEK_API_KEY",
        base_url_env="DEEPSEEK_BASE_URL",
        base_url_default="https://api.deepseek.com/v1",
        system=system,
        user=user,
        max_tokens=2048,
    )


def call_grok(system: str, user: str, model: str = "grok-4.3") -> LLMResponse:
    return _openai_compat_call(
        vendor="grok",
        model=model,
        api_key_env="XAI_API_KEY",
        base_url_env="XAI_BASE_URL",
        base_url_default="https://api.x.ai/v1",
        system=system,
        user=user,
    )


def call_kimi(system: str, user: str, model: str = "kimi-k2.6") -> LLMResponse:
    # Kimi K2.6 hanya menerima temperature=1.0 (per error API). Determinism
    # diandalkan dari few-shot + structured output prompt, bukan low temp.
    return _openai_compat_call(
        vendor="kimi",
        model=model,
        api_key_env="KIMI_API_KEY",
        base_url_env="KIMI_BASE_URL",
        base_url_default="https://api.moonshot.ai/v1",
        system=system,
        user=user,
        max_tokens=4096,
        temperature=1.0,
    )
