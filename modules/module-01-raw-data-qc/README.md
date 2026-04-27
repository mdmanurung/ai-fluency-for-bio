# Module 1: Introduction to scRNA-seq & Raw Data QC

**Estimated Time to Complete: ~60 mins**

> **Tools needed:** FastQC (local or HPC), Claude or ChatGPT (free web)
> **HPC required?** Yes, for running FastQC on large files. A personal laptop works for the exercises using the provided example reports.

---

## Hook: The Files Have Arrived

The sequencing core emails you a link: 300 GB of `.fastq.gz` files, split across lanes.
Before you touch Cell Ranger, before you think about clustering — you need to answer
one question: **are these reads worth aligning?**

Bad library prep, adapter contamination, low Q-scores, or a failed lane will corrupt
every downstream result. Five minutes of QC here saves days of debugging later.

---

## Part 1: What Is scRNA-seq?

Single-cell RNA sequencing (scRNA-seq) measures gene expression in **individual cells**
rather than averaging across a tissue. This lets you:

- Discover rare cell types that bulk RNA-seq would dilute away
- Map cell states along a differentiation trajectory
- Compare how different conditions shift cell-type composition

### Why 10x Chromium?

10x Genomics Chromium is the dominant scRNA-seq platform. It encapsulates single cells
in droplets (GEMs — Gel Beads in Emulsion), barcodes each cell's RNA with a unique
**cell barcode (CB)**, and tags each RNA molecule with a **Unique Molecular Identifier (UMI)**
to enable accurate counting.

**Key numbers for a standard run:**
- ~500–10,000 cells captured (depending on input)
- ~20,000–50,000 reads per cell
- Median ~1,000–3,000 genes detected per cell

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

- **Cell Barcode:** Identifies which cell the read came from
- **UMI:** Identifies which individual RNA molecule was captured (removes PCR duplicates)

### Read 2 structure (typically 90–150 bp)

Contains the actual cDNA sequence — this is what gets aligned to the reference genome.

> **Key insight for AI prompting:** When asking an LLM to help you interpret a FASTQ
> read, always specify "this is 10x Chromium R1" or "this is R2 cDNA." The read
> structure differs between platforms, and an unspecified prompt will produce a
> generic answer that may not apply.

---

## Part 3: Quality Control with FastQC

FastQC checks the raw reads **before alignment**. For scRNA-seq, the most informative
modules are:

| FastQC Module | What to Look For | Typical scRNA-seq Pattern |
|---------------|-----------------|--------------------------|
| Per-base sequence quality | Q ≥ 30 across positions | R2 may drop at 3′ end — acceptable |
| Per-sequence quality scores | Peak at Q > 35 | Sharp peak = good library |
| Per-base sequence content | First 28 bp of R1 will FAIL | Normal — CB+UMI is not random sequence |
| Sequence duplication levels | High duplication is expected | UMI collapsing handles this downstream |
| Overrepresented sequences | Adapter sequences present? | Flag if > 5% — check trimming |
| Adapter content | Should be low in R2 | High adapter = short inserts |

> **Important:** FastQC was designed for bulk sequencing. The "FAIL" on
> Per-base sequence content for R1 is **not a problem** — it reflects the
> fixed cell barcode structure, not a library quality issue. Always interpret
> FastQC output in the context of your library type.

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

## Part 4: AI-Assisted QC Interpretation

FastQC HTML reports are rich but require interpretation experience.
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

A well-calibrated LLM should explain:

**Expected / ignore:**
- `FAIL Per base sequence content` on R1 — the CB+UMI is a fixed, non-random sequence by design
- `FAIL Sequence duplication levels` on R2 — high duplication is normal in scRNA-seq; UMI deduplication in Cell Ranger / STARsolo corrects for PCR amplification bias
- `WARN Sequence length distribution` — if reads are variable length after trimming, this is expected

**Investigate further:**
- `WARN Per sequence quality scores` — if the peak Q-score is below 28, you may lose significant fractions of reads during alignment; check if the sequencing run had issues
- `WARN Adapter content` on R2 — if adapter percentage is above ~5–10%, your cDNA inserts are short (fragmentation issue or very low input); trimming with Trim Galore or Cutadapt before alignment may help

**Red flags (not present here but worth knowing):**
- `FAIL Overrepresented sequences` on R2 with a rRNA sequence — indicates poor rRNA depletion or no poly-A selection
- `FAIL Per sequence GC content` with a bimodal distribution — possible contamination

</details>

---

## Exercise: Interpreting a FastQC Report with AI

**Scenario:** You have run FastQC on your R2 reads and the report shows:
- Mean Q-score of 32 across all positions
- A sharp drop in quality at the last 10 bp (positions 141–150)
- 3.2% adapter content at the 3′ end
- Sequence duplication level of 78%

Use Claude or ChatGPT to answer: **Is this library acceptable for Cell Ranger alignment? What, if anything, should you do before proceeding?**

Use the prompt template from Part 4, substituting your actual summary.

<details>
<summary>View Gold Standard Output</summary>

**Expected answer from AI (and the correct interpretation):**

This library is **acceptable for alignment without trimming**, with one optional step:

1. **Q32 mean with a 3′ drop** — The quality dip at positions 141–150 is common and will be
   handled by Cell Ranger's built-in read trimming. No action needed.

2. **3.2% adapter content** — Below the 5–10% threshold where adapter trimming becomes
   important. Cell Ranger trims adapters by default. Acceptable as-is.

3. **78% duplication** — This sounds alarming but is **expected** in scRNA-seq.
   UMIs allow Cell Ranger to distinguish true reads from PCR duplicates.
   Duplication rate in FastQC is not a meaningful QC metric for UMI-based libraries.

**Verdict:** Proceed to Cell Ranger. No trimming required.

**If the AI recommends aggressive trimming of all reads due to the quality drop or
duplication rate, that answer is incorrect for UMI-based scRNA-seq** — push back
with: *"This is a UMI-based 10x Chromium library. Does that change your recommendation
about the duplication level?"*

</details>

---

## Key Takeaways

1. **R1 is the barcode read; R2 is the biology.** Always run FastQC on both, but focus your QC interpretation on R2.
2. **Several FastQC "FAIL" flags are normal for 10x data.** Per-base sequence content (R1) and sequence duplication levels are expected failures.
3. **LLMs can interpret FastQC reports accurately — if you specify the platform.** The prompt must include "10x Chromium" and the read type for the answer to be relevant.
4. **MultiQC aggregates across all samples.** Run it on all your FastQC outputs before making any pass/fail decision on a whole experiment.

---

## → Next: Module 2 — Alignment & Count Matrix Generation

[Open Module 2](../module-02-alignment-count-matrix/README.md)

*In Module 2, you will run Cell Ranger or STARsolo to align your reads to a reference
genome and produce the count matrix that all downstream analysis depends on.*
