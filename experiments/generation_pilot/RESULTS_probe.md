# Generation pilot — detection probe + QC panel results (2026-06-29 sesi 5)

Paper-facing synthesis. The verbatim synthetic hate lives in gitignored files
(`detect_report.md`, `*.jsonl`); this file holds only aggregate tables + interpretation
(no offensive verbatim), per the project ethics policy.

Inputs: the register-stratified matrix (4 register-pragmatic niches × 9 SARA targets =
36 cells, DeepSeek-generated) from `generate.py` + `fill_arab_cell.py`. Three downstream
automated analyses, none requiring the native expert:

1. **Detection blind-spot probe at scale** (`detect_probe.py`) — runs every cell through
   the production detector (prompt v2, the Pilot #3 winner) with 5 detectors.
2. **Multi-model generation** (`gen_local.py`) — regenerates the matrix with two free
   local models (gemma3:27b, qwen3:14b) for the inter-model axis.
3. **Non-native QC judge panel** (4-agent workflow) — pre-triage before native validation.

---

## 1. Detection blind-spot probe (the headline)

Controlled experiment: generator held constant (DeepSeek); register-pragmatic **niche** is
the manipulated variable; each detector's hate=true/false is the dependent variable.
Cell = hate-detection rate (caught / valid verdicts). **0 parse/refusal failures** across
all 180 (example × detector) pairs; table independently recomputed (matches exactly).

| niche \ detector | deepseek (cloud) | grok (cloud) | qwen3:14b (local) | gemma3:27b (local) | gpt-oss:20b (local) |
|---|---|---|---|---|---|
| ngoko_direct (hot/vulgar)        | 100% | 100% | 100% | 100% | 100% |
| krama_report (polite, group)     | 78%  | 89%  | 44%  | 89%  | 44%  |
| **krama_sarcastic (irony/pasemon)** | **11%** | **11%** | **0%** | **0%** | **0%** |
| krama_cold_contempt (cold moral) | 78%  | 89%  | 56%  | 78%  | 78%  |

Per-detector overall: grok 72% · deepseek 67% · gemma3:27b 67% · gpt-oss:20b 56% · qwen3:14b 50%.

### The corrected, stronger thesis

The earlier `register_probe/FINDINGS.md §3` claim — from a single minimal pair — was that
the irony blind spot is *model-dependent* (cheap qwen3 fails, cloud catches). **At scale that
is wrong in an important way:**

- **Pasemon/irony in krama is a NEAR-UNIVERSAL blind spot, not a cheap-model failure.**
  Across 9 krama_sarcastic cells, the strongest cloud models caught only **1/9 (11%)** and
  all three local models **0/9**. Total: **2 of 45** sarcastic verdicts were "hate". The
  earlier "cloud catches it" reading was an artifact of one lucky example.
- **ngoko_direct = 100% for every detector** — explicit hot hostility is trivial (control).
- **Politeness alone does NOT blind detectors.** krama_report (polite surface, but explicit
  derogatory propositional content) is caught 78–89% by cloud + gemma3. What evades is
  *implicature*, not honorific register — exactly FINDINGS §3, now at scale.
- **Model capability modulates the *non-ironic* krama niches.** On krama_report and
  krama_cold_contempt the cheaper local models (qwen3, gpt-oss) drop 30–45 points below
  cloud (e.g. krama_report 44% vs 89%). So capability matters for "polite-but-explicit"
  hate — but for genuine irony, *no detector in this set is reliable*.

### Cells that evaded ALL 5 detectors (0/5)

9 of 36 cells were missed by every detector — **7 of the 9 krama_sarcastic cells** (corrected 2026-07-09: the matrix has 9 krama_sarcastic cells — cf. '1/9' rates above; '8' was a typo) plus
`krama_report × politik_kolektif` and `krama_cold_contempt × politik_kolektif`. (The two
political-collective misses align with the QC panel's note that politik_kolektif is the
softest "identity" category — polite political derogation reads as ordinary criticism.)

### Why this matters for the real dataset

The production trio (deepseek + grok + qwen3) is exactly what labeled the **728 real
tweets** (`data/labeled/`). This probe shows that trio systematically under-detects krama
irony — so the real dataset almost certainly **under-labels** the rare krama-sarcastic hate
it contains. The synthetic register-stratified set surfaces a blind spot the collection
pipeline cannot see in itself. Honest caveat: deepseek and qwen3 are **both generator and
detector** here — DeepSeek *generated* these ironic attacks as hate yet flags only 11% of
them as hate, i.e. it cannot recognize the implicature it just produced. That is a finding,
not a confound.

---

## 2. Multi-model generation (inter-model axis)

Same matrix, three generators. Non-native + heuristic signal (native validation pending):

- **DeepSeek** — authentic across all four niches (judge panel: 0 museum-krama, 0
  Indonesian-leak; native judged the krama "sangat bagus" in the prior session).
- **gemma3:27b (local)** — produces genuine Javanese (real ngoko + krama), somewhat more
  generic; a viable free generator.
- **qwen3:14b (local)** — **fails the krama registers: it defaults to Indonesian**, not
  Javanese krama (e.g. cold-contempt cells came back in colloquial Indonesian "…tuh nggak
  pernah…"). The cheap local model that has the *detection* blind spot also cannot
  *generate* the uncollectable register.

This is the inter-model story FINDINGS §5 asked for: **generating the uncollectable krama
register is model-dependent** — strong models (DeepSeek; gemma3 partially) can, the cheap
local model cannot. It mirrors the detection result: capability, not locality, is decisive.

---

## 3. Non-native QC judge panel (pre-triage)

4 Claude agents, 4 lenses, over the 36 DeepSeek cells (advisory — a native makes the final
authenticity call). Aggregate:

- **Javanese authenticity:** 36/36 read as living Javanese; **0 museum-krama, 0
  Indonesian-leak** (only typos: `naming`→`namung` ×6, `sisah`→`susah`).
- **Register/niche fidelity:** 35/36 on-mode. One flag — **#21** (santri sarcasm) reads as a
  *sincere* krama blessing; the intended pasemon is not recoverable from the text → likely
  the single hardest detection case (and indeed evaded 0/5).
- **Target/hate fidelity:** 35/36 on-target. One flag — **#26** (Arek×Mataraman sarcasm) too
  weak/ambiguous (never names Arek; mock-praises Mataraman).
- **Formulaic/diversity critic:** 12 near-template clones — `krama_report` "Mugi…enggal…"
  (9/9 share the opener), `krama_sarcastic` "…ingkang sampun paring…" (7/8), and
  `krama_cold_contempt` the "lacks isin/unggah-ungguh" accusation (7/9). **This is the
  authentic-rich vs formulaic question the native must adjudicate.**

The judge panel does **not** replace native validation; it focuses it. The enriched form
(`rebuild_form.py`) marks **27 PRIORITAS** rows (detector-evasive OR judge-flagged DeepSeek
cells + one slice per local-model × niche) so Bapak validates the contested ~30, not 108 blind.

---

## 4. What native validation (the irreducible step) will resolve

The bottleneck stays exactly where the framing predicts — register-pragmatic authenticity:

1. **Is the formulaic device authentic-rich or formulaic-fake?** (the "Mugi…enggal", "ingkang
   sampun paring", "lacks-isin" templates). Native call.
2. **N3b group-directed cold-contempt** — does it land as real hate to a Javanese ear?
   (Open question from FINDINGS §5; the probe shows it is *detected* 56–89%, but native
   authenticity is the separate question.)
3. **Which generator** (DeepSeek vs gemma3 vs qwen3) produces authentic Javanese per niche
   — the model × niche table in `validation_result.md` after scoring.
4. **The evasive-but-authentic cross-tab:** for cells that evaded all detectors, are they
   authentic hate? If yes → they are the dataset's reason to exist (hate the automated
   pipeline cannot catch).

Pipeline ready: native fills `VALIDATION_FORM.xlsx` (PRIORITAS first) → `score_validation.py`
→ per-model / per-niche / evasion×authenticity tables.
