# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

### Added — branch `claude/course-improvement-feedback-Dc10Y` (open-source / reuse pass)

- **`environment.yml`** + **`requirements.txt`** — pin the full Scanpy + scrublet + leidenalg + igraph + jupyterlab stack at the repo root so self-paced learners can reproduce the hands-on track without dependency drift. Closes the "Commit a pinned environment" item in `PLANS.md` Infrastructure.
- **`.github/workflows/link-check.yml`** — Lychee link-check on push, PR, and a weekly Monday cron. Catches link rot in the URL-heavy further-reading lists across all 12 fluency / literacy / bioinformatics pages.
- **`modules/module-0[3,4,5]-*/notebook.ipynb`** — paired runnable Jupyter notebooks for the three Colab modules (preprocessing, clustering/UMAP, annotation). Generated from the existing README content via `tools/readme_to_ipynb.py`; each module README now has an "Open in Colab" badge at the top resolving to the notebook on `main`.
- **`tools/readme_to_ipynb.py`** — small idempotent helper that converts a module README into a paired notebook (markdown for prose, code cells for `python` blocks). Lets maintainers keep README and notebook in sync by re-running.
- **`reference/glossary.qmd`** — alphabetical glossary covering the AI/LLM and scRNA-seq vocabulary used throughout the course (~30 entries: agent, attention, blast radius, context window, fabrication, RAG, system prompt, temperature, token, tool use, AnnData, count matrix, doublet, FASTQ, GEM-X, HTO, leiden, marker gene, mt fraction, PBMC 3k, UMAP, etc.). Each entry cross-links to the page that introduces it.
- **`reference/prompt-library.qmd`** — fill-in-the-blank prompt templates distilled from each bioinformatics page: debugging (four-part pattern), test writing (`validate_qc_outputs`-style), literature triage (five-step verification), protocol critique mode. Templates link back to the source page for the full worked example.
- **`reference/peer-review.qmd`** — peer-review template that mirrors the four disclosure-rubric dimensions (tools listed, use described, verification stated, rejections noted) plus two open-ended prompts. Tone callout cross-links to `fluency/discernment.qmd` ("name the move that would have caught it, not the person").
- **`_quarto.yml`** — added a "Reference" sidebar section (glossary, prompt library, peer-review template).
- **`course-syllabus.qmd`** — linked the participation/peer-review row to `reference/peer-review.qmd`.
- **`course-team.qmd`, `course-support.qmd`** — added a "course template" callout flagging the page placeholders as fork-and-replace targets, so adopters know they are fork-friendly and not pre-filled for a specific cohort.
- **`weeks/starter-week3-python.qmd`** — Setup section now references `environment.yml` / `requirements.txt` for local installs.
- **`README.md`** — "What you need" references the pinned env files.

### Changed — branch `claude/review-ai-fluency-course-QgsyP` (course merge)

Merge the 5-module scRNA-seq pipeline (PBMC 3k) into the 4-week instructor-led course. The two were previously inconsistent — README and modules described a self-paced FASTQ→UMAP course; the Quarto site described a 4-week AI-fluency course on bulk RNA-seq (GSE96870). After the merge, the course is one coherent thing:

