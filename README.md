# AI Fluency for Biology — Course Home

> **Who this is for:** Practicing biologists, healthcare professionals, and bio-researchers
> who want to use AI tools effectively and responsibly in their daily work.
> No machine-learning background required.

**Estimated Time to Complete This Orientation: 10 mins**

---

## The Biology Problem First

You receive a FASTA file containing 3,000 protein sequences from a metagenomic study.
A colleague suggests running them through an LLM to predict function.
You have three immediate questions:

- Can an LLM actually "read" a FASTA file, or will it hallucinate annotations?
- Should you use a predictive model (like ESMFold) or a generative model (like GPT-4)?
- What happens to your sequences if you paste them into a commercial chat tool?

This course gives you the vocabulary and habits to answer those three questions confidently —
and to ask better ones for your own data.

---

## What You Will Learn

By the end of this course you will be able to:

| # | Outcome | Module |
|:--|:--------|:-------|
| 1 | Distinguish **Predictive AI** (AlphaFold, ESMFold) from **Generative AI** (LLMs) and choose the right tool for a biology task | 1 |
| 2 | Explain how AI ingests biological data (1D sequences, 2D gel/microscopy images, 3D PDB structures) and why data quality is the binding constraint | 2 |
| 3 | Write structured prompts for literature synthesis, protocol troubleshooting, and RAG-based document queries using only browser tools | 3 |
| 4 | Use an LLM as a coding assistant to automate repetitive bioinformatics tasks — and catch the errors it introduces | 4 |
| 5 | Identify algorithmic bias in genomics datasets, evaluate biosecurity and data-sovereignty risks, and know when to run a local model instead | 5 |

---

## Course Modules

All modules run entirely in your browser — no local software installation required.
Tools used: **Google Colab**, **ChatGPT / Claude (web)**, **NotebookLM**.

---

### Module 1 — The Bio-AI Landscape

**[→ Open Module 1](modules/module-01-bio-ai-landscape/README.md)**

**Hook:** AlphaFold predicted the structure of nearly every known protein in two years.
GPT-4 cannot reliably tell you whether a missense variant is pathogenic.
Why? And what does that tell you about which tool to use when?

**What you will cover:**
- Core AI vocabulary mapped to biology: tokenization ≈ codons; embeddings ≈ sequence space
- Predictive AI vs. Generative AI — a decision framework for bio researchers
- Bio-AI Glossary: 20 terms every researcher needs before reading a preprint
- Matching exercise: AI concept → biological equivalent

**Estimated Time: ~45 mins**

---

### Module 2 — Biological Data Literacy and AI

**[→ Open Module 2](modules/module-02-data-literacy/README.md)**

**Hook:** A lab uploads a PDB file to ChatGPT and asks for a binding-site summary.
The model returns a confident, detailed answer — based on a protein it has never seen,
because the file contents were not actually parsed by the model.

**What you will cover:**
- How AI ingests 1D sequences, 2D images, and 3D structures — what is actually read vs. ignored
- The GIGO principle applied to genomics, proteomics, and clinical data
- Hands-on (Google Colab): use Biopython to parse a `.fasta` file, compute GC-content, and flag low-quality entries via an AI-generated script

**Estimated Time: ~60 mins**

---

### Module 3 — Prompt Engineering and RAG for Science

**[→ Open Module 3](modules/module-03-prompting-rag/README.md)**

**Hook:** Two researchers ask the same LLM to summarize the same paper.
One gets a hallucinated methods section. The other gets an accurate, citable summary.
The only difference is how they structured the prompt.

**What you will cover:**
- Retrieval-Augmented Generation (RAG): NotebookLM and ChatGPT document upload as zero-install RAG environments
- Lab Exercise 1: Literature Synthesis — build an evidence table from 5 uploaded PDFs
- Lab Exercise 2: Protocol Troubleshooting — diagnose a failed PCR setup using structured prompting

**Estimated Time: ~75 mins**

---

### Module 4 — Bio-Prototyping and Workflow Automation

**[→ Open Module 4](modules/module-04-prototyping/README.md)**

**Hook:** The Excel gene-name error: SEPT2, MARCH1, DEC1 — Excel silently auto-corrects
these to dates, corrupting gene lists. This error appeared in ~20% of published genomics
papers before journals issued formal warnings. An LLM can write the fix in two lines.
Can you tell whether the fix is correct?

**What you will cover:**
- LLMs as coding assistants: scaffolding, debugging, and the failure modes they reliably introduce
- Hands-on fix for the Excel gene-name error using an LLM-generated Python script
- Capstone exercise: prompt an AI to write a script that cross-references messy gene data with the HGNC database, then verify its output

**Estimated Time: ~90 mins**

---

### Module 5 — Bio-Ethics, Bias, and Secure Deployment

**[→ Open Module 5](modules/module-05-ethics-security/README.md)**

**Hook:** A clinical AI trained predominantly on European genomics data is deployed in
a West African hospital. Diagnostic performance drops significantly. No one flagged this at deployment.
What review process should have caught it?

**What you will cover:**
- Algorithmic bias in genomics: GWAS dataset ancestry imbalance and downstream clinical risk
- Biosecurity: dual-use risks when prompting LLMs with pathogen sequence data
- Data sovereignty: Consumer Tier vs. Enterprise/API Tier — what you must NOT paste into a commercial chat tool
- HIPAA-compliant options: introducing Local LLMs (Ollama) as a secure sandbox concept
- Reflection exercise: diagnostic AI case study analysis

**Estimated Time: ~60 mins**

---

## How This Course Works

### Structure of Every Module

Each module follows the same four-part pattern:

1. **Hook** — A real biology problem that the AI concept solves (or complicates)
2. **Concept** — Concise explanation with biology-native analogies
3. **Hands-on** — A guided exercise using only browser tools
4. **Check** — A gold-standard output so you can compare your own work:

```html
<details>
<summary>View Gold Standard Output</summary>

[Expected result, with explanation of why it is correct]

</details>
```

### Tooling Policy

This course uses **zero local installations**.
Every exercise runs in one of:

| Tool | Free? | Used in |
|------|-------|---------|
| [Google Colab](https://colab.research.google.com/) | Yes | Modules 2, 4 |
| [Claude](https://claude.ai/) or [ChatGPT](https://chat.openai.com/) | Free tier sufficient | All modules |
| [NotebookLM](https://notebooklm.google.com/) | Yes | Module 3 |

If an exercise in any module asks you to install software locally, that is a content error —
please [open an issue](https://github.com/mdmanurung/ai-fluency-for-bio/issues).

---

## Getting Started

1. You are on the course home page. Read the module hooks above to gauge your starting point.
2. Open [Module 1](modules/module-01-bio-ai-landscape/README.md). Each module ends with a direct link to the next.
3. Modules are largely independent — if you are already comfortable with the Bio-AI Landscape, start at Module 2.

**Total estimated course time: ~5.5 hours across 5 modules.**
Designed for self-paced completion over 1–2 weeks alongside an active research schedule.

---

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
You may reuse and adapt these materials for your own teaching with attribution.

---

## For Course Contributors and Developers

Looking to build the Quarto site locally, add module content, or deploy to GitHub Pages?
See [CONTRIBUTING.md](CONTRIBUTING.md).
