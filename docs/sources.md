# Sources

Last checked: 2026-07-08.

Use primary sources first. Secondary sources are allowed only when they point back to papers, specs, code, measurements, or serious forum threads.

## Core Sources

| Source | Use For | Monitor |
| --- | --- | --- |
| [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) | Cryptography, ZK, protocol security, PQC, verifiable compute. | Weekly |
| [arXiv cs.DC](https://arxiv.org/list/cs.DC/recent) | Distributed systems, consensus, execution, scalability. | Weekly |
| [arXiv search](https://arxiv.org/search/) | Targeted searches for ZK, MEV, EVM, Bitcoin, PQC, DeFi. | Weekly |
| [EthResearch categories](https://ethresear.ch/categories) | Ethereum research discussion across economics, ZK, L2, execution, privacy, cryptography, consensus. | Twice weekly |
| [Bitcoin Delving categories](https://delvingbitcoin.org/categories) | Bitcoin protocol design and implementation discussion. | Twice weekly |
| [IACR ePrint](https://eprint.iacr.org/) | Cryptography preprints before or outside arXiv. | Weekly |
| [Ethereum EIPs](https://github.com/ethereum/EIPs) | Protocol/interface proposals that may become implementation work. | Weekly |
| [Ethereum Magicians](https://ethereum-magicians.org/categories) | EIP discussion and Ethereum coordination. | Weekly |
| [Ethereum PM](https://github.com/ethereum/pm) | AllCoreDevs and protocol coordination notes. | Weekly |
| [Bitcoin BIPs](https://github.com/bitcoin/bips) | Bitcoin proposal texts and status. | Weekly |
| [Bitcoin Optech](https://bitcoinops.org/) | Bitcoin development summaries, PR review club, protocol explainers. | Weekly |

## Secondary Sources

| Source | Use For | Caution |
| --- | --- | --- |
| [Flashbots writings](https://writings.flashbots.net/) | MEV, PBS, auctions, market structure. | Follow links to papers/specs before saving conclusions. |
| [Paradigm research](https://www.paradigm.xyz/research) | Mechanism design, DeFi, crypto engineering. | Often high signal, but still a company research feed. |
| [a16z crypto research](https://a16zcrypto.com/research/) | Cryptography, systems, governance, market structure. | Use as lead generation, not authority. |
| [zkSecurity blog](https://www.zksecurity.xyz/blog) | ZK bugs, audits, circuit/security patterns. | Great for implementation risk; not a replacement for papers/specs. |
| [L2BEAT](https://l2beat.com/) | L2 system inventory and risk surface. | Monitoring source, not deep research by itself. |

## Query Seeds

Use these as starting queries, then tighten them when the results get noisy.

### arXiv

- `zero-knowledge blockchain`
- `zkVM`
- `verifiable computation`
- `MEV blockchain`
- `EVM execution`
- `Bitcoin covenant`
- `Bitcoin post-quantum`
- `automated market maker`
- `decentralized finance security`
- `AI agents blockchain`

### EthResearch

Watch categories:

- Economics
- zk-s[nt]arks
- Layer 2
- Execution Layer Research
- Security
- Privacy
- Cryptography
- Consensus
- EVM

Local collector:

```bash
python tools/forums/fetch_discourse.py
```

Output table: `data/inbox/forums/ethresearch.md`

### Bitcoin Delving

Watch categories:

- Protocol Design
- Implementation
- Economics, only when tied to concrete protocol incentives

Local collector:

```bash
python tools/forums/fetch_discourse.py
```

Output table: `data/inbox/forums/delving-bitcoin.md`

## Save Criteria

Save an item when at least one is true:

- It introduces a new mechanism.
- It shows a bottleneck with measurements.
- It proposes a protocol/spec change.
- It exposes a failure mode.
- It connects two tracks, such as ZK with AI agents, DeFi with MEV, or Bitcoin policy with wallet design.

Drop an item when it is mostly narrative, token marketing, or a generic survey without a new question.