- **`README.md`** — rewritten to describe the merged structure: the 4-week course is primary; modules 1–5 are the concrete scRNA-seq project run alongside the theory tracks. Both Colab (default) and local conda/uv supported. Repo layout section added.
- **`_quarto.yml`** — added "scRNA-seq pipeline (modules)" section to the sidebar (modules 1–5 now linkable from the rendered site). Updated site description and weekly section labels (Week 3 → "scRNA-seq I", Week 4 → "scRNA-seq II").
- **`index.qmd`** — schedule rebuilt to show readings + hands-on + deliverable per week, with module references inlined. Placeholder dates ("Announced before term") replace bare TBDs.
- **`course-overview.qmd`** — practical-track scope and outcome 4 reframed around scRNA-seq; structure section now lists the 5-module project explicitly.
- **`course-syllabus.qmd`** — required-tools changed to Python (Scanpy) primary with Seurat as supported alternative; AI-second baseline scoped to a 25-line PBMC 3k QC sketch; structure table updated to show modules; data policy note updated to PBMC 3k.
- **`weeks/week-3.qmd`** — full rewrite: PBMC 3k as dataset; modules 1–2 as pre-class reading, Module 3 in-class, Module 4 after-class; mini-project deliverable updated to (a) AI-free baseline on PBMC 3k QC, (b) AI-assisted clustering extension, (c) accept/reject log, (d) reproducibility artifact, (e) disclosure.
- **`weeks/week-4.qmd`** — full rewrite: Module 5 walkthrough as the in-class block; capstone explicitly forks into Path A (scRNA-seq analysis), Path B (literature brief), Path C (protocol design), retaining flexibility for non-genomics students; learning objectives callout added.
- **`bioinformatics/data-analysis.qmd`** — full rewrite from R/DESeq2/GSE96870 to Python/Scanpy/PBMC 3k; explicit page-vs-Module-3 differentiation (page = AI-fluency principles; module = runnable procedure); 7-step QC walkthrough with discernment moves named at every step; closing 4 D's callout retained; further reading updated to Wolf 2018 (Scanpy), Heumos 2023 (sc best practices), Wolock 2019 (Scrublet), 10x PBMC 3k docs.
- **`bioinformatics/code-assistance.qmd`** — worked example rewritten from `validate_sample_sheet` (GSE96870 coldata) to `validate_qc_outputs` (PBMC 3k post-QC AnnData); debugging weak/strong example rewritten around the realistic `KeyError: 'mt'` scanpy QC error; R/Seurat note revised to a brief "the workflow transfers" pointer (no longer parallel R path); organism-conventions trap (`MT-` vs. `mt-`) added to common failure modes.
- **`weeks/starter-week3-python.qmd`** — full rewrite for `sc.datasets.pbmc3k()`; load + shape assertion + non-zero-genes-per-cell summary table; install instructions for both Colab (default) and local pip.
- **`weeks/starter-week3-r.qmd`** — **deleted**. R/Seurat parity dropped; students who prefer R can use the Seurat equivalent of the Python starter without instructor scaffolding.
- **`course-team.qmd`, `course-support.qmd`** — bare `TBD` replaced with explicit "to be announced before week 1" placeholders.
- **`fluency/description.qmd`** — worked example rewritten from a postdoc planning a bulk RNA-seq QC script (DESeq2 / `vst` / batch-coloured PCA) to a postdoc planning a PBMC 3k scRNA-seq QC script (Scanpy / mt prefix / QC violins / log-norm). Same five-part Description framework; aligned with the rest of the course.
- **`fluency/diligence.qmd`** — disclosure-statement template example updated from "drafted the DESeq2 scaffold" to "drafted the Scanpy QC scaffold".
- **`PLANS.md`** — superseded callouts on the GSE96870 dataset lock and R/Python parity lock; infrastructure section updated to reference the active branch; nice-to-have updated.

### Added — branch `claude/propose-next-steps-yVScm` (PR-5)

- **`weeks/week-2.qmd`** — full fill: added learning-objectives callout (4 objectives); expanded "In class" into three named blocks (short lecture, 40-min prompt clinic with the 4-step BYO-prompt → diagnose → fix → rerun protocol, 20-min bibliography-cleanup agent demo); added disclosure-statement requirement to deliverable; replaced bare TODO supplementary.
- **`weeks/week-1.qmd` and `weeks/week-4.qmd`** — replaced bare `*TODO.*` Supplementary sections with: *Slides, recording, and notebooks will be posted here after each session.*
- **`literacy/prompting.qmd`** — added Mermaid flowchart diagram of prompt anatomy (system / user / assistant boxes inside a "flat token stream" subgraph, feeding into LLM → completion), placed between the bullet-list anatomy and the explanatory prose.
- **`literacy/how-llms-work.qmd`** — added "Attention in one head: a toy calculation" subsection: 4-token sentence `gene is not expressed`; full Q·K dot-product table, √d_k scaling, exp/softmax table, weighted-V output formula, and explicit teaching note on what the arithmetic does and does not show.

