# DeFiPapers

## Inbox Tables

| Table | Source |
| --- | --- |
| [Ranked arXiv papers](data/inbox/arxiv/latest.md) | arXiv |
| [EthResearch topics](data/inbox/forums/ethresearch.md) | ethresear.ch |
| [Delving Bitcoin topics](data/inbox/forums/delving-bitcoin.md) | delvingbitcoin.org |

## Refresh

```bash
python tools/arxiv/fetch_arxiv.py
python tools/arxiv/json_to_markdown.py data/inbox/arxiv/latest.json --output data/inbox/arxiv/latest.md
python tools/forums/fetch_discourse.py
```