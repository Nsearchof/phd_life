# Task 1 — setup_repo

**Issue:** https://github.com/Nsearchof/phd_life/issues/1
**Branch:** `1-setup_repo`

## Goal

Stand up the repo that holds all PhD-related research documentation, tasking, milestones, deliverables, and schedule — plus a reference-document database for the literature review and a Gantt chart tracking tasking/milestones/deliverables/schedule.

## Scope

- [x] uv Python project (`pyproject.toml`, `.python-version`)
- [x] Obsidian vault config (`.obsidian/`) with wikilinks
- [x] `.dev/` tasking — research brief, STATE log, this task file
- [x] `Literature/` reference database — Bibliography (YAML → BibTeX) + Papers + Reading_Notes
- [x] `Research/` — Theory + Experiments (lab-notebook template)
- [x] `Planning/` — `schedule.yaml` → Gantt chart, milestones, deliverables
- [x] Repo guidance in `CLAUDE.md`, overview in `README.md`
- [x] `.gitignore` extended (Obsidian state, generated BibTeX, two-tier PDF policy, data)

## Follow-ups (not in this task)

- Populate `Planning/schedule.yaml` with real program dates and regenerate `GANTT.md`.
- Add the first real Bibliography cite-cards for the literature review.
- Set the current research thread in `.dev/research/brief.md`.
