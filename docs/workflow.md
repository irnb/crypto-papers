# Operating Workflow

This repo should create a research loop, not a bookmark pile.

## Weekly Loop

Time box: 2 to 3 hours.

1. Scan primary feeds.
2. Pick at most 5 items.
3. Write short notes for at most 3 items.
4. Promote at most 1 item into an experiment, implementation note, or deeper write-up.
5. Delete stale inbox data.

Suggested local scan:

```bash
python tools/arxiv/fetch_arxiv.py
python tools/arxiv/json_to_markdown.py data/inbox/arxiv/latest.json --output data/inbox/arxiv/latest.md
python tools/forums/fetch_discourse.py
```

## Monthly Report

Create one file in `reports/YYYY-MM-topic.md`.

Required sections:

- `What moved`: concrete shifts in research or implementation direction.
- `Problems people are stuck on`: open problems, tradeoffs, or bottlenecks.
- `Ideas worth testing`: small experiments or code-reading projects.
- `Dropped threads`: topics that looked interesting but did not survive scrutiny.
- `Next month focus`: 1 to 3 tracks only.

## Note Quality Bar

A useful note must answer:

- What problem is this solving?
- Why is the problem hard now?
- What changed recently?
- What assumptions does the author rely on?
- What would I build, measure, or read next?

Avoid long summaries. If the note does not produce a question or next action, it is probably just a saved link.

## Triage Labels

Use these labels in notes and reports:

- `watch`: worth following, no immediate action.
- `read-deep`: read carefully and summarize.
- `replicate`: run code, reproduce a benchmark, or inspect an implementation.
- `spec-read`: read the linked BIP/EIP/spec before forming an opinion.
- `idea`: possible project or article seed.
- `drop`: not useful for current direction.

## Cadence

- Weekly: source scan and notes.
- Monthly: one report.
- Quarterly: one focused build/read project, such as a small prover benchmark, Bitcoin policy simulation, EVM execution experiment, or DeFi mechanism model.
