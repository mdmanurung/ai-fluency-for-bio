# Module 1: Introduction to scRNA-seq and raw data QC

Estimated time to complete: 60 mins.

> Tools needed: FastQC (local or HPC), Claude or ChatGPT (free web)
> HPC required? Yes, for running FastQC on large files. A personal laptop works for the exercises using the provided example reports.

---

## Hook: the files have arrived

The sequencing core emails you a link: 300 GB of `.fastq.gz` files, split across lanes.
Before you touch Cell Ranger, before you think about clustering, you need to answer
one question. Are these reads worth aligning?

Bad library prep, adapter contamination, low Q-scores, or a failed lane will corrupt
every downstream result. Five minutes of QC here saves days of debugging later.

---

## Part 1: what is scRNA-seq?

Single-cell RNA sequencing (scRNA-seq) measures gene expression in *individual cells*
rather than averaging across a tissue. This lets you:

- Discover rare cell types that bulk RNA-seq would dilute away.
- Map cell states along a differentiation trajectory.
- Compare how different conditions shift cell-type composition.

### Why 10x Chromium?

10x Genomics Chromium is the dominant scRNA-seq platform. It encapsulates single cells
in droplets (GEMs, or Gel Beads in Emulsion), barcodes each cell's RNA with a unique
*cell barcode (CB)*, and tags each RNA molecule with a *unique molecular identifier (UMI)*
to enable accurate counting.

Key numbers for a standard run:

- 500 to 10,000 cells captured (depending on input).
- 20,000 to 50,000 reads per cell.
- A median of 1,000 to 3,000 genes detected per cell.

---

## Part 2: Anatomy of a 10x FASTQ File

A typical 10x output contains paired FASTQ files per lane:

```
sample_S1_L001_R1_001.fastq.gz   # Read 1: Cell Barcode + UMI
sample_S1_L001_R2_001.fastq.gz   # Read 2: cDNA insert (gene expression)
sample_S1_L001_I1_001.fastq.gz   # Index 1: Sample index (for demultiplexing)
```

### Read 1 structure (28 bp for 10x Chromium v3)

```
|------- 16 bp --------|--- 12 bp ---|
   Cell Barcode (CB)       UMI
```

- *Cell barcode*: identifies which cell the read came from.
- *UMI*: identifies which individual RNA molecule was captured (removes PCR duplicates).

### Read 2 structure (typically 90 to 150 bp)

Contains the actual cDNA sequence. This is what gets aligned to the reference genome.

> When asking an LLM to help you interpret a FASTQ read, always specify "this is 10x
> Chromium R1" or "this is R2 cDNA". The read structure differs between platforms, and
> an unspecified prompt will produce a generic answer that may not apply.

---

## Part 3: quality control with FastQC

FastQC checks the raw reads *before alignment*. For scRNA-seq, the most informative
modules are:

| FastQC module | What to look for | Typical scRNA-seq pattern |
|---------------|-----------------|--------------------------|
| Per-base sequence quality | Q at least 30 across positions | R2 may drop at the 3′ end (acceptable) |
| Per-sequence quality scores | Peak at Q above 35 | A sharp peak means a good library |
| Per-base sequence content | First 28 bp of R1 will FAIL | Normal: CB plus UMI is not random sequence |
| Sequence duplication levels | High duplication is expected | UMI collapsing handles this downstream |
| Overrepresented sequences | Adapter sequences present? | Flag if above 5%; check trimming |
| Adapter content | Should be low in R2 | High adapter means short inserts |

> FastQC was designed for bulk sequencing. The "FAIL" on per-base sequence content for
> R1 is *not a problem*. It reflects the fixed cell barcode structure, not a library
> quality issue. Always interpret FastQC output in the context of your library type.

### Running FastQC

```bash
# Single file
fastqc sample_S1_L001_R2_001.fastq.gz -o ./fastqc_output/

# All files in parallel (HPC recommended for large datasets)
fastqc *.fastq.gz -t 8 -o ./fastqc_output/

# Aggregate multiple samples with MultiQC
multiqc ./fastqc_output/ -o ./multiqc_output/
```

---

## Part 4: AI-assisted QC interpretation

FastQC HTML reports are rich but need interpretation experience.
LLMs are good at explaining what a specific pattern means and suggesting next steps.

### Prompt template for FastQC interpretation

```
I am analyzing a 10x Chromium single-cell RNA-seq library.
Here is the summary status table from my FastQC report for Read 2 (cDNA read):

PASS  Basic Statistics
PASS  Per base sequence quality
WARN  Per sequence quality scores
FAIL  Per base sequence content
PASS  Per sequence GC content
PASS  Per base N content
WARN  Sequence length distribution
FAIL  Sequence duplication levels
PASS  Overrepresented sequences
WARN  Adapter content

Please explain each WARNING and FAIL result in the context of 10x scRNA-seq data,
indicate which ones are expected vs. which ones I should investigate further,
and suggest any remediation steps if needed.
```

