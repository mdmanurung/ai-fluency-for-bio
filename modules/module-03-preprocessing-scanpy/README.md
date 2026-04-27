# Module 3: Preprocessing & Quality Control in Scanpy

**Estimated Time to Complete: ~75 mins**

> **Tools needed:** Google Colab (free, no installation), Claude or ChatGPT (free web)
> **HPC required?** No. Everything in this module runs in your browser.
> **Dataset:** 10x PBMC 3k (loaded directly by Scanpy — no download needed)

---

## Hook: Are Those 5,000 "Cells" Real Cells?

Cell Ranger reports 5,013 detected cells. But some of those barcodes represent:
- **Dead or dying cells** — high mitochondrial RNA, low gene count
- **Empty droplets** — ambient RNA, almost no genes
- **Doublets** — two cells captured in one droplet, artificially high gene count

If you skip QC and cluster raw data, your "cell types" will include dead-cell clusters,
doublet artifacts, and noisy background populations. Annotation becomes impossible.

**QC is not optional.** This module teaches you what to measure, what to cut, and
how to use AI to help justify your thresholds.

---

## Setup: Open Google Colab

1. Go to [colab.research.google.com](https://colab.research.google.com/)
2. Create a new notebook
3. Copy and run each code block below in sequence

---

## Part 1: Install and Import

```python
# Run this cell first — takes ~2 minutes
!pip install scanpy scrublet -q

import scanpy as sc
import numpy as np
import pandas as pd
import scrublet as scr
import matplotlib.pyplot as plt

sc.settings.verbosity = 1
sc.settings.figdir = './'
print(f"Scanpy version: {sc.__version__}")
```

---

## Part 2: Load the PBMC 3k Dataset

The PBMC 3k dataset (2,700 PBMCs from a healthy donor, 10x Chromium v1) is built into
Scanpy for tutorial purposes.

```python
# Load directly from Scanpy's built-in datasets
adata = sc.datasets.pbmc3k()

print(adata)
# AnnData object with n_obs × n_vars = 2700 × 32738
# The AnnData object is the core data structure in Scanpy:
#   adata.X      = count matrix (cells × genes)
#   adata.obs    = cell metadata (rows)
#   adata.var    = gene metadata (columns)
```

**If you have your own Cell Ranger output,** replace the above with:

```python
# Load from Cell Ranger filtered output
adata = sc.read_10x_mtx(
    '/path/to/filtered_feature_bc_matrix/',
    var_names='gene_symbols',   # use gene symbols (e.g. CD3E) not Ensembl IDs
    cache=True
)
adata.var_names_make_unique()  # ensure gene names are unique
```

---

## Part 3: Calculate QC Metrics

```python
# Flag mitochondrial genes (human: MT- prefix; mouse: mt- prefix)
adata.var['mt'] = adata.var_names.str.startswith('MT-')

# Calculate QC metrics — adds columns to adata.obs and adata.var
sc.pp.calculate_qc_metrics(
    adata,
    qc_vars=['mt'],
    percent_top=None,
    log1p=False,
    inplace=True
)

# Key new columns in adata.obs:
# n_genes_by_counts  = number of genes with at least 1 count
# total_counts       = total UMI count per cell
# pct_counts_mt      = % of counts from mitochondrial genes
```

### Visualize QC metrics

```python
sc.pl.violin(
    adata,
    ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
    jitter=0.4,
    multi_panel=True
)
```

**What you're looking for:**
- `n_genes_by_counts`: most cells should cluster in a clear range; outliers at the bottom are empty/dead, at the top are doublets
- `total_counts`: should mirror n_genes; extreme outliers at the top = doublets
- `pct_counts_mt`: healthy cells < 20%; a long tail above 20–25% = dying cells

```python
# Scatter plot to visualize the relationship
sc.pl.scatter(adata, x='total_counts', y='pct_counts_mt')
sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts')
```

---

## Part 4: Filter Low-Quality Cells

### AI-assisted threshold selection

Before filtering, use this prompt:

```
I am analyzing 10x scRNA-seq data from human PBMCs.
My QC violin plots show:
- n_genes_by_counts: median ~1,200, range 200–5,000, with a few cells above 3,500
- total_counts: median ~2,500, range 500–20,000
- pct_counts_mt: median ~3%, with a tail up to 30%

What filtering thresholds should I use for:
1. Minimum genes per cell
2. Maximum genes per cell (to remove doublets)
3. Maximum mitochondrial percentage

Please justify each threshold and note any assumptions about my tissue type.
```

<details>
<summary>View Gold Standard Output</summary>

A well-calibrated LLM should recommend approximately:

- **Minimum genes:** 200–300 (removes empty droplets; PBMC median of 1,200 means this is a conservative lower bound)
- **Maximum genes:** 2,500–3,500 (the few cells above 3,500 likely represent doublets; the exact cutoff should be set just above the main distribution shoulder)
- **Maximum mitochondrial %:** 5–10% for PBMCs (PBMCs are robust; more fragile tissues like neurons may require up to 20–25%)

**Correct reasoning the AI should include:**
- Doublet threshold is tissue/protocol dependent — for PBMCs a max of ~2,500 genes is standard; for a complex tissue like brain you'd set it higher
- Mitochondrial threshold for PBMCs can be strict (5%) because healthy PBMCs have low mt expression; tissues with high metabolic activity (muscle, heart) warrant more permissive thresholds

**Flag if the AI omits:** tissue context matters — a single universal threshold does not exist.

</details>

### Apply filters

```python
# Apply thresholds (adjust based on your own violin plots)
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)

# Filter by QC thresholds
adata = adata[adata.obs.n_genes_by_counts < 2500, :]
adata = adata[adata.obs.pct_counts_mt < 5, :]

print(f"Cells after filtering: {adata.n_obs}")
print(f"Genes after filtering: {adata.n_vars}")
# Expected for PBMC 3k: ~2,638 cells, ~13,000 genes
```

---

## Part 5: Doublet Detection with Scrublet

```python
# Run Scrublet to score each cell for doublet probability
scrub = scr.Scrublet(adata.X)
doublet_scores, predicted_doublets = scrub.scrub_doublets()

adata.obs['doublet_score'] = doublet_scores
adata.obs['predicted_doublet'] = predicted_doublets

# Visualize doublet score distribution
scrub.plot_histogram()

# Remove predicted doublets
print(f"Predicted doublets: {predicted_doublets.sum()}")
adata = adata[~adata.obs['predicted_doublet'], :]
print(f"Cells after doublet removal: {adata.n_obs}")
```

---

## Part 6: Normalization & Log-Transformation

```python
# Normalize each cell to 10,000 total counts (library size correction)
sc.pp.normalize_total(adata, target_sum=1e4)

# Log-transform: log(X + 1) — stabilizes variance, makes data more normally distributed
sc.pp.log1p(adata)

# Save the normalized, log-transformed values as the 'raw' layer for later use
adata.raw = adata
```

---

## Part 7: Highly Variable Gene (HVG) Selection

Working with all ~13,000 genes is computationally expensive and adds noise.
Highly variable genes carry the most biological signal.

```python
# Identify highly variable genes
sc.pp.highly_variable_genes(
    adata,
    min_mean=0.0125,
    max_mean=3,
    min_disp=0.5
)

# Visualize HVG distribution
sc.pl.highly_variable_genes(adata)

print(f"Highly variable genes: {adata.var.highly_variable.sum()}")
# Expected: ~1,800–2,000 HVGs for PBMC 3k

# Subset to HVGs for downstream analysis
adata = adata[:, adata.var.highly_variable]
print(f"AnnData after HVG selection: {adata}")
```

---

## Exercise: Interpret a QC Issue

You run the QC pipeline on a new dataset and observe:
- Two distinct clusters in the `total_counts` vs `n_genes_by_counts` scatter plot — one cluster has low counts and low genes, one has normal counts and genes
- The low cluster accounts for ~30% of cells
- `pct_counts_mt` for the low cluster averages 28%

Use Claude or ChatGPT: **What does this pattern indicate, and what is the correct course of action?**

<details>
<summary>View Gold Standard Output</summary>

**The pattern indicates a large fraction of dying or stressed cells.**

Two-cluster structure in `total_counts` vs `n_genes_by_counts` where one cluster has:
- Low UMI counts + low gene counts + high mt% = classic "damaged cell" signature

**Correct course of action:**
1. Set a strict mt% threshold (e.g., 20–25%) to remove the damaged cluster
2. Investigate the biology: was this a tissue dissociation artifact? Long time from dissection to library prep? Cold ischemia?
3. If >30% of cells are low quality, consider whether the experiment is salvageable — a high ambient RNA signal may also be present, warranting Cellbender or SoupX correction

**What the AI should NOT say:**
- That a two-cluster pattern is always normal (it is not)
- That you should retain the low-quality cells because "they might be a real cell type" without evidence

If the AI suggests running Cellbender or SoupX for ambient RNA correction on top of the mt% filtering, that is a correct and advanced recommendation.

</details>

---

## Key Takeaways

1. **Three core QC metrics:** `n_genes_by_counts` (doublets up, dead cells down), `total_counts` (mirrors genes), `pct_counts_mt` (dead cells up).
2. **Thresholds are not universal.** PBMCs tolerate strict mt% cutoffs; neurons do not. Always use tissue and protocol context when asking AI for threshold recommendations.
3. **Normalization to 10,000 counts + log-transform is the standard starting point.** Save `adata.raw` before any further scaling — you'll need raw log-counts for differential expression later.
4. **HVG selection reduces noise.** ~2,000 HVGs is typical; using all genes adds compute cost without improving clustering quality for most datasets.

---

## → Next: Module 4 — Dimensionality Reduction, Clustering & UMAP

[Open Module 4](../module-04-clustering-umap/README.md)

*In Module 4, you will scale the data, run PCA, build a neighborhood graph,
generate a UMAP embedding, and cluster cells with the Leiden algorithm.*
