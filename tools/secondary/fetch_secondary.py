import argparse
import html as html_lib
import json
import re
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config" / "secondary.yaml"
USER_AGENT = "crypto-papers secondary inbox/0.1"


def load_config(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return yaml.safe_load(handle)


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def term_matches(text: str, term: str) -> bool:
    flags = 0 if term.isupper() and len(term) > 1 else re.IGNORECASE
    pattern = r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])"
    return re.search(pattern, text, flags) is not None


def unique(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def strip_markup(value: object) -> str:
    text = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


def decode_js_string(value: str) -> str:
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return html_lib.unescape(value.replace(r"\/", "/"))


def normalize_date(value: object) -> str:
    parsed = parse_datetime(value)
    if parsed:
        return parsed.date().isoformat()
    text = str(value or "").strip()
    return text[:10]


def parse_datetime(value: object) -> Optional[datetime]:
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)

    text = str(value or "").strip()
    if not text:
        return None

    try:
        parsed = parsedate_to_datetime(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError, IndexError, OverflowError):
        pass

    iso_text = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(iso_text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def collect_rss(source: dict[str, Any]) -> list[dict[str, Any]]:
    feed = fetch_text(source["url"])
    root = ET.fromstring(feed)
    items = []

    for item in root.findall(".//item"):
        items.append(
            {
                "title": child_text(item, "title"),
                "url": child_text(item, "link"),
                "summary": strip_markup(child_text(item, "description")),
                "published_at": normalize_date(child_text(item, "pubDate")),
                "author": child_text(item, "author"),
            }
        )

    atom_ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", atom_ns):
        link = ""
        link_node = entry.find("atom:link", atom_ns)
        if link_node is not None:
            link = link_node.attrib.get("href", "")
        items.append(
            {
                "title": namespaced_text(entry, "title", atom_ns),
                "url": link,
                "summary": strip_markup(namespaced_text(entry, "summary", atom_ns)),
                "published_at": normalize_date(namespaced_text(entry, "updated", atom_ns)),
                "author": "",
            }
        )

    return items


def child_text(node: ET.Element, tag: str) -> str:
    child = node.find(tag)
    return child.text.strip() if child is not None and child.text else ""


def namespaced_text(node: ET.Element, tag: str, namespaces: dict[str, str]) -> str:
    child = node.find(f"atom:{tag}", namespaces)
    return child.text.strip() if child is not None and child.text else ""


def collect_paradigm_research(source: dict[str, Any]) -> list[dict[str, Any]]:
    html = fetch_text(source["url"])
    pattern = re.compile(
        r'slug:"(?P<slug>[^"]+)",title:"(?P<title>(?:\\.|[^"])*)",summary:"'
        r'(?P<summary>(?:\\.|[^"])*)".*?publishedAt:"(?P<published_at>[^"]+)"',
        re.S,
    )
    items = []
    for match in pattern.finditer(html):
        slug = match.group("slug")
        items.append(
            {
                "title": decode_js_string(match.group("title")),
                "url": urljoin(source["base_url"], f"/{slug}"),
                "summary": strip_markup(decode_js_string(match.group("summary"))),
                "published_at": normalize_date(match.group("published_at")),
                "author": "",
            }
        )
    return items


def collect_a16z_preloaded_posts(source: dict[str, Any]) -> list[dict[str, Any]]:
    html = fetch_text(source["url"])
    match = re.search(
        r'<script type="application/json" id="a16z-preloaded-posts">(.*?)</script>',
        html,
        re.S,
    )
    if not match:
        return []

    payload = json.loads(html_lib.unescape(match.group(1)))
    items = []
    for hit in payload.get("hits", []):
        summary = (
            hit.get("post_description")
            or hit.get("post_meta_description")
            or hit.get("post_excerpt")
            or ""
        )
        items.append(
            {
                "title": strip_markup(hit.get("post_title")),
                "url": urljoin(source["base_url"], hit.get("permalink", "")),
                "summary": strip_markup(summary),
                "published_at": normalize_date(hit.get("post_date")),
                "author": "",
            }
        )
    return items


def collect_monitor_page(source: dict[str, Any]) -> list[dict[str, Any]]:
    html = fetch_text(source["url"])
    title = first_match(html, r"<title>(.*?)</title>") or source["label"]
    summary = (
        first_match(html, r'<meta name="description" content="([^"]+)"')
        or first_match(html, r'<meta property="og:description" content="([^"]+)"')
        or ""
    )
    return [
        {
            "title": strip_markup(title),
            "url": source["url"],
            "summary": strip_markup(summary),
            "published_at": date.today().isoformat(),
            "author": "",
        }
    ]


def first_match(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.S | re.I)
    return html_lib.unescape(match.group(1)).strip() if match else ""


COLLECTORS = {
    "rss": collect_rss,
    "paradigm_research": collect_paradigm_research,
    "a16z_preloaded_posts": collect_a16z_preloaded_posts,
    "monitor_page": collect_monitor_page,
}


def collect(config: dict[str, Any]) -> list[dict[str, Any]]:
    max_items = int(config.get("max_items_per_source", 20))
    seen_urls: set[str] = set()
    items = []

    for source in config["sources"]:
        collector = COLLECTORS[source["kind"]]
        source_items = collector(source)
        for item in source_items[:max_items]:
            if not item.get("url") or item["url"] in seen_urls:
                continue
            seen_urls.add(item["url"])
            items.append(normalize_item(source, item, config))

    return sort_items(items)


def normalize_item(
    source: dict[str, Any],
    item: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    score, signals = score_item(source, item, config)
    return {
        "source": source["label"],
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "summary": item.get("summary", ""),
        "published_at": item.get("published_at", ""),
        "author": item.get("author", ""),
        "quality_score": score,
        "quality_signals": signals,
    }


def score_item(
    source: dict[str, Any],
    item: dict[str, Any],
    config: dict[str, Any],
) -> tuple[int, list[str]]:
    haystack = f"{item.get('title', '')}\n{item.get('summary', '')}"
    signals = list(source.get("signals", []))
    score = int(source.get("source_weight", 0))

    terms = config.get("watch_terms", []) + source.get("watch_terms", [])
    matched_terms = [term for term in terms if term_matches(haystack, term)]
    if matched_terms:
        score += min(15, len(matched_terms) * 3)
        signals.extend(matched_terms[:5])

    quality_terms = [term for term in config.get("quality_terms", []) if term_matches(haystack, term)]
    if quality_terms:
        score += min(6, len(quality_terms) * 2)
        signals.extend(quality_terms[:3])

    published = item.get("published_at")
    try:
        age_days = (date.today() - date.fromisoformat(published)).days
    except (TypeError, ValueError):
        age_days = 9999

    if age_days <= 30:
        score += 4
        signals.append("recent")
    elif age_days <= 180:
        score += 2
        signals.append("fresh")
    elif age_days <= 365:
        score += 1

    return score, unique(signals)[:8]


def sort_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (
            item.get("quality_score", 0),
            item.get("published_at", ""),
            item.get("source", ""),
        ),
        reverse=True,
    )


def markdown_link(label: str, url: str) -> str:
    return f"[{escape_cell(label)}]({url})"


def escape_cell(value: object) -> str:
    return str(value or "").replace("\n", " ").replace("|", "\\|").strip()


def truncate(value: object, limit: int = 180) -> str:
    text = escape_cell(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def source_slug(source: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")
    return slug or "source"


def items_by_source(items: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(item["source"], []).append(item)
    return {source: sort_items(source_items) for source, source_items in grouped.items()}


def render_index(items: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = items_by_source(items)
    lines = [
        "# Secondary source inbox",
        "",
        f"Generated at: `{generated_at}`",
        "",
        f"Rows: `{len(items)}` secondary-source leads.",
        "",
        "## Source Index",
        "",
        "| source | rows | table |",
        "| --- | ---: | --- |",
    ]

    for source, source_items in sorted(grouped.items()):
        slug = source_slug(source)
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(source),
                    escape_cell(len(source_items)),
                    markdown_link(f"{slug}.md", f"{slug}.md"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Scored Leads",
            "",
            "| score | source | title | signals | date |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )

    for item in items:
        row = [
            item.get("quality_score", 0),
            item.get("source"),
            markdown_link(item["title"], item["url"]),
            ", ".join(item.get("quality_signals", [])),
            item.get("published_at"),
        ]
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")

    return "\n".join(lines) + "\n"


def render_source_markdown(source: str, items: list[dict[str, Any]]) -> str:
    lines = [
        f"# {source}",
        "",
        f"Rows: `{len(items)}` secondary-source leads.",
        "",
        "| score | title | signals | summary | date |",
        "| ---: | --- | --- | --- | --- |",
    ]

    for item in items:
        row = [
            item.get("quality_score", 0),
            markdown_link(item["title"], item["url"]),
            ", ".join(item.get("quality_signals", [])),
            truncate(item.get("summary")),
            item.get("published_at"),
        ]
        lines.append("| " + " | ".join(escape_cell(value) for value in row) + " |")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch secondary crypto research sources.")
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-markdown", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    output_json = args.output_json or ROOT / config["output_json"]
    output_markdown = args.output_markdown or ROOT / config["output_markdown"]

    items = collect(config)
    grouped = items_by_source(items)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(items, indent=2))

    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.write_text(render_index(items))

    for source, source_items in grouped.items():
        source_path = output_markdown.parent / f"{source_slug(source)}.md"
        source_path.write_text(render_source_markdown(source, source_items))

    print(f"wrote {len(items)} secondary-source leads to {output_json}")
    print(f"wrote Markdown index to {output_markdown}")
    for source, source_items in sorted(grouped.items()):
        source_path = output_markdown.parent / f"{source_slug(source)}.md"
        print(f"wrote {len(source_items)} {source} leads to {source_path}")


if __name__ == "__main__":
    main()
