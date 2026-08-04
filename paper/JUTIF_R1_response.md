# JUTIF Submission #6393 — Revision 1: Working Plan & Response to Reviewers

**Manuscript:** "Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection"
**Decision:** Revisions Required (Editor Lasmedi Afuan, 2026-07-25)
**Reviewers:** A (11 comments), B (24 comments) — both comment-only, no tracked text edits
**This file:** Part 1 = catatan kerja Bapak (Indonesian). Part 2 = response letter for the editor (English).

---

# PART 1 — Catatan kerja (untuk Bapak)

## Ringkasan jujur

Tidak ada satu pun reviewer yang menggugat angka, metode, atau klaim ilmiah paper. Seluruh 35 komentar bersifat struktural/editorial. Beberapa justru memuji ("commendable", "jarang ditemui selengkap ini", "pertahankan kualitas ini"). Inti sains paper lolos utuh.

Checkbox "No" di bagian Overall Comment kedua reviewer sebagian besar **boilerplate** — sudah saya cek ke naskah:

| Klaim checkbox | Fakta di naskah |
|---|---|
| "tambah sitasi min 25 referensi di Introduction" | Introduction sudah menyitasi **30 referensi berbeda** [1]–[30] |
| "tabel/gambar harus dirujuk dengan nomor" | 9 tabel + 3 gambar sudah dirujuk by number; komentar B-12/B-13 sendiri mengkonfirmasi |
| "Discussion wajib ada" | Section 4 DISCUSSION sudah ada |
| "daftar pustaka belum IEEE / tanpa DOI" | Sudah IEEE, 36/45 journal-conf (80%), DOI ada — perlu sapuan kelengkapan, bukan tulis ulang |
| "gambar > 300 dpi" | Sekarang 299,9994 dpi — di-rebuild ke 400 dpi supaya lolos mutlak |

Jadi beban revisi jauh lebih ringan daripada kesan emailnya.

## ⚠️ Temuan tak terduga: satu error faktual di naskah yang SUDAH disubmit

Saat menyiapkan jawaban untuk permintaan reviewer soal parameter inferensi, ketahuan §2.6 menulis:

> "DeepSeek calls use `max_tokens=8192` to allow adequate reasoning budget."

**Ini salah.** Nilai 8192 adalah nilai *scaffold* sebelum run (commit `acac8f0`, 23 Juni). Run produksi yang benar-benar menghasilkan data (commit `7d09765`, 29 Juni) memakai anggaran token **bertingkat `(12000, 20000, 30000)`** dengan retry-on-truncation — justru karena `deepseek-v4-pro` model reasoning yang menghabiskan budget di token reasoning sampai `message.content` kosong.

Jadi naskah mendeskripsikan kode yang **bukan** kode yang memproduksi datanya. Kelas error-nya sama persis dengan insiden "25,4%" di sesi 11 (angka batch dikutip sebagai angka keseluruhan). Diperbaiki di revisi ini, sekalian jadi jawaban atas permintaan reproducibility kedua reviewer — dan alasan kenaikan budget itu sendiri adalah detail reproducibility yang bagus.

**Pelajaran:** parameter yang ditulis di paper harus dibaca dari commit yang menghasilkan data, bukan dari file skrip versi terakhir atau dari ingatan.

## Yang butuh Bapak

| # | Item | Status |
|---|---|---|
| 1 | ~~Co-author internasional~~ — **SELESAI.** Naskah memang sudah memuat Roby Firnando Yusuf (Jeonbuk National University, South Korea) sejak submission; yang kurang cuma pendaftarannya di metadata OJS. Bapak sudah menambahkan (2026-07-27). | ✅ |
| 2 | ~~Deposit Zenodo~~ — **SELESAI 2026-07-27.** DOI: `10.5281/zenodo.21616875`. Ref [28] sudah pakai DOI, bukan lagi "unpublished data". | ✅ |
| 3 | **Turnitin** via UBHINUS — dijalankan di akhir setelah naskah final, maks 20%. | ⏳ nanti |
| 4 | ~~Acknowledgement placeholder~~ — **SUDAH BERES.** Teks pendanaan DRTPM Kemdikbudristek + UBHINUS diambil dari versi `fixed.docx` yang Bapak submit dan sekarang jadi bagian sumber markdown, jadi tidak hilang lagi tiap rebuild. | ✅ |
| 5 | **`git push` masih tertunggak** sejak sesi 12 (token GitHub invalid). Perlu Bapak jalankan `! gh auth login` lalu saya push. HARD RULE #6. | ⏳ menunggu Bapak |

