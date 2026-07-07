# Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection

> **JINITA-conformant draft v5 (2026-07-06). Diagnostic-suite framing (D20).** Replaces v4 (generation-headline framing). Reframe rationale: generation is repositioned as the stimulus-construction *method* in service of a detection-blind-spot *diagnosis* (the headline contribution), rather than as the contribution itself — this closes the dual-use framing risk and better matches what the evidence supports. Taxonomy (§2) and scarcity evidence (§3.1) are unchanged from v4. Added: second independent scarcity anchor (§1, Table 1, lexicon-based Twitter measurement) and an explicit dual-use statement (§4.8). All numbers from experiments: `experiments/generation_pilot/validation_result.md`, `experiments/generation_pilot/RESULTS_probe.md`, `experiments/register_probe/FINDINGS.md`, `experiments/pilot05_bulk_labeling/report.md`. Reference list lit-pass completed 2026-07-06 (24 references, all verified and cited in-text; see change log appendix); only [4]'s exact page range needs a final manual check before submission (publisher vs. aggregator discrepancy).

**Mukhlis Amien¹, Yekti Asmoro Kanthi², Daniel Rudiaman Sijabat³**
¹,²,³ Department of Informatics, Universitas Bhinneka Nusantara, Malang, Indonesia
email: ¹amien@ubhinus.ac.id, ²yektiasmoro@ubhinus.ac.id, ³daniel223@ubhinus.ac.id

*(Article info / history block to be filled by the editor. Blinded version for peer review: remove authors and affiliations.)*

---

## ABSTRACT

Hate speech in Javanese — spoken by roughly 80 million people — poses a distinct detection challenge because its honorific register system (*unggah-ungguh*) lets identical hostile content surface as vulgar *ngoko* or as deceptively refined *krama*. *Krama* hostility is diglossically confined to formal, face-to-face contexts and thus structurally absent from social-media corpora, leaving corpus-based detection blind to an entire class of Javanese hate by construction. We diagnose this blind spot, constructing a register-stratified stimulus set via LLMs across four register-pragmatic niches and nine SARA target groups (a 36-cell matrix), validated for authenticity by a native Javanese speaker. Of 108 constructed examples (three models), 59 (55%) are judged authentic; DeepSeek reaches 97% (35/36) across all niches, while the free local model Qwen3-14B fails entirely at *krama*, producing Indonesian instead of Javanese. Running the stimuli through five detectors reveals a near-universal blind spot: only 2 of 45 verdicts (4%) correctly flag ironic Javanese hate, versus 100% for *ngoko-direct* hate. Politeness alone does not blind detectors — *krama-report* without irony is still caught at 78–89% — the failure is pragmatic implicature (*pasemon*). Two independent scarcity measurements corroborate the diagnosis: a labeling run on 735 texts finds zero consensus *krama*-hate, and a lexicon-based scan of 1.42 million general-topic tweets finds Javanese, despite 84 million speakers, at only 0.093% presence — the highest of ten regional languages surveyed, still under 0.1%. The stimulus set and blind-spot proof together form a reproducible instrument for an under-studied detection failure mode in diglossic, register-rich languages.

**Keywords:** Javanese; hate speech detection; register; large language model; detection blind spot

---

## 1. INTRODUCTION

Javanese is spoken by roughly 80 million people and carries significant online hate speech directed at ethnic minorities (Madurese, Chinese-Indonesian, Arab communities), religious groups, women, and LGBTQ+ individuals [1]. Yet the language is severely under-resourced in NLP relative to general-Indonesian resources [2], [3], [16], and the few published hate-speech datasets for Javanese either remain unreleased [4] or conflate Javanese with broader Indonesian [5], [20]. Prior work has explored GPT-based data augmentation for low-resource, code-mixed Indonesian hate speech detection more broadly [13], [14], but without Javanese register-pragmatic structure as the organizing axis — the central contribution of this paper.

A feature of Javanese that existing approaches entirely overlook is its *unggah-ungguh* (speech-level) system: the same hostile proposition can be expressed in coarse *ngoko* — the register of in-group bluntness — or in the refined *krama* register, producing qualitatively different pragmatic effects. Hot, direct rage is *ngoko*; cold contempt, ironic superiority, and indirect defamation — the forms that most damage group dignity — are *krama*. This is not a stylistic choice but a rule-governed pragmatic constraint, validated by a native speaker in this work.

The practical consequence is a data collection paradox. Social-media Javanese hate speech is almost entirely *ngoko* with code-mixing [17]; pure *krama* is essentially absent from public posts because *krama* is used in formal or face-to-face contexts, not in Twitter or WhatsApp broadcasts [6]. A standard corpus-filtering pipeline will collect *ngoko* hate, confirm the register, and leave *krama* hate completely uncollected. We verified this directly: filtering 12,700 tweets from a public Indonesian hate-speech dump [7] yields 735 candidate Javanese texts, of which **zero** carry consensus *krama*-hate in the majority-vote labeling.

This scarcity is not an artifact of one corpus or one filtering method. An unrelated companion measurement of Javanese digital presence — a lexicon-based scan of a general-topic (non-hate-filtered) Indonesian Twitter corpus spanning 32 cities and roughly 1.42 million cleaned, deduplicated tweets — confirms the same pattern from an independent angle [8]. Counting a tweet as confirmed-Javanese only if it contains two or more lexically distinctive Javanese function words or particles, just 1,321 tweets (0.093%) qualify. Table 1 places this in comparative context: among ten Indonesian regional languages surveyed in the same corpus, Javanese has both the largest speaker population (84.3 million, exceeding the other nine combined) and the *highest* confirmed-tweet rate — yet even this best case clears well under one tweet in a thousand. Two measurements that share no data, no method, and no base population — an LLM-based semantic filter over an already hate-labeled corpus (74/8,269 ≈ 0.9% [7]) and a lexicon-keyword filter over a general-topic corpus (1,321/1,419,641 ≈ 0.093% [8]) — converge on the same conclusion: Javanese is structurally underrepresented in exactly the public channels that hate-speech corpora are built from, regardless of how the filtering is done. This is not a contradiction of Javanese's 80-million-speaker population but consistent with it: sociolinguistic work on Javanese specifically argues that speaker-population size alone does not guarantee domain vitality, and documents a real, urbanization- and class-linked shift away from Javanese (particularly its *krama* register) toward Indonesian in exactly the informal, everyday domains that social media represents [25], [26].

