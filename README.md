# AI Fluency for Biology

A [Quarto](https://quarto.org/) course website for a 4-week short course on using AI effectively in biological research. Structured around:

1. **The 4 D's of AI fluency** — Delegation, Description, Discernment, Diligence.
2. **LLM literacy** for bio researchers.
3. **Hands-on bioinformatics** with AI assistants.

Published site: <https://mdmanurung.github.io/ai-fluency-for-bio/> *(enable after first deploy)*.

## Local development

Requires [Quarto](https://quarto.org/docs/get-started/) (≥ 1.4).

```bash
# Install Quarto, then:
quarto check     # verify the install
quarto preview   # live preview at http://localhost:4200
quarto render    # build the static site into _site/
```

No R or Python environment is required — the site is pure markdown.

## Project structure

```
_quarto.yml               # site config, sidebar, theme
index.qmd                 # landing + schedule
course-*.qmd              # overview, syllabus, support, team, FAQ
404.qmd                   # custom 404
fluency/                  # Track 1: the 4 D's
literacy/                 # Track 2: AI literacy for bio
bioinformatics/           # Track 3: hands-on
weeks/                    # 4-week weekly modules
theme.scss, theme-dark.scss
.github/workflows/publish.yml   # GitHub Pages deploy
```

## Deploying to GitHub Pages

The `.github/workflows/publish.yml` workflow renders the site and publishes to the `gh-pages` branch on every push to `main`.

First-time setup:

1. Push to `main`. The Action will run and create the `gh-pages` branch.
2. In the repo **Settings → Pages**, set source to `Deploy from a branch` → `gh-pages` / `/ (root)`.
3. The site becomes available at `https://mdmanurung.github.io/ai-fluency-for-bio/`.

## Authoring content

Every topical and weekly page is scaffolded with headings, learning objectives, and `TODO` markers. Fill them in as you prepare each week.

## License

Content is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless noted otherwise.
