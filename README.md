# AI-Assisted Single-Cell RNA-seq: From FASTQ to UMAP

> **Who this is for:** Biologists and bioinformaticians who want to analyze
> single-cell RNA-seq data end-to-end — and use AI tools to write, debug,
> and explain their analysis code along the way.

**Estimated Time to Complete This Orientation: 5 mins**

---

## The Problem

You just received 300 GB of FASTQ files from the sequencing core.
Your 10x Chromium run captured \~8,000 cells from mouse lung tissue after influenza infection.
You need to go from raw reads to a UMAP plot showing distinct immune cell populations —
and your PI wants interpretable results by end of week.

Where do you start? What tools do you use? And how can AI help you move faster without
introducing errors you won't catch until your lab meeting?

This course answers all three questions.

---

## What You Will Learn

| # | Outcome | Module |
|:--|:--------|:-------|
| 1 | Understand scRNA-seq library structure, interpret FastQC output, and use AI to flag quality issues | 1 |
| 2 | Run Cell Ranger or STARsolo to generate a count matrix, and use AI to write HPC job scripts | 2 |
| 3 | Load a count matrix into Scanpy, apply QC filters, normalize, and select highly variable genes | 3 |
| 4 | Perform PCA, build a neighborhood graph, generate a UMAP, and cluster cells with Leiden | 4 |
| 5 | Identify marker genes, annotate cell types, run differential expression, and export publication-ready figures | 5 |

---

## Course Modules

### Module 1 — Introduction to scRNA-seq & Raw Data QC

**[→ Open Module 1](modules/module-01-raw-data-qc/README.md)**

Raw FASTQ files, 10x Chromium read anatomy, FastQC interpretation, AI-assisted QC triage.

**Tools:** FastQC (local or HPC), Claude / ChatGPT (web) | **Estimated Time: ~60 mins**

---

### Module 2 — Alignment & Count Matrix Generation

**[→ Open Module 2](modules/module-02-alignment-count-matrix/README.md)**

Cell Ranger and STARsolo workflows, reference genome setup, filtered vs. raw matrix outputs,
AI-generated HPC submission scripts.

**Tools:** Cell Ranger or STARsolo (HPC / cloud VM required), Claude / ChatGPT (web) | **Estimated Time: ~90 mins**

---

### Module 3 — Preprocessing & Quality Control in Scanpy

**[→ Open Module 3](modules/module-03-preprocessing-scanpy/README.md)**

Loading 10x data into AnnData, QC metric violin plots, cell filtering, doublet detection,
normalization, log-transformation, and highly variable gene selection.
AI used to interpret thresholds and explain filtering decisions.

**Tools:** Google Colab (free), Claude / ChatGPT (web) | **Estimated Time: ~75 mins**

---

### Module 4 — Dimensionality Reduction, Clustering & UMAP

**[→ Open Module 4](modules/module-04-clustering-umap/README.md)**

PCA, k-NN graph, UMAP embedding, Leiden clustering, and parameter tuning.
AI used to explain algorithm choices and debug unexpected outputs.

**Tools:** Google Colab (free), Claude / ChatGPT (web) | **Estimated Time: ~90 mins**

---

### Module 5 — Cell Type Annotation & Biological Interpretation

**[→ Open Module 5](modules/module-05-annotation-interpretation/README.md)**

Marker gene discovery, dotplot and violin visualization, automated annotation with CellTypist,
differential expression between conditions, and export of final annotated UMAP.
AI used to interpret gene lists and draft biological summaries.

**Tools:** Google Colab (free), Claude / ChatGPT (web) | **Estimated Time: ~90 mins**

---

## Dataset Used Throughout This Course

All hands-on exercises use the **10x PBMC 3k dataset** — 2,700 peripheral blood mononuclear
cells from a healthy donor, sequenced on the Illumina NextSeq 500.

- Public domain, freely downloadable from 10x Genomics
- Small enough to run in Google Colab on a free tier
- Contains 8 well-characterized cell types (T cells, B cells, NK cells, monocytes, dendritic cells)
- The canonical "hello world" dataset for single-cell analysis

---

## Tools at a Glance

| Module | Key Tools | Installation Required? |
|--------|-----------|----------------------|
| 1 | FastQC, Claude / ChatGPT | FastQC: local or HPC |
| 2 | Cell Ranger or STARsolo | HPC or cloud VM |
| 3 | Google Colab + Scanpy | None (browser) |
| 4 | Google Colab + Scanpy | None (browser) |
| 5 | Google Colab + Scanpy + CellTypist | None (browser) |

> **Modules 3–5 are fully browser-based.** If you do not have HPC access,
> you can skip to Module 3 using the pre-processed PBMC 3k count matrix
> provided in that module.

---

## Getting Started

1. If you have HPC or cloud access: start at [Module 1](modules/module-01-raw-data-qc/README.md)
2. If you only have a browser: skip to [Module 3](modules/module-03-preprocessing-scanpy/README.md) — a pre-processed count matrix is provided

**Total estimated time: ~7.5 hours across 5 modules.**

---

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
You may reuse and adapt these materials with attribution.

---

## For Course Contributors and Developers

See [CONTRIBUTING.md](CONTRIBUTING.md).