**Table 1.** Confirmed-tweet rate for ten Indonesian regional languages in a general-topic, 32-city Twitter corpus (≈1.42M cleaned tweets; lexicon match, ≥2 distinctive-word threshold per tweet) [8]. Not to be confused with the hate-detector verdict rates in Table 4.

| Language | Speakers (M) | Confirmed tweets | Confirmed rate |
|---|---|---|---|
| Javanese | 84.3 | 1,321 | 0.093% |
| Acehnese | 3.5 | 515 | 0.036% |
| Banjarese | 3.5 | 302 | 0.021% |
| Minangkabau | 5.5 | 286 | 0.020% |
| Sundanese | 34.0 | 256 | 0.018% |
| Balinese | 3.3 | 81 | 0.006% |
| Ngaju | 0.9 | 71 | 0.005% |
| Toba Batak | 2.0 | 38 | 0.003% |
| Madurese | 7.0 | 11 | 0.0008% |
| Buginese | 5.0 | 2 | 0.0001% |

This paper addresses the collection paradox with a diagnostic approach: rather than filtering and labeling an existing corpus, we construct a register-stratified set of Javanese hate-speech stimuli [12] — using LLMs as the construction *method*, not as the object of study — validate each stimulus with a native expert, and probe the set with five independent hate-speech detectors. The contribution is not a large dataset but a controlled diagnostic instrument: a minimal sufficient set that proves a specific failure mode exists, is reproducible, and is systematically missed by current automated detection. Generation is the *means* by which the otherwise-uncollectable *krama* niches become testable; the finding that matters is what the resulting stimuli reveal about detection, not the stimuli themselves.

**Why the human bottleneck matters here.** This work is directly motivated by a prior failure: student annotators in a precursor project produced nominally "Javanese" data primarily by back-translating Indonesian and English hate speech, yielding labels that were internally consistent but not grounded in authentic Javanese expression. The corruption was invisible until downstream models failed to generalize. The generator approach avoids this bottleneck by design: the human role collapses to *authenticity refereeing* (native speaker judges whether generated text sounds like real Javanese hate), which requires native comprehension rather than full annotation labor.

**Contributions.** (1) Empirical proof of a *detection blind spot*: Javanese ironic hate (*pasemon* in *krama*) evades all five tested detectors — cloud and local — at a rate of 96%, while explicit *ngoko* hate is caught at 100%; the failure traces to pragmatic implicature, not surface politeness. (2) A *register-pragmatic model* of Javanese hate speech — a taxonomy of four niches defined by the interaction of register and pragmatic mode, validated with a native expert — that explains *why* the blind spot exists, not merely that it does. (3) A register-stratified diagnostic stimulus set, constructed via LLM generation and validated for native authenticity, that makes the otherwise-uncollectable *krama* niches testable for the first time; generation here is a construction method in service of diagnosis, not an end in itself, and the resulting set is released under a restricted, research-only license precisely because it demonstrates how current detectors can be evaded. (4) A publicly released codebook, diagnostic construction scripts, and evaluation pipeline for reproducible extension to other diglossic, register-rich languages.

---

## 2. REGISTER-PRAGMATIC TAXONOMY

### 2.1. Hate speech definition

We define hate speech operationally as text that **attacks, demeans, dehumanizes, or incites violence or discrimination against a person or group based on group identity** — ethnicity (*suku*), religion or belief (*agama/kepercayaan*), gender or sexual orientation, social class, or political collective. The decisive criterion is *direction of attack toward group identity*, not coarseness of language. Javanese is rich in profanity (*pisuhan*: *asu*, *jancuk*, *cok*) that functions as in-group bonding in the Arek/Surabaya register; coarseness alone is not hate. This distinction is the single most error-prone boundary in Javanese moderation.

### 2.2. Four-dimensional taxonomy

The taxonomy has four dimensions (full definitions, decision trees, and worked examples in the released codebook):

**Target group** — ethnicity (*suku Madura, Tionghoa, Sunda, Batak, Arab*, …), intra-Javanese region (*Mataraman, Arek, Banyumasan*), religion or belief, gender/LGBTQ+, political collective, or *tidak ada*.

**Severity** — *BUK* (not hate) / *ringan* (light: stereotyping) / *sedang* (moderate: dehumanization, exclusion) / *berat* (severe: threats, incitement).

**Register** — *ngoko / madya / krama / campur kasar*. This dimension is the paper's primary focus; see §2.3.

**Form** — *direct / sarcastic / idiomatic (pasemon) / code-switched*.

### 2.3. The register-pragmatic model: four niches

Hostility in Javanese is not register-flat. The interaction between speech level and pragmatic intent produces four empirically distinct niches, validated by a native Javanese speaker:

| Niche | Register | Pragmatic mode | Mechanism |
|---|---|---|---|
| N1 *ngoko direct* | ngoko/kasar | Hot, open aggression | Explicit slur + profanity to addressee or about group |
| N2 *krama report* | krama alus | Derogatory report, absent target | Polite prayer/concern framing derogate-third-party ("*Mugi tiyang X enggal…*") |
| N3a *krama sarcastic* | krama alus | Ironic over-praise (pasemon) | Mock-deference: weaponized honorifics ("*Panjenengan wicaksana sanget…*") |
| N3b *krama cold contempt* | krama alus | Moral/hierarchical superiority | Cold indictment: target accused of lacking *isin* or *unggah-ungguh* |

A key empirical finding (§4.5) is that N2–N3b are essentially absent from social-media data — confirmed by zero consensus *krama*-hate in 728 labeled real texts — establishing the collection paradox and motivating generation.

### 2.4. Why *krama* hate is uncollectable

Two structural factors make *krama* hate unrepresented in social-media corpora. First, *diglossia*: *krama* is the register of formal, elder-addressee, or face-to-face speech; social-media Javanese defaults to *ngoko* with Indonesian code-mixing [6]. Second, *irony recognition* [23]: even if a *krama-sarcastic* post were found, an automated classifier would need to resolve pragmatic implicature (*pasemon*) — a specifically Javanese indirect speech act — rather than surface lexical hostility. §4.4 shows this is beyond all five tested detectors.

---

## 3. METHOD

### 3.1. Evidence of scarcity: the labeling baseline

