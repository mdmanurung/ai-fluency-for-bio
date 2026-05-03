# Module 4: dimensionality reduction, clustering, and UMAP

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mdmanurung/ai-fluency-for-bio/blob/main/modules/module-04-clustering-umap/notebook.ipynb)

Estimated time to complete: 90 mins.

> Tools needed: Google Colab (free, no installation), and Claude or ChatGPT (free web).
> Prerequisites: complete Module 3, or start fresh using the setup code below.
>
> Click the Open in Colab badge above to launch the runnable notebook. The README below is the narrative companion.

---

## Hook: 20,000 dimensions won't fit on a page

After Module 3 you have a matrix of about 2,600 cells by about 2,000 highly variable genes.
Each cell is a point in 2,000-dimensional space. You cannot visualize 2,000 dimensions.
You cannot cluster points you cannot measure distances between.

The solution is to:

1. *Compress* 2,000 dimensions into about 50 meaningful components with PCA.
2. *Map* those 50 components to 2D with UMAP for visualisation.
3. *Group* similar cells with graph-based clustering (Leiden).

The result is a UMAP plot where each dot is a cell, coloured by cluster. That plot is
what this module builds.

---

## Setup: continue from Module 3 or reload

If continuing from Module 3, your `adata` object is ready. Otherwise:

```python
!pip install scanpy -q

import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt

sc.settings.verbosity = 1

# Reload the PBMC 3k dataset and re-run preprocessing
adata = sc.datasets.pbmc3k()
adata.var['mt'] = adata.var_names.str.startswith('MT-')
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.n_genes_by_counts < 2500, :]
adata = adata[adata.obs.pct_counts_mt < 5, :]
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
adata.raw = adata
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
adata = adata[:, adata.var.highly_variable]

print(f"Ready: {adata}")
```

---

## Part 1: scale the data

Before PCA, scale each gene to zero mean and unit variance. This prevents highly-expressed
genes from dominating the PCA.

```python
sc.pp.scale(adata, max_value=10)
# max_value=10 clips extreme outliers (more than 10 standard deviations) to prevent
# them from dominating PCA components
```

> Why scale? Without scaling, a gene with 10,000 counts per cell would contribute far
> more variance to PCA than a gene with 100 counts. Scaling ensures that a two-fold
> change in a lowly expressed gene is treated equally to a two-fold change in a highly
> expressed gene.

---

## Part 2: principal component analysis (PCA)

PCA finds the directions of maximum variance in the gene expression space and
projects all cells onto these axes (principal components, PCs).

```python
sc.tl.pca(adata, svd_solver='arpack', n_comps=50)

# Inspect how much variance each PC explains
sc.pl.pca_variance_ratio(adata, log=True, n_pcs=50)
```

Reading the elbow plot:

- The x-axis is PC number, the y-axis is % variance explained.
- Look for an "elbow" where the curve flattens.
- For PBMC 3k, the elbow is typically around PC 10 to 15.
- Use 10 to 40 PCs for downstream steps. More is not always better. Noise PCs hurt clustering.

### AI-assisted PC selection

```
I ran PCA on scRNA-seq PBMC data (2,638 cells, 1,838 HVGs).
The variance ratio plot shows:
- PC1: 8.2%, PC2: 5.1%, PC3: 3.4%, PC4: 2.8%, PC5: 2.1%
- The curve gradually flattens; by PC 15 each PC explains <1%
- There is no sharp elbow

How many PCs should I use for building the neighborhood graph?
What are the consequences of using too few vs too many?
```

<details>
<summary>View Gold Standard Output</summary>

For this elbow profile, 10 to 20 PCs is a reasonable range. The standard recommendation
for PBMC data is 15 to 20 PCs.

Consequences:

- *Too few PCs* (5, say). You discard real biological variance. Rare cell types that
  are captured in PC 8 to 15 may merge with larger populations or disappear.
- *Too many PCs* (40 or more). You include noise PCs that represent technical
  variation (sequencing depth differences, cell cycle effects), which can create
  artifactual sub-clusters.

