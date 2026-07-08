# 2026-06-19 Revival Research Report

Status: first-pass source scan.

Sources checked on 2026-06-19: arXiv API/search, arXiv recent `cs.CR` and `cs.DC`, EthResearch Discourse categories/latest feed, and Bitcoin Delving Discourse categories/latest feed.

## Direction Shift

The old repo was correctly named for 2021: DeFi was the main application surface where new crypto mechanisms were easy to observe.

The 2026 version should be broader. The technical action is now spread across:

- ZK/proving infrastructure and zkVMs.
- EVM execution, state, gas, parallelism, L2 forced inclusion, and privacy.
- Bitcoin protocol design and implementation, especially PQC, covenants/vaults, transaction privacy, Lightning, and wallet policy.
- MEV and market structure as the part of DeFi that still creates deep mechanism questions.
- AI agents and verifiable compute as an adjacent track.

## Source Snapshot

### arXiv Signals

| Date | Track | Item | Why Watch |
| --- | --- | --- | --- |
| 2026-06-18 | Ethereum execution | [EVM Workloads in the Wild](http://arxiv.org/abs/2606.19869v1) | Directly relevant to gas metering, state growth, delayed execution, and parallelism. |
| 2026-06-12 | ZK / mechanism design | [Censorship-Resistant Sealed-Bid Auctions on Blockchains](http://arxiv.org/abs/2606.14939v1) | Connects privacy, auctions, censorship resistance, and on-chain market design. |
| 2026-06-08 | Privacy / compliance | [Proof of Source of Funds](http://arxiv.org/abs/2606.10172v1) | Practical privacy/compliance intersection for cryptoassets. |
| 2026-06-03 | DeFi security | [A formal framework for the economic security of DeFi compositions](http://arxiv.org/abs/2606.05418v1) | DeFi as formal security/economic composition, not just app-layer usage. |
| 2026-06-02 | MEV / interoperability | [Signals and Spoils](http://arxiv.org/abs/2606.03434v1) | Oracle extractable value in cross-chain settings. |
| 2026-05-30 | MEV / execution | [To Wait or To Probe](http://arxiv.org/abs/2606.00720v1) | Arbitrage behavior under high-throughput execution. |
| 2026-05-26 | DeFi mechanism design | [A Trilemma in AMM Mechanism Design](http://arxiv.org/abs/2605.27602v1) | Good candidate for a small model/simulation note. |
| 2026-05-25 | zkVM infra | [ZK-Tracer](http://arxiv.org/abs/2605.25493v2) | Low-level proving performance and trace generation. |
| 2026-02-19 | ZK / AI | [Jolt Atlas](http://arxiv.org/abs/2602.17452v1) | Verifiable inference through lookup arguments. |
| 2026-02-18 | ZK infra | [push0](http://arxiv.org/abs/2602.16338v1) | Orchestration for proof generation, likely relevant to real prover systems. |
| 2025-12-10 | zkVM systems | [ZeroOS](http://arxiv.org/abs/2512.09300v1) | zkVM operating-system abstraction; good systems-reading candidate. |
| 2026-03-27 | Bitcoin / DeFi | [Bitcoin Smart Accounts](http://arxiv.org/abs/2603.26293v1) | Example of native Bitcoin DeFi direction; requires skepticism and spec-level reading. |
| 2026-06-12 | PQC | [Quantum Horizon](http://arxiv.org/abs/2606.14484v1) | Bitcoin/Ethereum quantum-threat framing. |

### EthResearch Signals

Recent topics show a useful split between serious Ethereum protocol work and noisy idea posts. Filter aggressively.

| Date | Track | Topic | Why Watch |
| --- | --- | --- | --- |
| 2026-06-19 | L2 / forced inclusion | [Repurposing FOCIL as an L2 forced transaction mechanism](https://ethresear.ch/t/repurposing-focil-as-an-l2-forced-transaction-mechanism/25233) | Forced inclusion and censorship-resistance mechanics. |
| 2026-06-19 | Execution | [Scaling in Hegota](https://ethresear.ch/t/scaling-in-hegota-using-the-eth-transfer-to-anchor-execution-and-bandwidth/25232) | Execution/bandwidth scaling idea; triage before trusting. |
| 2026-06-18 | Privacy | [Etherveil - An Ethereum Privacy Browser](https://ethresear.ch/t/etherveil-an-ethereum-privacy-browser/25224) | Privacy UX and wallet/browser surface. |
| 2026-06-16 | Privacy / EVM | [Ownership fragmentation as a privacy primitive](https://ethresear.ch/t/exploring-ownership-fragmentation-as-a-privacy-primitive-for-the-post-pectra-evm/25213) | Privacy at the account/ownership layer. |
| 2026-06-16 | Mempool privacy | [Criticism of LUCID and encrypted mempools](https://ethresear.ch/t/a-criticism-of-lucid-and-encryption-scheme-agnostic-encrypted-mempool-designs/25210) | Useful adversarial reading for encrypted mempool designs. |
| 2026-06-15 | MEV | [Origins of MEV](https://ethresear.ch/t/the-origins-of-mev-systematic-attribution-of-arbitrage-opportunity-creation-at-scale/25124) | Attribution of arbitrage opportunity creation. |
| 2026-06-15 | AI agents / mechanism design | [Treating autonomous agents as untrusted participants](https://ethresear.ch/t/treating-autonomous-agents-as-untrusted-participants-what-the-claude-code-harness-suggests-for-on-chain-mechanism-design/25202) | Good bridge between AI agents and crypto mechanism design. |
| 2026-06-15 | Privacy tokens | [pERC20 private token standard draft](https://ethresear.ch/t/perc20-private-token-standard-draft/25200) | Private asset standards are worth following. |
| 2026-06-12 | PQC / EVM | [SPHINCS minus on the EVM](https://ethresear.ch/t/sphincs-minus-efficient-stateless-post-quantum-signature-verification-on-the-evm/25165) | Concrete EVM/PQC verification cost problem. |
| 2026-06-11 | MEV / governance | [Extraction Is Conserved](https://ethresear.ch/t/extraction-is-conserved-from-mev-to-gev/24953) | MEV generalization; read critically. |

### Bitcoin Delving Signals

Bitcoin Delving currently looks high value for low-level implementation and protocol design.

| Date | Track | Topic | Why Watch |
| --- | --- | --- | --- |
| 2026-06-18 | Privacy | [State of the transaction privacy work in Bitcoin](https://delvingbitcoin.org/t/state-of-the-transaction-privacy-work-in-bitcoin/2622) | Good entry point into current Bitcoin privacy work. |
| 2026-06-18 | Lightning / DoS | [LND Zero-Timestamp Gossip DoS disclosure](https://delvingbitcoin.org/t/lnd-zero-timestamp-gossip-dos-disclosure/2621) | Implementation security and protocol behavior. |
| 2026-06-16 | Taproot / annex | [Defining 0x50 0x00 as unstructured taproot annex data](https://delvingbitcoin.org/t/defining-0x50-0x00-as-unstructured-taproot-annex-data/2620) | Low-level transaction semantics. |
| 2026-06-06 | BIP-360 | [Public key recovery for EC leaves in P2MR](https://delvingbitcoin.org/t/public-key-recovery-for-ec-leaves-in-p2mr-bip-360/2603) | Concrete BIP-level protocol design. |
| 2026-06-02 | AI / Bitcoin | [A Bitcoin-native LLM](https://delvingbitcoin.org/t/a-bitcoin-native-llm-dataset-architecture-and-open-questions/2550) | Adjacent to AI research loop; inspect quality before investing time. |
| 2026-05-28 | Covenants / vaults | [CTV-only Vault Concept](https://delvingbitcoin.org/t/ctv-only-vault-concept-v0-1-0-release/2539) | Direct path to covenant/vault implementation thinking. |
| 2026-05-24 | PQC / UTXO | [P2WOTS](https://delvingbitcoin.org/t/p2wots-post-quantum-utxo-winternitz-signatures/2530) | Post-quantum UTXO signature design. |
| 2026-05-21 | PQC | [Quantum Attack Game Theory](https://delvingbitcoin.org/t/quantum-attack-game-theory/2524) | Economic/security migration framing. |
| 2026-04-19 | Client filters | [Binary Fuse filters as an alternative to BIP 158 GCS](https://delvingbitcoin.org/t/binary-fuse-filters-as-an-alternative-to-bip-158-gcs/2428) | Implementation and wallet sync performance. |
| 2026-04-13 | Lightning | [Onion Message Jamming in the Lightning Network](https://delvingbitcoin.org/t/onion-message-jamming-in-the-lightning-network/2414) | DoS/resilience in a real protocol. |

## Suggested Focus For First Month

Pick three tracks only:

1. ZK/proving systems: zkVM, proof orchestration, lookup arguments, prover bottlenecks.
2. Bitcoin protocol implementation: PQC, covenants/vaults, transaction privacy, annex/policy details.
3. MEV/privacy/execution bridge: encrypted mempools, forced inclusion, auctions, EVM execution constraints.

Keep DeFi as a source of mechanisms and failures, not the repo's only identity.

## First Experiments

- Read `EVM Workloads in the Wild` and extract one table of execution bottlenecks.
- Read one Bitcoin Delving PQC thread and map it to the relevant BIP/spec/code surface.
- Pick one AMM/MEV arXiv paper and build a tiny simulation rather than writing a long summary.
- For AI agents, start with verifiable inference/provenance instead of broad AI market commentary.

## Repo Actions Taken

- Keep old arXiv scrape as historical data.
- Add source map, topic radar, note template, and workflow docs.
- Use reports as the monthly synthesis surface.
- Keep scripts as helpers, not the main product.