Before generation, we establish the scarcity empirically. We filter a public Indonesian hate-speech dump [7] for Javanese and code-mixed text using an LLM filter (validated at 100% JSON validity, 9.6% Javanese yield in pilot), apply a two-stage cascade (free local pre-screen → cloud verification), and label the resulting pool with three LLM raters (DeepSeek, Grok, Qwen3-14B/local) using a culturally-grounded prompt [9]. The cascade's cloud confirmation rate of **25.4%** for pre-screen survivors is itself a finding: cheap local models reduce a candidate pool but cannot replace cloud precision for filtering.

The resulting pool yields **728 consensus-labeled instances** (158 hate, 21.7%; α Krippendorff [15] 0.51 three-rater held-out, 0.69 for the cloud pair), of which **register is *ngoko* for 157/158 hate instances** and *krama*-hate consensus is zero. This negative result serves two purposes: it motivates generation by proving the collection paradox, and the 728 texts serve as a realism anchor for generator calibration.

Full methodology of the labeling pipeline — prompt engineering (Δα ≈ +0.23 from two definition corrections), vendor selection, cascade economics, and adversarial verification — is documented in the supplementary report. The core finding relevant to this paper: **social-media filtering cannot produce *krama* hate at meaningful scale, even from a 12,700-tweet dump.**

### 3.2. Constructing the diagnostic stimulus set

We construct a **4-niche × 9-target = 36-cell matrix** of Javanese hate-speech stimuli using DeepSeek [18] as the primary construction model and Gemma3-27B and Qwen3-14B [19] (both running locally) for comparison, producing **108 total examples** (3 per cell). The nine target groups span the SARA taxonomy: *suku* (Madura, Tionghoa, Arab), *agama* (Islam, Kristen), *gender* (wanita, LGBTQ+), *politik* (collective), and intra-Javanese (*Arek vs. Mataraman*).

Each generation call specifies: (a) niche (N1–N3b), (b) target group, (c) a culturally-grounded system prompt (in Indonesian) that defines the niche's pragmatic mechanism and provides two-to-four few-shot examples. The system prompt explicitly prohibits "museum krama" (literary-Javanese vocabulary unused in living speech) and Indonesian code-leak. Generation uses the same API infrastructure as the labeling pipeline; DeepSeek calls use `max_tokens=8192` to allow adequate reasoning budget. The specific API endpoint used (`deepseek-v4-pro`) postdates the cited DeepSeek-V3 technical report [18]; no separate V4 technical report could be independently verified at the time of writing, so [18] is cited as the closest documented architecture family rather than an exact version match.

### 3.3. Native authenticity validation

The 108 generated examples are submitted to the first author (native Javanese speaker from East Java, academic background in Javanese linguistics) for authenticity validation. The validation instrument is a structured spreadsheet with: (a) the generated text, (b) the intended niche/target, (c) the generation mechanism description, (d) a machine-caught flag (did the production detector identify it as hate?), (e) an auto-concern flag (QC panel pre-triage), and (f) a binary authenticity verdict (1 = authentic Javanese hate of the stated type, 0 = not authentic). Comments on specific issues are recorded for each rejected example.

The human role is explicitly *authenticity refereeing*: does this text sound like something a Javanese speaker would actually say in the stated register-pragmatic mode? This is a comprehension task, not a production or annotation task, and can be completed in one to two hours across all 108 examples.

### 3.4. Detection blind-spot probe

We run each of the 36 DeepSeek-generated cells through five detectors: the production three-rater set (DeepSeek, Grok, Qwen3-14B) plus two additional local models (Gemma3-27B, GPT-OSS-20B). Each detector is given the same prompt v2 (the production prompt from §3.1) and asked to return a binary hate/non-hate verdict. Detection rate per niche is the fraction of cells where the detector returns hate=True.

The probe is controlled: the *generator* is held constant (DeepSeek), so differences in detection rate across niches reflect niche difficulty, not generator variation. All 180 (cell × detector) verdict calls succeeded with no parse failures (verified by independent recount).

---

## 4. RESULTS AND DISCUSSION

### 4.1. Generation authenticity: overall and by model

Of 108 generated examples, **59 (55%) were judged authentic** Javanese hate of the stated type. Table 2 breaks this down by generator.

**Table 2.** Native authenticity rate by generator model.

| Generator | Authentic | Rate | Primary failure mode |
|---|---|---|---|
| DeepSeek | 35/36 | **97%** | 1 item: *krama-sarcastic* read as sincere blessing, not irony |
| Gemma3-27B (local) | 20/36 | 56% | *Krama-sarcastic*: Indonesian leak in sarcastic punchline (0/9) |
| Qwen3-14B (local) | 4/36 | **11%** | *Krama* registers: generates Indonesian (not Javanese); hallucinated word *kacandran* |

