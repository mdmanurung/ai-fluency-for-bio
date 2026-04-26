# Contributing & Developer Guide

This file is for **course authors and contributors** who need to build or modify the Quarto site.
Learners looking for course materials should start at [README.md](README.md).

## Prerequisites

Requires [Quarto](https://quarto.org/docs/get-started/) version 1.4 or later.
No R or Python environment is required — the site is pure Markdown/QMD.

## Local development

```bash
quarto check     # verify the install
quarto preview   # live preview at http://localhost:4200
quarto render    # build the static site into _site/
```

## Project structure

```
_quarto.yml               # site config, sidebar, theme
index.qmd                 # landing page + schedule
course-*.qmd              # overview, syllabus, support, team, FAQ
404.qmd                   # custom 404
fluency/                  # Track 1: the 4 D's of AI fluency
literacy/                 # Track 2: AI literacy for bio
bioinformatics/           # Track 3: hands-on bioinformatics
weeks/                    # weekly module materials (weeks 1–4)
modules/                  # self-paced learner modules (modules 1–5)
theme.scss, theme-dark.scss
.github/workflows/publish.yml   # GitHub Pages deploy workflow
```

## Deploying to GitHub Pages

The `.github/workflows/publish.yml` workflow renders the site and publishes to the
`gh-pages` branch on every push to `main`.

First-time setup:

1. Push to `main`. The Action will run and create the `gh-pages` branch.
2. In the repo **Settings → Pages**, set source to `Deploy from a branch` → `gh-pages` / `/ (root)`.
3. The site becomes available at `https://mdmanurung.github.io/ai-fluency-for-bio/`.

## Authoring content

Every topical page is scaffolded with headings, learning objectives, and `TODO` markers.
See `PLANS.md` for the current PR backlog and locked architectural decisions.

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless noted otherwise.