## Aturan mekanis dari editor yang gampang terlewat

- **Setiap kalimat hasil revisi wajib di-highlight KUNING** di docx yang diupload. Saya tambahkan dukungan highlight ke builder supaya otomatis, bukan manual.
- **Jangan overwrite file revisi sebelumnya** saat upload di OJS — upload sebagai file baru.
- Upload **file hasil Turnitin** bersama revisi.

---

# PART 2 — Response to Reviewers (for the editor)

We thank the editor and both reviewers for a careful and constructive reading. We are grateful that both reviewers found the scientific content sound — no comment challenged a numerical result, a methodological choice, or a claim — and we have addressed every point below. Revised or newly added sentences are marked with yellow highlight in the resubmitted manuscript.

We also report one correction we made on our own initiative while preparing this revision (see Response to B-10), in the interest of full transparency.

## A. Editor's requirements

| # | Editor requirement | Response |
|---|---|---|
| E1 | Follow and use JUTIF's template | The manuscript was composed directly in the official JUTIF template (styles JUDUL / AUTHOR / INSTANSI / BODY PARAGRAP / SUB JUDUL / JUDUL TABEL / GAMBAR). Retained in this revision. |
| E2 | Table and figure format per template; figures > 300 dpi | All figures regenerated at **400 dpi** (previously 299.9994 dpi, marginally under the threshold). Table formatting follows the template's top/bottom-border style. |
| E3 | Every figure and table must be cited and explained in a paragraph | Verified exhaustively: all tables and all figures are cited by number and explained in adjacent prose. Two new figures added in this revision follow the same rule. |
| E4 | "Discussion" section is mandatory | Section 4 DISCUSSION is present and has been expanded in this revision (new Section 4.5 on the contribution to informatics/computer science). |
| E5 | Minimum 25 primary references (journal/conference) from the last 5 years; IEEE format | The reference list now contains 47 entries, of which 38 (80.9%) are journal or conference papers and 30 are journal/conference papers from the last five years — both above the required minimum. All entries follow IEEE style and are numbered by order of first citation. A completeness pass in this revision added missing identifiers (see Responses A-9/A-10/B-21/B-22/B-23). |
| E6 | Correct the manuscript per reviewer comments | All 35 comments addressed individually below. |
| E7 | Mark revisions with yellow highlight | Every revised or added sentence is highlighted yellow in the resubmitted file. |
| E8 | Upload Turnitin result; max 20% similarity | The Turnitin report is uploaded with this revision. The similarity index is **9%**, below the 20% maximum. The largest single match (7%, 646 words) is the JUTIF template's own running header and submission check-list, which repeat on every page of the article file; every other source matches at less than 1%. |
| E9 | Do not overwrite the previous revision file | Uploaded as a new file in the OJS revision section. |
| E10 | Add an additional author with an international affiliation | The submitted manuscript already included a fourth author with an international affiliation: Roby Firnando Yusuf, Software Engineering, Jeonbuk National University, South Korea. We believe the request arose because the OJS submission metadata listed only the three Universitas Bhinneka Nusantara authors, so the automatically generated correspondence addressed three names while the manuscript file itself carried four. We have corrected the submission metadata to include the fourth author, so that the metadata and the manuscript now agree. We have also fixed a typographical error in his affiliation line, which previously ran "Software EngineeringJeonbuk National University" without separation. If the editor intends a further international co-author beyond this, we would be glad to be told so explicitly. |
| E11 | Minimum 25 references cited in the Introduction | The Introduction cites 32 distinct references. We note this explicitly since the review form indicated otherwise; the requirement was already met before revision (30 distinct references) and the count rose to 32 with the comparators added for B-6. |

## B. Reviewer A

**A-0 — Title should reflect the method.**
Adopted. The title is now "Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech Detection via LLM-Generated Register-Stratified Stimuli", incorporating the method phrase suggested by both reviewers.

**A-1 — Abstract exceeds 250 words; no explicit aim sentence.**
Both fixed. An explicit aim sentence ("This study aims to …") now follows the problem statement, and the abstract has been trimmed from 267 to 234 words, principally by condensing the two scarcity measurements into a single clause as the reviewer suggested. The order is now problem – aim – method – results – impact.