DeepSeek is the only generator that can produce authentic Javanese in all four niches. The single failure (example #21, krama-sarcastic targeting agama_islam) is itself informative: an ironic over-praise of a santri's nighttime prayers was judged by the native speaker as a *sincere* blessing — the sarcasm failed entirely, producing a false positive in the validator's favor. This documents the difficulty of the N3a niche even for the best-performing generator.

This ranking is robust to which native validator scores it: splitting Table 2 by validator (Mukhlis / Yekti / Daniel), DeepSeek ranks first for all three (97% / 100% / 97%), and the full ordering DeepSeek > Gemma3-27B > Qwen3-14B holds for all three despite Yekti's generally more lenient absolute rates (97% / 56% / 11% vs. Yekti's 100% / 97% / 75% and Daniel's 97% / 39% / 0%; full breakdown in `experiments/generation_pilot/disagreement_analysis.md`). The headline generator-quality claim survives multi-rater scrutiny even though the pooled 55% authenticity figure does not (§4.7).

### 4.2. Register difficulty: *krama-sarcastic* is the hardest niche

Table 3 shows authenticity by niche, pooled across generators.

**Table 3.** Native authenticity rate by register-pragmatic niche (all generators combined, n=27 per niche).

| Niche | Authentic | Rate |
|---|---|---|
| N1 *ngoko direct* | 22/27 | 81% |
| N2 *krama report* | 17/27 | 63% |
| N3a *krama sarcastic* | 8/27 | **30%** |
| N3b *krama cold contempt* | 12/27 | 44% |

N1 (*ngoko direct*) is easiest — explicit profanity and slur targeting are within all generators' capability. N3a (*krama sarcastic*) is hardest at 30%; the Gemma3 failures account for nearly all the deficit (Gemma3 produced 0/9 authentic krama-sarcastic examples due to Indonesian leak). DeepSeek achieves 8/9 (89%) on this hardest niche; the single failure is example #21 above.

The N3b (*krama cold contempt*) result is particularly meaningful: this niche — a group-directed moral indictment in refined krama — was an open research question at the start of this work (could LLMs generate authentic krama hate *directed at a SARA group*, not just at individuals?). The answer is **yes, at 44% overall and 9/9 (100%) for DeepSeek**. The DeepSeek N3b examples use a recurring device — accusing the target group of lacking *isin* (shame/modesty) or *unggah-ungguh* (proper etiquette) — which the native speaker judged authentic and recognizable as a real Javanese contempt pattern. The formulaic character of this device is itself a finding, suggesting LLMs learned it from literary and religious Javanese text.

### 4.3. Model capability mirrors detection capability

The three generators show a consistent ordering — DeepSeek > Gemma3 > Qwen3 — in both generation authenticity and detection performance (§4.4). Qwen3, the cheapest local model, fails both tasks: it cannot *generate* authentic krama Javanese (defaulting to Indonesian), and it cannot *detect* krama hate. Gemma3 partially succeeds at generation (56%) and detection (67% overall), while DeepSeek leads both. This parallelism suggests a shared underlying competence: models that understand Javanese register sufficiently to generate it also understand it sufficiently to detect it, and the converse holds.

An additional finding: Qwen3 hallucinated the word *kacandran* (non-existent in standard Javanese; likely a confabulation of *kekacauan* with Javanese morphology) in five of nine ngoko-direct examples. This is a concrete instance of a known LLM failure mode — lexical confabulation in a low-resource language — and underscores the necessity of native validation even for the "easiest" niche.

### 4.4. Detection blind spot: *pasemon* evades every detector

Table 4 shows detection rates across all five detectors for each niche.

**Table 4.** Hate detection rate by niche and detector (DeepSeek-generated cells; n=9 cells per niche per detector).

| Niche | DeepSeek | Grok | Qwen3-14B | Gemma3-27B | GPT-OSS-20B |
|---|---|---|---|---|---|
| N1 *ngoko direct* | 100% | 100% | 100% | 100% | 100% |
| N2 *krama report* | 78% | 89% | 44% | 89% | 44% |
| **N3a *krama sarcastic*** | **11%** | **11%** | **0%** | **0%** | **0%** |
| N3b *krama cold contempt* | 78% | 89% | 56% | 78% | 78% |

The N3a result is striking: across 45 total detector verdicts on krama-sarcastic cells, only **2 (4%)** correctly identify the content as hate. This holds for both cloud models (11% each) and all three local models (0%). N1 (*ngoko direct*) is caught at 100% everywhere — explicit hostility is trivial. The detection challenge is not *surface politeness* (N2 krama-report is caught at 78–89% by cloud models) but *pragmatic implicature*: an ironic over-compliment in krama does not contain lexically hateful tokens, only the pragmatic inversion of apparent praise into attack.

Nine of the 36 cells were missed by **all five detectors** simultaneously: seven of the eight krama-sarcastic cells plus two *krama-report × politik_kolektif* cells (polite political derogation reads as ordinary criticism to all five raters). These 9 cells represent the extremity of the blind spot — hate that the entire automated detection ecosystem cannot see.

A notable caveat: DeepSeek, which *generated* the krama-sarcastic attacks and coded them as hate internally, then *detects* only 11% of them when serving as a rater. This shows that generation capability does not imply detection capability at the pragmatic level; the model can produce ironic text by following a register-pragmatic prompt without learning to recognize the implicature from the surface form alone.

### 4.5. The authentic-but-evasive cross-tab

Combining native authenticity (§4.1) and detection status (§4.4), we can identify the cells that are simultaneously (a) native-authentic Javanese hate and (b) missed by detectors. Within the PRIORITAS (flagged-for-validation) subset and among items with machine-caught data, all items that evaded ≥ half the detectors were also native-validated as authentic. This is the key cross-tabulation: **the hate that detectors miss is real Javanese hate**, not edge cases or false positives. This makes the synthetic register-stratified set useful precisely as a *benchmark of failure*: a collection of examples that automated pipelines reliably miss.

### 4.6. Supporting results: labeling baseline confirms scarcity

The 728 labeled social-media texts (§3.1) provide the empirical grounding for the generation argument. Register is *ngoko* for 157/158 hate instances; the single krama instance lacks group identity and is not hate per taxonomy. *Krama*-hate consensus is zero. This is not a trivial finding — it directly rules out the alternative explanation that krama hate is collectable in volume and that generation is unnecessary. The labeling pipeline achieves a moderate cross-model agreement (cloud pair α 0.69 held-out, three-rater α 0.51 held-out), demonstrating that the multi-LLM consensus approach is reliable for the types of hate it can collect, while leaving the krama register uncovered by design of the data source.

The comparison with the source dataset's human labels (agreement 54.5%, κ = 0.19) reflects a definitional difference rather than an error [21]: the cultural prompt deliberately narrows hate to group-directed attacks, excluding bare profanity, and flags genuine Javanese identity slurs missed by an Indonesian-context annotator. This alignment between the labeling baseline and the generation taxonomy is methodological consistency, not an artifact.

### 4.7. Limitations

(1) **Native inter-rater reliability is low, not confirmatory.** The authenticity rates reported in §4.1–4.2 (Table 2, Table 3) come from the first author (native Javanese speaker). A second and third independent, blind pass on the same 108 items was subsequently completed by co-author Yekti Asmoro Kanthi (native Javanese speaker) and co-author Daniel Rudiaman Sijabat (a long-term East Java resident of 30 years, highly proficient in Javanese as an additional language, but not a native speaker). Each judged independently, blind to the first author's verdicts and to each other's answers. The result does not confirm the 55% figure as a stable consensus: per-validator authenticity rates were 55% (Mukhlis), 91% (Yekti), and 45% (Daniel), and pairwise Krippendorff's α on the binary authenticity judgment was 0.095 (Mukhlis–Yekti), 0.779 (Mukhlis–Daniel), and −0.039 (Yekti–Daniel), with a 3-rater α of 0.336 (95% CI [0.224, 0.449]) — below the conventional 0.667 threshold used even for tentative conclusions [15]. Notably, the two participants who are both native Javanese speakers (Mukhlis, Yekti) disagree at a level statistically indistinguishable from chance, while Daniel — despite not being a native speaker — tracks Mukhlis's judgments closely. We read this as a finding rather than a nuisance result: authenticity, as operationalized by a binary refereeing task, is not a high-consensus construct even between native Javanese speakers, and the 55%/97%/11% generator rates in Table 2 should be read as one qualified evaluator's estimate rather than an inter-subjectively validated ground truth. We therefore report all three rates and the full pairwise-α matrix rather than pooling them, and we do not use Daniel's agreement with Mukhlis to claim generalizability, since his linguistic background differs from the two native raters'. What drives the Mukhlis–Yekti divergence is not fully an open question: a follow-up analysis of the disagreement rows themselves finds a specific, largely explicable pattern, rather than unstructured noise. All 39 Mukhlis–Yekti disagreements run in one direction (Mukhlis judged "not authentic," Yekti judged "authentic"); 19 of the 27 *krama-sarcastic* items (70% of that niche) are disagreement rows, and the niche accounts for 19/39 (49%) of all disagreements — either way, *krama-sarcastic* (already the hardest niche in Table 3) dominates. In 34 of the 39 rows Yekti's own notes mark the item as ambiguous on the hate dimension (JELAS_HATE = 0), 31 of which explicitly cite code-mixing with Indonesian as unremarkable to her ("*Campur wajar*" — mixing is normal). Recomputing agreement with Yekti's two answers combined (authentic AND clearly-hate, approximating the single question Mukhlis's original one-column instrument had to answer at once) raises Mukhlis–Yekti α from 0.095 to 0.519 — moderate, not chance-level; this correction does not extend to Daniel, whose agreement with Mukhlis instead *drops* under the same transformation (0.779 to 0.448), and whose 12 disagreements pair JELAS_HATE = 1 with OTENTIK = 0 in 9 cases, consistent with a non-native rater doubting register correctness even when the hateful content is legible to him. Two things follow. First, a real part of the apparent native–native disagreement is an instrument artifact: Yekti's form separates "is this real Javanese" from "does this register as hate," while Mukhlis's original single-column form (fielded before the two-dimension split was introduced) could not. Second, the remaining, non-artifactual part tracks validator linguistic background: Yekti's home environment normalizes Javanese–Indonesian code-switching as everyday speech, while the first author's more Javanese-homogeneous environment treats the same code-mixing as a purity failure — a distinction consistent with documented urbanization- and class-linked *krama* attrition in Javanese sociolinguistics [26]. This is the same axis as Limitation (4) below (Central-Javanese prestige-purity norms vs. heterogeneous/Arek-urban norms), surfacing on the validation side of the pipeline rather than the generation side. A related, unresolved question this raises: "authentic Javanese" as judged here reflects the specific linguistic communities of our three validators, and content targeting an ethnic-minority group with its own documented Javanese sociolect (e.g., Chinese-Indonesian speakers, whose Javanese is reportedly distinguishable to other native ears) was not separately checked by a rater from that community — an open question for future validation rounds, not a claim this paper makes. Future authenticity claims for this stimulus-construction method should still report a range or per-rater breakdown rather than a single pooled percentage. (2) **Advisory scale.** 108 examples across 36 cells is sufficient for a controlled proof of concept, not a training dataset; the synthetic set demonstrates the failure mode rather than benchmarking it at statistical power. (3) **Generator bias.** DeepSeek's krama examples use a small set of recurring devices (the "lacks-isin/unggah-ungguh" accusation in N3b; "Mugi…enggal" opener in N2); whether these devices are representative of real krama hate diversity or artifacts of LLM text distribution is an open empirical question. (4) **Regional krama.** DeepSeek defaults to Central-Javanese krama prestige norms; East-Java/Arek krama variants are under-represented or absent. The same prestige-purity-vs-heterogeneous-urban axis reappears on the validation side in Limitation (1) above (validators' differing tolerance for code-switched Javanese as "authentic"), suggesting this is a general property of the register, not an artifact of one generator model. (5) **Detection scope.** The probe covers five detectors all using the same cultural prompt; detectors using different taxonomies or training data may differ.

