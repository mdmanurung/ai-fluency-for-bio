# Module 2: alignment and count matrix generation

Estimated time to complete: 90 mins.

> Tools needed: Cell Ranger (7.0 or later) or STARsolo, a reference genome, and HPC or cloud VM.
> HPC required? Yes. Cell Ranger and STARsolo need significant RAM (32 GB or more) and cannot run in a browser.
> No HPC access? Skip to [Module 3](../module-03-preprocessing-scanpy/README.md). A pre-processed count matrix is provided there.

---

## Hook: from 300 GB of reads to a matrix in one command

Your 300 GB of FASTQ files contain millions of short reads. Each read knows which
cell it came from (barcode) and which RNA molecule it represents (UMI), but it
doesn't know which gene. Alignment maps every R2 read to a genomic location, and
Cell Ranger or STARsolo then collapses reads into a *count matrix*:

```
rows    = genes  (~33,000 for human GRCh38)
columns = cells  (~5,000 detected barcodes)
values  = UMI counts (integer, mostly zero; the matrix is about 95% sparse)
```

This matrix is the input to every downstream analysis step. Everything in
Modules 3 to 5 depends on getting it right here.

---

## Part 1: choosing an aligner

Two tools dominate 10x scRNA-seq alignment:

| Tool | Speed | Accuracy | HPC RAM | When to use |
|------|-------|----------|---------|-------------|
| Cell Ranger (10x Genomics) | Slower | High | 64 GB or more | Standard 10x data, with the best documentation; required for some library types (ATAC, Multiome) |
| STARsolo (open source) | Two to five times faster | Comparable | 32 GB or more | When you need speed, flexibility, or non-10x library formats |

> If you're unsure which to use, describe your library type and compute constraints
> to an LLM. It will give you a concrete recommendation. Always verify the Cell Ranger
> version against your Chromium kit version.

---

## Part 2: Cell Ranger Workflow

### 2a. Download and install Cell Ranger

```bash
# Download from 10x Genomics (requires registration)
# https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/latest
tar -xzvf cellranger-8.0.1.tar.gz
export PATH=/path/to/cellranger-8.0.1:$PATH
cellranger --version
```

### 2b. Download a pre-built reference genome

```bash
# Human GRCh38 + Ensembl 2024 annotations (recommended)
wget https://cf.10xgenomics.com/supp/cell-exp/refdata-gex-GRCh38-2024-A.tar.gz
tar -xzvf refdata-gex-GRCh38-2024-A.tar.gz

# Mouse mm10 (GRCm38)
wget https://cf.10xgenomics.com/supp/cell-exp/refdata-gex-mm10-2020-A.tar.gz
```

> If you need a custom reference (a transgene, viral genome, or custom annotation),
> use `cellranger mkref`. Prompt an LLM with your GTF and FASTA requirements for a
> step-by-step `mkref` command.

### 2c. Run Cell Ranger count

```bash
cellranger count \
  --id=sample_A \
  --transcriptome=/path/to/refdata-gex-GRCh38-2024-A \
  --fastqs=/path/to/fastqs \
  --sample=sample_A \
  --localcores=16 \
  --localmem=128
```

Key parameters:

| Parameter | Description |
|-----------|-------------|
| `--id` | Output folder name |
| `--transcriptome` | Path to Cell Ranger reference |
| `--fastqs` | Directory containing FASTQ files |
| `--sample` | Sample prefix used in FASTQ filenames |
| `--localcores` | CPU threads (match your HPC allocation) |
| `--localmem` | RAM in GB (64 to 128 GB is typical) |

Expected runtime: 2 to 6 hours per sample on 16 cores.

---

## Part 3: understanding the output

Cell Ranger creates an output directory under `sample_A/outs/`:

```
sample_A/outs/
├── web_summary.html                    # Interactive QC report; open this first
├── metrics_summary.csv                 # Key metrics in CSV format
├── filtered_feature_bc_matrix/         # Use this for analysis
│   ├── barcodes.tsv.gz                 # Cell barcodes (one per row)
│   ├── features.tsv.gz                 # Gene names and IDs
│   └── matrix.mtx.gz                  # Sparse count matrix (Market Exchange format)
├── raw_feature_bc_matrix/             # All barcodes (including empty droplets)
├── molecule_info.h5                   # Per-molecule information (for advanced QC)
└── possorted_genome_bam.bam           # Aligned reads (large; needed for re-analysis)
```

