# AI Fluency Foundations for Biology

A 4-week course that teaches AI fluency to biologists by running a **single-cell RNA-seq pipeline** — FASTQ → annotated UMAP — with an AI assistant in the loop.

> **Course site:** <https://mdmanurung.github.io/ai-fluency-for-bio/>
> *(Enable GitHub Pages → Settings → Pages once `main` is updated.)*

---

## What this course is

AI tools — Claude, ChatGPT, Copilot, Cursor, agentic assistants — are entering biology research workflows fast. Used well, they accelerate analysis, surface relevant literature, and help draft code. Used carelessly, they introduce subtle errors, fabricated citations, and brittle pipelines.

This course teaches the framework, vocabulary, and habits to collaborate with AI tools productively and responsibly. The conceptual content is subfield-agnostic; the hands-on track is a complete single-cell RNA-seq pipeline on the 10x PBMC 3k dataset.

You finish the course with:

- A working understanding of the **4 D's of AI fluency** — Delegation, Description, Discernment, Diligence — adapted for biology research, following [Anthropic's AI Fluency Framework](https://www.anthropic.com/ai-fluency).
- A working-level mental model of how LLMs are trained, generate text, and fail.
- A reproducible, AI-assisted scRNA-seq analysis you wrote yourself, with disclosure and verification practices that hold up to peer review.

## How the course is structured

The course has three conceptual tracks and a weekly schedule that braids them together.

**Three tracks** (all in the [course site sidebar](https://mdmanurung.github.io/ai-fluency-for-bio/)):

1. **AI fluency: the 4 D's** — Delegation, Description, Discernment, Diligence.
2. **AI literacy for bio** — how LLMs work, prompting, tool use & agents, ethics & limits.
3. **Hands-on bioinformatics** — code assistance, data analysis, literature review, protocol design — with worked examples grounded in the scRNA-seq project.

**The hands-on project** is a 5-module scRNA-seq pipeline, taught alongside the theory:

| Module | Topic | Compute | When |
|:------:|:------|:--------|:-----|
| [1](modules/module-01-raw-data-qc/README.md) | Raw data QC (FastQC on 10x Chromium reads) | Local or HPC | Pre-week 3 reading |
| [2](modules/module-02-alignment-count-matrix/README.md) | Alignment & count matrix (Cell Ranger / STARsolo) | HPC (or skip — pre-built matrix in Module 3) | Pre-week 3 reading |
| [3](modules/module-03-preprocessing-scanpy/README.md) | Preprocessing & QC in Scanpy | Google Colab (free) | Week 3 in-class + mini-project |
| [4](modules/module-04-clustering-umap/README.md) | Dimensionality reduction, clustering, UMAP | Google Colab (free) | Week 3 after-class |
| [5](modules/module-05-annotation-interpretation/README.md) | Cell-type annotation & differential expression | Google Colab (free) | Week 4 capstone |

**Dataset:** 10x PBMC 3k throughout — 2,700 PBMCs from a healthy donor, ~8 well-characterised cell types, small enough to run in Colab on a free tier.

**Weekly schedule** (4 weekly meetings, ~2 hours each):

| Week | Theme | Deliverable |
|:----:|:------|:------------|
| [1](weeks/week-1.qmd) | AI fluency foundations — the 4 D's | Reflection + tooling check |
| [2](weeks/week-2.qmd) | LLM literacy for bio researchers | Prompt-engineering exercise |
| [3](weeks/week-3.qmd) | scRNA-seq I — QC, normalisation, clustering | Mini-project (PBMC 3k QC + clustering) + capstone proposal |
| [4](weeks/week-4.qmd) | scRNA-seq II — annotation, capstone | Capstone (annotation OR literature brief OR protocol — student choice) |

See the [Syllabus](course-syllabus.qmd) for the full assessment scheme, AI-use policy, disclosure rubric, and reading list.

## Two ways to take the material

- **The 4-week course (recommended).** Live sessions, weekly deliverables, capstone. The structure that makes the practice deliberate.
- **Self-paced through the modules.** Modules 1–5 are runnable end-to-end without the weekly meetings if you only want the scRNA-seq pipeline. You miss the fluency framework and the disclosure practice — those live in the [course site](https://mdmanurung.github.io/ai-fluency-for-bio/).

## What you need

- Working comfort with Python at a scripting level.
- A GitHub account.
- A free-tier LLM chat account (Claude, ChatGPT, or Gemini). Paid tiers help in weeks 3–4 but are not required.
- A coding assistant (Claude Code, Cursor, or VS Code + Copilot).
- A grounded literature tool (Elicit, Consensus, SciSpace, or Perplexity sources mode).
- For the hands-on weeks: a Google account for Colab. For a local install, use the pinned `environment.yml` (conda) or `requirements.txt` (pip / uv) at the repo root — `conda env create -f environment.yml && conda activate ai-fluency-for-bio` reproduces the full stack.
- HPC or cloud access *only* if you want to run Modules 1–2. Otherwise start at Module 3.

## Repo layout

```
.
├── _quarto.yml                 # site config and sidebar
├── index.qmd                   # site landing
├── course-overview.qmd         # learning outcomes
├── course-syllabus.qmd         # assessment, AI-use policy, disclosure rubric, readings
├── course-faq.qmd              # FAQ
├── course-team.qmd             # instructor + TAs
├── course-support.qmd          # how to get help
├── fluency/                    # 4 D's
│   ├── delegation.qmd
│   ├── description.qmd
│   ├── discernment.qmd
│   └── diligence.qmd
├── literacy/                   # LLM background
│   ├── how-llms-work.qmd
│   ├── prompting.qmd
│   ├── tool-use-and-agents.qmd
│   └── ethics-and-limits.qmd
├── bioinformatics/             # AI-fluency lens on hands-on tasks
│   ├── code-assistance.qmd
│   ├── data-analysis.qmd
│   ├── literature-review.qmd
│   └── protocol-design.qmd
├── modules/                    # scRNA-seq pipeline (FASTQ → annotated UMAP)
│   ├── module-01-raw-data-qc/
│   ├── module-02-alignment-count-matrix/
│   ├── module-03-preprocessing-scanpy/
│   ├── module-04-clustering-umap/
│   └── module-05-annotation-interpretation/
└── weeks/                      # weekly student-facing pages
    ├── week-1.qmd
    ├── week-2.qmd
    ├── week-3.qmd
    ├── week-4.qmd
    └── starter-week3-python.qmd
```

## Building the site locally

```bash
# install Quarto >= 1.5 (https://quarto.org/docs/get-started/)
quarto preview          # live preview at http://localhost:4444
quarto render           # build to _site/
```

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may reuse and adapt these materials with attribution.

## For contributors

See [CONTRIBUTING.md](CONTRIBUTING.md). Active development notes live in [PLANS.md](PLANS.md); recent changes are recorded in [CHANGELOG.md](CHANGELOG.md).