### 4.8. Ethics

This work is a detection audit, not a generation showcase: LLMs are used to construct the minimum set of stimuli needed to demonstrate a detection failure mode, and the paper's contribution is the diagnosis — a taxonomy and a measured blind spot — not the stimuli themselves. All synthetic texts were generated as controlled research stimuli, gitignored from the public repository, and handled under an ethics policy that treats them as equivalent to expert-produced test stimuli. The labeling corpus consists of public social-media posts; handles, mentions, and contact information were anonymized before labeling and the clean release is the only public version.

**Dual-use statement.** A method that reveals which forms of hate speech evade automated detection could, in principle, be repurposed to craft evasive hate speech. We mitigate this risk in three ways. First, the released artifact is the *diagnosis* — taxonomy, codebook, detection results, and evaluation scripts — not a general-purpose generation model; no fine-tuned or otherwise repurposable generator is released. Second, the synthetic stimulus set itself will be released under a restricted, gated, research-only license (no redistribution, request-based access), following norms established by adversarial test-suite resources such as HateCheck [22]. Third, the paper's conclusion (§5) is a call to close the blind spot in moderation systems, not to exploit it; we regard this as analogous to responsible vulnerability disclosure in security research, where documenting a flaw is the step that precedes and motivates its repair.

---

## 5. CONCLUSION

We diagnosed a systematic detection blind spot in Javanese hate speech: ironic and coldly contemptuous hostility carried in the *krama* honorific register evades automated detection almost entirely (4% correctly flagged), while explicit *ngoko* hate is caught at 100%. To make this blind spot measurable despite *krama* hate being structurally absent from social media — a collection paradox confirmed by two independent scarcity measurements — we constructed a register-stratified diagnostic stimulus set using LLMs as a construction method, validated for native authenticity (97% for the strongest generator, DeepSeek); cheaper local models (Qwen3-14B) fail entirely at *krama* registers. The failure traces to pragmatic implicature (*pasemon*), not surface politeness — *krama-report* content without irony is still caught at 78–89%. These findings have direct implications for moderation system design: a hate-speech classifier trained or evaluated only on *ngoko* data will systematically miss the coldest, most status-damaging form of Javanese group attack. The register-pragmatic taxonomy, diagnostic construction scripts, native validation instrument, and detection probe are released — the stimulus set itself under a restricted, research-only license — as reproducible infrastructure for auditing detection blind spots in other diglossic, register-rich languages.

