# A Fully-Automated, Register-Aware Pipeline for Culturally-Grounded Javanese Hate Speech Annotation

> **JINITA-conformant draft v2 (2026-06-23).** Formatted to the official JINITA template (`paper/jinita_guidelines/`): IMRaD numbered sections, English, abstract ≤250 words with no citations, max-5 keywords, IEEE numbered references. This markdown is the content master; final layout moves to the JINITA Word template (Times New Roman 10 pt, A4, single-spaced) before submission. Verified numbers come from `experiments/pilot05_bulk_labeling/report.md` (recomputed independently). References marked `[verify]` need DOI/page confirmation in the literature pass — per the JINITA Gen AI policy we do not fabricate citation details.

**Mukhlis Amien¹, Yekti Asmoro Kanthi², Daniel Rudiaman Sijabat³**
¹,²,³ Department of Informatics, Universitas Bina Husada Nusantara, Malang, Indonesia
email: ¹amien@ubhinus.ac.id, ²yektiasmoro@ubhinus.ac.id, ³daniel223@ubhinus.ac.id

*(Article info / history block to be filled by the editor. For peer review, prepare a blinded version with authors and affiliations removed.)*

---

## ABSTRACT

Hate-speech annotation in low-resource languages is bottlenecked by the cost and unreliability of human annotators. We are motivated by a concrete failure mode from a prior project, in which student annotators silently back-translated Indonesian and English hate speech into Javanese rather than annotating authentic text, corrupting the dataset undetectably until modeling failed. We argue that, for a single native-expert researcher under severe time constraints, a fully-automated, zero-human annotation pipeline is a methodological safeguard rather than a shortcut. This paper presents such a pipeline for Javanese, a language with roughly 80 million speakers but minimal computational resources. The pipeline combines a language-model Javanese filter, a cheap local-model toxicity pre-screen verified by a stronger cloud model, and a three-model consensus labeler, all driven by a culturally-grounded, register-aware four-dimensional taxonomy that captures Javanese speech levels, cultural innuendo, and organic code-mixing. From a public Indonesian hate-speech dump we produce 728 consensus-labeled instances at a total cost of about six US dollars and zero human labor. The primary rater pair reaches a Krippendorff alpha of 0.69 on 586 held-out texts, statistically indistinguishable from the prompt-tuning pool, showing that culturally-engineered prompting generalizes rather than overfits. We additionally report that principled prompt corrections raised agreement by about 0.21 without changing models, that a region-native model was a worse rater than a general one, and that adversarial auditing of the analysis code caught bugs that independent recomputation merely replicated. We release the dataset, codebook, and pipeline.

**Keywords:** Javanese; hate speech detection; large language model; inter-annotator agreement; low-resource language

---

## 1. INTRODUCTION

Javanese is spoken by roughly 80 million people, yet it remains severely under-resourced in natural language processing [1], [2]. Hate speech on Indonesian social media frequently surfaces in Javanese or in Javanese–Indonesian code-mixing, carrying ethnic, religious, gender, and political animus that is specific to the Javanese cultural context: target groups such as Madurese, Chinese-Indonesian, and Arab communities; intra-Javanese regional rivalries; and a speech-level (*unggah-ungguh*) system in which the same hostile content can be delivered in coarse *ngoko* or in deceptively polite *krama* [3]. General-purpose or even general-Indonesian hate-speech taxonomies and datasets [4], [5], [6] do not capture these dimensions, and the small number of Javanese-specific efforts [7] remain unreleased.

The dominant methodology for building such resources assumes a team of trained native annotators reaching acceptable inter-annotator agreement. This assumption is unrealistic in a genuinely low-resource setting: a single part-time researcher with no budget for an annotation team. Worse, human annotation under these constraints can be actively harmful. This work is directly motivated by a failure: in a prior effort to build a Javanese hate-speech dataset, student annotators — working with limited supervision and throughput-oriented incentives — produced "Javanese" data largely by *back-translating* existing Indonesian and English hate speech rather than annotating authentic Javanese text. The corruption was structural and silent; the labels were internally consistent, so it surfaced only when downstream models failed to generalize, by which point the annotators had graduated and were unavailable. This is a concrete instance of why human-in-the-loop annotation, under realistic low-resource constraints, is *high-risk* rather than a gold standard.