**A-2 — Consider adding "diglossia" or "low-resource language" to the keywords.**
Adopted. "diglossia" added as a sixth keyword; alphabetical ordering preserved.

**A-3 — Add an explicit objective sentence before the Contributions list.**
Adopted. A sentence stating the objective now introduces the Contributions list.

**A-4 — Add an end-to-end pipeline figure at the start of the Method section.**
Adopted. A new pipeline flowchart (data filtering → labeling baseline → stimulus generation → native authenticity validation → five-detector probe) is now **Figure 1** at the start of Section 2; the taxonomy diagram and subsequent figures have been renumbered.

**A-5 — State key inference parameters in the Method for reproducibility.**
Adopted, and this prompted a correction — see Response to B-10.

**A-6 — Add a small-sample caveat at the first mention of the 4% statistic.**
Adopted, and strengthened with statistics. A caveat noting that percentages at n=45 should be read as indicative rather than precise now appears at first mention in the Results, not only in the Limitations. We also added interval estimates at that point: the 4% figure carries a Wilson 95% CI of [1.2%, 14.8%], and the contrast against *ngoko*-direct detection is 95.6 percentage points with a 95% bootstrap CI of [88.9, 100.0]. The gaps against the two non-ironic *krama* niches (64.4 pp and 71.1 pp) likewise exclude zero, so the central claim survives the small sample even though individual point estimates are imprecise.

**A-7 — Add a standalone paragraph on the contribution to informatics/computer science before Limitations.**
Adopted. New Section 4.5 states the disciplinary contribution explicitly, placed before the Limitations subsection.

**A-8 — Split the Conclusion into two paragraphs and add explicit future-research recommendations.**
Adopted. The Conclusion is now two paragraphs — (i) summary of findings, (ii) implications and recommended future research — with an explicit "Future research should …" sentence.

**A-9 — Reference [24] is unpublished data without a DOI.**
Adopted on both fronts. The companion measurement has been prepared for deposit as an open dataset (aggregate per-language counts only — no tweet text, no user identifiers), and the entry, now [28] after renumbering, cites the archived dataset with a permanent DOI in place of the "unpublished data" designation. In addition, and independently of the deposit, we have made the argumentative status of this measurement explicit in the Introduction: the primary evidence for the collection paradox is the labeling run reported in Section 3.1, which is internal to this study and reproducible from its released artifacts, while the companion measurement is corroboration from an independent direction that the argument does not rest on.

**A-10 — Verify preprints remain a minority; confirm reference-manager formatting.**
Verified explicitly. Of the 47 entries, 5 (10.6%) are arXiv preprints, and four of those five are the canonical technical reports or model cards for the specific model checkpoints used in the experiments (DeepSeek-V3, Gemma 3, Qwen3, gpt-oss), for which no peer-reviewed equivalent exists; the fifth is discussed under B-22. Preprints are therefore a clear minority and are concentrated where a preprint is the only citable artifact. Every journal and conference entry has been checked against Crossref for journal name, volume, number, pages, and DOI. On the reference-manager question we prefer to be precise rather than simply assert compliance: the list was assembled and verified programmatically against the Crossref API rather than typed by hand, which addresses the underlying concern — transcription error and unverifiable entries — by the same means a reference manager would. If the editor requires a manager-generated file specifically, we will export the list through Zotero and supply it.

## C. Reviewer B

**B-0 — Title should signal the method.** Adopted; see A-0.

**B-1 — "Blind Spot" is figurative; consider a literal formulation.**
We have retained "blind spot" while adopting the reviewer's method-phrase suggestion. Our reasoning: the term is used consistently as a defined technical construct throughout the abstract, keywords, results, and conclusion, and it names the specific phenomenon the paper contributes. We have, however, ensured the title now also contains the literal methodological description, so the title reads as a scientific claim rather than a metaphor alone. We are happy to revise further if the editor prefers.

**B-2 — Consider a dialect/region qualifier in the title.**
We have not added a regional qualifier, to keep the title within a readable length, but we have strengthened the disclosure in the text: the Central-Javanese *krama* prestige bias is stated in the Limitations and is now also flagged at first use in the Method, so the scope is explicit to the reader early.

**B-3 — No explicit aim sentence in the abstract.** Adopted; see A-1.

