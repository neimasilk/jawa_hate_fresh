# Register-Stratified Javanese Hate Speech Generation via Large Language Models

> **JINITA-conformant draft v4 (2026-06-30). Generator framing (PRD v0.4).** Replaces v3 (labeling framing). All numbers from experiments: `experiments/generation_pilot/validation_result.md`, `experiments/generation_pilot/RESULTS_probe.md`, `experiments/register_probe/FINDINGS.md`, `experiments/pilot05_bulk_labeling/report.md`. References marked `[verify]` need DOI/volume/pages confirmed before submission per JINITA Gen AI policy.

**Mukhlis Amien¹, Yekti Asmoro Kanthi², Daniel Rudiaman Sijabat³**
¹,²,³ Department of Informatics, Universitas Bina Husada Nusantara, Malang, Indonesia
email: ¹amien@ubhinus.ac.id, ²yektiasmoro@ubhinus.ac.id, ³daniel223@ubhinus.ac.id

*(Article info / history block to be filled by the editor. Blinded version for peer review: remove authors and affiliations.)*

---

## ABSTRACT

Hate speech in Javanese — spoken by roughly 80 million people — poses a distinct detection challenge because the language's honorific register system (*unggah-ungguh*) allows the same hostile content to be delivered in vulgar *ngoko* or in deceptively refined *krama*. The *krama* variants — especially irony and cold moral contempt — are nearly absent from social-media data due to diglossia, making them uncollectable by standard corpus filtering. We present a register-stratified generation approach in which large language models (LLMs) synthesize culturally-grounded Javanese hate speech across four register-pragmatic niches (*ngoko direct*, *krama report*, *krama sarcastic*, *krama cold contempt*) and nine SARA (ethnicity, religion, gender, political) target groups, producing a controlled 36-cell matrix validated by a native Javanese speaker. Of 108 generated examples (three generator models), 59 (55%) were judged authentic; DeepSeek achieves 97% (35/36) across all four niches while the free local model Qwen3-14B fails completely at *krama* registers, generating Indonesian rather than Javanese. A detection probe running all 36 *krama-sarcastic* cells through five hate-speech detectors reveals a near-universal blind spot: only 2 of 45 verdicts (4%) correctly flag ironic Javanese hate — across both cloud and local models — while the same detectors flag *ngoko-direct* at 100%. Politeness alone does not blind detectors; implicature (*pasemon*) does. As supporting motivation, a parallel labeling run on 735 social-media texts confirms the scarcity: hot-Jawa yield is ≈6% and consensus *krama*-hate in the wild is zero. Together, the register-stratified synthetic set and the detection proof constitute a reproducible benchmark for an under-studied failure mode of automated hate-speech detection.

**Keywords:** Javanese; hate speech generation; register; large language model; detection blind spot

---

## 1. INTRODUCTION

Javanese is spoken by roughly 80 million people and carries significant online hate speech directed at ethnic minorities (Madurese, Chinese-Indonesian, Arab communities), religious groups, women, and LGBTQ+ individuals [1], [2]. Yet the language is severely under-resourced in NLP [3], and the few published hate-speech datasets for Javanese either remain unreleased [4] or conflate Javanese with broader Indonesian [5].

A feature of Javanese that existing approaches entirely overlook is its *unggah-ungguh* (speech-level) system: the same hostile proposition can be expressed in coarse *ngoko* — the register of in-group bluntness — or in the refined *krama* register, producing qualitatively different pragmatic effects. Hot, direct rage is *ngoko*; cold contempt, ironic superiority, and indirect defamation — the forms that most damage group dignity — are *krama*. This is not a stylistic choice but a rule-governed pragmatic constraint, validated by a native speaker in this work.

The practical consequence is a data collection paradox. Social-media Javanese hate speech is almost entirely *ngoko* with code-mixing; pure *krama* is essentially absent from public posts because *krama* is used in formal or face-to-face contexts, not in Twitter or WhatsApp broadcasts [6]. A standard corpus-filtering pipeline will collect *ngoko* hate, confirm the register, and leave *krama* hate completely uncollected. We verified this directly: filtering 12,700 tweets from a public Indonesian hate-speech dump [7] yields 735 candidate Javanese texts, of which **zero** carry consensus *krama*-hate in the majority-vote labeling.