Recent work shows that large language models can serve as competitive text annotators [8], [9], with reported inter-model agreement in ranges comparable to human teams [9]. However, this literature is overwhelmingly English and general-domain; whether *cultural, register-aware* prompting can make multi-model consensus reliable enough on authentic low-resource hate speech to replace human annotation entirely is open. We address this gap.

We make three primary contributions. First, a **fully-automated, zero-human annotation pipeline**: public dump → language-model Javanese filter → toxicity pre-screen → multi-model consensus labeling → automated reliability analysis, in which no human annotates or adjudicates any instance. Second, a **culturally-grounded, register-aware four-dimensional taxonomy** (target group, severity, register, form), released as a formal codebook; the *register* dimension, modeling *ngoko/madya/krama* and "polite-violent" *krama*, is to our knowledge novel in hate-speech taxonomies. Third, a **validation methodology for human-free annotation** that a peer reviewer can trust: cross-model Krippendorff alpha with bootstrap confidence intervals, an explicit held-out test against prompt overfitting, vendor-sensitivity analysis, and adversarial verification of the analysis code itself. We further report several transferable methodological findings (Section 4): principled prompt corrections raised agreement by Δα ≈ 0.21 with fixed models; a region-native model was a worse rater than a general one; a cheap local pre-screen had only ~25% precision against cloud verification; and independent recomputation can replicate rather than catch analysis bugs.

This paper does not claim a "first dataset" — Javanese hate-speech data has been built before [7], though not released. Our novelty rests on the pipeline, the taxonomy, and the validation methodology; the dataset is positioned as the first *publicly released* culturally-grounded Javanese set, and modeling baselines are deliberately left as future work so that the contribution is the method, not an F1 number.

## 2. THE CULTURAL TAXONOMY (PROPOSED FRAMEWORK)

We define hate speech operationally as text that **attacks, demeans, dehumanizes, or incites violence or discrimination against a person or group based on group identity** — ethnicity, religion or belief, gender or sexual orientation, social class, or political collective. The decisive criterion is the *direction of attack toward group identity*, **not** the coarseness of the language. Javanese is rich in profanity (*pisuhan*: *asu*, *jancuk*, *cuk*) that functions as in-group bonding (*banter*) in the Arek/Surabaya register; coarseness alone is not hate. This distinction is the single most error-prone boundary and is encoded throughout the taxonomy [10].

The taxonomy has four dimensions (full definitions, decision rules, and worked examples appear in the released codebook):

**2.1. Target group** — ethnicity (*suku Madura, Tionghoa, Sunda, Batak, Arab*, …), intra-Javanese region (*Mataraman, Arek, Banyumasan*), religion or belief (*Islam, Kristen, Katolik, Hindu, Buddha, Konghucu, kepercayaan*), class (*kutha/ndeso, priyayi/cilik*), gender or LGBTQ, political collective (figure, party, mass organization), or *tidak ada* (none).

**2.2. Severity** — *BUK* (not hate) / *ringan* (light: stereotyping) / *sedang* (moderate: dehumanization, exclusion) / *berat* (severe: threats, incitement). The consistency rule is that any non-*BUK* level requires `hate:true`.

**2.3. Register (novel)** — *ngoko* / *madya* / *krama* / *campur kasar*. Hate can be carried in polite *krama* ("polite-violent"); a register-aware taxonomy can capture this where a register-blind one cannot.

**2.4. Form** — *direct* / *sarcastic* / *idiomatic* (*pasemon*, cultural innuendo) / *code-switched*.