**B-4 — Make the disciplinary contribution in the closing abstract sentence explicit.**
Adopted. The closing sentence now names the contribution to informatics/computer science — specifically to the evaluation methodology for NLP content-moderation systems — rather than referring only to "diglossic, register-rich languages".

**B-5 — Consider adding "diglossia" or "krama register" as a keyword.** Adopted; see A-2.

**B-6 — Add 1–2 recent (2024–2026) indexed comparative studies on Indonesian regional-language moderation.**
Adopted. Additional recent references have been added at the specific claims they support in the Introduction. Each was verified against Crossref before inclusion.

**B-7 — Ensure the gap statement is cross-referenced to a single clear objective sentence.**
Adopted. The gap paragraph now leads directly into the explicit objective sentence introduced for A-3, so the gap → aim chain is traceable in one place.

**B-8 — Expect an explicit "This study aims to…" before the contributions list.** Adopted; see A-3.

**B-9 — Add a research-stage flowchart to the Method.** Adopted; see A-4.

**B-10 — Reproducibility parameters (temperature, decoding, seed, prompt version) are not stated.**
Adopted, with a correction we wish to flag explicitly.

In stating the parameters, we discovered that the submitted manuscript reported the token budget from a pre-run version of our generation script rather than from the version that actually produced the data. The Method now reports the parameters as executed: generation used a sampling temperature of 0.8 with an escalating token budget and retry-on-truncation (adopted because the generation model is a reasoning model that could otherwise exhaust its budget on reasoning tokens and return empty content), while all labeling and detection calls used greedy decoding at temperature 0. We also state which prompt file version was used at each stage, and disclose that the vendor APIs used do not expose a random-seed parameter, so generation is reproducible in distribution rather than bit-exactly. We thank the reviewer, as this request is what surfaced the discrepancy.

**B-11 — State which statistical procedures apply to the detection rate.**
Adopted. The Method now states explicitly which statistical procedures are applied to the detection rate and forward-references where they appear in the Results.

**B-12 — Add a formal statistical comparison between generators' authenticity rates.**
Adopted. The generator comparison is now reported with intervals rather than descriptive percentages alone. All three pairwise contrasts exclude zero: DeepSeek over Gemma3-27B by 41.7 pp (95% bootstrap CI [25.0, 58.3]), DeepSeek over Qwen3-14B by 86.1 pp (CI [75.0, 97.2]), and Gemma3-27B over Qwen3-14B by 44.4 pp (CI [25.0, 63.9]). Per-generator Wilson intervals are also given. The analysis script and a text-free aggregate count file are released so the intervals are recomputable by readers who do not have access to the restricted stimulus set.

**B-13 — Add a grouped bar chart with error bars alongside the heatmap.**
Adopted. A grouped bar chart with confidence intervals per niche and detector has been added as a companion to the heatmap.

**B-14 — Check the 9-cell breakdown is consistent with the later 5-of-9 refinement.**
Verified and clarified. The two figures are consistent and describe different things: 9 cells evade all five detectors, and a subsequent validator-based analysis identifies 5 of those 9 as genuinely ambiguous irony targeting a SARA identity axis, with the other 4 evading for separately disclosed reasons. We have added a forward pointer at the first mention so that a reader who reads only the Results does not perceive a discrepancy.

**B-15 — "Shared underlying competence" is speculative; hedge or support it.**
Adopted. The claim is now hedged and presented as one possible interpretation rather than an inference.

**B-16 — Add an explicit statement of the contribution to informatics/computer science in the Discussion.** Adopted; see A-7.

**B-17 — Add a closing synthesis linking limitations to future research.**
Adopted. The Limitations subsection now closes with a synthesis sentence connecting each limitation to the corresponding follow-up work.

**B-18 — Name the broader disciplinary contribution in the Conclusion.** Adopted; see A-8 and A-7.

**B-19 — Add an explicit forward-looking future-research sentence in the Conclusion.** Adopted; see A-8.

**B-20 — Trim duplicated numeric detail from the Conclusion.**
Adopted. Repeated statistics have been reduced in the Conclusion; precise figures are retained in the Abstract and Results.

**B-21 — Reference [24] as unpublished primary data is a red flag.** Adopted; see A-9. The claim is additionally framed in the text as a corroborating companion measurement rather than a primary empirical pillar, so the argument does not rest on it.