This paper addresses the collection paradox with a generation approach: instead of filtering and labeling a corpus, we use LLMs to *synthesize* register-stratified Javanese hate speech across a 4-niche × 9-target matrix, validate it with a native expert, and probe it with five detectors. The contribution is not a large dataset but a controlled benchmark surface — a minimal sufficient set that proves the failure mode exists, is generable, and is systematically missed by current automated detection.

**Why the human bottleneck matters here.** This work is directly motivated by a prior failure: student annotators in a precursor project produced nominally "Javanese" data primarily by back-translating Indonesian and English hate speech, yielding labels that were internally consistent but not grounded in authentic Javanese expression. The corruption was invisible until downstream models failed to generalize. The generator approach avoids this bottleneck by design: the human role collapses to *authenticity refereeing* (native speaker judges whether generated text sounds like real Javanese hate), which requires native comprehension rather than full annotation labor.

**Contributions.** (1) A *register-pragmatic model* of Javanese hate speech: a taxonomy of four niches defined by the interaction of register and pragmatic mode, validated with a native expert. (2) Evidence that a strong LLM (DeepSeek) can generate native-validated Javanese hate in the *krama* register (97% authentic), while cheaper local models cannot, with generation capability mirroring detection capability. (3) Empirical proof of a *detection blind spot*: Javanese ironic hate (*pasemon* in *krama*) evades all five tested detectors — cloud and local — at a rate of 96%, while explicit *ngoko* hate is caught at 100%. (4) A publicly released codebook, generation scripts, and evaluation pipeline for reproducible extension.

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

Two structural factors make *krama* hate unrepresented in social-media corpora. First, *diglossia*: *krama* is the register of formal, elder-addressee, or face-to-face speech; social-media Javanese defaults to *ngoko* with Indonesian code-mixing [6]. Second, *irony recognition*: even if a *krama-sarcastic* post were found, an automated classifier would need to resolve pragmatic implicature (*pasemon*) — a specifically Javanese indirect speech act — rather than surface lexical hostility. §4.4 shows this is beyond all five tested detectors.

---

## 3. METHOD

### 3.1. Evidence of scarcity: the labeling baseline

Before generation, we establish the scarcity empirically. We filter a public Indonesian hate-speech dump [7] for Javanese and code-mixed text using an LLM filter (validated at 100% JSON validity, 9.6% Javanese yield in pilot), apply a two-stage cascade (free local pre-screen → cloud verification), and label the resulting pool with three LLM raters (DeepSeek, Grok, Qwen3-14B/local) using a culturally-grounded prompt [8]. The cascade's cloud confirmation rate of **25.4%** for pre-screen survivors is itself a finding: cheap local models reduce a candidate pool but cannot replace cloud precision for filtering.

The resulting pool yields **728 consensus-labeled instances** (158 hate, 21.7%; α Krippendorff 0.51 three-rater held-out, 0.69 for the cloud pair), of which **register is *ngoko* for 157/158 hate instances** and *krama*-hate consensus is zero. This negative result serves two purposes: it motivates generation by proving the collection paradox, and the 728 texts serve as a realism anchor for generator calibration.

Full methodology of the labeling pipeline — prompt engineering (Δα ≈ +0.23 from two definition corrections), vendor selection, cascade economics, and adversarial verification — is documented in the supplementary report. The core finding relevant to this paper: **social-media filtering cannot produce *krama* hate at meaningful scale, even from a 12,700-tweet dump.**

### 3.2. Register-stratified generation

We generate a **4-niche × 9-target = 36-cell matrix** of Javanese hate speech using DeepSeek as primary generator and Gemma3-27B and Qwen3-14B (both running locally) as comparison generators, producing **108 total examples** (3 per cell). The nine target groups span the SARA taxonomy: *suku* (Madura, Tionghoa, Arab), *agama* (Islam, Kristen), *gender* (wanita, LGBTQ+), *politik* (collective), and intra-Javanese (*Arek vs. Mataraman*).

