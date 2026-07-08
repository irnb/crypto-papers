# DeFiPapers

## Inbox Tables

| Table | Source |
| --- | --- |
| [Ranked arXiv papers](data/inbox/arxiv/latest.md) | arXiv |
| [EthResearch topics](data/inbox/forums/ethresearch.md) | ethresear.ch |
| [Delving Bitcoin topics](data/inbox/forums/delving-bitcoin.md) | delvingbitcoin.org |

## Paper Track Index

| Track | Rows |
| --- | ---: |
| ZK blockchain | 98 |
| Ethereum execution | 95 |
| MEV | 95 |
| Bitcoin node policy | 91 |
| L2 architecture | 85 |
| Core protocol design | 80 |
| Protocol architecture | 73 |
| Rollups | 70 |
| Stablecoins and payments | 69 |
| DeFi | 64 |
| Intents and account abstraction | 60 |
| DePIN | 58 |
| Verifiable computation | 57 |
| AI agents crypto | 51 |
| Node internals | 50 |
| Bitcoin PQC | 42 |
| RWA tokenization | 35 |
| Consensus and networking | 22 |
| Wallet identity reputation | 20 |
| AMM / DEX | 18 |
| Prediction markets | 18 |
| zkVM | 13 |
| Emerging applications | 11 |
| BitVM | 5 |
| Bitcoin covenants | 5 |

## Forum Source Index

| Source | Rows |
| --- | ---: |
| EthResearch | 70 |
| Delving Bitcoin | 86 |

## Refresh

```bash
python tools/arxiv/fetch_arxiv.py
python tools/arxiv/json_to_markdown.py data/inbox/arxiv/latest.json --output data/inbox/arxiv/latest.md
python tools/forums/fetch_discourse.py
```
