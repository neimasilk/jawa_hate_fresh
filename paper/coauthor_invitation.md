# Undangan co-author internasional — JUTIF #6393

**Konteks:** Editor JUTIF mensyaratkan *"Please add an additional author with an international affiliation."* Bapak sudah punya kandidat.

**Yang saya butuh dari Bapak untuk memasukkan ke naskah + metadata OJS:**
nama lengkap (format sitasi), institusi, kota, negara, email, dan ORCID kalau ada.

---

## Catatan penting sebelum mengirim: bikin authorship-nya sah

Permintaan editor ini berisiko mendorong ke *gift authorship* — nama ditempel tanpa
kontribusi. Itu melanggar norma etik publikasi (ICMJE/COPE) dan, kalau ketahuan,
jauh lebih merusak daripada sekadar ditolak. Paper ini justru sedang menonjolkan
integritas metodologis (limitasi 6 poin, IRR rendah dilaporkan apa adanya) — akan
kontradiktif kalau daftar penulisnya tidak jujur.

Jadi undangan di bawah **meminta kontribusi nyata**, bukan sekadar izin pakai nama.
Tiga peran yang realistis dikerjakan dalam waktu singkat dan genuinely menambah nilai:

1. **Validasi silang taksonomi register-pragmatik** — menilai apakah kerangka
   4-niche masuk akal untuk bahasa diglosik lain (Jawa/Sunda/Bali, atau bahasa
   honorifik di luar Indonesia seperti Korea/Jepang). Ini langsung memperkuat
   klaim generalisasi yang sekarang masih normatif di §4.5 dan Conclusion.
2. **Review independen atas desain detection probe** — memeriksa apakah interpretasi
   hasil 5-detektor sudah tepat, dan apakah ada confound yang kami lewatkan.
   Reviewer B sudah menyinggung soal shared-prompt (Limitasi 5).
3. **Framing lintas-bahasa di Discussion** — menulis/menyunting bagian yang
   menghubungkan temuan ini ke literatur moderasi multibahasa internasional.

Salah satu dari tiga ini sudah cukup untuk memenuhi kriteria authorship
(kontribusi substansial + menyetujui versi final + bertanggung jawab atas isi).

---

## Draft email (bahasa Inggris)

> **Subject:** Invitation to co-author a paper on register-based blind spots in Javanese hate speech detection
>
> Dear Prof. / Dr. [NAME],
>
> I hope this finds you well. I am writing to invite you to join a paper of ours as a
> co-author, and to be upfront about both what we would be asking of you and why we are
> asking now.
>
> The paper is titled "Diagnosing a Register-Pragmatic Blind Spot in Javanese Hate Speech
> Detection via LLM-Generated Register-Stratified Stimuli." It is under review at Jurnal
> Teknik Informatika (JUTIF), a nationally accredited Indonesian journal, and has received
> a Revisions Required decision with broadly positive reviews.
>
> The core finding is this. Javanese is diglossic: the same hostile proposition can be
> expressed in the coarse *ngoko* register or in the refined *krama* register. Hostility
> carried in *krama* — particularly ironic over-praise, a culturally specific indirect
> speech act called *pasemon* — is almost invisible to automated detection. Across five
> detector models, explicit *ngoko* hate is caught in 100% of cases, while ironic *krama*
> hate is caught in only 4%. Because *krama* is confined to formal and face-to-face
> contexts, it is structurally absent from social media, so this class of hate cannot be
> collected by corpus filtering at all. We therefore constructed a register-stratified
> stimulus set with large language models and validated it with native raters, in order
> to make the failure measurable.
>
> We would value your involvement in one of the following, whichever fits your interests
> and time:
>
> 1. cross-checking whether our four-niche register-pragmatic taxonomy transfers to other
>    diglossic or honorific-rich languages, which would strengthen a generalization claim
>    we currently state but do not evidence;
> 2. an independent critical review of the detection-probe design and our reading of its
>    results, including confounds we may have missed;
> 3. helping frame the discussion against the international literature on multilingual
>    content moderation.
>
> I should be transparent about the timing: the journal's editor has asked us to add an
> author with an international affiliation. I did not want to extend an invitation on that
> basis alone, so the contributions above are real work we genuinely need rather than a
> formality, and I would rather you decline than accept a nominal listing. If you join, we
> would ask you to review and approve the final manuscript and to take responsibility for
> the content, as usual.
>
> I can send the current manuscript, the reviewer reports, and our response document
> immediately if you would like to look before deciding. The revision is due [DEADLINE], so
> an indication either way in the next week or so would help us greatly.
>
> With thanks and best regards,
>
> Mukhlis Amien
> Department of Informatics, Universitas Bhinneka Nusantara, Malang, Indonesia
> amien@ubhinus.ac.id

---

## Kalau kandidat menerima

Yang perlu diupdate:
- Baris penulis di naskah (`scripts/build_jutif_docx.py`, blok front matter) + afiliasi
  baru sebagai superscript ke-4, dan baris INSTANSI kedua untuk institusi luar negeri.
- Metadata OJS JUTIF (tambah contributor di submission #6393).
- `CONFLICT OF INTEREST` dan `ACKNOWLEDGEMENT` kalau relevan.
- Bagian naskah yang jadi kontribusi mereka — jangan lupa benar-benar dimasukkan.

## Kalau kandidat menolak / tidak sempat

Opsi jujur ke editor: sampaikan bahwa kami sudah berupaya dan tanyakan apakah syarat ini
mutlak. Lebih baik daripada menempel nama tanpa kontribusi.
