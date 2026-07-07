# Register-Pragmatics of Javanese Hate Speech — Findings (2026-06-23)

Emerged from a live session with the native-expert author (Mukhlis Amien) generating + judging
krama hate speech. This is candidate **core novelty** for the paper. Capture before it evaporates.

## 1. The core model: register encodes the *temperature* and *direction* of hostility

Javanese hate speech is not register-flat. The honorific system (*ngoko / madya / krama*) interacts
with the speech act of hate in a rule-governed way:

- **HOT / direct hostility** (rage, vulgar confrontation) → **ngoko / kasar**. Krama is impossible:
  you cannot scream an insult in a deference register.
- **COLD / controlled hostility** (contempt, moral/hierarchical superiority, irony) → **krama** is
  available, in distinct pragmatic niches.

Krama-hate niches identified (native-validated):

| Niche | Configuration | Mechanism | Example (native-validated) |
|---|---|---|---|
| N1 ngoko direct | target = addressee, hot | open aggression | "Wong Madura kuwi kasar kabeh..." |
| N2 krama report | target ≠ addressee | derogate absent group, defer to listener | "Mugi tiyang Tionghoa enggal wangsul..." |
| N3a krama sarcastic | target = addressee, ironic | weaponized over-praise (mock-deference) | "Inggih, panjenengan wicaksana sanget..." |
| N3b krama cold-contempt | target = addressee, cold | moral/hierarchical superiority | "Panjenengan boten gadhah unggah-ungguh" |

**Key correction to an earlier naive rule:** "krama can't be hostile face-to-face" is FALSE.
It can — N3a/N3b — when the hostility is *cold contempt / moral superiority / irony*, not hot rage.
The native expert's visceral reaction ("I'd feel offended and awkward if a younger person said that
to me") is the strongest authenticity signal: the text lands as a real attack.

## 2. LLM capability (hypothesis corrected by data)