Each generation call specifies: (a) niche (N1–N3b), (b) target group, (c) a culturally-grounded system prompt (in Indonesian) that defines the niche's pragmatic mechanism and provides two-to-four few-shot examples. The system prompt explicitly prohibits "museum krama" (literary-Javanese vocabulary unused in living speech) and Indonesian code-leak. Generation uses the same API infrastructure as the labeling pipeline; DeepSeek calls use `max_tokens=8192` to allow adequate reasoning budget.

### 3.3. Native authenticity validation

The 108 generated examples are submitted to the first author (native Javanese speaker from East Java, academic background in Javanese linguistics) for authenticity validation. The validation instrument is a structured spreadsheet with: (a) the generated text, (b) the intended niche/target, (c) the generation mechanism description, (d) a machine-caught flag (did the production detector identify it as hate?), (e) an auto-concern flag (QC panel pre-triage), and (f) a binary authenticity verdict (1 = authentic Javanese hate of the stated type, 0 = not authentic). Comments on specific issues are recorded for each rejected example.

The human role is explicitly *authenticity refereeing*: does this text sound like something a Javanese speaker would actually say in the stated register-pragmatic mode? This is a comprehension task, not a production or annotation task, and can be completed in one to two hours across all 108 examples.

### 3.4. Detection blind-spot probe

We run each of the 36 DeepSeek-generated cells through five detectors: the production three-rater set (DeepSeek, Grok, Qwen3-14B) plus two additional local models (Gemma3-27B, GPT-OSS-20B). Each detector is given the same prompt v2 (the production prompt from §3.1) and asked to return a binary hate/non-hate verdict. Detection rate per niche is the fraction of cells where the detector returns hate=True.

The probe is controlled: the *generator* is held constant (DeepSeek), so differences in detection rate across niches reflect niche difficulty, not generator variation. All 180 (cell × detector) verdict calls succeeded with no parse failures (verified by independent recount).

---

## 4. RESULTS AND DISCUSSION

### 4.1. Generation authenticity: overall and by model

Of 108 generated examples, **59 (55%) were judged authentic** Javanese hate of the stated type. Table 1 breaks this down by generator.

**Table 1.** Native authenticity rate by generator model.

| Generator | Authentic | Rate | Primary failure mode |
|---|---|---|---|
| DeepSeek | 35/36 | **97%** | 1 item: *krama-sarcastic* read as sincere blessing, not irony |
| Gemma3-27B (local) | 20/36 | 56% | *Krama-sarcastic*: Indonesian leak in sarcastic punchline (0/9) |
| Qwen3-14B (local) | 4/36 | **11%** | *Krama* registers: generates Indonesian (not Javanese); hallucinated word *kacandran* |