### Filtered or raw matrix: which to use?

- *`filtered_feature_bc_matrix/`*. Cell Ranger has applied its cell-calling algorithm
  to remove empty droplets. Use this for most analyses.
- *`raw_feature_bc_matrix/`*. Contains all detected barcodes. Use this if you want
  to apply your own cell-calling (EmptyDrops or CellBender for low-quality samples).

### Key metrics to check in `web_summary.html`

| Metric | Acceptable range | Red flag |
|--------|-----------------|----------|
| Estimated number of cells | As expected by the experiment | Below 500 or far above target input |
| Median genes per cell | 1,000 to 4,000 | Below 500 |
| Sequencing saturation | 40 to 80% | Above 90% (over-sequenced) or below 30% (under-sequenced) |
| Reads mapped confidently to transcriptome | Above 60% | Below 50% |
| Valid barcodes | Above 75% | Below 75% (library quality issue) |

---

## Part 4: STARsolo (an alternative to Cell Ranger)

STARsolo is integrated into STAR 2.7.9a or later and produces the same count matrix format.

### Build a STAR reference

```bash
STAR --runMode genomeGenerate \
  --genomeDir /path/to/star_genome \
  --genomeFastaFiles GRCh38.primary_assembly.genome.fa \
  --sjdbGTFfile gencode.v44.annotation.gtf \
  --runThreadN 16
```

### Run STARsolo for 10x Chromium v3

```bash
STAR --soloType CB_UMI_Simple \
  --soloCBwhitelist 3M-february-2018.txt \
  --soloCBstart 1 --soloCBlen 16 \
  --soloUMIstart 17 --soloUMIlen 12 \
  --genomeDir /path/to/star_genome \
  --readFilesIn R2.fastq.gz R1.fastq.gz \
  --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMattributes NH HI nM AS CR UR CB UB GX GN sS sQ sM \
  --runThreadN 16 \
  --outFileNamePrefix ./starsolo_out/
```

> R2 (cDNA) comes *before* R1 (barcode) in the `--readFilesIn` argument for STARsolo.
> This is the opposite of the intuitive order, and a common source of errors.

The 10x v3 barcode whitelist (`3M-february-2018.txt`) is bundled with Cell Ranger under
`cellranger-X.X.X/lib/python/cellranger/barcodes/`.

---

## Part 5: AI-assisted HPC job script generation

Writing SLURM or PBS submission scripts is tedious and error-prone.
LLMs are good at generating them if you provide the right context.

### Prompt template

```
I need to submit a Cell Ranger count job on a SLURM HPC cluster.

Details:
- Cell Ranger version: 8.0.1, installed at /software/cellranger-8.0.1/
- Reference genome: /data/ref/refdata-gex-GRCh38-2024-A
- FASTQ directory: /scratch/user/project/fastqs/
- Sample name: lung_d3
- I want to use 16 cores and 128 GB RAM
- Maximum walltime on our cluster is 48 hours
- My email is user@university.edu for job notifications
- The output should go to /scratch/user/project/cellranger_out/

Please generate a complete SLURM submission script.
```

<details>
<summary>View Gold Standard Output</summary>

A correct AI-generated script should look like:

```bash
#!/bin/bash
#SBATCH --job-name=cellranger_lung_d3
#SBATCH --output=cellranger_lung_d3_%j.log
#SBATCH --error=cellranger_lung_d3_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=48:00:00
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=user@university.edu

# Load Cell Ranger
export PATH=/software/cellranger-8.0.1:$PATH

# Run Cell Ranger count
cellranger count \
  --id=lung_d3 \
  --transcriptome=/data/ref/refdata-gex-GRCh38-2024-A \
  --fastqs=/scratch/user/project/fastqs/ \
  --sample=lung_d3 \
  --localcores=16 \
  --localmem=120 \
  --output-dir=/scratch/user/project/cellranger_out/
```

What to verify manually:

- `--localmem` is slightly below `--mem` (128 GB to 120 GB) to leave headroom for the OS.
- Check that `--sample` matches the prefix of your actual FASTQ filenames exactly.
- Verify the Cell Ranger path with `which cellranger` after loading.
- For STARsolo, double-check that `readFilesIn` lists R2 before R1.

A common AI mistake to watch for: some LLMs will add `--nosecondary` (which disables
secondary alignment) or `--no-bam` without being asked. These are valid flags but
remove outputs you may need later. Remove them unless you specifically want them.