A key empirical finding (Section 4.4) is that, in social-media data, register is overwhelmingly *ngoko*, with pure *krama*-hate essentially absent. We report this honestly: the register dimension's value is its *capability* to capture polite-violent hate plus the empirical confirmation that social-media Javanese hate is *ngoko* with code-mixing — not that *krama*-hate is frequent.

## 3. METHOD

### 3.1. Data sourcing and language-model Javanese filtering

We avoid live scraping in favor of an existing public Indonesian hate-speech dump [4]. Because Javanese-specific corpora are scarce and a generic streaming source proved nearly hate-free — yielding a degenerate α = 1.0 with all-non-hate labels, a cautionary result in itself — we filter the Indonesian dump for Javanese and Javanese-code-mixed content using a language model as filter. The filter is precise, correctly separating Sundanese, Malay, and Portuguese as *other*; however, the density of "hot" Javanese (Javanese carrying potential toxicity) is low (~3–4%), so large pools require filtering many rows. Pure Javanese is near-zero on social media (1/250); *code-mixing is the empirical reality* [11], [12] and is accepted as in scope.

### 3.2. Cascade filter: cheap local pre-screen, cloud verification

To enlarge the pool affordably we use a cascade: a free local model pre-screens for likely-Javanese (8,349 → 3,088), a stronger free local model pre-screens for likely-toxic (→ 1,687), and a cloud model *verifies* the survivors so the final pool remains cloud-confirmed. The cloud model confirmed only **25.4%** of the local pre-screen's keeps (1,687 → +304), i.e. the cheap local pre-screen substantially over-keeps. The cascade still saves cloud calls on the rejected majority, but cloud verification remains the precision and cost bottleneck — a concrete, quantified trade-off for practitioners. The single dump was exhausted at 12.7K filtered rows, ceiling-ing the pool at 735; scaling the dataset requires *new sources*, not deeper filtering.

### 3.3. Cultural prompt engineering

We iterate the labeling prompt on a fixed 149-text pool, measuring the agreement of the primary rater pair after each version (Table 1).

**Table 1.** Prompt iteration and inter-rater agreement (primary pair, n = 149).

| Prompt | Change | α | 95% CI |
|---|---|---|---|
| v0 | initial cultural taxonomy + 5 few-shot examples | 0.587 | [0.475, 0.698] |
| v1 | hate := group-directed; profanity ≠ hate; fixed a contradictory example | 0.554 | — |
| v2 | + "identity slur aimed at an individual is hate"; +2 few-shot examples | **0.763** | [0.624, 0.879] |

Two principled definition corrections raised α by **Δ ≈ 0.21 without changing the models**. A methodological caution surfaced here: α can stay flat (v0→v1) even when labels qualitatively improve, because skewed prevalence inflates chance agreement; one must read the flip table and raw agreement alongside α. We stopped at v2: the residual disagreements were genuinely ambiguous (meta-commentary, quoted hate, positive comparisons) and chasing them on the evaluation pool would risk overfitting. They are documented in the codebook as boundary cases.

### 3.4. Multi-model consensus labeling

Final labels are the majority vote of three independent raters: two cloud models (DeepSeek [16] and Grok) and one local, free model (Qwen3-14B [17]). The free local rater strengthens triangulation and makes the pipeline partially reproducible without paid APIs. Vendor selection was itself empirical (Section 4.5): one slow, low-validity reasoning model was dropped, and a *region-native* model failed as a rater despite its specialization, while the general local model passed. Per-vendor operating characteristics appear in Table 2.

**Table 2.** Per-vendor characteristics on the full pool (n = 735).

| Vendor | Refusal % | JSON valid % | Latency (ms) | Cost (USD) | Hate rate |
|---|---|---|---|---|---|
| DeepSeek | 0.7 | 96.5 | 15,409 | 3.63 | 22% |
| Grok | 0.1 | 99.9 | 5,179 | 2.49 | 28% |
| Qwen3-14B (local) | 0.1 | 99.7 | 10,869 | 0.00 | 14% |

