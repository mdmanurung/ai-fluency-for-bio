# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased]

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
