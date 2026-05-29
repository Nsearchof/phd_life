# Planning

Tasking, milestones, deliverables, and the schedule — the project-management layer of the PhD.

- **[schedule.yaml](schedule.yaml)** — source-of-truth timeline (sections → tasks with dates).
- **[build_gantt.py](build_gantt.py)** — regenerates the chart: `uv run python Planning/build_gantt.py`.
- **[GANTT.md](GANTT.md)** — generated Mermaid Gantt (renders on GitHub + Obsidian). Don't hand-edit.
- **[milestones.md](milestones.md)** — gating program/committee events.
- **[deliverables.md](deliverables.md)** — papers, talks, datasets, dissertation chapters.

Day-to-day tasking lives in [`.dev/tasks/`](../.dev/tasks/) (one file per GitHub issue) and on the GitHub issue tracker; this folder holds the longer-horizon plan.

## Workflow

1. Edit `schedule.yaml` (add/adjust sections and tasks).
2. `uv run python Planning/build_gantt.py` to regenerate `GANTT.md`.
3. Keep `milestones.md` / `deliverables.md` in sync for the human-readable detail.
