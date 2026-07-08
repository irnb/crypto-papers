# Topic Radar

Last updated: 2026-06-19.

This is the working scope for the revived repo. It should change as your interests and the market's technical direction change.

| Track | Why Watch It | Watch Terms | Good Output |
| --- | --- | --- | --- |
| ZK and proving systems | This is now core infrastructure, not only privacy. Follow prover performance, recursion, zkVMs, lookup arguments, proof orchestration, and circuit security. | zkVM, STARK, SNARK, lookup, recursion, prover, verifier, proof generation, constraint bugs | Benchmark note, implementation reading, proof-system map |
| Core Ethereum execution | Execution-layer bottlenecks are shifting toward state growth, gas metering, parallelism, delayed execution, encrypted mempools, and forced inclusion. | EVM, gas metering, state growth, parallel execution, mempool, FOCIL, PBS | Spec note, client-code reading, tradeoff write-up |
| Bitcoin protocol design | Bitcoin research is active around post-quantum migration, covenants/vaults, transaction privacy, Lightning DoS, filters, and wallet semantics. | covenant, CTV, vault, annex, PQC, Winternitz, ML-DSA, Lightning, BIP | BIP/spec note, policy simulation, Bitcoin Core PR reading |
| Privacy and identity | Privacy is moving from mixers into token standards, private assets, source-of-funds proofs, wallets, identity, and mempool design. | private token, pERC20, source of funds, encrypted mempool, stealth, ring signature, ownership fragmentation | Threat model, protocol comparison, implementation idea |
| MEV and market structure | DeFi still matters when it exposes mechanism-design, ordering, auction, oracle, or liquidity problems. | MEV, GEV, batch auction, oracle extractable value, AMM, arbitrage, liquidation | Problem map, mechanism model, small simulation |
| AI agents and verifiable compute | AI can become a crypto-adjacent source of demand for verification, provenance, sandboxing, and agent accountability. | verifiable inference, AI agent, proof of training, provenance, agent identity, zkML | Reading list, boundary map, experiment proposal |
| Application-layer DeFi | Keep DeFi in scope, but as a problem source rather than the whole repo identity. | lending, stablecoin, DEX, liquidation, oracle, risk, composability | Failure analysis, mechanism comparison, implementation note |

## Current Bias

Prefer tracks that produce low-level implementation questions:

- How is this represented in a spec or client?
- What invariant is being enforced?
- What bottleneck is measured?
- What breaks under adversarial behavior?
- What could be implemented in a weekend to understand the idea?

## Parking Lot

Topics that may become relevant but should not dominate the first month:

- Token narratives without technical novelty.
- Governance philosophy unless tied to mechanism design.
- Pure price/market commentary.
- Vendor announcements without paper, spec, code, or benchmark.
