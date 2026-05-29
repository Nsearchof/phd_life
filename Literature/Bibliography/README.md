# Bibliography

Cite source-of-truth. Every paper cited in any research note, planning doc, or reading note traces back to a single YAML-frontmatter Markdown file in this tree.

## Cite-key convention

`firstauthor + year + slug`, lowercase, snake-case, no diacritics. The slug is 1–3 words from the title.

Examples:
- `dirac1928_quantum_electron`
- `bcs1957_superconductivity` (conventional alias for the three-author BCS paper)
- `wilson1982_renormalization_group`
- `aspect1982_bell_test`

Cite-keys are globally unique within `Bibliography/`. Wikilink with the bare key: `[[dirac1928_quantum_electron]]`.

## YAML frontmatter schema

Every cite-card opens with this block. Unknown fields stay blank or `pending` — never delete a field.

```yaml
---
cite_key: dirac1928_quantum_electron
title: "The Quantum Theory of the Electron"
authors: ["Paul A. M. Dirac"]
year: 1928
type: primary                  # primary | secondary
kind: article                  # article | book | inproceedings | thesis | preprint | dataset | misc
tags: [quantum, relativistic, foundational]
journal: "Proceedings of the Royal Society A"
volume: 117
issue: "778"
pages: "610-624"
doi: "10.1098/rspa.1928.0023"
url: ""
arxiv_id: ""
pdf_status: pending            # acquired | pending | unavailable | open_access
pdf_path: ""
reading_note: ""               # wikilink/path to Reading_Notes/<cite_key>.md once written
human_reviewed: false          # true only after a human has read the source
---
```

After the frontmatter the body is freeform — typically a short summary written once the source has actually been read.

## `human_reviewed`

Records whether a human has *read the source*, not whether an AI summarized its abstract. New stubs default to `false`; flip to `true` only when the body reflects a reading. This keeps the literature review honest about what's actually been engaged.

## Tag taxonomy

Tags are namespace-scoped so Obsidian's Tag Pane can filter by any axis.

- **By area:** `#area/theory`, `#area/experiment`, `#area/methods`.
- **By topic** (free-form): `#renormalization`, `#superconductivity`, `#bell-inequalities`, …
- **By role in my work:** `#foundational` (load-bearing), `#background`, `#method` (a technique I use), `#tangential`.

## Layout

```
Bibliography/
├── README.md                   # this file
├── _template_bib_note.md       # the schema as a copy-paste skeleton
├── Primary/<cite_key>.md       # the works themselves
├── Secondary/<cite_key>.md     # reviews, textbooks, retrospectives
├── scaffold_bib_note.py        # new stub (+ optional --from-doi Crossref autofill)
└── build_bibtex.py             # YAML → bibliography.bib (gitignored; regenerable)
```

## Tooling

Run from the repo root via `uv run python …`.

- `scaffold_bib_note.py --cite-key <key> --type primary|secondary` — generate a stub with the full schema. Optional `--from-doi <doi>` auto-fills title/authors/year/journal/volume/pages via the Crossref REST API (no key required). `--dry-run` prints without writing.
- `build_bibtex.py` — walk every `Bibliography/**/*.md`, emit `bibliography.bib` (gitignored — YAML is canonical). Idempotent. `--dry-run` prints to stdout.