### Added — branch `claude/propose-next-steps-yVScm` (PR-4)

- **`bioinformatics/protocol-design.qmd`** — replaced the worked-example TODO with full content:
  - Five-step sparring-partner workflow elaborated into a realistic scRNA-seq pilot scenario (lung macrophages, influenza A, 3 time points, 6 samples, 10x Chromium GEM-X v4).
  - **AI confidently wrong (×2)**: recommended outdated Chromium v3.1 chemistry (current kit is GEM-X v4, CG000731, with different loading parameters); recommended 10,000 cells/reaction (inappropriate for large primary macrophages; correct range 5,000–7,000).
  - **AI usefully right**: critique-mode pass identified HTO hashtag multiplexing, which halves capture reactions, reduces batch effects, and enables doublet detection — a genuine improvement the postdoc had not planned.
  - Reconciliation table documenting each change, its source (human vs. AI), and rationale.
  - Closing 4 D's callout (Description, Delegation, Discernment, Diligence).
  - Common failure modes section: treating draft as protocol, accepting version numbers at face value, skipping critique pass.
  - 3 verified citations: Boiko et al. 2023 (*Nature*), Begley & Ellis 2012 (*Nature*), 10x GEM-X v4 user guide URL.

### Added — branch `claude/propose-next-steps-yVScm` (PR-3)

- **`bioinformatics/literature-review.qmd`** — replaced both TODOs with full content:
  - Five-step verification workflow (copy DOI → resolve via doi.org → check title/authors → verify on-topic via PubMed → incorporate; ~3 min/citation budget).
  - Worked example: "spatial transcriptomics in the tumor microenvironment" triage with explicit verification log across two tools. Shows one caught fabrication — a DOI that resolved to a real paper in an unrelated field — and explains why that is the most dangerous hallucination type.
  - Switched-tool comparison: base LLM (2/5 fabricated) vs. Elicit grounded search (0/3 fabricated, but summaries still require verification).
  - Step 3: AI for structured extraction from papers you already hold.
  - Closing 4 D's callout mapping Description / Discernment / Delegation / Diligence.
  - Common failure modes section: the DOI-resolves-wrong trap, unconditional grounded-tool trust, outsourcing synthesis.
  - 2 verified citations (Walters & Wilder 2023 *Scientific Reports*, Kay et al. 2024 AAAI/ACM AIES) plus internal cross-reference to `fluency/discernment.qmd`.

### Added — branch `claude/propose-next-steps-yVScm` (PR-2)

- **`bioinformatics/code-assistance.qmd`** — replaced both TODOs with full content:
  - Expanded "Debugging with AI" section with a four-part pattern (full traceback + minimal failing code + intent paragraph + environment) and a side-by-side weak/strong prompt illustration using the GSE96870 KeyError scenario.
  - Worked example: AI-assisted test writing for `validate_sample_sheet` in Python (pandas + pytest), continuing the GSE96870 grad-student persona. Shows three steps — write the contract yourself, ask AI for pytest bodies, prune brittle provenance tests and add the level-typo test AI missed.
  - R equivalent note pointing at `testthat`.
  - Closing 4 D's callout mapping Description / Delegation / Discernment / Diligence onto the worked example.
  - Common failure modes section: contract delegation, package hallucination, stale API signatures.
  - 2 verified citations added (Peng et al. 2023, Spracklen et al. 2024) plus internal cross-reference to `fluency/description.qmd`.