</details>

---

## Exercise: diagnose a failed Cell Ranger run

The following error appears in your Cell Ranger log:

```
[error] No input FASTQs were found for the sample: lung_d3
Detected FASTQ files in /scratch/user/project/fastqs/:
  lung_d3_1_S1_L001_R1_001.fastq.gz
  lung_d3_1_S1_L001_R2_001.fastq.gz
```

Paste this error into Claude or ChatGPT and ask it to explain the cause and provide the corrected Cell Ranger command.

<details>
<summary>View Gold Standard Output</summary>

Root cause. The FASTQ filenames contain an extra `_1_` segment after the sample name
(`lung_d3_1_S1_L001_R1_001.fastq.gz`). Cell Ranger's `--sample` argument matches
only the prefix before `_S[0-9]`, so `--sample=lung_d3` does not match a file
prefixed `lung_d3_1`.

Fix. Change `--sample=lung_d3` to `--sample=lung_d3_1`, or rename the FASTQs to
remove the extra `_1`.

Correct command:

```bash
cellranger count \
  --id=lung_d3 \
  --transcriptome=/data/ref/refdata-gex-GRCh38-2024-A \
  --fastqs=/scratch/user/project/fastqs/ \
  --sample=lung_d3_1 \
  --localcores=16 \
  --localmem=120
```

If the AI gives this explanation and fix, the answer is correct. If it suggests
`--fastqs` points to the wrong directory, that is a secondary hypothesis. The file
listing in the error confirms the FASTQs are present, so the sample-name mismatch is
the actual issue.

</details>

---

## Self-check

Try to answer before checking. If you miss two, re-read the worked Cell Ranger example.

1. Why use `filtered_feature_bc_matrix/` for analysis instead of `raw_feature_bc_matrix/`? What is the cost of getting this wrong?
2. The `web_summary.html` shows a 65% valid barcode rate, with 5,000 cells expected vs. 28,000 detected. Which number do you trust, and what does the discrepancy suggest?
3. You are choosing between Cell Ranger and STARsolo for a standard 3' gene-expression library. List one consideration that would push you toward each.

<details>
<summary>Self-check answers</summary>

1. The *filtered* matrix has been processed by Cell Ranger's empty-droplet filter (EmptyDrops or knee-point detection), so it contains only barcodes that look like real cells. The *raw* matrix includes every barcode that received any read, usually more than 100,000 of them, and mostly empty droplets. Loading raw into Scanpy and running normalisation or clustering on it produces meaningless results dominated by ambient RNA noise. This is a common silent failure when an AI suggests "load the count matrix" without specifying which one.
2. Trust the detected count, but investigate the discrepancy. 28,000 cells when you expected 5,000 is a five- to six-fold over-detection. That is usually a sign of high ambient RNA inflating the empty-droplet filter, or of an overloaded chip. The 65% valid-barcode rate is a separate concern. Above 90% is healthy, and 65% suggests sequencing or chemistry issues. Both numbers indicate the run needs investigation before proceeding to Scanpy.
3. Cell Ranger: use it if you have an unusual library (VDJ, ATAC, Feature Barcoding), if your collaborators use it (reproducibility), or if you want the canonical web summary. STARsolo: use it if compute is a constraint (much faster), if you want finer control over alignment parameters, or if you're integrating with an existing STAR-based pipeline.

</details>

---

## Key takeaways

1. Cell Ranger is the standard. STARsolo is the fast alternative. Both produce compatible output. Use Cell Ranger if you have an unusual library type (ATAC, VDJ, Feature Barcoding).
2. Always open `web_summary.html` first. Sequencing saturation, valid barcode rate, and median genes per cell will tell you in 30 seconds whether alignment succeeded.
3. Use `filtered_feature_bc_matrix/` for analysis. The raw matrix includes empty droplets.
4. LLMs generate correct HPC scripts if you give them the full context. Always verify `--sample` against actual FASTQ filename prefixes. This is the most common source of Cell Ranger failures.

---

## Next: Module 3, preprocessing and QC in Scanpy

[Open Module 3](../module-03-preprocessing-scanpy/README.md)

*In Module 3, you will load your count matrix into Scanpy in Google Colab, visualize
QC metrics, filter low-quality cells, normalize counts, and select highly variable genes.*