---

## GEN AI DISCLOSURE STATEMENT

In accordance with the JINITA Generative AI policy: large language models are the *object of study and primary method* of this work [10], [11], [24] and are described in full in Sections 3 and 4. Separately, the authors used an AI assistant to help draft and copy-edit portions of this manuscript. All AI-assisted text, all numerical results, and all references were reviewed and verified by the authors, who take full responsibility for the content; no references were generated without author verification. No confidential or personally identifiable data were submitted to third-party AI tools beyond the already-public, anonymized corpus.

---

## ACKNOWLEDGEMENTS

*(To be completed: institutional support from Universitas Bhinneka Nusantara; any grant or sponsor; compute resources — RTX 4080 local inference.)*

---

## REFERENCES

> *IEEE numbered style. Verified 2026-07-06 (lit-pass, D20) via ACL Anthology / arXiv / Crossref / IEEE Xplore / DBLP / publisher records — no fabricated details per JINITA Gen AI policy. Two references present in an earlier draft (Gwet 2008; AI Singapore SEA-LION) were removed because they were never actually cited in the body text of this version of the paper (a leftover from an earlier draft's scope) — every reference below is cited at least once. One entry, [4], has a publisher/aggregator page-range discrepancy noted inline and should get a final manual check before submission.*

[1] A. F. Aji, G. I. Winata, F. Koto, S. Cahyawijaya, A. Romadhony, R. Mahendra, K. Kurniawan, D. Moeljadi, R. E. Prasojo, T. Baldwin, J. H. Lau, and S. Ruder, "One country, 700+ languages: NLP challenges for underrepresented languages and dialects in Indonesia," in *Proc. 60th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, 2022, pp. 7226–7249, arXiv:2203.13357.

[2] S. Cahyawijaya et al., "NusaCrowd: Open source initiative for Indonesian NLP resources," in *Findings of the Assoc. Comput. Linguistics: ACL 2023*, pp. 13745–13818, arXiv:2212.09648.

[3] I. Alfina, A. Yuliawati, D. Tanaya, and D. Zeman, "A gold standard dataset for Javanese tokenization, POS tagging, morphological feature tagging, and dependency parsing," *Forum for Linguistic Studies*, vol. 6, no. 5, pp. 131–148, 2024, doi: 10.30564/fls.v6i5.6957.

[4] S. D. A. Putri, M. O. Ibrohim, and I. Budi, "Abusive language and hate speech detection for Javanese and Sundanese languages in tweets: Dataset and preliminary study," in *Proc. 2021 11th Int. Workshop Comput. Sci. Eng. (WCSE)*, Hong Kong, 2021, pp. 65–69, doi: 10.18178/wcse.2021.02.011. *(Publisher lists pp. 65–69; one aggregator lists pp. 461–465 — confirm exact pages before submission.)*

[5] M. O. Ibrohim and I. Budi, "Multi-label hate speech and abusive language detection in Indonesian Twitter," in *Proc. 3rd Workshop on Abusive Language Online (ALW3), ACL*, 2019, pp. 46–57, doi: 10.18653/v1/W19-3506.

[6] J. J. Errington, *Structure and Style in Javanese: A Semiotic View of Linguistic Etiquette*. Philadelphia, PA, USA: Univ. of Pennsylvania Press, 1988.

[7] haipradana (Pradana Yahya Abdillah), "indonesian-twitter-hate-speech-cleaned," Hugging Face Datasets, 2025. [Online]. Available: https://huggingface.co/datasets/haipradana/indonesian-twitter-hate-speech-cleaned

[8] M. Amien, "Digital Vitality Index for Indonesian regional languages on Twitter: a lexicon-based measurement across 32 cities," unpublished data, 2026. Companion measurement, cited with the author's permission; not part of the present dataset.

[9] T. Davidson, D. Warmsley, M. Macy, and I. Weber, "Automated hate speech detection and the problem of offensive language," *Proc. Int. AAAI Conf. Web and Social Media (ICWSM)*, vol. 11, no. 1, pp. 512–515, 2017, doi: 10.1609/icwsm.v11i1.14955.

[10] F. Gilardi, M. Alizadeh, and M. Kubli, "ChatGPT outperforms crowd workers for text-annotation tasks," *Proc. Natl. Acad. Sci. (PNAS)*, vol. 120, no. 30, e2305016120, 2023.

[11] C. Ziems, W. Held, O. Shaikh, J. Chen, Z. Zhang, and D. Yang, "Can large language models transform computational social science?," *Comput. Linguistics*, vol. 50, no. 1, pp. 237–291, 2024, doi: 10.1162/coli_a_00502.

[12] A. G. Møller, A. Pera, J. Dalsgaard, and L. M. Aiello, "The parrot dilemma: Human-labeled vs. LLM-augmented data in classification tasks," in *Findings of the Assoc. Comput. Linguistics: EACL 2024*, pp. 179–192, doi: 10.18653/v1/2024.eacl-short.17.

[13] E. W. Pamungkas, D. Purworini, W. Widayat, D. G. P. Putri, and I. Amal, "Enhancing hate speech detection in low-resource code-mixed Indonesian tweets via GPT-based data augmentation," *Eng., Technol. & Appl. Sci. Res. (ETASR)*, vol. 15, no. 6, pp. 30649–30656, 2025, doi: 10.48084/etasr.14342.

[14] E. W. Pamungkas and P. Chiril, "Ngalawan Ujaran Sengit: Hate speech detection in Indonesian code-mixed social media data," *Lang. Resources and Evaluation*, vol. 59, no. 3, pp. 2387–2414, 2025, doi: 10.1007/s10579-025-09810-x.

[15] K. Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4th ed. Thousand Oaks, CA, USA: SAGE, 2019.

[16] B. Wilie et al., "IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding," in *Proc. AACL-IJCNLP*, 2020, pp. 843–857, doi: 10.18653/v1/2020.aacl-main.85.

[17] G. I. Winata, S. Cahyawijaya, Z. Liu, Z. Lin, A. Madotto, and P. Fung, "Are multilingual models effective in code-switching?," in *Proc. 5th Workshop on Computational Approaches to Linguistic Code-Switching (CALCS), NAACL-HLT*, 2021, pp. 142–153, doi: 10.18653/v1/2021.calcs-1.20.

[18] DeepSeek-AI, "DeepSeek-V3 technical report," arXiv preprint arXiv:2412.19437, 2024.

[19] Qwen Team, "Qwen3 technical report," arXiv preprint arXiv:2505.09388, 2025.

[20] I. Alfina, R. Mulia, M. I. Fanany, and Y. Ekanata, "Hate speech detection in the Indonesian language: A dataset and preliminary study," in *Proc. ICACSIS*, 2017, pp. 233–237, doi: 10.1109/ICACSIS.2017.8355039.

[21] M. Wiegand, J. Ruppenhofer, and T. Kleinbauer, "Detection of abusive language: The problem of biased datasets," in *Proc. NAACL-HLT*, 2019, pp. 602–608.

[22] P. Röttger, B. Vidgen, D. Nguyen, Z. Waseem, H. Margetts, and J. Pierrehumbert, "HateCheck: Functional tests for hate speech detection models," in *Proc. 59th Annu. Meeting Assoc. Comput. Linguistics and 11th Int. Joint Conf. Natural Language Process. (ACL-IJCNLP), Vol. 1: Long Papers*, 2021, pp. 41–58, doi: 10.18653/v1/2021.acl-long.4.

[23] A. Joshi, P. Bhattacharyya, and M. J. Carman, "Automatic sarcasm detection: A survey," *ACM Comput. Surv.*, vol. 50, no. 5, Art. 73, 2017, doi: 10.1145/3124420.

[24] P. Törnberg, "Best practices for text annotation with large language models," *Sociologica*, vol. 18, no. 2, pp. 67–85, 2024, doi: 10.6092/issn.1971-8853/19461.

[25] M. Ravindranath and A. C. Cohn, "Can a language with millions of speakers be endangered?," *J. Southeast Asian Linguistics Society (JSEALS)*, vol. 7, pp. 64–75, 2014.

[26] N. J. Smith-Hefner, "Language shift, gender, and ideologies of modernity in Central Java, Indonesia," *J. Linguistic Anthropology*, vol. 19, no. 1, pp. 57–77, 2009, doi: 10.1111/j.1548-1395.2009.01019.x.

---

## APPENDIX: Paper v3 → v4 change log (internal, remove before submission)

| Section | Change |
|---|---|
| Title | Labeling → generation framing |
| Abstract | Rewritten: generator + validation + detection blind spot (was: labeling + α + κ) |
| §1 Introduction | Added: collection paradox, register motivation, generation rationale. Preserved: prior-failure story, zero-human motivation |
| §2 Taxonomy | Added: register-pragmatic model (4 niches Table). §2.4 *krama* uncollectable = new. §2.1–2.2 taxonomy same |
| §3 Method | Restructured: generation as main (§3.2–3.3); labeling as scarcity baseline (§3.1). Old §3.3–3.5 condensed |
| §4 Results | Replaced: §4.1–4.5 = generation/detection results. Old §4.1–4.8 condensed into §4.6 + moved to supp |
| §5 Conclusion | Rewritten: detection blind spot + register implication |
| References | [3], [11]–[13], [24] added; [7] updated; [22]–[23] retained |

## APPENDIX: Paper v4 → v5 change log (internal, remove before submission)

Session 2026-07-06 (D20). Reframe from generation-headline to diagnostic-suite framing per Bapak's decision (venue target: JINITA Sinta 2 only, not the Scopus/Q-tier stretch package — see `STRATEGY.md`).

| Section | Change |
|---|---|
| Affiliation | **Correction:** "Universitas Bina Husada Nusantara" → correct name **"Universitas Bhinneka Nusantara"** (UBHINUS = **U**niversitas **B**H**I**nneka **NUS**antara; a new university, formerly STIKI Malang). Same fix applied to `codebook/CODEBOOK.md`. |
| Title | "...Hate Speech Generation via LLMs" → "Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection" — blind spot is now the headline, generation is the method |
| Abstract | Rewritten and reordered (still ≤250 words): leads with the blind-spot diagnosis; generation described as construction method; adds the Table 1 scarcity anchor sentence |
| §1 Introduction | Added: Table 1 + companion-measurement paragraph (independent Twitter DVI scarcity anchor, [8], see below). "This paper addresses..." paragraph reframed: diagnostic approach, generation as means not end |
| Contributions | Reordered: blind-spot proof now (1); taxonomy (2) explicitly framed as explaining the blind spot; diagnostic stimulus set (3) states the restricted-license rationale inline; codebook/scripts (4) unchanged in substance |
| §3.2 | Retitled "Register-stratified generation" → "Constructing the diagnostic stimulus set"; opening sentence reworded (generate → construct) |
| §4.7 Limitations | Item (1) updated: second/third native validator pass (Yekti, Daniel — confirmed active Javanese speakers) now described as in progress, not conditional |
| §4.8 Ethics | Added **Dual-use statement** subsection (three-part mitigation: no repurposable generator released, gated/restricted stimulus-set license per HateCheck norms, vulnerability-disclosure framing) |
| §5 Conclusion | Rewritten to lead with the diagnosis, not the generation approach |

## APPENDIX: Paper v5 → v6 change log (internal, remove before submission)

Session 2026-07-07. Yekti and Daniel filled the blind validation forms; `score_multivalidator.py` run for the first time.

| Section | Change |
|---|---|
| §4.7 Limitations | Item (1) rewritten from "pass in progress" to actual results: per-validator rates (55%/91%/45%), full pairwise-α matrix (Mukhlis–Yekti 0.095, Mukhlis–Daniel 0.779, Yekti–Daniel −0.039, 3-rater 0.336), reframed as a finding (native–native judgment disagrees near chance) rather than an IRR confirmation |
| §4.7 Limitations | **Correction:** Daniel Rudiaman Sijabat's credential corrected from "confirmed active Javanese speaker" (native) to "long-term East Java resident (30 years), highly proficient in Javanese as an additional language, not a native speaker" — this was inaccurate in earlier drafts and in `PRD.md`/`HANDOFF.md`/wiki (being corrected separately) |
| References | **Full lit-pass completed (D20, 2026-07-06):** all 26 v4 references checked against ACL Anthology/arXiv/Crossref/IEEE Xplore/DBLP/publisher records. Of 5 entries marked "(Authors TBD)": 2 were genuinely fabricated and replaced ([3] Javanese NLP benchmark → real Javanese treebank paper; former [25] sarcasm survey → Joshi et al. ACM CSUR); 3 turned out to correspond to real papers with that exact title, just missing author/venue details, now filled in (former [13]/[14] Pamungkas et al. Indonesian code-mixed hate speech GPT-augmentation papers; former [26] Törnberg LLM-annotation paper). 9 entries had wrong/incomplete details corrected (wrong title words, wrong venue, wrong pages, or a fabricated 4th author in one case — Møller et al.). 2 entries (Gwet 2008; SEA-LION) were **dropped**, not because they were inaccurate but because they were never actually cited anywhere in this version's body text — a leftover from an earlier draft's scope; every reference must be cited at least once. New [8] = companion Twitter DVI measurement (unpublished, cited with permission, E7). **10 previously-uncited references now have real in-text citations added** at natural points (Krippendorff at the α-Krippendorff mention; DeepSeek/Qwen3 at first mention in §3.2; Møller's "Parrot Dilemma" and the two Pamungkas papers as related work in §1; IndoNLU/Winata alongside the resource-landscape and code-mixing claims; Wiegand at the source-dataset-comparison discussion in §4.6; sarcasm survey at "irony recognition" in §2.4; Gilardi/Ziems/Törnberg in the Gen AI Disclosure). Final count: **24 references, all cited, DOIs/arXiv IDs included where available.** One item ([4], WCSE 2021 pages) has a publisher-vs-aggregator page discrepancy flagged inline for a final manual check. HateCheck (formerly [24], now [22]) remains cited in the Dual-use statement. |
| Not changed (at time of writing; see P0 fixes below for a later §4.1 addition) | §2 Taxonomy, §3.1 scarcity baseline, §3.3–3.4 method detail, §4.1–4.6 results — all substantively unchanged per Bapak's instruction not to rewrite what already works |
| §4.7 Limitations | Item (1) extended with a disagreement-row diagnosis (Bapak's own hypothesis, verified against the data): all 39 Mukhlis–Yekti disagreements run one direction, 70% concentrate in *krama-sarcastic*, and most trace to (a) an instrument artifact (Mukhlis's original single-column form conflates authenticity with hate-clarity; harmonizing recovers α 0.095→0.519) and (b) validator linguistic background (Yekti's heterogeneous/code-switching-normalized environment vs. the first author's more homogeneous one) — cross-referenced to Limitation (4). Added a one-sentence open question re: ethnolect-specific validation (e.g., Chinese-Indonesian Javanese) not being separately checked. |
| §4.7 Limitations | Item (4) Regional krama: added one sentence cross-referencing Limitation (1)'s validator-background finding as the same prestige-purity-vs-heterogeneous axis on the other side of the pipeline |
| §1 Introduction | Added one sentence after the Table 1/DVI scarcity paragraph, citing new refs [25]–[26]: large speaker population does not contradict domain-specific scarcity, per documented Javanese-specific sociolinguistic literature |
| References | Added **[25]** Ravindranath & Cohn 2014 ("Can a language with millions of speakers be endangered?", JSEALS) and **[26]** Smith-Hefner 2009 (krama attrition, J. Linguistic Anthropology) — both verified via independent web search + primary-source fetch before citing, appended at the end of the list rather than renumbered in (existing body citations are not in strict first-appearance order already, e.g. [16]/[20] appear before other lower numbers — appending avoids introducing new renumbering risk into an already lit-pass-verified list) |

### P0 fixes following Fable's audit of the E1 results (STRATEGY.md §12, same day)

Fable reviewed the diagnosis above and found a denominator error already in the text, plus cited numbers that had never been reproduced from a committed script. P0-1/P0-2/P0-4 below are fixed; P0-3 (E6-lite JELAS_HATE × machine_caught cross-tab) surfaced a result gated to Bapak per STRATEGY.md's explicit guard rail (do not rewrite §4.5 before that number is reviewed) — see `experiments/generation_pilot/disagreement_analysis.md` for the number and the open question raised to Bapak.

| Section | Change |
|---|---|
| §4.7 Limitations | **Fixed denominator bug (P0-1):** "70% (19/27) concentrate in the krama-sarcastic niche" conflated two different fractions. Corrected to state both correctly: 19 of the 27 krama-sarcastic items (70% of that niche) are disagreement rows, and the niche accounts for 19/39 (49%) of all disagreements. |
| — | **Reproducibility (P0-2):** all disagreement-diagnosis numbers in Limitation (1) (39/12 disagreements, direction counts, niche breakdown, JELAS_HATE distribution, the 31-row code-switching-note count and its nesting inside the 34 JELAS_HATE=0 rows, harmonized alpha 0.095→0.519 / 0.779→0.448) are now reproduced by a committed script, `experiments/generation_pilot/analyze_disagreement.py` → `disagreement_analysis.md`, cross-checked against a second, differently-coded closed-form alpha implementation during development (documented in the script's docstring). Previously these were computed ad-hoc and not rerunnable, a D17 SOP gap. |
| §4.1 | **Added (P0-4):** one paragraph reporting that the DeepSeek-first, DeepSeek > Gemma3-27B > Qwen3-14B ranking in Table 2 holds for all three validators (Mukhlis/Yekti/Daniel), not just Mukhlis — the headline generator-quality claim is robust to multi-rater scrutiny even though the pooled 55% figure is not. |
| §4.5 | **Not yet edited — gated to Bapak.** The E6-lite cross-tab (P0-3) found that of the 9 cells that evade all 5 detectors, 0/9 are rated JELAS_HATE=1 by Yekti and 0/9 by Daniel (both say these specific items do not clearly read as hate). This weakens, without a caveat, the current §4.5 claim that "the hate that detectors miss is real Javanese hate." Per STRATEGY.md's guard rail, this is not rewritten here; see the AskUserQuestion raised to Bapak in the same session. |