Total cost, including merged prompt-iteration calls, was **USD 6.13**. Refusal is negligible (≤ 0.7%), confirming that safety alignment is not a blocker for forensic hate-speech classification framed as academic analysis.

### 3.5. Validation design

All validation is human-free and has three layers. (i) **Cross-model reliability** — Krippendorff α for nominal data in its canonical coincidence-matrix form, with 5,000-sample bootstrap confidence intervals, treating the models as raters [13]. (ii) **Held-out generalization** — α computed separately on the texts *outside* the prompt-iteration pool, to test whether the engineered prompt overfits. (iii) **Adversarial verification** — the analysis code is audited by independent agents *and* recomputed from scratch, treating our own pipeline as the adversary.

## 4. RESULTS AND DISCUSSION

### 4.1. Dataset characterization

The pipeline yields **728 consensus instances** (158 hate, 21.7%; 570 non-hate), of which **569 are unanimous** and only **7 are ties** (released separately as boundary material). Among hate instances, target groups are led by *gender_wanita* (49), political collectives (party 20, figure 17, organization 9), *gender_lgbtq* (19), *suku_tionghoa* (15), and *agama_islam* (15), with Christian, Arab, and belief targets present in smaller numbers and Madurese, Sundanese, Batak and others rare. Severity is dominated by *sedang* and *ringan*; *berat* (incitement, threats) is rare. Form is overwhelmingly *direct*.

### 4.2. Inter-model reliability and held-out validation

This is the central result. For the primary rater pair, the apples-to-apples overfitting test is shown in Table 3.

**Table 3.** Primary-pair α: held-out vs. prompt-tuning pool.

| Subset | n | α | 95% CI |
|---|---|---|---|
| Held-out (outside tuning pool) | 586 | **0.688** | [0.614, 0.759] |
| Prompt-tuning pool | 149 | 0.747 | [0.611, 0.861] |
| Full pool | 735 | 0.701 | [0.637, 0.765] |

Held-out α (0.688) is well above the 0.6 acceptability threshold, and its confidence interval overlaps that of the tuning pool (0.747): the culturally-engineered prompt *generalizes; it does not overfit*. Held-out α here is in fact higher and its interval tighter than in a smaller earlier validation (0.670), i.e. the anti-overfitting claim strengthens with scale.

### 4.3. Vendor sensitivity

Table 4 shows pairwise α. The free local model is the noisiest rater, so the three-rater α (0.513 held-out) is lower than the primary pair; we therefore report the primary pair for the headline reliability claim and treat the local model as a free, reproducible third vote. Comparing α across *different* rater sets would be misleading — the fair overfitting test holds the rater set fixed (Section 4.2).

**Table 4.** Pairwise α (held-out, n = 586).

| Rater pair | α | 95% CI |
|---|---|---|
| DeepSeek + Grok | 0.688 | [0.614, 0.759] |
| DeepSeek + Qwen3-14B | 0.401 | [0.299, 0.496] |
| Grok + Qwen3-14B | 0.398 | [0.304, 0.485] |

### 4.4. Cascade and register findings

The local pre-screen's 25.4% confirmation rate (Section 3.2) shows that free local models can cheaply *reduce* a candidate pool but cannot replace cloud verification for precision; the economically rational design is local-recall-then-cloud-precision, with cloud cost scaling with pre-screen over-keep. On register: theory predicts polite-violent *krama* as a distinctive Javanese hate carrier, but empirically social-media hate is 157/158 *ngoko*. We report this honestly: the register dimension's value is capability and confirmation, not frequency. Polite-violent *krama* likely lives in formal or elite discourse, not comment sections — a hypothesis for future targeted sampling.

### 4.5. Region-native is not a better rater

