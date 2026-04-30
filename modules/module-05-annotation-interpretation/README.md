# Module 5: Cell Type Annotation & Biological Interpretation

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mdmanurung/ai-fluency-for-bio/blob/main/modules/module-05-annotation-interpretation/notebook.ipynb)

**Estimated Time to Complete: ~90 mins**

> **Tools needed:** Google Colab (free, no installation), Claude or ChatGPT (free web)
> **Prerequisites:** Complete Module 4, or load the saved `pbmc3k_processed.h5ad`
>
> Click the **Open in Colab** badge above to launch the runnable notebook. The README below is the narrative companion.

---

## Hook: 12 Clusters, No Labels

You have a beautiful UMAP. Twelve numbered clusters. But cluster 0 is not a cell type —
it is a set of cells that share a transcriptional state. The biology only begins when you
answer: **which genes define each cluster, and what cell type does that pattern represent?**

This is the step where domain knowledge, literature, and AI work together. No algorithm
can fully replace knowing that *NKG7* + *GNLY* means NK cell — but AI can dramatically
speed up the lookup, flag contradictions, and draft your annotation rationale.

---

## Setup: Load the Processed Data

```python
!pip install scanpy celltypist -q

import scanpy as sc
import numpy as np
import pandas as pd
import celltypist
import matplotlib.pyplot as plt

sc.settings.verbosity = 1

# Load from Module 4 output
adata = sc.read('pbmc3k_processed.h5ad')
print(adata)
```

If you don't have the saved file, re-run the Module 4 setup block first.

---

## Part 1: Find Marker Genes per Cluster

Scanpy's `rank_genes_groups` finds genes that are differentially expressed in each
cluster compared to all other cells.

```python
# Use the raw (log-normalized) counts stored in adata.raw
sc.tl.rank_genes_groups(
    adata,
    groupby='leiden',
    use_raw=True,
    method='wilcoxon',    # Wilcoxon rank-sum test — more robust than t-test for scRNA-seq
    n_genes=25
)

# Table of top markers per cluster
sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
```

### Extract the top markers as a DataFrame

```python
marker_df = sc.get.rank_genes_groups_df(adata, group=None)
# Shows: cluster, gene name, score, log-fold change, p-value, adjusted p-value

# Top 5 markers per cluster
top5 = (
    marker_df
    .groupby('group')
    .apply(lambda x: x.nlargest(5, 'scores'))
    .reset_index(drop=True)
)
print(top5.to_string())
```

---

## Part 2: Visualize Markers with Dotplots

A dotplot shows, for each cluster, the fraction of cells expressing a gene (dot size)
and the mean expression level (color intensity).

```python
# Known PBMC marker genes from literature
marker_genes = {
    'CD4 T':         ['IL7R', 'CCR7', 'CD3D'],
    'CD8 T':         ['CD8A', 'CD8B', 'GZMK'],
    'NK cells':      ['GNLY', 'NKG7', 'KLRD1'],
    'B cells':       ['MS4A1', 'CD79A', 'CD19'],
    'CD14+ Mono':    ['CD14', 'LYZ', 'S100A8'],
    'FCGR3A+ Mono':  ['FCGR3A', 'MS4A7', 'IFITM2'],
    'Dendritic':     ['FCER1A', 'CST3', 'HLA-DQA1'],
    'Platelets':     ['PPBP', 'PF4', 'GP1BB'],
}

sc.pl.dotplot(adata, marker_genes, groupby='leiden', use_raw=True)
sc.pl.stacked_violin(adata, marker_genes, groupby='leiden', use_raw=True)
```

---

## Part 3: AI-Assisted Cluster Annotation

For each cluster, take the top 10 marker genes and ask an LLM to identify the cell type.

### Prompt template

```
I am annotating clusters from a single-cell RNA-seq experiment on human PBMCs.

Cluster 3 top marker genes (ranked by Wilcoxon score):
MS4A1, CD79A, CD79B, HLA-DRA, HLA-DQB1, CD19, BANK1, PAX5, IGHM, IGHD

Please:
1. Identify the most likely cell type for this cluster
2. Explain which specific genes are the most diagnostic markers
3. Note any alternative interpretations or sub-types I should consider
4. Suggest 2–3 additional genes I could check to confirm the annotation
```

