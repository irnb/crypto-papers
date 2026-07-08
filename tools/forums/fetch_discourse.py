import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "forums.yaml"


def load_config(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return yaml.safe_load(handle)


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(
        url,
        headers={"User-Agent": "DeFiPapers research inbox/0.1"},
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def source_url(source: dict[str, Any], path: str, params: Optional[dict[str, int]] = None) -> str:
    url = source["base_url"].rstrip("/") + "/" + path.lstrip("/")
    if params:
        return url + "?" + urlencode(params)
    return url


def category_map(source: dict[str, Any]) -> dict[int, dict[str, Any]]:
    data = fetch_json(source_url(source, source["categories_path"]))
    categories = data.get("category_list", {}).get("categories", [])
    return {category["id"]: category for category in categories}


def topic_url(source: dict[str, Any], topic: dict[str, Any]) -> str:
    return f'{source["base_url"].rstrip("/")}/t/{topic["slug"]}/{topic["id"]}'


def term_matches(text: str, term: str) -> bool:
    flags = 0 if term.isupper() and len(term) > 1 else re.IGNORECASE
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, text, flags) is not None


def should_keep_topic(topic: dict[str, Any], category: Optional[dict[str, Any]], source: dict[str, Any]) -> bool:
    category_name = category["name"] if category else ""
    if category_name in source.get("watch_categories", []):
        return True

    title = topic.get("title", "")
    terms = source.get("watch_terms", [])
    return any(term_matches(title, term) for term in terms)


def score_topic(topic: dict[str, Any], category: Optional[dict[str, Any]], source: dict[str, Any]) -> tuple[int, list[str]]:
    title = topic.get("title", "")
    category_name = category["name"] if category else ""
    terms = source.get("watch_terms", [])

    score = 0
    signals = []

    if category_name in source.get("watch_categories", []):
        score += 5
        signals.append(category_name)

    matched_terms = [term for term in terms if term_matches(title, term)]
    if matched_terms:
        score += min(8, len(matched_terms) * 3)
        signals.extend(matched_terms[:3])

    posts_count = int(topic.get("posts_count") or 0)
    views = int(topic.get("views") or 0)
    like_count = int(topic.get("like_count") or 0)

    if posts_count > 1:
        score += min(6, int(math.log2(posts_count)) + 1)
        signals.append("discussion")
    if views >= 200:
        score += min(5, views // 400 + 1)
        signals.append("views")
    if like_count:
        score += min(4, like_count // 3 + 1)
        signals.append("likes")

    if source["label"] == "Delving Bitcoin":
        score += 2
    elif source["label"] == "EthResearch" and category_name in {
        "zk-s[nt]arks",
        "Execution Layer Research",
        "Cryptography",
        "Privacy",
        "Consensus",
    }:
        score += 2

    return score, unique(signals)[:5]


def unique(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def normalize_topic(
    source: dict[str, Any],
    topic: dict[str, Any],
    category: Optional[dict[str, Any]],
) -> dict[str, Any]:
    score, signals = score_topic(topic, category, source)
    return {
        "source": source["label"],
        "title": topic.get("title", ""),
        "url": topic_url(source, topic),
        "category": category["name"] if category else None,
        "category_slug": category["slug"] if category else None,
        "created_at": topic.get("created_at"),
        "last_posted_at": topic.get("last_posted_at"),
        "posts_count": topic.get("posts_count", 0),
        "views": topic.get("views", 0),
        "like_count": topic.get("like_count", 0),
        "quality_score": score,
        "quality_signals": signals,
        "topic_id": topic.get("id"),
        "slug": topic.get("slug"),
    }


def collect_source(source: dict[str, Any], max_pages: int) -> list[dict[str, Any]]:
    categories = category_map(source)
    topics_by_id: dict[int, dict[str, Any]] = {}

    for page in range(max_pages):
        data = fetch_json(source_url(source, source["latest_path"], {"page": page}))
        for topic in data.get("topic_list", {}).get("topics", []):
            category = categories.get(topic.get("category_id"))
            if should_keep_topic(topic, category, source):
                topics_by_id[topic["id"]] = normalize_topic(source, topic, category)

    return list(topics_by_id.values())


def collect(config: dict[str, Any]) -> list[dict[str, Any]]:
    max_pages = int(config.get("max_pages_per_source", 1))
    topics: list[dict[str, Any]] = []
    for source in config["sources"]:
        topics.extend(collect_source(source, max_pages))

    return sort_topics(topics)


def sort_topics(topics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        topics,
        key=lambda topic: (
            topic.get("quality_score", 0),
            topic.get("last_posted_at") or topic.get("created_at") or "",
        ),
        reverse=True,
    )


def markdown_link(label: str, url: str) -> str:
    return f"[{escape_cell(label)}]({url})"


def escape_cell(value: object) -> str:
    return str(value or "").replace("\n", " ").replace("|", "\\|").strip()


def source_slug(source: str) -> str:
    return source.lower().replace(" ", "-")


def topics_by_source(topics: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for topic in topics:
        grouped.setdefault(topic["source"], []).append(topic)
    return {source: sort_topics(items) for source, items in grouped.items()}


def render_index(topics: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = topics_by_source(topics)
    lines = [
        "# Forum inbox",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "| source | rows | table |",
        "| --- | ---: | --- |",
    ]

    for source, source_topics in sorted(grouped.items()):
        slug = source_slug(source)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(source),
                    escape_cell(len(source_topics)),
                    markdown_link(f"{slug}.md", f"{slug}.md"),
                ]
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def render_source_markdown(source: str, topics: list[dict[str, Any]]) -> str:
    lines = [
        f"# {source}",
        "",
        f"Rows: `{len(topics)}` ranked forum topics.",
        "",
        "| rank | score | last post | category | topic | signals | posts | views |",
        "| ---: | ---: | --- | --- | --- | --- | ---: | ---: |",
    ]

    for rank, topic in enumerate(topics, start=1):
        row = [
            rank,
            topic.get("quality_score", 0),
            (topic.get("last_posted_at") or "")[:10],
            topic.get("category"),
            markdown_link(topic["title"], topic["url"]),
            ", ".join(topic.get("quality_signals", [])),
            topic.get("posts_count"),
            topic.get("views"),
        ]
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch watched Discourse forum topics.")
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-markdown", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    output_json = args.output_json or ROOT / config["output_json"]
    output_markdown = args.output_markdown or ROOT / config["output_markdown"]

    topics = collect(config)
    grouped = topics_by_source(topics)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(topics, indent=2))

    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.write_text(render_index(topics))

    for source, source_topics in grouped.items():
        source_path = output_markdown.parent / f"{source_slug(source)}.md"
        source_path.write_text(render_source_markdown(source, source_topics))

    print(f"wrote {len(topics)} forum topics to {output_json}")
    print(f"wrote Markdown index to {output_markdown}")
    for source, source_topics in sorted(grouped.items()):
        source_path = output_markdown.parent / f"{source_slug(source)}.md"
        print(f"wrote {len(source_topics)} {source} topics to {source_path}")


if __name__ == "__main__":
    main()
