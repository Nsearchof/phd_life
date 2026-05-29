# Literature

The literature-review reference database. Three layers:

- **[Bibliography/](Bibliography/)** — one YAML-frontmatter cite-card per source. This is the *cite source-of-truth*; everything else points here by `cite_key`.
- **[Papers/](Papers/)** — the PDFs themselves, under a two-tier git policy (open-access committed via `git add -f`; in-copyright kept local — see [.gitignore](../.gitignore)).
- **[Reading_Notes/](Reading_Notes/)** — a per-source reading note (what the paper says, what I take from it), wikilinked to its cite-card.

## Adding a source

```bash
# 1. Scaffold the cite-card (auto-fills metadata if you have a DOI)
uv run python Literature/Bibliography/scaffold_bib_note.py \
    --cite-key dirac1928_quantum_electron --type primary --from-doi 10.1098/rspa.1928.0023

# 2. Hand-edit tags / fields the lookup missed.
# 3. Drop the PDF in Literature/Papers/ (git add -f if open-access).
# 4. Write the reading note in Literature/Reading_Notes/ once you've read it;
#    flip human_reviewed: true on the cite-card.
# 5. Regenerate BibTeX:
uv run python Literature/Bibliography/build_bibtex.py
```

See [Bibliography/README.md](Bibliography/README.md) for the cite-key convention, the full YAML schema, and the tag taxonomy.