<details>
<summary>View Gold Standard Output</summary>

**Expected AI response for this cluster:**

**Most likely cell type: B cells (naïve or transitional)**

**Diagnostic markers:**
- `MS4A1` (CD20) — canonical B cell surface marker, used clinically for B cell depletion therapy
- `CD79A` / `CD79B` — components of the B cell receptor complex; highly specific for B cells
- `CD19` — pan-B cell marker; present from pro-B to mature B cells
- `PAX5` — transcription factor required for B cell lineage commitment
- `IGHM` + `IGHD` — co-expression suggests naïve B cells (IgM+IgD+ is the naïve B cell surface receptor isotype)

**Alternative interpretations:**
- If `IRF4` and `PRDM1` (Blimp-1) are also elevated, some cells may be transitioning to plasmablasts
- Check for `JCHAIN` and `MZB1` — if present, a plasma cell sub-cluster may be contaminating this cluster

**Confirmatory genes to check:**
- `VPREB3` — late pre-B / transitional B cell marker
- `TCL1A` — enriched in naïve and transitional B cells vs. memory B cells
- `CD27` — memory B cell marker; absence supports naïve annotation

**Red flag to watch for:** If the AI annotates this as a T cell because of the HLA genes,
that is wrong — HLA-DR expression is present on professional antigen-presenting cells
including B cells, and is not T cell-specific.

</details>

---

## Part 4: Automated Annotation with CellTypist

For a quick first pass, CellTypist uses a pre-trained classifier to annotate cells
against a reference atlas.

```python
# CellTypist requires log1p-normalized data in adata.X
# Ensure adata.X has log-normalized values (not the HVG-subset scaled values)
# We'll use adata.raw.to_adata() to get the full log-normalized matrix

adata_full = adata.raw.to_adata()

# Download the Immune_All_Low model (covers all major immune cell types)
model = celltypist.models.Model.load(model='Immune_All_Low.pkl')

# Run prediction
predictions = celltypist.annotate(
    adata_full,
    model=model,
    majority_voting=True    # assign one label per Leiden cluster by majority vote
)

# Transfer predictions back to adata
adata.obs['celltypist_label'] = predictions.predicted_labels.majority_voting.values

# Visualize
sc.pl.umap(adata, color=['leiden', 'celltypist_label'], ncols=2)
```

> **Treat CellTypist as a hypothesis, not a ground truth.** It excels at major immune
> populations but may split or merge sub-populations incorrectly. Always cross-check
> with your own marker gene analysis from Part 1.

---

## Part 5: Assign Final Cell Type Labels

After reviewing dotplots, AI-assisted annotation, and CellTypist:

```python
# Map Leiden cluster numbers to cell type names
# (Adjust this mapping based on your own marker gene analysis)
cell_type_map = {
    '0': 'CD4 T',
    '1': 'CD14+ Monocyte',
    '2': 'CD4 T',
    '3': 'B cell',
    '4': 'CD8 T',
    '5': 'NK cell',
    '6': 'CD14+ Monocyte',
    '7': 'Dendritic cell',
    '8': 'FCGR3A+ Monocyte',
}

adata.obs['cell_type'] = adata.obs['leiden'].map(cell_type_map)

# Final annotated UMAP
sc.pl.umap(
    adata,
    color=['cell_type'],
    legend_loc='on data',
    legend_fontsize=10,
    title='PBMC 3k — Annotated Cell Types',
    frameon=False,
    save='pbmc3k_annotated_umap.pdf'    # saves to ./pbmc3k_annotated_umap.pdf
)
```

---

## Part 6: Differential Expression Between Conditions

When comparing two conditions (e.g., treated vs. untreated, day 0 vs. day 7):

