import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Union


ANCHOR_TERMS = {
    "zkVM": 6,
    "zero-knowledge": 5,
    "zero knowledge": 5,
    "STARK": 5,
    "SNARK": 5,
    "prover": 4,
    "verifier": 4,
    "proof system": 5,
    "lookup argument": 5,
    "verifiable computation": 5,
    "verifiable inference": 5,
    "formal verification": 5,
    "protocol design": 6,
    "protocol architecture": 6,
    "software architecture": 5,
    "system architecture": 5,
    "node": 3,
    "node internals": 6,
    "client": 3,
    "client architecture": 5,
    "p2p": 5,
    "peer-to-peer": 5,
    "networking": 4,
    "consensus": 5,
    "state sync": 5,
    "storage": 4,
    "mempool policy": 5,
    "relay policy": 5,
    "EVM": 5,
    "Ethereum": 4,
    "gas metering": 5,
    "state growth": 5,
    "parallel execution": 5,
    "rollup": 4,
    "data availability": 5,
    "MEV": 5,
    "PBS": 5,
    "prediction market": 6,
    "prediction markets": 6,
    "Polymarket": 6,
    "futarchy": 5,
    "information market": 5,
    "auction": 3,
    "intent": 4,
    "intents": 4,
    "account abstraction": 5,
    "ERC-4337": 5,
    "smart account": 4,
    "encrypted mempool": 5,
    "mempool": 4,
    "Bitcoin": 4,
    "BitVM": 6,
    "covenant": 5,
    "vault": 4,
    "Lightning": 4,
    "taproot": 4,
    "miniscript": 4,
    "post-quantum": 5,
    "PQC": 5,
    "ML-DSA": 5,
    "Winternitz": 5,
    "privacy": 3,
    "security": 3,
    "attack": 3,
    "exploit": 3,
    "oracle": 3,
    "payment": 3,
    "payments": 3,
    "x402": 5,
    "payment channel": 4,
    "RWA": 4,
    "real-world asset": 4,
    "tokenization": 4,
    "tokenized": 3,
    "DePIN": 4,
    "wallet": 3,
    "identity": 3,
    "reputation": 3,
    "consumer crypto": 4,
    "application layer": 4,
    "on-chain": 2,
    "dApp": 3,
    "decentralized application": 3,
    "AMM": 4,
    "DEX": 3,
    "liquidation": 3,
    "stablecoin": 3,
    "benchmark": 4,
    "implementation": 4,
    "trade-off": 4,
    "tradeoff": 4,
    "dataset": 3,
}

QUERY_WEIGHTS = {
    "zkVM": 5,
    "ZK blockchain": 4,
    "Ethereum execution": 4,
    "Bitcoin covenants": 5,
    "Bitcoin PQC": 5,
    "MEV": 4,
    "Rollups": 3,
    "Verifiable computation": 4,
    "AI agents crypto": 2,
    "AMM / DEX": 2,
    "DeFi": 1,
    "Core protocol design": 5,
    "Node internals": 5,
    "Protocol architecture": 5,
    "Consensus and networking": 4,
    "Bitcoin node policy": 5,
    "BitVM": 5,
    "L2 architecture": 4,
    "Prediction markets": 5,
    "Intents and account abstraction": 4,
    "Stablecoins and payments": 4,
    "RWA tokenization": 3,
    "Emerging applications": 3,
    "Wallet identity reputation": 3,
    "DePIN": 2,
}

NOISE_TERMS = {
    "clinical": 5,
    "healthcare": 4,
    "medical": 4,
    "genomic": 4,
    "5G": 3,
    "6G": 3,
    "chatbot": 3,
    "education": 3,
    "student": 3,
    "physics": 4,
    "qubit": 3,
    "anti-money laundering": 5,
    "AML": 5,
    "VASP": 4,
    "energy": 4,
    "IoT": 4,
    "wireless": 4,
    "supply chain": 4,
    "vehicular": 4,
    "federated learning": 4,
    "FinTech": 3,
}


def first_sentence(summary: str) -> str:
    if "." not in summary:
        return summary.strip()
    return summary[: summary.index(".") + 1].strip()


def normalize_items(data: Union[dict, list]) -> list[dict]:
    if isinstance(data, list):
        return data
    return list(data.values())


def escape_cell(value: object) -> str:
    return str(value or "").replace("\n", " ").replace("|", "\\|").strip()


def markdown_link(label: str, url: str) -> str:
    if not url:
        return escape_cell(label)
    return f"[{escape_cell(label)}]({url})"


