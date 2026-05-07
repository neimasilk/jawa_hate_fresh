"""Quick connectivity test untuk 3 LLM API.

Kirim 1 message minimal ke tiap vendor, ukur latency, validasi response.
TIDAK call task klasifikasi penuh — cuma "are you alive?" check.

Cost estimate: < $0.001 total (3 sapaan singkat).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.llm_clients import call_deepseek, call_grok, call_kimi  # noqa: E402

SYSTEM = "You are a helpful assistant. Respond in one short sentence."
USER = "Sebutkan satu kata sapaan dalam Bahasa Jawa krama, lalu sebutkan model name kamu."


def fmt(resp) -> str:
    if resp.error:
        return f"FAIL — {resp.error}"
    body = resp.raw_text.strip().replace("\n", " ")[:200]
    return (
        f"OK ({resp.latency_ms}ms, in={resp.input_tokens}, out={resp.output_tokens})"
        f"\n  Response: {body}"
    )


def main() -> None:
    print("=" * 60)
    print("API connectivity test — 3 vendors")
    print("=" * 60)

    for label, fn in [
        ("DeepSeek V4 Pro    (deepseek-v4-pro)", call_deepseek),
        ("xAI Grok 4.3       (grok-4.3)",        call_grok),
        ("Moonshot Kimi K2.6 (kimi-k2.6)",       call_kimi),
    ]:
        print(f"\n[{label}]")
        resp = fn(SYSTEM, USER)
        print(f"  {fmt(resp)}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
