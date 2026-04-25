# Plans

Tracked next steps for the course site. Items are ordered by priority within each section.

---

## Content — immediate

These are the remaining stub pages that must be filled before the site is usable as a course.

### Track 3: Hands-on bioinformatics (`bioinformatics/`)

- [ ] **`code-assistance.qmd`** — expand the debugging section: show the full pattern of pasting error + failing code + one-paragraph intent description; add a worked example of AI-assisted test-writing for a bioinformatics script; add further reading.
- [ ] **`data-analysis.qmd`** — fill the RNA-seq worked example: sample sheet construction → library-size checks → PCA → outlier flagging, with the AI's role explicitly called out at each step; add further reading.
- [ ] **`literature-review.qmd`** — expand citation-verification guidance (confirm every cited paper via PubMed/DOI before incorporating); fill the AI-assisted triage worked example with explicit verification at each hand-off step; add further reading.
- [ ] **`protocol-design.qmd`** — fill the worked example: realistic iteration cycle for designing a small pilot study using AI to surface design considerations, with a human-review gate before any decision is finalised; add further reading.

### Weekly materials (`weeks/`)

- [ ] **`week-1.qmd`** — add links to slides, recording, and demo notebooks once materials exist.
- [ ] **`week-2.qmd`** — fully stubbed; fill with session outline, readings, and exercises for the LLM literacy week.
- [ ] **`week-3.qmd`** — add dataset link (see infrastructure below), starter repo, and baseline analysis stub for the hands-on bioinformatics I session.
- [ ] **`week-4.qmd`** — fully stubbed; fill with session outline for hands-on bioinformatics II.

---

## Infrastructure

- [ ] **Enable GitHub Pages** — go to repo Settings → Pages, set source to `Deploy from a branch` → `gh-pages` / `/ (root)`. The workflow (`.github/workflows/publish.yml`) is already in place; this one-click step triggers the first deployment to `https://mdmanurung.github.io/ai-fluency-for-bio/`.
- [ ] **Merge `claude/setup-gh-pages-course-tJTne` → `main`** — the CI workflow only deploys on push to `main`; all content added since PR #2 is not yet live.

---

## Nice-to-have

- [ ] **Diagrams for literacy pages** — `images/` is currently empty. Two diagrams would materially strengthen weak spots: (1) a transformer attention schematic for `how-llms-work.qmd`; (2) a system/user/assistant prompt anatomy diagram for `prompting.qmd`.
- [ ] **Pin a public dataset for weeks 3–4** — a small, permissively licensed GEO RNA-seq dataset (e.g., GSE96870, Homo sapiens, ~6 samples) would make the hands-on materials fully self-contained without requiring students to locate their own data.
- [ ] **Starter analysis notebook** — a minimal Quarto notebook (R or Python) that loads the week-3 dataset, runs library-size and PCA checks, and flags outliers. Serves as the hands-on scaffold for week 3.
- [ ] **404 page polish** — `404.qmd` exists but may benefit from a navigation prompt back to the course home once all sections are live.

---

## Done

- [x] Quarto site scaffold with full sidebar, theme, and CI workflow (PR #2)
- [x] Multi-persona audit and syllabus revision (PR #3)
- [x] Fluency track: all 4 pages filled — Delegation, Description, Discernment, Diligence (PR #4)
- [x] Literacy track: all 4 pages filled — How LLMs work, Prompting, Tool use & agents, Ethics & limits
