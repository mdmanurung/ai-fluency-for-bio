# AI Fluency Foundations for Biology

A **self-paced** course that teaches AI fluency to biologists by running a **single-cell RNA-seq pipeline** — FASTQ → annotated UMAP — with an AI assistant in the loop. Plan on ~1 week per unit at ~3–5 hours; allow 4–8 weeks total. No instructor, no grades, fully solo.

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

The course is organised as **four self-paced units** ("Week N"), each combining readings from three conceptual tracks with a hands-on scRNA-seq pipeline. Each week page is self-contained: **readings → practice → knowledge check → project → self-rubric**.

**Three conceptual tracks** (anchored to weeks, but cross-referenced as needed):

1. **AI fluency: the 4 D's** — Delegation, Description, Discernment, Diligence (Week 1).
2. **AI literacy for bio** — how LLMs work, prompting, tool use & agents, ethics & limits (Week 2).
3. **Hands-on bioinformatics** — code assistance, data analysis, literature review, protocol design — grounded in the scRNA-seq project (Weeks 3 & 4).

**The hands-on project** is a 5-module scRNA-seq pipeline:

| Module | Topic | Compute | When |
|:------:|:------|:--------|:-----|
| [1](modules/module-01-raw-data-qc/README.md) | Raw data QC (FastQC on 10x Chromium reads) | Local or HPC | Week 3 reading |
| [2](modules/module-02-alignment-count-matrix/README.md) | Alignment & count matrix (Cell Ranger / STARsolo) | HPC (or skip — pre-built matrix in Module 3) | Week 3 reading |
| [3](modules/module-03-preprocessing-scanpy/README.md) | Preprocessing & QC in Scanpy | Google Colab (free) | Week 3 hands-on |
| [4](modules/module-04-clustering-umap/README.md) | Dimensionality reduction, clustering, UMAP | Google Colab (free) | Week 3 hands-on |
| [5](modules/module-05-annotation-interpretation/README.md) | Cell-type annotation & differential expression | Google Colab (free) | Week 4 hands-on |

**Dataset:** 10x PBMC 3k throughout — 2,700 PBMCs from a healthy donor, ~8 well-characterised cell types, small enough to run in Colab on a free tier.

**Suggested pacing** (~1 week per unit, ~3–5 hours; allow 4–8 weeks total):

| Unit | Theme | Project (with self-rubric) |
|:----:|:------|:------------|
| [1](weeks/week-1.qmd) | AI fluency foundations — the 4 D's | Reflection + tooling check |
| [2](weeks/week-2.qmd) | LLM literacy for bio researchers | Prompt-engineering exercise |
| [3](weeks/week-3.qmd) | scRNA-seq I — QC, normalisation, clustering | Mini-project (PBMC 3k QC + clustering, AI-free baseline + AI-assisted iteration) |
| [4](weeks/week-4.qmd) | scRNA-seq II — annotation, final project | Final project (annotation OR literature brief OR protocol — your choice) |

See the [Syllabus](course-syllabus.qmd) for the AI-use policy, disclosure rubric, data policy, and reading list. See [How to use this course](course-how-to-use.qmd) for the self-pacing model and self-assessment mechanisms.

## Self-assessment

There are no grades. Four mechanisms let you check your own progress:

- **Per-page "Check your understanding" callouts** at the bottom of each conceptual page (3–5 questions, worked answers).
- **Per-week knowledge checks** at the end of each week page (5–8 questions, worked answers).
- **Per-week hands-on practice exercises** with self-check answers.
- **Per-project self-rubrics** so you can grade your own work against the same dimensions an instructor would.

## What you need

- Working comfort with Python at a scripting level.
- A GitHub account.
- A free-tier LLM chat account (Claude, ChatGPT, or Gemini). Paid tiers help in Weeks 3–4 but are not required.
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
├── course-how-to-use.qmd       # self-paced model + learner-progress checklist
├── course-team.qmd             # about the author
├── course-support.qmd          # how to get unstuck
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
├── weeks/                      # per-week learner-facing pages
│   ├── week-1.qmd
│   ├── week-2.qmd
│   ├── week-3.qmd
│   ├── week-4.qmd
│   └── starter-week3-python.qmd
└── reference/                  # cross-cutting reference material
    ├── glossary.qmd
    ├── prompt-library.qmd
    ├── peer-review.qmd         # self-review template
    └── topic-index.qmd         # by-subject index
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
