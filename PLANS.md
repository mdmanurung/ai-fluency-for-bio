# Plans

Tracked next steps for the course site. **If you are a fresh Claude session, read "Locked decisions" first** — those choices look like preferences but are non-trivial to undo.

::: {.callout-warning}
## Pivot to scRNA-seq merged into the 4-week course (April 2026)

The course was restructured to merge the 5-module scRNA-seq pipeline (PBMC 3k) into the 4-week instructor-led structure. As a result, the GSE96870 bulk-RNA-seq lock and the R/Python parity decision below are **superseded**. The active dataset is 10x PBMC 3k (loaded by `sc.datasets.pbmc3k()`); the active hands-on language is Python (Scanpy). R/Seurat is supported as a student preference, not a course-default parallel path.

The historical lock entries below are kept for context — they explain why the bioinformatics pages and starter notebooks looked the way they did before the merge — and to make the change visible.
:::

---

## Locked decisions (do not re-litigate)

### Course dataset for weeks 3–4 *(superseded April 2026 — see callout above)*

~~**GSE96870 cerebellum subset (22 mouse cerebellum samples).**~~ Superseded by **10x PBMC 3k** (≈2,700 PBMCs from a healthy donor, 10x Chromium v1, bundled in Scanpy as `sc.datasets.pbmc3k()`). The PBMC 3k dataset is the spine of Modules 3–5 and is now the spine of the week 3 mini-project and the Path-A capstone.

### Language allocation across the bioinformatics track *(partially superseded April 2026)*

Pre-pivot intent was R/Python parity:

- `bioinformatics/data-analysis.qmd` — was R (DESeq2 + tidyverse). **Now Python (Scanpy + PBMC 3k).**
- `bioinformatics/code-assistance.qmd` — Python (validate function + pytest). Worked example **rewritten** from `validate_sample_sheet` (GSE96870) to `validate_qc_outputs` (PBMC 3k AnnData).
- `bioinformatics/literature-review.qmd` — language-agnostic (no code). Unchanged.
- `bioinformatics/protocol-design.qmd` — language-agnostic (wet-lab). Unchanged (still scRNA-seq pilot worked example, which now matches the rest of the course).

R/Seurat is a supported alternative for students who prefer it; the course default for instructor-led demos and the modules is Python.

### Worked-example personas (continuity across pages)

- `data-analysis.qmd` (Python) and `code-assistance.qmd` (Python): graduate student running QC on PBMC 3k.
- `protocol-design.qmd`: postdoc planning a small scRNA-seq pilot. *(Already aligned.)*
- `literature-review.qmd`: graduate student scoping "spatial transcriptomics in the tumor microenvironment." *(Already aligned.)*

### Audit corrections (carry into every PR)

- **A4 — starter notebook scope.** Starters must NOT do the QC analysis. Scope: load + confirm shape + one summary table. Otherwise students copy from the starter into their AI-free baseline and short-circuit the week 3 mini-project. PR-1 starters honour this; future starters must too.
- **A5 — citation verification.** No further-reading list ships unverified. Use WebSearch / WebFetch to confirm each cited paper before merging. Flag any uncertain citation with `<!-- VERIFY -->` rather than risk fabrication.
- **A6 — transformer diagram dropped.** PR-5 was originally to add a transformer-architecture schematic; that was replaced (in plan) with a worked numerical attention-weights example in prose in `literacy/how-llms-work.qmd`. The prompt-anatomy diagram in `literacy/prompting.qmd` is still planned (Mermaid).

### Page depth and structure target

- ~80–110 lines, matching `fluency/description.qmd` (the reference for tone and depth).
- Preserve existing scaffold: Learning objectives → Where AI helps most/least → A workflow → Worked example → Common failure modes → Exercises → Further reading.
- Each bioinformatics page maps onto **at least 2 of the 4 D's** explicitly. A closing callout works well — see `bioinformatics/data-analysis.qmd` for the pattern.
- Further reading: 3–4 verified citations with one-sentence relevance notes each.

### PR sequencing

5 PRs total, one per major chunk. Each independently mergeable.

- **PR-1** — done. Branch `claude/course-next-steps-fCxoV`, commit `a2470c4`.
- **PR-2** — done. Branch `claude/propose-next-steps-yVScm`.
- **PR-3** — done. Branch `claude/propose-next-steps-yVScm`.
- **PR-4** — done. Branch `claude/propose-next-steps-yVScm`.
- **PR-5** — done. Branch `claude/propose-next-steps-yVScm`.

