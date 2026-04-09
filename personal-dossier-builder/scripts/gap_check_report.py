#!/usr/bin/env python3
"""Generate a markdown gap-check report from the personal dossier scan."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

import scan_personal_dossier as scanner

THEMES = [
    (
        "values_tradeoffs",
        "价值观与取舍规则",
        [r"价值观", r"自由", r"公平", r"平等", r"取舍", r"优先级"],
    ),
    (
        "anti_goals_boundaries",
        "反目标与边界",
        [r"不想成为", r"底线", r"不想进入", r"工作环境", r"边界"],
    ),
    (
        "career_route",
        "职业主线与长期方向",
        [r"职业", r"主线", r"北极星", r"岗位", r"主业", r"产品", r"咨询", r"投资"],
    ),
    (
        "energy_system",
        "能量与拖延模式",
        [r"激活", r"消耗", r"拖延", r"进入状态", r"任务"],
    ),
    (
        "risk_boundaries",
        "风险边界",
        [r"风险", r"波动", r"试错", r"暴露"],
    ),
    (
        "life_structure",
        "生活结构与时间分配",
        [r"一周", r"分配", r"时间", r"休息", r"运动", r"陪伴", r"生活"],
    ),
    (
        "public_positioning",
        "对外定位与表达边界",
        [r"定位", r"表达", r"公开", r"出镜", r"品牌"],
    ),
]


def classify_theme(text: str) -> tuple[str, str]:
    for theme_id, label, patterns in THEMES:
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            return theme_id, label
    return ("unclassified", "未归类")


def bucket_open_items(items: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    buckets: dict[str, dict[str, object]] = defaultdict(lambda: {"label": "", "items": []})
    for item in items:
        theme_id, label = classify_theme(str(item["text"]))
        buckets[theme_id]["label"] = label
        buckets[theme_id]["items"].append(item)
    return dict(buckets)


def pick_next_focus(buckets: dict[str, dict[str, object]]) -> tuple[str, dict[str, object]] | None:
    for theme_id, label, _patterns in THEMES:
        bucket = buckets.get(theme_id)
        if bucket and bucket["items"]:
            return (label, bucket)
    bucket = buckets.get("unclassified")
    if bucket and bucket["items"]:
        return ("未归类", bucket)
    return None


def render_file_discovery(discovered: dict[str, dict[str, object] | None]) -> list[str]:
    lines = ["## File Discovery", ""]
    for role, info in discovered.items():
        if not info:
            lines.append(f"- `{role}`: missing")
            continue
        lines.append(f"- `{role}`: `{info['primary']}`")
        for alt in info["alternates"]:
            lines.append(f"  - alternate: `{alt}`")
    lines.append("")
    return lines


def render_bucket(title: str, items: list[dict[str, object]]) -> list[str]:
    lines = [f"### {title}", ""]
    if not items:
        lines.append("- none")
        lines.append("")
        return lines
    for item in items:
        location = f"{item['file']}:{item['line']}"
        section = item.get("section")
        if section:
            location += f" [{section}]"
        lines.append(f"- `{location}` {item['text']}")
    lines.append("")
    return lines


def render_open_themes(buckets: dict[str, dict[str, object]]) -> list[str]:
    lines = ["## Open Themes", ""]
    non_empty = [(bucket["label"], len(bucket["items"])) for bucket in buckets.values() if bucket["items"]]
    if not non_empty:
        lines.append("- none")
        lines.append("")
        return lines
    for label, count in sorted(non_empty, key=lambda item: (-item[1], item[0])):
        lines.append(f"- {label}: {count}")
    lines.append("")
    return lines


def render_next_focus(buckets: dict[str, dict[str, object]]) -> list[str]:
    lines = ["## Highest-Leverage Next Focus", ""]
    choice = pick_next_focus(buckets)
    if not choice:
        lines.append("- no clear next focus from current scan")
        lines.append("")
        return lines
    label, bucket = choice
    lines.append(f"- Theme: {label}")
    lines.append(f"- Reason: this is the highest-priority theme with unresolved items in the current scan.")
    lines.append("- Suggested next questions:")
    for item in bucket["items"][:5]:
        lines.append(f"  - {item['text']}")
    lines.append("")
    return lines


def build_report(root: Path, limit: int) -> str:
    scan = scanner.build_scan(root, limit)
    buckets = bucket_open_items(scan["open_items"])
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    lines = [
        "# Personal Dossier Gap Check",
        "",
        f"- Root: `{root}`",
        f"- Generated: `{timestamp}`",
        f"- Notes: heuristic report for triage, not final truth",
        "",
    ]
    lines.extend(render_file_discovery(scan["discovered_files"]))
    lines.append("## Current Snapshot")
    lines.append("")
    lines.extend(render_bucket("Confirmed Candidates", scan["confirmed_candidates"]))
    lines.extend(render_bucket("Open Items", scan["open_items"]))
    lines.extend(render_bucket("Conflict Signals", scan["conflict_signals"]))
    lines.extend(render_open_themes(buckets))
    lines.extend(render_next_focus(buckets))
    lines.append("## Usage Notes")
    lines.append("")
    lines.append("- Review the report before any writeback.")
    lines.append("- Treat confirmed candidates as starting points, not auto-approved facts.")
    lines.append("- If open items look stale, update the master dossier before the next interview round.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a markdown gap-check report.")
    parser.add_argument("--root", required=True, help="Path to the personal root directory")
    parser.add_argument("--limit", type=int, default=12, help="Max items per bucket")
    parser.add_argument("--output", help="Optional output markdown file path")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"[ERROR] Root does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"[ERROR] Root is not a directory: {root}", file=sys.stderr)
        return 1

    report = build_report(root, args.limit)
    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report + "\n", encoding="utf-8")
        print(f"[OK] Wrote {output_path}")
        return 0

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