### Added — branch `claude/course-next-steps-fCxoV` (PR-1)

- **`bioinformatics/data-analysis.qmd`** — replaced TODO worked example with a six-step QC walkthrough on the GSE96870 cerebellum subset (sample sheet → library size → vst transform → PCA → correlation heatmap → outlier decision). Each step names the AI's role and the human's discernment move; closing callout maps onto Description / Discernment / Diligence / Delegation. Added 4 verified citations (Love et al. 2014, Conesa et al. 2016, Blackmore et al. 2017, Carpentries bioc-rnaseq).
- **`weeks/starter-week3-r.qmd`, `weeks/starter-week3-python.qmd`** — new starter notebooks. Scope deliberately narrow (load + confirm shape + one summary table) so they do not short-circuit the AI-free baseline that the week 3 mini-project requires.
- **`weeks/week-3.qmd`** — added Course dataset section pointing at the starters; replaced TODO Supplementary section with concrete links.

### Added — branch `claude/setup-gh-pages-course-tJTne`

- **`literacy/how-llms-work.qmd`** — replaced TODO with a working-level explainer of next-token prediction, tokenisation, the transformer attention mechanism, temperature, and context windows.
- **`literacy/prompting.qmd`** — filled three stubs:
  - Anatomy-of-a-prompt section: system prompt / user prompt / assistant turns with explanatory prose.
  - Worked example: weak → strong prompt progression for structured extraction from methods sections, including a JSON schema pattern and an iteration-log workflow.
  - Further reading: 4 references (Anthropic prompt-engineering docs, Wei et al. chain-of-thought, Brown et al. GPT-3 few-shot, Schulhoff et al. prompt report).
- **`literacy/tool-use-and-agents.qmd`** — filled two stubs:
  - Worked example: bibliography-cleanup agent loop (read → lookup → propose → human-confirm → write), with analysis of why the confirm gate is the critical design decision.
  - Further reading: 4 references (Anthropic building-effective-agents, Weng agent blog post, Yao et al. ReAct, Ruan et al. agent risk sandbox).
- **`literacy/ethics-and-limits.qmd`** — filled authorship & attribution TODO with the three convergent publisher positions as of early 2026 (AI cannot be an author; use must be disclosed; verbatim text must be marked), plus a callout to verify policies before each use.

---

## [0.4.0] — 2026-04-24 (PR #4, merged to `claude/setup-gh-pages-course-tJTne`)

### Added

- **`fluency/diligence.qmd`** — expanded disclosure norms with a policy-comparison table and a reusable disclosure-statement template; added further reading.
- **`fluency/discernment.qmd`** — expanded verification checklist with step-by-step guidance; added further reading.
- **`fluency/description.qmd`** — added RNA-seq QC before/after worked example; added further reading.
- **`fluency/delegation.qmd`** — expanded delegation rubric with quadrant explanations; added BLAST batch-scripting worked example; added further reading.

---

## [0.3.0] — 2026-04-24 (PR #3, merged to `main` via `claude/quarto-ai-course-site-70lTB`)

### Changed

- Revised syllabus and supporting pages following a multi-persona audit (student, instructor, external reviewer perspectives).

---

## [0.2.0] — 2026-04-24 (PR #2, merged to `main` via `claude/quarto-ai-course-site-70lTB`)

### Added

- Full Quarto site scaffold: `_quarto.yml`, `index.qmd`, `course-*.qmd`, `404.qmd`, `theme.scss`, `theme-dark.scss`, `.nojekyll`.
- Stub pages for all three tracks: `fluency/`, `literacy/`, `bioinformatics/`.
- Weekly module stubs: `weeks/week-1.qmd` through `week-4.qmd`.
- GitHub Actions workflow: `.github/workflows/publish.yml` (Quarto → `gh-pages` branch on push to `main`).

---

## [0.1.0] — Initial commit

- Repository initialised with `README.md` and project structure.