---

## Active PRs

### PR-2 — `bioinformatics/code-assistance.qmd` (Python worked example)

Branch suggestion: `claude/code-assistance-fill-XXXXX`.

Scope:

- Replace the `## Debugging with AI` TODO with a full pattern: paste full error → minimal failing code → one-paragraph intent → environment + package versions. Show the same bug debugged with and without that pattern, and explain *why* the pattern wins.
- Add an AI-assisted test-writing worked example: a small `validate_sample_sheet()` Python function for the GSE96870 coldata CSV (checks expected columns, factor-level coverage, sample order vs counts header). The AI proposes pytest test cases; the human prunes / extends. Frame as Discernment (rejecting redundant tests) + Diligence (owning the contract).
- One-paragraph "R equivalent" note pointing at `testthat`.
- Closing 4 D's callout (mirroring `data-analysis.qmd`).
- Further reading: 3–4 verified citations. Candidates to verify:
  - Peng et al. (2023) GitHub Copilot productivity study.
  - One paper on LLM code hallucination / package fabrication (Lanyado et al.'s "package hallucination" paper is one option — verify).
  - Anthropic Claude Code or related code-assistant docs.
  - Internal link back to `fluency/description.qmd`.

Continuity: reuse the GSE96870 grad-student persona from PR-1's `data-analysis.qmd`.

### PR-3 — `bioinformatics/literature-review.qmd`

Branch suggestion: `claude/literature-review-fill-XXXXX`.

Scope:

- Replace the `## A verification workflow` TODO with a numbered procedure: copy DOI from AI output → resolve via doi.org → confirm title + authors match what the AI claimed → check PubMed for the abstract → only then incorporate. Include a budget guideline (~3 minutes per citation; refuse to cite if it cannot be verified).
- Replace the worked-example TODO ("scoping a review on spatial transcriptomics in the tumor microenvironment") with an explicit verification log at each hand-off step. Show **one fabrication caught in the act** (a plausible-looking citation that resolves to a real DOI but a *different* paper, or a DOI that does not resolve at all) and explain how it was caught.
- Closing 4 D's callout — Description (framing the search) and Discernment (verification) land hardest here.
- Further reading: 3–4 verified citations. Candidates:
  - A recent paper on LLM citation fabrication rates (verify; the Bhattacharyya et al. and Walters & Wilder papers are candidates).
  - Kay et al. 2024 epistemic injustice (already cited in syllabus).
  - Elicit or Consensus methods/whitepaper if one exists.
  - A grounded-vs-ungrounded RAG reference.

### PR-4 — `bioinformatics/protocol-design.qmd`

Branch suggestion: `claude/protocol-design-fill-XXXXX`.

Scope:

- Replace the `## Worked example: designing an scRNA-seq pilot` TODO with: scientific question → AI-drafted protocol given constraints → human critique against tacit lab knowledge → AI critique-mode pass for missing controls → reconcile and document. Show **at least one place the AI was confidently wrong** (e.g., suggested an outdated 10x chemistry version, wrong cell-loading concentration, or a deprecated reagent) and **one place it was usefully right** (e.g., a control the student forgot).
- Make the 4 D's mapping explicit; the existing learning objectives already require it ("Apply the 4 D's to protocol design").
- Further reading: 3–4 verified citations. Candidates:
  - A recent review of AI for experimental design in biology.
  - Boiko et al. 2023 (chemistry, already in syllabus — useful as analogy).
  - A paper on protocol reproducibility (Begley & Ellis 2012 is a classic but check fit).
  - 10x Genomics or equivalent vendor protocol page (verify URL is current).

### PR-5 — Weekly cleanup, prompt-anatomy diagram, attention example

Branch suggestion: `claude/weeks-and-diagrams-XXXXX`.

Scope:

- **`weeks/week-2.qmd`** — full fill (currently 34 lines). Add learning-objectives callout matching other weeks. Expand "In class" with a concrete prompt-clinic protocol (BYO prompt → diagnose → fix → rerun) and reuse the bibliography-cleanup agent demo from `literacy/tool-use-and-agents.qmd` (do not invent a new one). Add the disclosure-statement requirement to the deliverable.
- **`weeks/week-1.qmd` and `weeks/week-4.qmd`** — replace bare `*TODO*` Supplementary section with: *Slides, recording, and notebooks will be posted here after each session.* (Same pattern PR-1 used for week-3.)
- **`literacy/prompting.qmd`** — add a Mermaid diagram for prompt anatomy (system / user / assistant boxes with arrows + annotations). Embed near the existing anatomy section. Quarto renders Mermaid natively.
- **`literacy/how-llms-work.qmd`** — add a worked numerical attention example: 4-token toy sentence; show Q/K/V dot products and softmax weights for one head, by hand, with arithmetic visible. This replaces the originally planned transformer schematic (see audit point A6).
- Update `PLANS.md` and `CHANGELOG.md` to reflect everything shipped in PR-2 through PR-5; mark all four PRs Done.

---

## Infrastructure

- [ ] **Enable GitHub Pages** — Settings → Pages, set source to `Deploy from a branch` → `gh-pages` / `/ (root)`. The workflow (`.github/workflows/publish.yml`) is already in place; this one-click step triggers the first deployment to `https://mdmanurung.github.io/ai-fluency-for-bio/`.
- [ ] **Merge the merged-course branch → `main`** — work for the merge sits on `claude/review-ai-fluency-course-QgsyP`. The publish workflow only fires on push to `main`, so nothing is live until that PR merges.
- [ ] **Commit a pinned environment** — the syllabus offers `conda` / `uv` as a local alternative to Colab. Adding an `environment.yml` (Scanpy + scrublet + leidenalg + matplotlib + pandas) makes that alternative reproducible.

---

## Nice-to-have

- [ ] **404 page polish** — `404.qmd` exists but may benefit from a navigation prompt back to the course home once all sections are live.
- [ ] **Pre-built count matrix for Module 3 fallback** — if a student does Module 1–2 on their own data instead of skipping to PBMC 3k, a small public `.h5ad` (e.g., a public 10x mouse lung subset) staged in a GitHub release would give them a second teaching dataset. Currently optional.

---

## Done

- [x] **PR-5** (branch `claude/propose-next-steps-yVScm`): weekly cleanup + literacy diagrams — week-2.qmd fully filled (learning objectives, prompt-clinic protocol, disclosure requirement); week-1 & week-4 supplementary placeholders added; Mermaid prompt-anatomy diagram in prompting.qmd; worked numerical attention example (Q/K dot products, softmax, weighted V output) in how-llms-work.qmd.
- [x] **PR-4** (branch `claude/propose-next-steps-yVScm`): `bioinformatics/protocol-design.qmd` fully filled — scRNA-seq lung macrophage pilot worked example; AI wrong on chemistry version (v3.1 vs GEM-X v4) and cell loading (10k vs 5–7k for large cells); AI right on HTO multiplexing; reconciliation table; closing 4 D's callout; 3 verified citations (Boiko et al. 2023, Begley & Ellis 2012, 10x GEM-X v4 user guide).
- [x] **PR-3** (branch `claude/propose-next-steps-yVScm`): `bioinformatics/literature-review.qmd` fully filled — five-step verification workflow with 3-min/citation budget, spatial-transcriptomics worked example with explicit verification log showing one caught fabrication (DOI resolves to wrong paper), base-LLM vs. Elicit comparison, closing 4 D's callout, Common failure modes, 2 verified citations (Walters & Wilder 2023, Kay et al. 2024).
- [x] **PR-2** (branch `claude/propose-next-steps-yVScm`): `bioinformatics/code-assistance.qmd` fully filled — four-part debugging pattern with weak/strong prompt comparison, `validate_sample_sheet` pytest worked example with Discernment pruning step, R/testthat equivalent note, closing 4 D's callout, Common failure modes section, 2 verified citations (Peng et al. 2023, Spracklen et al. 2024).
- [x] **PR-1** (commit `a2470c4`, branch `claude/course-next-steps-fCxoV`): GSE96870 dataset pinned and verified; `bioinformatics/data-analysis.qmd` worked example filled with 4 verified citations; R + Python starter notebooks added (scope: load + shape + summary table only); `weeks/week-3.qmd` Course dataset and Supplementary sections updated.
- [x] Quarto site scaffold with full sidebar, theme, and CI workflow (PR #2)
- [x] Multi-persona audit and syllabus revision (PR #3)
- [x] Fluency track: all 4 pages filled — Delegation, Description, Discernment, Diligence (PR #4)
- [x] Literacy track: all 4 pages filled — How LLMs work, Prompting, Tool use & agents, Ethics & limits