```python
# Example: Compare CD14+ monocytes between two conditions
# (For PBMC 3k this is a single sample — this code applies to multi-sample datasets)

# Subset to one cell type
mono = adata[adata.obs['cell_type'] == 'CD14+ Monocyte'].copy()

# Run DE (requires a 'condition' column in mono.obs)
# sc.tl.rank_genes_groups(mono, groupby='condition', method='wilcoxon', use_raw=True)

# For a single sample, you can compare across clusters:
sc.tl.rank_genes_groups(
    adata,
    groupby='cell_type',
    groups=['CD8 T'],
    reference='CD4 T',     # compare CD8 T vs. CD4 T as reference
    method='wilcoxon',
    use_raw=True
)
sc.pl.rank_genes_groups_violin(adata, groups='CD8 T', n_genes=10)
```

---

## Capstone Exercise: Full Annotation

Run the complete annotation pipeline on the PBMC 3k dataset and answer the following
questions using your dotplots, marker gene tables, and AI assistance:

1. Which cluster expresses both `CD3D` (T cell) and `NKG7` (NK cell)? What cell type is this likely to be?
2. There are two monocyte clusters — what distinguishes CD14+ monocytes from FCGR3A+ monocytes at the marker gene level?
3. One cluster has very few cells (<50) and expresses `FCER1A` and `CST3`. What is it, and why is it numerically rare in PBMCs?

<details>
<summary>View Gold Standard Output</summary>

**Q1: CD3D + NKG7 co-expressing cluster**
This is most likely **NKT cells** (Natural Killer T cells) or cytotoxic T cells
with NK-like features. Key distinctions:
- If the cluster also expresses `GNLY` and `KLRD1` at high levels: NKT or NK-like CD8 T
- Check for `TRAV10` (invariant NKT marker) or `CD56` (NCAM1) to confirm NKT identity
- A small population with this phenotype is expected in healthy PBMC — not an annotation error

**Q2: CD14+ vs. FCGR3A+ Monocytes**
- **CD14+ monocytes** (classical): `CD14`, `LYZ`, `S100A8`, `S100A9` — pro-inflammatory, phagocytic
- **FCGR3A+ monocytes** (non-classical): `FCGR3A` (CD16), `MS4A7`, `IFITM2`, `CX3CR1` — patrol vasculature, anti-viral functions, lower `CD14` expression
- The two populations represent a developmental continuum; classical monocytes can differentiate into non-classical
- In healthy blood: ~85% classical, ~15% non-classical — which explains the size difference between these clusters

**Q3: Small FCER1A+ CST3+ cluster**
This is **plasmacytoid or conventional dendritic cells (DCs)**.
- `FCER1A` (FcεRI alpha) + `CST3` + `HLA-DQA1` = myeloid/conventional DC (cDC2)
- Numerically rare because DCs represent <1% of PBMCs in healthy blood
- They are detectable here because 10x Chromium captures all cells without pre-selection

</details>

---

## Key Takeaways

1. **Marker genes, not UMAP proximity, define cell types.** Run `rank_genes_groups` before annotating.
2. **LLMs are fast annotation assistants, not oracles.** Provide the top 10 ranked genes and ask for alternative interpretations — always verify against a primary reference (Human Cell Atlas, CellMarker database).
3. **CellTypist gives you a starting hypothesis.** It works well for major immune populations; it struggles with rare or disease-specific states.
4. **Save your final annotated `.h5ad` file.** It is the complete, reproducible record of your analysis.

---

## You Have Completed the Course

Starting from raw FASTQ files, you have:

1. ✅ Assessed raw data quality with FastQC
2. ✅ Aligned reads and generated a count matrix with Cell Ranger / STARsolo
3. ✅ Loaded, filtered, normalized, and selected features in Scanpy
4. ✅ Performed PCA, UMAP, and Leiden clustering
5. ✅ Annotated cell types using marker genes, AI assistance, and CellTypist

Your final output is a publication-ready annotated UMAP with biologically validated cell type labels.

**Next steps to explore:**
- Trajectory analysis: [Scanpy trajectory tutorial (PAGA)](https://scanpy-tutorials.readthedocs.io/en/latest/paga-paul15.html)
- Multi-sample integration: [Harmony](https://portals.broadinstitute.org/harmony/) or Scanorama
- RNA velocity: [scVelo](https://scvelo.readthedocs.io/)
- Spatial transcriptomics: [Squidpy](https://squidpy.readthedocs.io/)

---

*[← Back to Course Home](../../README.md)*