<details>
<summary>View Gold Standard Output</summary>

A well-calibrated LLM should explain the following.

Expected, ignore:

- `FAIL Per base sequence content` on R1. The CB plus UMI is a fixed, non-random sequence by design.
- `FAIL Sequence duplication levels` on R2. High duplication is normal in scRNA-seq. UMI deduplication in Cell Ranger or STARsolo corrects for PCR amplification bias.
- `WARN Sequence length distribution`. If reads are variable length after trimming, this is expected.

Investigate further:

- `WARN Per sequence quality scores`. If the peak Q-score is below 28, you may lose significant fractions of reads during alignment. Check if the sequencing run had issues.
- `WARN Adapter content` on R2. If adapter percentage is above 5 to 10%, your cDNA inserts are short (a fragmentation issue or very low input). Trimming with Trim Galore or Cutadapt before alignment may help.

Red flags (not present here but worth knowing):

- `FAIL Overrepresented sequences` on R2 with an rRNA sequence. This indicates poor rRNA depletion or no poly-A selection.
- `FAIL Per sequence GC content` with a bimodal distribution. Possible contamination.

</details>

---

## Exercise: interpreting a FastQC report with AI

Scenario. You have run FastQC on your R2 reads and the report shows:

- A mean Q-score of 32 across all positions.
- A sharp drop in quality at the last 10 bp (positions 141 to 150).
- 3.2% adapter content at the 3′ end.
- A sequence duplication level of 78%.

Use Claude or ChatGPT to answer: is this library acceptable for Cell Ranger alignment? What, if anything, should you do before proceeding?

Use the prompt template from Part 4, substituting your actual summary.

<details>
<summary>View Gold Standard Output</summary>

The expected answer from AI (and the correct interpretation):

This library is acceptable for alignment without trimming, with one optional step.

1. *Q32 mean with a 3′ drop.* The quality dip at positions 141 to 150 is common and will
   be handled by Cell Ranger's built-in read trimming. No action needed.

2. *3.2% adapter content.* Below the 5 to 10% threshold where adapter trimming becomes
   important. Cell Ranger trims adapters by default. Acceptable as-is.

3. *78% duplication.* This sounds alarming, but is expected in scRNA-seq. UMIs let Cell
   Ranger distinguish true reads from PCR duplicates. Duplication rate in FastQC is not
   a meaningful QC metric for UMI-based libraries.

Verdict: proceed to Cell Ranger. No trimming required.

If the AI recommends aggressive trimming of all reads due to the quality drop or
duplication rate, that answer is incorrect for UMI-based scRNA-seq. Push back with:
*"This is a UMI-based 10x Chromium library. Does that change your recommendation about
the duplication level?"*

</details>

---

## Self-check

Try to answer before checking. If you miss two, re-read the worked example.

1. You see "FAIL" on per-base sequence content for R1 in a 10x Chromium dataset. Should you act on this flag? Why or why not?
2. The AI suggests trimming all reads aggressively because of high duplication. What is wrong with this advice for a UMI-based library?
3. Why is R2 the focus of QC interpretation rather than R1, and what would change for a non-UMI bulk RNA-seq library?

<details>
<summary>Self-check answers</summary>

1. Don't act. R1 is the cell barcode plus UMI for 10x Chromium. The first 16 bp are barcode and the next 10 to 12 bp are UMI, both with non-uniform composition by design. FastQC's "FAIL" is a false positive. The per-base content of a barcode read is not informative.
2. UMIs let Cell Ranger collapse PCR duplicates downstream. High raw duplication is expected in a UMI library because the same cDNA molecule is sequenced many times to confirm the UMI. The duplicates are the signal. Trimming for this reason throws away real reads.
3. R2 carries the cDNA sequence. That is the biology. R1 is structural (barcode plus UMI). For non-UMI bulk RNA-seq, both reads are biology (paired-end), so per-base composition and duplication on either read are interpretable normally.

</details>

---

## Key takeaways

1. R1 is the barcode read. R2 is the biology. Always run FastQC on both, but focus your QC interpretation on R2.
2. Several FastQC "FAIL" flags are normal for 10x data. Per-base sequence content (R1) and sequence duplication levels are expected failures.
3. LLMs can interpret FastQC reports accurately, if you specify the platform. The prompt must include "10x Chromium" and the read type for the answer to be relevant.
4. MultiQC aggregates across all samples. Run it on all your FastQC outputs before making any pass-or-fail decision on a whole experiment.

---

## Next: Module 2, alignment and count matrix generation

[Open Module 2](../module-02-alignment-count-matrix/README.md)

*In Module 2, you will run Cell Ranger or STARsolo to align your reads to a reference
genome and produce the count matrix that all downstream analysis depends on.*