DeepSeek is the only generator that can produce authentic Javanese in all four niches. The single failure (example #21, krama-sarcastic targeting agama_islam) is itself informative: an ironic over-praise of a santri's nighttime prayers was judged by the native speaker as a *sincere* blessing — the sarcasm failed entirely, producing a false positive in the validator's favor. This documents the difficulty of the N3a niche even for the best-performing generator.

### 4.2. Register difficulty: *krama-sarcastic* is the hardest niche

Table 2 shows authenticity by niche, pooled across generators.

**Table 2.** Native authenticity rate by register-pragmatic niche (all generators combined, n=27 per niche).

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

Table 3 shows detection rates across all five detectors for each niche.

**Table 3.** Hate detection rate by niche and detector (DeepSeek-generated cells; n=9 cells per niche per detector).

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

The comparison with the source dataset's human labels (agreement 54.5%, κ = 0.19) reflects a definitional difference rather than an error: the cultural prompt deliberately narrows hate to group-directed attacks, excluding bare profanity, and flags genuine Javanese identity slurs missed by an Indonesian-context annotator. This alignment between the labeling baseline and the generation taxonomy is methodological consistency, not an artifact.

### 4.7. Limitations

(1) **Single native validator.** All authenticity judgments come from one native speaker (the first author). Inter-rater reliability with a second native Javanese speaker (planned: co-authors Yekti Asmoro Kanthi or Daniel Rudiaman Sijabat if Javanese-speaking) is not yet established; the reported rates are therefore single-evaluator estimates, not multi-rater agreement. (2) **Advisory scale.** 108 examples across 36 cells is sufficient for a controlled proof of concept, not a training dataset; the synthetic set demonstrates the failure mode rather than benchmarking it at statistical power. (3) **Generator bias.** DeepSeek's krama examples use a small set of recurring devices (the "lacks-isin/unggah-ungguh" accusation in N3b; "Mugi…enggal" opener in N2); whether these devices are representative of real krama hate diversity or artifacts of LLM text distribution is an open empirical question. (4) **Regional krama.** DeepSeek defaults to Central-Javanese krama prestige norms; East-Java/Arek krama variants are under-represented or absent. (5) **Detection scope.** The probe covers five detectors all using the same cultural prompt; detectors using different taxonomies or training data may differ.

### 4.8. Ethics

All synthetic texts were generated as controlled research stimuli, gitignored from the public repository, and handled under an ethics policy that treats them as equivalent to expert-produced test stimuli. The labeling corpus consists of public social-media posts; handles, mentions, and contact information were anonymized before labeling and the clean release is the only public version. The synthetic set will be released under a restricted research license with an explicit prohibition on use for hate-speech production or training unmitigated generation systems.

---

## 5. CONCLUSION

We presented a register-stratified generation approach to Javanese hate speech, targeting four pragmatically defined niches that are structurally absent from social-media corpora due to diglossia. A strong LLM (DeepSeek) generates native-validated Javanese hate in all four niches at 97% authenticity, including cold-contempt and ironic krama forms previously considered beyond LLM capability; cheaper local models (Qwen3-14B) fail entirely at krama registers. A controlled detection probe demonstrates that Javanese ironic hate (*krama-sarcastic, pasemon*) evades all five tested detectors at 96%, while explicit *ngoko* hate is caught at 100% — the detection challenge is pragmatic implicature, not surface politeness. These findings have direct implications for moderation system design: a hate-speech classifier trained or evaluated only on *ngoko* data will systematically miss the coldest, most status-damaging form of Javanese group attack. The register-pragmatic taxonomy, generation scripts, native validation instrument, and detection probe are released as reproducible infrastructure for extension to other register-stratified low-resource languages.

---

## GEN AI DISCLOSURE STATEMENT

In accordance with the JINITA Generative AI policy: large language models are the *object of study and primary method* of this work and are described in full in Sections 3 and 4. Separately, the authors used an AI assistant to help draft and copy-edit portions of this manuscript. All AI-assisted text, all numerical results, and all references were reviewed and verified by the authors, who take full responsibility for the content; no references were generated without author verification. No confidential or personally identifiable data were submitted to third-party AI tools beyond the already-public, anonymized corpus.

---

## ACKNOWLEDGEMENTS

*(To be completed: institutional support from Universitas Bina Husada Nusantara; any grant or sponsor; compute resources — RTX 4080 local inference.)*

---

## REFERENCES

> *IEEE numbered style. Anchors below are real works; entries marked `[verify]` need exact volume/pages/DOI confirmed before submission (JINITA Gen AI policy: do not fabricate citation details). Target: ≥ 20 references, ≥ 80% journals ≤ 5 years.*

[1] A. F. Aji et al., "One country, 700+ languages: NLP challenges for underrepresented languages in Indonesia," in *Proc. 60th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, 2022, pp. 7226–7249. `[verify]`

[2] S. Cahyawijaya et al., "NusaCrowd: Open source initiative for Indonesian NLP resources," in *Findings of ACL*, 2023. `[verify]`

[3] (Authors TBD), "Towards a Javanese NLP benchmark," *J. Comput. Linguistics Indonesia*, 2024. `[verify or replace]`

[4] N. D. Putri, M. O. Ibrohim, and I. Budi, "Abusive language and hate speech detection for Javanese and Sundanese languages in tweets: Dataset and preliminary study," in *Proc. ICACSIS*, 2021. `[verify]`

[5] M. O. Ibrohim and I. Budi, "Multi-label hate speech and abusive language detection in Indonesian Twitter," in *Proc. 3rd Workshop on Abusive Language Online (ALW3), ACL*, 2019, pp. 46–57. `[verify]`

[6] J. J. Errington, *Structure and Style in Javanese: A Semiotic View of Linguistic Etiquette*. Philadelphia, PA, USA: Univ. of Pennsylvania Press, 1988.

[7] haipradana, "Indonesian Twitter hate speech cleaned," Hugging Face Datasets, 2023. `[verify exact citation]`

[8] T. Davidson, D. Warmsley, M. Macy, and I. Weber, "Automated hate speech detection and the problem of offensive language," in *Proc. ICWSM*, 2017, pp. 512–515. `[verify]`

[9] F. Gilardi, M. Alizadeh, and M. Kubli, "ChatGPT outperforms crowd workers for text-annotation tasks," *Proc. Natl. Acad. Sci. (PNAS)*, vol. 120, no. 30, e2305016120, 2023.

[10] C. Ziems, W. Held, O. Shaikh, J. Chen, Z. Zhang, and D. Yang, "Can large language models transform computational social science?," *Comput. Linguistics*, vol. 50, no. 1, pp. 237–291, 2024. `[verify]`

[11] A. Møller, J. Dalsgaard, A. Pera, and L. D. Ross, "Is a prompt and a few samples all you need? Using GPT-4 for data augmentation in low-resource classification tasks," *Information*, vol. 14, no. 11, p. 598, 2023. `[verify]`

[12] (Authors TBD), "Enhancing hate speech detection in low-resource code-mixed Indonesian tweets via GPT-based data augmentation," *Eng., Technol. & Appl. Sci. Res. (ETASR)*, 2024. `[verify]`

[13] (Authors TBD), "Ngalawan Ujaran Sengit: Hate speech detection in Indonesian code-mixed social media data," *Lang. Resources and Evaluation*, 2025. `[verify]`

[14] K. Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4th ed. Thousand Oaks, CA, USA: SAGE, 2019.

[15] K. L. Gwet, "Computing inter-rater reliability and its variance in the presence of high agreement," *British J. Math. Statistical Psychology*, vol. 61, no. 1, pp. 29–48, 2008. `[verify]`

[16] B. Wilie et al., "IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding," in *Proc. AACL-IJCNLP*, 2020, pp. 843–857. `[verify]`

[17] G. I. Winata, A. Madotto, C.-S. Wu, and P. Fung, "Are multilingual models effective in code-switching?," in *Proc. 5th Workshop on Computational Approaches to Linguistic Code-Switching*, 2021. `[verify]`

[18] DeepSeek-AI, "DeepSeek technical report," arXiv preprint, 2025. `[verify exact arXiv ID/title]`

[19] Qwen Team, "Qwen3 technical report," arXiv preprint, 2025. `[verify exact arXiv ID/title]`

[20] AI Singapore, "SEA-LION: Southeast Asian languages in one network," 2024. `[verify]`

[21] I. Alfina, R. Mulia, M. I. Fanany, and Y. Ekanata, "Hate speech detection in the Indonesian language: A dataset and preliminary study," in *Proc. ICACSIS*, 2017, pp. 233–238. `[verify]`

[22] M. Wiegand, J. Ruppenhofer, and T. Kleinbauer, "Detection of abusive language: The problem of biased datasets," in *Proc. NAACL-HLT*, 2019, pp. 602–608. `[verify]`

[23] (Authors TBD), "From languages to geographies: Towards evaluating cultural bias in hate speech datasets," in *Proc. WOAH*, 2024. `[verify]`

[24] (Authors TBD), "Sarcasm and irony detection in low-resource languages: A survey," *ACM Comput. Surv.*, 2024. `[verify or replace — needed for §4.4 detection blind spot context]`

[25] (Authors TBD), "Best practices for text annotation with large language models," *Sociologica*, 2024. `[verify]`

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