A regionally specialized Southeast-Asian model failed as a consensus rater (α 0.422, noise in both directions), while a general 14-billion-parameter model passed (α 0.660), despite the latter's lack of explicit Javanese specialization. For structured cultural classification, general instruction-following capacity appears to dominate language-specific pretraining; the region-native model remained useful only for the easier filtering task. This is a counter-intuitive, citable finding for the low-resource community.

### 4.6. Adversarial verification

Before release, the analysis was audited by independent agents and independently recomputed. This caught two real bugs: a deduplication load-order bug in which stale records overwrote valid labels (which had inflated an earlier α to an artefactual value), and a non-canonical α formula (pooled-pairs rather than the weighted coincidence matrix). Both were fixed and re-validated against a reference dataset with known α = 0.743. Crucially, the *independent recomputation replicated the same bugs* and thus "confirmed" the wrong number; only the code audit caught them. The lesson is that verification of human-free pipelines needs two distinct paths — audit and recompute — not a single recomputation.

### 4.7. Limitations

A single dump skews targets toward gender, politics, Chinese, and Islam, and under-represents Madurese, Sundanese, Batak, and the *krama* register; the taxonomy provides these categories but the dataset does not yet populate them. The 728 instances suffice to validate the pipeline and taxonomy but fall below the threshold for robust supervised fine-tuning, so baseline modeling is framed as future work rather than a headline result. Severity is the noisiest dimension (raters agree on 89/158 hate instances), so the core label is binary. Finally, the hardest annotation boundary is *use vs. mention* — text that quotes or criticizes a slur versus text that deploys it — which current model raters do not reliably distinguish.

### 4.8. Ethics

All texts are from public posts and are fully anonymized (usernames, mentions, and URLs removed or placeholdered); no re-identification is attempted, and no private messages or groups are used. The dataset is released under CC BY-NC-SA 4.0 for research and moderation purposes only. The models perform classification, not generation of offensive content, and refusal rates were negligible.

## 5. CONCLUSION

We showed that a fully-automated, culturally-grounded, register-aware pipeline can produce a reliably-labeled Javanese hate-speech dataset with zero human annotation, reaching a held-out inter-model α of 0.688 at a total cost of USD 6.13. Beyond the dataset and codebook, we contribute a validation methodology — held-out generalization plus adversarial code verification — that we argue is the appropriate standard for human-free annotation, together with transferable findings on prompt engineering, region-native rater quality, and cascade-filter economics. Future work will add sources to populate under-represented target groups and the *krama* register, test the polite-violent *krama* hypothesis through targeted sampling of formal discourse, train baseline models as dataset characterization, and address use-vs-mention disambiguation.

## GEN AI DISCLOSURE STATEMENT

In accordance with the JINITA Generative AI policy: large language models are the *object of study and the annotation method* of this work and are described in full in Section 3. Separately, the authors used an AI assistant to help draft and copy-edit portions of this manuscript. All AI-assisted text, all numerical results, and all references were reviewed and verified by the authors, who take full responsibility for the content; no references were generated without author verification. No confidential or personally identifiable data were submitted to third-party AI tools beyond the already-public, anonymized corpus.

## ACKNOWLEDGEMENTS

*(To be completed: institutional support from Universitas Bina Husada Nusantara; any grant or sponsor; compute resources.)*

## REFERENCES

> *IEEE numbered style. Anchors below are real works; entries marked `[verify]` need exact volume/pages/DOI confirmed during the literature pass (JINITA Gen AI policy: do not present unverified citation details). Target: ≥ 20 references, ≥ 80% journal papers from the last five years — to be finalized in the literature pass.*

[1] A. F. Aji et al., "One country, 700+ languages: NLP challenges for underrepresented languages in Indonesia," in *Proc. 60th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, 2022, pp. 7226–7249. `[verify]`

[2] S. Cahyawijaya et al., "NusaCrowd: Open source initiative for Indonesian NLP resources," in *Findings of ACL*, 2023. `[verify]`

