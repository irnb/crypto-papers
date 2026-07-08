import argparse
import json
import re
import time
from pathlib import Path

import arxiv
import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "arxiv.yaml"


def load_config(path: Path) -> dict:
    with path.open() as handle:
        return yaml.safe_load(handle)


def matches_filter(summary: str, title: str, filters: list[str]) -> bool:
    haystack = f"{title}\n{summary}"
    return any(term_matches(haystack, word) for word in filters)


def term_matches(haystack: str, term: str) -> bool:
    flags = 0 if term.isupper() and len(term) > 1 else re.IGNORECASE
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, haystack, flags) is not None


def collect(config: dict) -> list[dict]:
    seen: set[str] = set()
    papers: list[dict] = []
    max_results = int(config.get("max_results_per_query", 100))
    sleep_seconds = float(config.get("sleep_seconds", 2))
    filters = config.get("filter_words", [])
    client = arxiv.Client(
        page_size=max_results,
        delay_seconds=sleep_seconds,
        num_retries=3,
    )

    for item in config["queries"]:
        label, query = normalize_query(item)
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )

        for result in client.results(search):
            if result.entry_id in seen:
                continue

            seen.add(result.entry_id)
            if filters and not matches_filter(result.summary, result.title, filters):
                continue

            papers.append(
                {
                    "title": result.title,
                    "summary": result.summary,
                    "pdf_url": canonical_pdf_url(result),
                    "entry_id": result.entry_id,
                    "categories": arxiv_categories(result),
                    "published": result.published.isoformat(),
                    "query": label,
                }
            )

        time.sleep(sleep_seconds)

    return papers


def normalize_query(item: object) -> tuple[str, str]:
    if isinstance(item, str):
        return item, item
    if isinstance(item, dict):
        return item["label"], item["query"]
    raise TypeError(f"unsupported query config item: {item!r}")


def canonical_pdf_url(result: arxiv.Result) -> str:
    return f"https://arxiv.org/pdf/{result.get_short_id()}.pdf"


def arxiv_categories(result: arxiv.Result) -> list[str]:
    categories = []
    for category in result.categories:
        categories.append(getattr(category, "term", category))
    return categories


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch filtered arXiv results.")
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    output = args.output or ROOT / config["output_path"]
    output.parent.mkdir(parents=True, exist_ok=True)

    papers = collect(config)
    with output.open("w") as handle:
        json.dump(papers, handle, indent=2)

    print(f"wrote {len(papers)} papers to {output}")


if __name__ == "__main__":
    main()
