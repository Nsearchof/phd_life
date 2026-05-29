# phd_life

The single home for everything my PhD touches: **research documentation**, **literature**, **tasking / milestones / deliverables**, and the **schedule** that ties them together.

The repo doubles as an [Obsidian](https://obsidian.md) vault — notes cross-link with `[[wikilinks]]` and the same files render on GitHub. The field is **theoretical + experimental physics**, so the work splits into derivations (`Research/Theory/`) and lab work (`Research/Experiments/`), both feeding a shared literature database.

## Layout

```
.dev/                      # working state — research brief, STATE log, numbered tasks
Literature/                # the literature-review reference database
├── Bibliography/          # one YAML cite-card per source (→ BibTeX); the cite source-of-truth
│   ├── Primary/           # the works themselves
│   └── Secondary/         # reviews, textbooks, retrospectives
├── Papers/                # PDFs (two-tier git policy — see .gitignore)
└── Reading_Notes/         # per-source reading notes, wikilinked to the cite-card
Research/
├── Theory/                # derivations, symbolic checks, analytic notes
└── Experiments/           # lab-notebook entries (one file per run/experiment)
Planning/                  # milestones, deliverables, and the Gantt schedule
├── schedule.yaml          # source-of-truth for the timeline
├── build_gantt.py         # schedule.yaml → Mermaid Gantt
└── GANTT.md               # generated chart (renders on GitHub + Obsidian)
```

## Quickstart

```bash
uv sync                                                    # set up the Python env

# Add a literature source (auto-fills metadata from a DOI)
uv run python Literature/Bibliography/scaffold_bib_note.py --cite-key foo2024_slug --type primary --from-doi 10.xxxx/...

# Regenerate BibTeX from the YAML cite-cards
uv run python Literature/Bibliography/build_bibtex.py

# Rebuild the Gantt chart after editing the schedule
uv run python Planning/build_gantt.py
```

Conventions for working in this repo (for me and for Claude Code) live in [CLAUDE.md](CLAUDE.md).

## Owner

[Trey Morris](https://github.com/Nsearchof) — <morris.trey.j@gmail.com>
