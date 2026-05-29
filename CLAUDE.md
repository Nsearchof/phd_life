# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repository.

## What this repo is

`phd_life` is the working home for a **theoretical + experimental physics PhD**. It is mostly **Markdown** — research notes, literature cite-cards, planning docs — plus a small amount of **Python tooling** (bibliography + Gantt generation). It is not an application; "does it build" is not the quality bar. Quality is measured by whether the research notes are correct, the citations are real, and the schedule reflects reality.

The repo doubles as an **Obsidian vault** (`.obsidian/` is checked in). Cross-references between notes use Obsidian **wikilinks** (`[[cite_key]]`, `[[note-name#anchor]]`), not relative URLs.

## Python: always via `uv`

All scripts run from the repo root through `uv`:

```bash
uv sync                                   # install deps into .venv/
uv run python <path/to/script.py> [--dry-run] …
```

Never invoke bare `python`/`pip`. The only dependency is `pyyaml` (the tooling reads YAML frontmatter and `schedule.yaml`); don't add top-level deps without noting it in the commit/PR.

## Repository structure

```
.dev/
├── research/{brief,STATE}.md            # current research brief + dated state log
└── tasks/<n>-<slug>.md                  # one file per GitHub issue / task
Literature/
├── Bibliography/                        # ⭐ the cite source-of-truth
│   ├── README.md                        # cite-key + YAML schema + tag taxonomy
│   ├── _template_bib_note.md
│   ├── {Primary,Secondary}/<cite_key>.md
│   ├── scaffold_bib_note.py             # new stub (+ optional --from-doi Crossref autofill)
│   └── build_bibtex.py                  # YAML → bibliography.bib (gitignored; regenerable)
├── Papers/                              # PDFs — two-tier git policy (see .gitignore)
└── Reading_Notes/<cite_key>.md          # reading notes, wikilinked to the cite-card
Research/
├── Theory/                              # derivations + symbolic/analytic notes
└── Experiments/<date>_<slug>.md         # lab-notebook entries (one per run)
Planning/
├── schedule.yaml                        # source-of-truth timeline
├── build_gantt.py                       # schedule.yaml → Mermaid Gantt
├── GANTT.md                             # generated — do NOT hand-edit; rerun build_gantt.py
├── milestones.md                        # committee/program milestones
└── deliverables.md                      # papers, talks, chapters, datasets
```

## Bibliography conventions

Every source cited anywhere in the repo traces to one YAML-frontmatter file under `Literature/Bibliography/{Primary,Secondary}/`. Full spec in [`Literature/Bibliography/README.md`](Literature/Bibliography/README.md). Key rules:

- **Cite-key**: `firstauthor + year + slug`, lowercase snake-case, globally unique (e.g. `dirac1928_quantum_electron`). Wikilink with the bare key: `[[dirac1928_quantum_electron]]`.
- **Never invent a citation.** Every cite-key referenced in a research note must correspond to an existing file under `Bibliography/`. If it doesn't exist yet, scaffold the stub first (`scaffold_bib_note.py`), don't fabricate metadata.
- **`human_reviewed`** flips to `true` only after a human has read the source — not from an AI-written abstract.
- `bibliography.bib` is generated and gitignored; the YAML is canonical.

## Planning & the Gantt chart

`Planning/schedule.yaml` is the single source-of-truth for tasking, milestones, deliverables, and dates. `GANTT.md` is **generated** from it:

```bash
uv run python Planning/build_gantt.py        # rewrites Planning/GANTT.md
```

Edit `schedule.yaml`, never `GANTT.md` directly. The chart is a Mermaid `gantt` block, which renders natively on GitHub and in Obsidian. Milestones and deliverables also get human-readable tracking in `milestones.md` / `deliverables.md`.

## Research notes

- **Theory** (`Research/Theory/`): step-through derivations. Cite sources by wikilink. When an algebra step is verified symbolically (e.g. SymPy / Mathematica), record what was run inline so it's reproducible.
- **Experiments** (`Research/Experiments/`): one Markdown file per run/experiment, dated `YYYY-MM-DD_slug.md`, following `_template_experiment.md` (objective → setup → procedure → data → analysis → conclusion). Raw/large data lives outside git (or via pointer); the notebook entry records what was done and where the data is.

## AI-use disclosure

This is academic work; AI assistance is disclosed honestly.
- Claude is **never an author** — use `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` trailers only, never `Author:` fields or bylines.
- Tag substantive AI contributions (drafting argument-bearing prose, proposing a derivation) distinctly from pragmatic ones (formatting, BibTeX, validator runs) in commit messages or note frontmatter.
- Never commit a fabricated citation (see bibliography rules above) — the most common failure mode.

## Git hygiene

- `add` changed files explicitly; avoid `git add -A` sweeps.
- New commits over `--amend`; never `push --force`, `reset --hard`, or `clean -f` without explicit instruction.
- Work happens on issue branches (`<n>-<slug>`); `main` stays clean.