A practical approach the AI should mention: try n_pcs=10 and n_pcs=20 and compare the
resulting clusterings. For PBMC 3k with known cell types, both should recover the same
8 populations or so.

</details>

---

## Part 3: neighborhood graph

UMAP and Leiden clustering both need a *k-nearest-neighbour (kNN) graph* of the cells,
built in PC space.

```python
sc.pp.neighbors(
    adata,
    n_neighbors=10,    # k: number of nearest neighbors per cell
    n_pcs=40           # number of PCs to use
)
```

Key parameters:

- `n_neighbors`. Higher values give smoother clusters with less fine structure. Lower values are noisier but capture rare cells. Typical range: 5 to 30.
- `n_pcs`. Use the number identified from the elbow plot.

---

## Part 4: UMAP embedding

UMAP (Uniform Manifold Approximation and Projection) arranges cells in 2D so that
cells with similar transcriptomes are placed near each other.

```python
sc.tl.umap(adata)

# Visualize. Color by total counts first to check for batch effects or gradients
sc.pl.umap(adata, color='total_counts', title='UMAP colored by total UMI counts')
```

> UMAP is a visualisation tool, not a clustering tool. Distances between clusters on a
> UMAP plot are *not* quantitatively meaningful. Two clusters that look far apart may
> be closer in PC space than they appear. Always confirm cluster identity with marker
> genes, not visual proximity.

---

## Part 5: Leiden clustering

Leiden clustering builds communities in the kNN graph: groups of cells that are
more connected to each other than to the rest of the dataset.

```python
sc.tl.leiden(adata, resolution=0.5)

# Visualize clusters on UMAP
sc.pl.umap(
    adata,
    color=['leiden'],
    legend_loc='on data',
    title='Leiden clusters (resolution=0.5)'
)
```

### Understanding the resolution parameter

```python
# Compare different resolutions
for res in [0.3, 0.5, 0.8, 1.2]:
    sc.tl.leiden(adata, resolution=res, key_added=f'leiden_{res}')

sc.pl.umap(
    adata,
    color=[f'leiden_{r}' for r in [0.3, 0.5, 0.8, 1.2]],
    ncols=2
)
```

| Resolution | Effect |
|-----------|--------|
| 0.1 to 0.3 | Fewer, larger clusters. Coarse cell types. |
| 0.5 to 0.8 | Standard for PBMCs. Recovers known major populations. |
| 1.0 to 2.0 | Many small clusters. Sub-populations. May over-fragment. |

A rule of thumb: start at 0.5 for PBMCs. Adjust based on biology. If you expect fine
subtypes (CD4 T cell subsets), increase resolution for that lineage after initial annotation.

---

## Exercise: diagnose a bad UMAP

You run the full pipeline and generate this UMAP:

- All cells form a single large blob with no visible separation.
- Leiden clustering at resolution 0.5 returns only two clusters.

Use Claude or ChatGPT to diagnose: what are the three most likely causes of a UMAP with no cluster structure, and what would you check first?

<details>
<summary>View Gold Standard Output</summary>

Three most likely causes, in order of likelihood:

1. *Scaling was skipped or applied incorrectly.* If `sc.pp.scale()` was not run, or was
   run before `log1p`, the PCA will be dominated by highly expressed genes and cells will
   not separate. Check `adata.X`. Values should be z-scores (mean 0, std 1).

2. *Too few PCs used for the neighbourhood graph.* Using only two or three PCs discards
   the signal that separates cell types. Check `sc.pp.neighbors(..., n_pcs=X)`. Try n_pcs=15.

3. *QC filtering was too aggressive.* If you removed all but a single cell type (by
   using a very low mt% threshold on a dataset where one cell type is metabolically
   active), there is no diversity left to cluster. Check cluster cell counts.

What to check first:

- Print `adata.X[:5, :5]`. Are the values z-scores (around -2 to +2)? If they are raw
  counts (0, 1, 5, 200, and so on), scaling was not applied correctly.

Less common causes the AI might also mention:

- Batch effects overwhelming biological signal (use Harmony or Scanorama to correct).
- All cells from the same cell line or sorted population (no transcriptomic diversity by design).

</details>

---

## Final check: save your processed AnnData

```python
# Save the full processed object for use in Module 5
adata.write('pbmc3k_processed.h5ad')
print("Saved.")

# Summary of what adata now contains
print(adata)
# Should show:
#   obs: 'n_genes_by_counts', 'total_counts', 'pct_counts_mt', 'doublet_score', 'leiden'
#   var: 'mt', 'highly_variable', 'mean', 'std'
#   obsm: 'X_pca', 'X_umap'
#   obsp: 'distances', 'connectivities'
```

---

## Self-check

Try to answer before checking. If you miss two, re-read the section on the dependency chain.

1. Why does running PCA on the un-scaled matrix give different (and usually worse) results than on the scaled matrix? What is the underlying reason for scaling first?
2. You compute Leiden at resolution 0.5 and get 9 clusters. You re-run at resolution 1.5 and get 22 clusters. Which is "correct"? How do you decide?
3. The AI tells you "the UMAP shows three groups, so there are three cell types". What is the Discernment problem? What is the right tool for "how many cell types are there"?
4. You build the neighbour graph with `n_neighbors=5` and the UMAP collapses into one blob. Then you set `n_neighbors=50` and it explodes into many disconnected sub-blobs. Which one is right, and what does the parameter do?

<details>
<summary>Self-check answers</summary>

1. PCA finds directions of *maximum variance*. Without scaling, genes with high mean expression dominate the variance simply because they have larger absolute count fluctuations. PC1 reflects "gene with highest mean", not biological structure. Scaling (mean-centring and variance-standardising) puts every gene on equal footing so PCA finds biologically informative directions instead of expression-magnitude artefacts. This is why Scanpy's tutorial sequence is normalise, log, HVG, scale, then PCA, in that order.
2. Neither is "correct" in isolation. Resolution is a hyperparameter that trades off granularity. The right answer is to (a) check stability. Does the cluster count change much between resolution 0.4 and 0.6? If yes, the choice is unstable. (b) Run marker-gene detection at both resolutions and see whether 0.5's "cluster 4" is two biologically distinct populations at 1.5 (a defensible split) or just over-clustering noise (the split is artefactual). Resolution should be tuned with the downstream biological question in mind, not chosen by feel.
3. UMAP geometry is dominated by neighbour-graph topology, not cell biology. Three visual groups in UMAP may be one cell type with batch structure, or eight cell types where some pairs happen to overlap in 2D. The right tool for "how many cell types" is marker-gene analysis on Leiden clusters: `sc.tl.rank_genes_groups` followed by checking known markers. UMAP confirms that clusters are well-separated. It doesn't define them.
4. The right value is whatever makes downstream Leiden clustering and marker-gene analysis sensible. Typically `n_neighbors=10` to 20 for a few-thousand-cell PBMC dataset. `n_neighbors=5` is too local: every cell connects only to nearest neighbours, the graph fragments, UMAP can't find global structure, and Leiden under-clusters. `n_neighbors=50` is too global: distinct populations bleed into each other through dense connections, and Leiden over-fragments. The parameter controls the *scale* at which you're asking "what's nearby?". Too small and you see only the local neighbourhood. Too large and everything looks like one population.

</details>

---

## Key takeaways

1. Scale, PCA, neighbours, UMAP, Leiden, in that order. Each step depends on the previous one.
2. UMAP is for visualisation only. Do not interpret inter-cluster distances as meaningful.
3. Leiden resolution controls granularity. Start at 0.5 and compare across resolutions before annotating.
4. If your UMAP is a blob, check scaling first. It is the most common cause of failed cluster separation.

---

## Next: Module 5, cell-type annotation and biological interpretation

[Open Module 5](../module-05-annotation-interpretation/README.md)

*In Module 5, you will find marker genes for each cluster, annotate cell types
using known markers and CellTypist, run differential expression, and produce a
final annotated UMAP ready for a figure panel.*
