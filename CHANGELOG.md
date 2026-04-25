# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Unreleased] — branch `claude/setup-gh-pages-course-tJTne`

### Added

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