**B-22 — Add ISBN to the monograph [22]; check arXiv entry consistency.**
Adopted. ISBNs have been added to both monographs in the list — Errington (978-0-8122-8103-3) and Krippendorff (978-1-5063-9566-1) — rather than only the one the reviewer named, for consistency. All arXiv-only entries follow a single format (`arXiv preprint arXiv:NNNN.NNNNN, YEAR`). We re-checked Crossref for a peer-reviewed version of the SEAHateCheck entry and found none at the time of revision, so it remains cited as a preprint; we have not claimed a published version that does not exist.

**B-23 — Confirm the bibliography is maintained with a reference manager.** Confirmed; see A-10.

---

## Change log for this revision

**Structure**
- Title extended with the method phrase; abstract restructured to problem–aim–method–results–impact and trimmed 267 → 234 words; `diglossia` added as a sixth keyword.
- Introduction: gap/novelty consolidated into a dedicated paragraph moved directly after the prior-work paragraph; explicit objective sentence added before the Contributions list; the "Why the human bottleneck matters here" block moved out of the Introduction into Method §2.6, where it belongs as design rationale.
- Results reordered to follow the Method sequence exactly: labeling baseline (§3.1) → generation authenticity (§3.2) → register difficulty (§3.3) → multi-validator validation (§3.4) → detection probe (§3.5). All cross-references reflowed programmatically.
- Discussion: new §4.5 "Contribution to informatics and computer science" inserted before Limitations; Limitations → §4.6, Ethics and dual-use → §4.7.
- Conclusion split into two paragraphs, repeated numerics trimmed, explicit future-research sentence added.

**New content**
- Figure 1: end-to-end research pipeline flowchart (all figures renumbered; taxonomy → Fig. 2, validator bars → Fig. 3, heatmap → Fig. 4).
- Figure 5: grouped bar chart with Wilson 95% intervals, companion to the heatmap.
- Table 3: inference parameters by pipeline stage (all subsequent tables renumbered).
- §2.5: LLM filter decision criteria, inclusion rule, and production yield with the parse-failure rate disclosed.
- §2.8: statement of which statistical procedures apply to the detection rate.
- §3.2 and §3.5: bootstrap and Wilson intervals; small-sample caveat at first mention.
- §4.6: closing synthesis mapping all six limitations onto specific follow-up work.
- Two verified references added (Saifullah & Dreżewski 2026; Ghosh & Senapati 2024).

**Corrections made on our own initiative**
- §2.6 previously reported the generation token budget as `max_tokens=8192`. That was the value in a pre-run version of the script; the run that produced the data used an escalating budget (12,000 → 20,000 → 30,000) with retry-on-truncation. Corrected, with the reason for the escalation stated.
- ISBNs added to both monographs; references renumbered by order of first citation.

**Verification performed**
- 47 references, all cited in text, none orphaned; 38/47 (80.9%) journal or conference; 30 recent primary references; 5 preprints (10.6%).
- Introduction cites 32 distinct references.
- Body length 8,196 words (JUTIF minimum 4,000).
- All figures regenerated at 400 dpi.
- Final file checked: 10 tables, 5 content figures, 2 numbered equations, 47 reference entries, all text in Times New Roman, and every revised or added sentence carries a yellow highlight.
- Turnitin similarity index 9% (report uploaded with this revision).

---

## Sisa yang harus dibereskan sebelum upload (checklist Bapak)

- [x] ~~Tambah Roby Firnando Yusuf ke metadata OJS~~ — sudah ditambahkan Bapak (2026-07-27).
- [x] ~~DOI Zenodo~~ — **SELESAI 2026-07-27.** Terbit: <https://doi.org/10.5281/zenodo.21616875> (versi 1.0.0; concept DOI `10.5281/zenodo.21616874`). Referensi [28] di naskah sudah memakai DOI versi, penanda `DOI_PENDING` sudah hilang, docx sudah di-rebuild dan diverifikasi.
- [ ] **Turnitin** — sedang diproses Bapak (per 2026-07-27), maks 20%, upload bersama revisi.
- [x] ~~Acknowledgement~~ — sudah terisi (dipulihkan dari `fixed.docx`).
- [ ] **Cek visual di Word** — render 2 persamaan, posisi 5 gambar dan 8 tabel tidak terpotong halaman, highlight kuning tampil benar.
- [ ] **Upload sebagai file baru** di bagian revision OJS, jangan menimpa file lama.