[3] J. J. Errington, *Structure and Style in Javanese: A Semiotic View of Linguistic Etiquette*. Philadelphia, PA, USA: Univ. of Pennsylvania Press, 1988.

[4] M. O. Ibrohim and I. Budi, "Multi-label hate speech and abusive language detection in Indonesian Twitter," in *Proc. 3rd Workshop on Abusive Language Online (ALW3), ACL*, 2019, pp. 46–57. `[verify]`

[5] I. Alfina, R. Mulia, M. I. Fanany, and Y. Ekanata, "Hate speech detection in the Indonesian language: A dataset and preliminary study," in *Proc. ICACSIS*, 2017, pp. 233–238. `[verify]`

[6] T. Davidson, D. Warmsley, M. Macy, and I. Weber, "Automated hate speech detection and the problem of offensive language," in *Proc. 11th Int. AAAI Conf. Web and Social Media (ICWSM)*, 2017, pp. 512–515. `[verify]`

[7] N. D. Putri, M. O. Ibrohim, and I. Budi, "Abusive language and hate speech detection for Javanese and Sundanese languages in tweets: Dataset and preliminary study," in *Proc. Int. Conf. Advanced Computer Science and Information Systems (ICACSIS)*, 2021. `[verify]`

[8] F. Gilardi, M. Alizadeh, and M. Kubli, "ChatGPT outperforms crowd workers for text-annotation tasks," *Proc. Natl. Acad. Sci. (PNAS)*, vol. 120, no. 30, e2305016120, 2023.

[9] C. Ziems, W. Held, O. Shaikh, J. Chen, Z. Zhang, and D. Yang, "Can large language models transform computational social science?," *Comput. Linguistics*, vol. 50, no. 1, pp. 237–291, 2024. `[verify]`

[10] M. Wiegand, J. Ruppenhofer, and T. Kleinbauer, "Detection of abusive language: The problem of biased datasets," in *Proc. NAACL-HLT*, 2019, pp. 602–608. `[verify]`

[11] (Authors TBD), "Ngalawan Ujaran Sengit: Hate speech detection in Indonesian code-mixed social media data," *Lang. Resources and Evaluation*, 2025. `[verify]`

[12] (Authors TBD), "Enhancing hate speech detection in low-resource code-mixed Indonesian tweets via GPT-based data augmentation," *Eng., Technol. & Appl. Sci. Res. (ETASR)*, 2024. `[verify]`

[13] K. Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4th ed. Thousand Oaks, CA, USA: SAGE, 2019.

[14] B. Wilie et al., "IndoNLU: Benchmark and resources for evaluating Indonesian natural language understanding," in *Proc. 1st Conf. Asia-Pacific Chapter ACL (AACL-IJCNLP)*, 2020, pp. 843–857. `[verify]`

[15] G. I. Winata, A. Madotto, C.-S. Wu, and P. Fung, "Are multilingual models effective in code-switching?," in *Proc. 5th Workshop on Computational Approaches to Linguistic Code-Switching*, 2021. `[verify]`

[16] DeepSeek-AI, "DeepSeek technical report," 2025. `[verify exact title/version]`

[17] Qwen Team, "Qwen technical report," 2025. `[verify exact title/version]`

[18] (Authors TBD), "From languages to geographies: Towards evaluating cultural bias in hate speech datasets," in *Proc. Workshop on Online Abuse and Harms (WOAH)*, 2024. `[verify]`

[19] (Authors TBD), "Indonesian hate speech detection using IndoBERTweet and BiLSTM on Twitter," *JOIV: Int. J. Informatics Visualization*, 2023. `[verify]`

[20] (Authors TBD), "Best practices for text annotation with large language models," *Sociologica*, 2024. `[verify]`

[21] (Authors TBD), "Monitoring hate speech in Indonesia: An NLP-based system," in *Proc. EMNLP (System Demonstrations)*, 2024. `[verify]`

[22] AI Singapore, "SEA-LION: Southeast Asian languages in one network," 2024. `[verify]`
