import argparse
import json
import re
from pathlib import Path
from typing import Union

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "arxiv.yaml"


def load_filters(path: Path) -> list[str]:
    with path.open() as handle:
        config = yaml.safe_load(handle)
    return config["filter_words"]


def item_matches(item: dict, filters: list[str]) -> bool:
    summary = item.get("summary", "")
    title = item.get("title", "")
    haystack = f"{title}\n{summary}"
    return any(term_matches(haystack, word) for word in filters)


def term_matches(haystack: str, term: str) -> bool:
    flags = 0 if term.isupper() and len(term) > 1 else re.IGNORECASE
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, haystack, flags) is not None


def normalize_items(data: Union[dict, list]) -> list[dict]:
    if isinstance(data, list):
        return data
    return list(data.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter an arXiv JSON export.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    filters = load_filters(args.config)
    with args.input.open() as handle:
        data = json.load(handle)

    filtered = [item for item in normalize_items(data) if item_matches(item, filters)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        json.dump(filtered, handle, indent=2)

    print(f"wrote {len(filtered)} filtered papers to {args.output}")


if __name__ == "__main__":
    main()
