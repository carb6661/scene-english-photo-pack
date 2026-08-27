from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable


PRIMARY_PDF_PREFIX = "English for Everyone English Vocabulary Builder"
BANK_NAMES = {
    "雅思写作大作文语料库进阶.pdf",
    "雅思大作文15个常见话题论点参考.pdf",
    "Ideas_for_IELTS_topics_（simon）.pdf",
    "雅思口语50道part 2高分素材.pdf",
    "雅思口语20道part 3高分素材.pdf",
    "《雅思口语必备900句》.pdf",
}
WORDLIST_NAMES = {"ielts_core.json", "cet4.json", "vocabulary.json"}
SKIP_DIRS = {".git", ".agents", ".codex", "node_modules", "__pycache__", "output", "tmp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Return a compact topic index for local IELTS sources without loading whole books into model context."
    )
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--keywords", nargs="+", default=[])
    parser.add_argument("--max-pages", type=int, default=8)
    parser.add_argument("--max-json-hits", type=int, default=12)
    return parser.parse_args()


def discover(workspace: Path) -> tuple[list[Path], list[Path], list[Path]]:
    primary: list[Path] = []
    banks: list[Path] = []
    wordlists: list[Path] = []
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS and not name.startswith(".")]
        root_path = Path(root)
        for name in files:
            path = root_path / name
            if name.startswith(PRIMARY_PDF_PREFIX) and name.lower().endswith(".pdf"):
                primary.append(path)
            elif name in BANK_NAMES:
                banks.append(path)
            elif name in WORDLIST_NAMES:
                wordlists.append(path)
    return sorted(primary), sorted(banks), sorted(wordlists)


def scan_pdf_pages(path: Path, keywords: list[str], limit: int) -> dict:
    result = {"path": str(path), "pages": [], "scan": "not_requested"}
    if not keywords:
        return result
    try:
        from pypdf import PdfReader
    except ImportError:
        result["scan"] = "pypdf_unavailable"
        return result

    needles = [keyword.casefold() for keyword in keywords if keyword.strip()]
    result["scan"] = "complete"
    reader = PdfReader(path)
    for index, page in enumerate(reader.pages):
        text = (page.extract_text() or "").casefold()
        if any(needle in text for needle in needles):
            result["pages"].append(index + 1)
            if len(result["pages"]) >= limit:
                result["scan"] = "capped"
                break
    return result


def scalar_record_text(node: dict) -> str:
    values = []
    for key, value in node.items():
        if isinstance(value, (str, int, float, bool)):
            values.append(f"{key}={value}")
    return " | ".join(values)


def matching_json_records(node, needles: list[str]) -> Iterable[str]:
    if isinstance(node, dict):
        record = scalar_record_text(node)
        if record and any(needle in record.casefold() for needle in needles):
            yield record[:260]
        for value in node.values():
            if isinstance(value, (dict, list)):
                yield from matching_json_records(value, needles)
    elif isinstance(node, list):
        for value in node:
            yield from matching_json_records(value, needles)


def scan_json(path: Path, keywords: list[str], remaining: int) -> list[dict]:
    if not keywords or remaining <= 0:
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return []
    needles = [keyword.casefold() for keyword in keywords if keyword.strip()]
    hits = []
    seen = set()
    for record in matching_json_records(data, needles):
        if record in seen:
            continue
        seen.add(record)
        hits.append({"path": str(path), "record": record})
        if len(hits) >= remaining:
            break
    return hits


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        raise SystemExit(f"Workspace not found: {workspace}")
    keywords = [value.strip() for value in args.keywords if value.strip()]
    primary, banks, wordlists = discover(workspace)
    pdf_index = [scan_pdf_pages(path, keywords, max(1, args.max_pages)) for path in primary[:1]]
    json_hits: list[dict] = []
    for path in wordlists:
        remaining = max(0, args.max_json_hits - len(json_hits))
        if not remaining:
            break
        json_hits.extend(scan_json(path, keywords, remaining))
    result = {
        "workspace": str(workspace),
        "keywords": keywords,
        "primary_vocabulary_source": pdf_index,
        "topic_banks_available": [str(path) for path in banks],
        "wordlists_found": [str(path) for path in wordlists],
        "json_hits": json_hits,
        "next_step": "Inspect only returned PDF pages or matching records; do not load entire sources.",
    }
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
