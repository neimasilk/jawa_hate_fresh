"""Pilot #2 — analisis hasil LLM-as-Jawa-filter.

Output:
  - Distribusi kategori bahasa (jawa / campuran / indonesia / lainnya)
  - Yield Jawa+campuran (= densitas teks Jawa di dump Indonesia)
  - Cross-tab bahasa x label hate asli (apakah subset Jawa cukup "panas")
  - Ekstrak subset panas (jawa+campuran) -> outputs/hot_jawa_subset.jsonl
  - Contoh-contoh untuk inspeksi manual
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "outputs"
LOG_PATH = OUT_DIR / "pilot02_responses.jsonl"
HOT_PATH = OUT_DIR / "hot_jawa_subset.jsonl"
REPORT_PATH = Path(__file__).resolve().parent / "report.md"

JAWA_CATS = {"jawa", "campuran"}


def load() -> list[dict]:
    latest: dict[str, dict] = {}
    with LOG_PATH.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            latest[rec["source_id"]] = rec
    return list(latest.values())


def main() -> None:
    recs = load()
    n = len(recs)
    lang = Counter()
    valid = 0
    crosstab: dict[str, Counter] = defaultdict(Counter)
    hot = []
    examples: dict[str, list] = defaultdict(list)

    for r in recs:
        p = r.get("parsed") or {}
        if "_parse_error" in p or r.get("error"):
            lang["_invalid"] += 1
            continue
        valid += 1
        b = p.get("bahasa", "?")
        lang[b] += 1
        crosstab[b][r.get("orig_label")] += 1
        if b in JAWA_CATS:
            hot.append(r)
        if len(examples[b]) < 4:
            examples[b].append(r)

    with HOT_PATH.open("w", encoding="utf-8") as f:
        for r in hot:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    jawa_n = lang.get("jawa", 0) + lang.get("campuran", 0)
    hot_hate = sum(1 for r in hot if r.get("orig_label") == "hate")

    L = ["# Pilot #2 — LLM-as-Jawa-filter Report", ""]
    L.append(f"**Sumber:** haipradana/indonesian-twitter-hate-speech-cleaned (raw text)")
    L.append(f"**Total diproses:** {n}  |  **valid JSON:** {valid}  |  **invalid:** {lang.get('_invalid',0)}")
    L.append(f"**Filter LLM:** Grok 4.3, prompt jawa_filter_v0")
    L.append("")
    L.append("## Distribusi kategori bahasa")
    L.append("")
    L.append("| Kategori | N | % dari valid |")
    L.append("|---|---|---|")
    for cat in ["jawa", "campuran", "indonesia", "lainnya"]:
        c = lang.get(cat, 0)
        L.append(f"| {cat} | {c} | {100*c/valid:.1f}% |" if valid else f"| {cat} | {c} | - |")
    L.append("")
    L.append(f"**Yield Jawa+campuran:** {jawa_n}/{valid} = **{100*jawa_n/valid:.1f}%**" if valid else "n/a")
    L.append("")
    L.append("## Cross-tab bahasa × label hate asli")
    L.append("")
    L.append("| Kategori | hate | neutral |")
    L.append("|---|---|---|")
    for cat in ["jawa", "campuran", "indonesia", "lainnya"]:
        ct = crosstab.get(cat, Counter())
        L.append(f"| {cat} | {ct.get('hate',0)} | {ct.get('neutral',0)} |")
    L.append("")
    L.append(f"**Subset panas (Jawa+campuran):** {len(hot)} teks, di antaranya **{hot_hate} berlabel hate** "
             f"({100*hot_hate/len(hot):.0f}%)." if hot else "**Subset panas kosong.**")
    L.append(f"Disimpan ke `outputs/hot_jawa_subset.jsonl`.")
    L.append("")
    L.append("## Contoh per kategori (max 4)")
    L.append("")
    for cat in ["jawa", "campuran", "indonesia", "lainnya"]:
        L.append(f"### {cat}")
        for r in examples.get(cat, []):
            p = r["parsed"]
            mk = p.get("penanda_jawa", [])
            L.append(f"- [{r.get('orig_label')}] _{p.get('register','?')}_ penanda={mk}")
            L.append(f"  > {r['text'][:160]}")
        L.append("")

    report = "\n".join(L)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Report -> {REPORT_PATH}")
    print("\n" + report.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
