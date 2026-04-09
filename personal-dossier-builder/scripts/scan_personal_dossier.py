#!/usr/bin/env python3
"""Heuristic scanner for a personal dossier directory.

This script does three lightweight things:
1. discover key dossier files under a personal root
2. extract initial confirmed/open candidates from markdown structure
3. surface conflict signals for human follow-up

It is intentionally heuristic. It helps a skill start with a useful map; it does
not decide truth by itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROLE_FILENAMES = {
    "master_dossier": ["personal-master-dossier.md"],
    "confirmed_summary": ["personal-summary-confirmed.md"],
    "profile": ["profile.md"],
    "preferences": ["preferences.md"],
    "operating_manual": ["personal-operating-manual.md"],
    "public_bio": ["public-bio.md"],
}

OPEN_HEADING_PATTERNS = [
    r"\bopen items?\b",
    r"待补",
    r"待确认",
    r"未定",
    r"待完成事项",
    r"\btodo\b",
    r"待办",
    r"仍值得.*观察",
    r"可选优化项",
]

CONFIRMED_HEADING_PATTERNS = [
    r"已确认",
    r"确认版摘要",
    r"稳定结论",
    r"长期定义",
    r"当前稳定结论",
    r"核心结论",
]

SUMMARY_META_HEADING_PATTERNS = [
    r"\bpersonal summary confirmed\b",
    r"\bsummary\b",
]

CONFLICT_LINE_PATTERNS = [
    r"冲突项",
    r"存在冲突",
    r"有冲突",
    r"相互冲突",
    r"\bconflict\b",
    r"前后不一致",
    r"内容不一致",
    r"明显矛盾",
    r"前后矛盾",
    r"互相打架",
    r"矛盾",
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)(.+?)\s*$")
TASK_RE = re.compile(r"^\s*[-*+]\s+\[(?: |x)\]\s+(.+?)\s*$", re.IGNORECASE)


def score_candidate(root: Path, path: Path) -> tuple[int, int, str]:
    rel = path.relative_to(root)
    depth = len(rel.parts)
    archive_penalty = 1 if "archive" in {part.lower() for part in rel.parts} else 0
    return (depth + archive_penalty, archive_penalty, str(rel).lower())


def discover_files(root: Path) -> dict[str, dict[str, object] | None]:
    all_md = [path for path in root.rglob("*.md") if path.is_file()]
    by_name: dict[str, list[Path]] = {}
    for path in all_md:
        by_name.setdefault(path.name.lower(), []).append(path)

    discovered: dict[str, dict[str, object] | None] = {}
    for role, filenames in ROLE_FILENAMES.items():
        matches: list[Path] = []
        for filename in filenames:
            matches.extend(by_name.get(filename.lower(), []))
        matches = sorted(set(matches), key=lambda p: score_candidate(root, p))
        if not matches:
            discovered[role] = None
            continue
        discovered[role] = {
            "primary": str(matches[0]),
            "alternates": [str(path) for path in matches[1:]],
        }
    return discovered


def load_markdown(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()


def parse_sections(lines: list[str]) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current = {
        "heading": "",
        "level": 0,
        "start_line": 1,
        "lines": [],
    }
    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            sections.append(current)
            current = {
                "heading": match.group(2).strip(),
                "level": len(match.group(1)),
                "start_line": index,
                "lines": [],
            }
            continue
        current["lines"].append(line)
    sections.append(current)
    return sections


def heading_matches(heading: str, patterns: list[str]) -> bool:
    heading = heading.strip().lower()
    return any(re.search(pattern, heading, re.IGNORECASE) for pattern in patterns)


def extract_items(
    section: dict[str, object],
    *,
    fallback_paragraphs: bool = True,
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    lines = section["lines"]
    start_line = int(section["start_line"])
    for offset, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()
        match = TASK_RE.match(line) or LIST_ITEM_RE.match(line)
        if match:
            items.append(
                {
                    "line": start_line + offset,
                    "text": match.group(1).strip(),
                    "section": section["heading"] or "(preamble)",
                }
            )
    if items:
        return items

    if not fallback_paragraphs:
        return items

    # Fallback: keep up to the first two substantive lines from the section.
    for offset, raw_line in enumerate(lines, start=1):
        text = raw_line.strip()
        if not text or text.startswith(">") or text.startswith("```"):
            continue
        items.append(
            {
                "line": start_line + offset,
                "text": text,
                "section": section["heading"] or "(preamble)",
            }
        )
        if len(items) >= 2:
            break
    return items


def gather_open_items(paths: list[Path]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        sections = parse_sections(load_markdown(path))
        for section in sections:
            if not heading_matches(str(section["heading"]), OPEN_HEADING_PATTERNS):
                continue
            for item in extract_items(section, fallback_paragraphs=True):
                key = (path.as_posix(), str(item["text"]).lower())
                if key in seen:
                    continue
                seen.add(key)
                found.append(
                    {
                        "file": str(path),
                        "line": item["line"],
                        "section": item["section"],
                        "text": item["text"],
                    }
                )
    return found


def gather_confirmed_candidates(summary_path: Path | None) -> list[dict[str, object]]:
    if summary_path is None or not summary_path.exists():
        return []

    sections = parse_sections(load_markdown(summary_path))
    confirmed: list[dict[str, object]] = []
    seen: set[str] = set()

    for section in sections:
        heading = str(section["heading"])
        if heading_matches(heading, OPEN_HEADING_PATTERNS):
            continue
        if heading_matches(heading, SUMMARY_META_HEADING_PATTERNS):
            continue
        for item in extract_items(section, fallback_paragraphs=False):
            text = str(item["text"]).strip()
            norm = text.lower()
            if not text or norm in seen:
                continue
            seen.add(norm)
            confirmed.append(
                {
                    "file": str(summary_path),
                    "line": item["line"],
                    "section": item["section"],
                    "text": text,
                }
            )
    return confirmed


def gather_conflict_signals(paths: list[Path]) -> list[dict[str, object]]:
    signals: list[dict[str, object]] = []
    for path in paths:
        for line_number, line in enumerate(load_markdown(path), start=1):
            text = line.strip()
            if not text:
                continue
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in CONFLICT_LINE_PATTERNS):
                signals.append(
                    {
                        "file": str(path),
                        "line": line_number,
                        "text": text,
                    }
                )
    return signals


def limit_items(items: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    if limit <= 0:
        return items
    return items[:limit]


def build_scan(root: Path, limit: int) -> dict[str, object]:
    discovered = discover_files(root)
    primary_paths = [
        Path(info["primary"])
        for info in discovered.values()
        if info and isinstance(info, dict) and "primary" in info
    ]
    summary_info = discovered.get("confirmed_summary")
    summary_path = Path(summary_info["primary"]) if isinstance(summary_info, dict) else None

    result = {
        "root": str(root),
        "discovered_files": discovered,
        "confirmed_candidates": limit_items(gather_confirmed_candidates(summary_path), limit),
        "open_items": limit_items(gather_open_items(primary_paths), limit),
        "conflict_signals": limit_items(gather_conflict_signals(primary_paths), limit),
        "notes": [
            "This scan is heuristic and intended for triage.",
            "Confirmed candidates are usually extracted from the confirmed summary file.",
            "Open items and conflict signals should be reviewed before any writeback.",
        ],
    }
    return result


def print_human(scan: dict[str, object]) -> None:
    print(f"Root: {scan['root']}")
    print("")
    print("Discovered files:")
    discovered = scan["discovered_files"]
    for role, info in discovered.items():
        if not info:
            print(f"- {role}: (missing)")
            continue
        print(f"- {role}: {info['primary']}")
        for alt in info["alternates"]:
            print(f"  alt: {alt}")

    def print_bucket(title: str, items: list[dict[str, object]]) -> None:
        print("")
        print(f"{title} ({len(items)}):")
        if not items:
            print("- (none)")
            return
        for item in items:
            location = f"{item['file']}:{item['line']}"
            if "section" in item and item["section"]:
                location += f" [{item['section']}]"
            print(f"- {location} {item['text']}")

    print_bucket("Confirmed candidates", scan["confirmed_candidates"])
    print_bucket("Open items", scan["open_items"])
    print_bucket("Conflict signals", scan["conflict_signals"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a personal dossier directory.")
    parser.add_argument("--root", required=True, help="Path to the personal root directory")
    parser.add_argument("--limit", type=int, default=20, help="Max items per bucket")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human output")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"[ERROR] Root does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"[ERROR] Root is not a directory: {root}", file=sys.stderr)
        return 1

    scan = build_scan(root, args.limit)
    if args.json:
        print(json.dumps(scan, ensure_ascii=False, indent=2))
    else:
        print_human(scan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