def term_matches(text: str, term: str) -> bool:
    flags = 0 if term.isupper() and len(term) > 1 else re.IGNORECASE
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, text, flags) is not None


def parse_published(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.fromisoformat(value[:10] + "T00:00:00+00:00")
        except ValueError:
            return None


def recency_score(published: str) -> int:
    parsed = parse_published(published)
    if not parsed:
        return 0

    now = datetime.now(timezone.utc)
    age_days = max((now - parsed.astimezone(timezone.utc)).days, 0)
    if age_days <= 30:
        return 4
    if age_days <= 90:
        return 3
    if age_days <= 180:
        return 2
    if age_days <= 365:
        return 1
    return 0


def score_item(item: dict) -> tuple[int, list[str]]:
    title = item.get("title", "")
    summary = item.get("summary", "")
    query = item.get("query", "")
    text = f"{title}\n{summary}"

    score = QUERY_WEIGHTS.get(query, 0)
    signals = []

    if score:
        signals.append(query)

    for term, weight in ANCHOR_TERMS.items():
        if term_matches(title, term):
            score += weight + 2
            signals.append(term)
        elif term_matches(summary, term):
            score += weight
            signals.append(term)

    action_terms = [
        "we implement",
        "we implemented",
        "we evaluate",
        "we benchmark",
        "we prove",
        "we present",
        "we introduce",
        "we propose",
        "empirical",
        "formal",
        "open-source",
        "open source",
    ]
    for term in action_terms:
        if term in text.lower():
            score += 2
            signals.append(term)
            break

    score += recency_score(item.get("published") or item.get("date") or "")

    for term, weight in NOISE_TERMS.items():
        if term_matches(text, term):
            score -= weight

    unique_signals = []
    for signal in signals:
        if signal not in unique_signals:
            unique_signals.append(signal)

    return max(score, 0), unique_signals[:5]


def ranked_items(data: Union[dict, list], min_score: int, limit: int) -> list[dict]:
    items = []
    for item in normalize_items(data):
        score, signals = score_item(item)
        if score < min_score:
            continue
        ranked = dict(item)
        ranked["quality_score"] = score
        ranked["quality_signals"] = signals
        items.append(ranked)

    items.sort(
        key=lambda item: (
            item["quality_score"],
            item.get("published") or item.get("date") or "",
        ),
        reverse=True,
    )

    if limit > 0:
        return items[:limit]
    return items


def build_markdown(input_path: Path, min_score: int, limit: int) -> str:
    with input_path.open() as handle:
        data = json.load(handle)

    total = len(normalize_items(data))
    items = ranked_items(data, min_score, limit)

    all_items = normalize_items(data)
    lines = [
        "# Ranked arXiv inbox",
        "",
        f"Rows: `{len(items)}` selected from `{total}` papers. Minimum score: `{min_score}`.",
        "",
        "| rank | score | published | track | paper | signals | pdf |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]

    for rank, item in enumerate(items, start=1):
        pdf_url = item.get("pdf_url") or item.get("pdf url") or ""
        entry_id = item.get("entry_id") or ""
        published = item.get("published") or item.get("date") or ""
        paper = markdown_link(item.get("title", ""), entry_id)
        pdf = markdown_link("pdf", pdf_url)
        row = [
            rank,
            item["quality_score"],
            published[:10],
            item.get("query", ""),
            paper,
            ", ".join(item.get("quality_signals", [])),
            pdf,
        ]
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")

    lines.extend(render_unranked_table(all_items))

    return "\n".join(lines) + "\n"


def render_unranked_table(items: list[dict]) -> list[str]:
    lines = [
        "",
        "## All arXiv papers, unranked",
        "",
        f"Rows: `{len(items)}` in original fetch order.",
        "",
        "| number | published | track | paper | first sentence | pdf |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]

    for number, item in enumerate(items, start=1):
        pdf_url = item.get("pdf_url") or item.get("pdf url") or ""
        entry_id = item.get("entry_id") or ""
        published = item.get("published") or item.get("date") or ""
        row = [
            number,
            published[:10],
            item.get("query", ""),
            markdown_link(item.get("title", ""), entry_id),
            first_sentence(item.get("summary", "")),
            markdown_link("pdf", pdf_url),
        ]
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an arXiv JSON export to ranked Markdown.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-score", default=8, type=int)
    parser.add_argument("--limit", default=120, type=int, help="Use 0 for no limit.")
    args = parser.parse_args()

    markdown = build_markdown(args.input, args.min_score, args.limit)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown)
        print(f"wrote ranked Markdown table to {args.output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