Earlier lean: "LLMs can't generate authentic krama hate." **This is wrong.**
- DeepSeek produced cold-contempt krama (N3b: *"Panjenengan punika tiyang ingkang boten gadhah
  unggah-ungguh"*, *"Kula mboten sami kaliyan panjenengan ingkang asor"*, *"Menapa panjenengan
  mboten gadhah isin?"*) that the native expert judged **"sangat bagus"** (authentic).
- The capability boundary is narrower than "can't": LLMs produce **authentic** krama hate when it is
  short + high-frequency living vocabulary + cold-contempt mode; they produce **"museum krama"**
  (grammatical but textbook, fossil literary vocabulary like *prayogi/dedunung/kitha* that even an
  educated native does not actively use) when reaching for elaborate literary forms; and they
  **default to the Central-Javanese prestige standard**, erasing regional (e.g. East-Java/Arek) variety.

**Why can LLMs do krama contempt?** (a) Composition: register competence × hate semantics, learned
separately, combined — no real "krama hate" example needed. (b) The textual record DOES contain krama
conflict: classical Javanese literature and wayang/drama are full of refined-register conflict among
nobles. So LLMs are good at the register that is well-represented *in writing* (literary krama) and
weak at the register that is spoken-only (living regional ngoko hate) — the inverse of what can be
collected.

## 3. Detection blind-spot probe (experiment, blindspot_test.py)

Minimal pair (same hateful meaning, target suku_madura) + the expert's interpersonal examples, run
through the production pipeline (DeepSeek + Grok + qwen3, prompt v2):

- **ngoko direct** → hate=True by all 3 (control).
- **krama report (N2, polite surface, group)** → hate=True by **all 3**. Politeness alone does NOT
  blind the detector — explicit hateful propositional content wins.
- **krama sarcastic (N3a, ironic, group)** → DeepSeek/Grok True (ringan), **qwen3 False/BUK** (read it
  as "formal praise"). The blind spot is **irony/implicature, not politeness**, and it is
  **model-dependent** (cheap local model fails).
- **cold-contempt interpersonal (N3b, no group)** → correctly BUK by most (no group identity → not
  SARA hate per taxonomy). Grok flagged the *asor* one as hate (its known over-flag bias).

**Corrected thesis:** the detection challenge is not surface politeness but **implicature (irony,
sarcasm, pasemon)** in the krama register — and the cheapest rater (qwen3) is exactly where it breaks.
This ties register + pasemon + the limits of cheap full-automation + vendor bias into one finding.

### 3b. AT SCALE (2026-06-29): the blind spot is NEAR-UNIVERSAL, not cheap-model-only

The minimal-pair claim above ("cheap qwen3 fails, cloud catches") was **partly wrong** — an
artifact of one example. Running the full register matrix (36 cells, DeepSeek-generated) through
the production detector with 5 raters (`experiments/generation_pilot/detect_probe.py`, verified
recompute, 0 parse failures) gives the corrected picture:

| niche | deepseek | grok | qwen3:14b | gemma3:27b | gpt-oss:20b |
|---|---|---|---|---|---|
| ngoko_direct | 100% | 100% | 100% | 100% | 100% |
| krama_report | 78% | 89% | 44% | 89% | 44% |
| **krama_sarcastic** | **11%** | **11%** | **0%** | **0%** | **0%** |
| krama_cold_contempt | 78% | 89% | 56% | 78% | 78% |

- **krama_sarcastic (irony/pasemon) evades EVERYONE**, cloud included: 2/45 verdicts were "hate".
  No detector in this set reliably catches Javanese irony — this is the stronger, more honest claim.
- **ngoko_direct = 100%** everywhere (control); **krama_report 78–89%** for cloud+gemma3 → politeness
  alone does not blind (explicit propositional hate wins). Implicature, not honorifics, is the wall.
- Model capability modulates the *non-ironic* krama niches (cheap local drops 30–45 pts on
  krama_report), but for genuine irony capability does not rescue detection.
- **Tie-back:** the same production trio labeled the 728 real tweets → it systematically
  under-labels krama-sarcastic hate. DeepSeek even fails to detect the irony it *generated* (11%).
  Full results: `experiments/generation_pilot/RESULTS_probe.md`.

## 4. Implications for the paper

The strongest, most honest paper now unifies three threads:
1. **Characterization** — the register-pragmatic model above (novel; absent from existing hate taxonomies).
2. **Generation/augmentation** — LLMs can generate native-validated krama hate, the register that is
   *uncollectable* from public social media (diglossia). A small, register-stratified, native-validated
   set is a genuine contribution.
3. **Detection probe** — implicature (not politeness) is the blind spot, and it is model-dependent —
   a concrete limit of cheap full-automation that motivates the lightweight native-expert role.

Human role collapses to **authenticity refereeing** (native comprehension > production suffices),
not annotation — consistent with the "eliminate the human bottleneck" framing, with the honest
qualification that the bottleneck is irreducible exactly at register-pragmatic authenticity.

## 5. Open questions / next steps

**Progress 2026-06-29 (sesi 5):** Group-directed cold-contempt → **generated** (9 cells, matrix
complete); detection-wise it is caught 56–89% (not the blind spot — irony is). Systematize → **done
as a real matrix** (4 niches × 9 targets × 3 generator models × 5 detectors + 4-lens QC panel; see
`experiments/generation_pilot/RESULTS_probe.md`). Regional axis → partially: qwen3 defaults to
**Indonesian** (not even Central-Java krama) for krama niches; DeepSeek/gemma3 produce Javanese.
Native authenticity validation + second native judge = still open (the irreducible human step).

- **Group-directed krama cold-contempt**: the N3b examples are interpersonal; test whether authentic
  SARA-group krama hate can be generated (mock-praising/morally-indicting a religious/ethnic group).
- **Second native judge** (Yekti / Daniel, if Javanese) → authenticity inter-rater reliability.
  **Done (D21, 2026-07-07):** Yekti is native, Daniel is not (30yr East Java resident, non-native).
  IRR came back low (native-native Mukhlis-Yekti α=0.095) — see `experiments/generation_pilot/multivalidator_result.md`.
- **Systematize**: N stimuli × niches × models × native ratings → a real table, not anecdotes.
- **Regional axis**: does the LLM default to Central-Java krama and erase Arek/East-Java? Quantify.
