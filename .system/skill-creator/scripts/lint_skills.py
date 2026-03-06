#!/usr/bin/env python3
"""
Repository-wide linting for skill definitions.

This script complements quick_validate.py:
- quick_validate.py: single skill, structural checks only
- lint_skills.py: repository or directory scan, structural + semantic checks
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
DEFAULT_ROOT = Path(__file__).resolve().parents[3]

COMPAT_ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}
STRICT_ALLOWED_PROPERTIES = {"name", "description"}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(?:\n|$)", re.DOTALL)

DESCRIPTION_OLD_PATTERNS = [
    (
        re.compile(r"\bUse only when\b"),
        "description_old_phrase",
        'description should prefer "Use when ... Not for ..." over "Use only when"',
    ),
    (
        re.compile(r"\bUse this\b"),
        "description_old_phrase",
        'description should avoid "Use this ..." phrasing and start with a capability summary',
    ),
    (
        re.compile(r"\bUse for\b"),
        "description_old_phrase",
        'description should prefer "Use when ..." over "Use for ..."',
    ),
    (
        re.compile(r"\bTriggers when\b"),
        "description_old_phrase",
        'description should avoid "Triggers when ..." and use a standard "Use when ..." form',
    ),
]

BODY_GLOBAL_PATTERNS = [
    (
        re.compile(r"/verify"),
        "body_legacy_command",
        'body contains legacy command reference "/verify"',
    ),
    (
        re.compile(r"This skill should be used whenever"),
        "body_old_trigger_phrase",
        'body contains old trigger phrasing "This skill should be used whenever"',
    ),
    (
        re.compile(r"Triggers when"),
        "body_old_trigger_phrase",
        'body contains old trigger phrasing "Triggers when"',
    ),
]


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int | None = None


@dataclass
class SkillResult:
    name: str
    path: str
    issues: list[Issue] = field(default_factory=list)

    @property
    def status(self) -> str:
        if any(issue.severity == "error" for issue in self.issues):
            return "ERROR"
        if any(issue.severity == "warning" for issue in self.issues):
            return "WARN"
        return "OK"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lint skill frontmatter and routing quality across a skill repository."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help="Root directory or SKILL.md file to lint (default: current skills repository).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use strict frontmatter validation (name + description only).",
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Show only skills with structural errors.",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Return non-zero when warnings are present.",
    )
    parser.add_argument(
        "--include-body-checks",
        dest="include_body_checks",
        action="store_true",
        help="Enable body consistency checks (default).",
    )
    parser.add_argument(
        "--no-body-checks",
        dest="include_body_checks",
        action="store_false",
        help="Disable body consistency checks.",
    )
    parser.set_defaults(include_body_checks=True)
    return parser.parse_args()


def line_number(content: str, match_start: int, base_line: int = 1) -> int:
    return base_line + content.count("\n", 0, match_start)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> tuple[dict | None, str | None, int | None, Issue | None]:
    if not content.startswith("---"):
        return None, None, None, Issue("error", "missing_frontmatter", "No YAML frontmatter found", 1)

    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None, None, Issue("error", "invalid_frontmatter", "Invalid frontmatter format", 1)

    frontmatter_text = match.group(1)
    body = content[match.end() :]
    body_start_line = content.count("\n", 0, match.end()) + 1
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as exc:
        return None, body, body_start_line, Issue(
            "error", "invalid_yaml", f"Invalid YAML in frontmatter: {exc}", 2
        )

    if not isinstance(frontmatter, dict):
        return None, body, body_start_line, Issue(
            "error",
            "invalid_frontmatter_type",
            "Frontmatter must be a YAML dictionary",
            2,
        )

    return frontmatter, body, body_start_line, None


def validate_name(name: object) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(name, str):
        return [Issue("error", "invalid_name_type", f"Name must be a string, got {type(name).__name__}")]

    normalized = name.strip()
    if not normalized:
        return [Issue("error", "empty_name", "Name cannot be empty")]

    if not re.fullmatch(r"[a-z0-9-]+", normalized):
        issues.append(
            Issue(
                "error",
                "invalid_name_format",
                f"Name '{normalized}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        )
    if normalized.startswith("-") or normalized.endswith("-") or "--" in normalized:
        issues.append(
            Issue(
                "error",
                "invalid_name_hyphen_usage",
                f"Name '{normalized}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        )
    if len(normalized) > MAX_SKILL_NAME_LENGTH:
        issues.append(
            Issue(
                "error",
                "name_too_long",
                f"Name is too long ({len(normalized)} characters). Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )
        )
    if "todo" in normalized.lower():
        issues.append(Issue("error", "template_placeholder", "Name contains a TODO-style placeholder"))
    return issues


def validate_description(description: object) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(description, str):
        return [
            Issue(
                "error",
                "invalid_description_type",
                f"Description must be a string, got {type(description).__name__}",
            )
        ]

    normalized = description.strip()
    if not normalized:
        return [Issue("error", "empty_description", "Description cannot be empty")]

    if "<" in normalized or ">" in normalized:
        issues.append(Issue("error", "invalid_description_chars", "Description cannot contain angle brackets"))
    if len(normalized) > MAX_DESCRIPTION_LENGTH:
        issues.append(
            Issue(
                "error",
                "description_too_long",
                f"Description is too long ({len(normalized)} characters). Maximum is {MAX_DESCRIPTION_LENGTH} characters.",
            )
        )
    if "todo" in normalized.lower():
        issues.append(Issue("error", "template_placeholder", "Description contains a TODO-style placeholder"))
    return issues


def lint_description(description: str) -> list[Issue]:
    issues: list[Issue] = []
    if not re.search(r"\bUse when\b", description) and not re.search(
        r"\bwhen the user (asks?|needs|wants)\b", description
    ):
        issues.append(
            Issue(
                "warning",
                "description_missing_use_when",
                'Description should use a standard "Use when ..." routing phrase',
            )
        )
    if description.startswith("Use when") or description.startswith("Use this") or description.startswith("When "):
        issues.append(
            Issue(
                "warning",
                "description_missing_capability_first",
                "Description should begin with the core capability before the routing clause",
            )
        )
    for pattern, code, message in DESCRIPTION_OLD_PATTERNS:
        if pattern.search(description):
            issues.append(Issue("warning", code, message))
    if len(description) > 450:
        issues.append(
            Issue(
                "warning",
                "description_long",
                "Description is long enough that it may be acting like a mini-spec instead of routing metadata",
            )
        )
    return dedupe_issues(issues)


def lint_body(skill_name: str, body: str, body_start_line: int) -> list[Issue]:
    issues: list[Issue] = []
    for pattern, code, message in BODY_GLOBAL_PATTERNS:
        match = pattern.search(body)
        if match:
            issues.append(Issue("warning", code, message, line_number(body, match.start(), body_start_line)))

    if skill_name == "codex-cli-trigger":
        for pattern in (
            re.compile(r"(?m)^\s*-\s*GPT"),
            re.compile(r"OpenAI、openai"),
            re.compile(r"让 GPT/Codex/OpenAI 来做"),
        ):
            match = pattern.search(body)
            if match:
                issues.append(
                    Issue(
                        "warning",
                        "body_generic_model_trigger",
                        "Body still includes generic GPT/OpenAI trigger wording that may cause over-routing",
                        line_number(body, match.start(), body_start_line),
                    )
                )
                break

    if skill_name == "gemini-cli-trigger":
        for pattern in (
            re.compile(r"Google AI、Google"),
            re.compile(r"Gemini/Google AI"),
        ):
            match = pattern.search(body)
            if match:
                issues.append(
                    Issue(
                        "warning",
                        "body_generic_model_trigger",
                        "Body still includes generic Google AI trigger wording that may cause over-routing",
                        line_number(body, match.start(), body_start_line),
                    )
                )
                break

    if skill_name == "baoyu-slide-deck":
        for phrase in ("reading and sharing", "social media sharing"):
            idx = body.find(phrase)
            if idx != -1:
                issues.append(
                    Issue(
                        "warning",
                        "body_outdated_scope",
                        "Body still contains older share-first positioning instead of the newer image-first deck boundary",
                        line_number(body, idx, body_start_line),
                    )
                )
                break

    if skill_name == "baoyu-html-deck":
        if not re.search(r"##\s*(何时使用|When to Use)", body):
            issues.append(
                Issue(
                    "warning",
                    "body_missing_use_section",
                    "Body is missing a clear routing section such as '何时使用' or 'When to Use'",
                )
            )

    if skill_name == "baoyu-post-to-wechat" and "Publish-only guard" not in body:
        issues.append(
            Issue(
                "warning",
                "body_missing_publish_guard",
                "Body should explicitly guard publish-only usage and redirect conversion-only tasks",
            )
        )

    if skill_name == "continuous-learning":
        phrase = "Setting up automatic pattern extraction from Claude Code sessions"
        idx = body.find(phrase)
        if idx != -1:
            issues.append(
                Issue(
                    "warning",
                    "body_legacy_scope_conflict",
                    "Body still presents the v1 workflow as a default setup path instead of a legacy workflow",
                    line_number(body, idx, body_start_line),
                )
            )

    if skill_name == "project-guidelines-example":
        phrase = "Reference this skill when working on the specific project it's designed for."
        idx = body.find(phrase)
        if idx != -1:
            issues.append(
                Issue(
                    "warning",
                    "body_template_scope_conflict",
                    "Body still frames this example as live project guidance instead of a template",
                    line_number(body, idx, body_start_line),
                )
            )

    if skill_name == "eval-harness":
        for phrase in (
            "Claude Code sessions",
            "Test if Claude can do something it couldn't before:",
            "Use Claude to evaluate open-ended outputs:",
        ):
            idx = body.find(phrase)
            if idx != -1:
                issues.append(
                    Issue(
                        "warning",
                        "body_product_specific_scope",
                        "Body still uses overly Claude-specific wording instead of prompt/agent/workflow language",
                        line_number(body, idx, body_start_line),
                    )
                )
                break

    return dedupe_issues(issues)


def dedupe_issues(issues: list[Issue]) -> list[Issue]:
    seen: set[tuple[str, str, str, int | None]] = set()
    result: list[Issue] = []
    for issue in issues:
        key = (issue.severity, issue.code, issue.message, issue.line)
        if key not in seen:
            seen.add(key)
            result.append(issue)
    return result


def collect_skill_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.name == "SKILL.md" else []

    if not target.exists():
        return []

    unique_paths: dict[Path, Path] = {}
    for path in target.rglob("SKILL.md"):
        try:
            unique_paths[path.resolve()] = path
        except OSError:
            unique_paths[path] = path
    return sorted(unique_paths.values())


def lint_skill_file(skill_md: Path, strict: bool, include_body_checks: bool) -> SkillResult:
    result = SkillResult(name=skill_md.parent.name, path=str(skill_md))

    try:
        content = read_text(skill_md)
    except OSError as exc:
        result.issues.append(Issue("error", "read_error", f"Failed to read SKILL.md: {exc}"))
        return result

    frontmatter, body, body_start_line, parse_error = parse_frontmatter(content)
    if parse_error:
        result.issues.append(parse_error)
        return result

    assert frontmatter is not None
    assert body is not None
    assert body_start_line is not None

    allowed = STRICT_ALLOWED_PROPERTIES if strict else COMPAT_ALLOWED_PROPERTIES
    unexpected = sorted(set(frontmatter.keys()) - allowed)
    if unexpected:
        result.issues.append(
            Issue(
                "error",
                "unexpected_frontmatter_keys",
                f"Unexpected frontmatter key(s): {', '.join(unexpected)}. Allowed: {', '.join(sorted(allowed))}",
            )
        )

    if "name" not in frontmatter:
        result.issues.append(Issue("error", "missing_name", "Missing 'name' in frontmatter"))
    else:
        result.issues.extend(validate_name(frontmatter["name"]))

    if "description" not in frontmatter:
        result.issues.append(Issue("error", "missing_description", "Missing 'description' in frontmatter"))
    else:
        result.issues.extend(validate_description(frontmatter["description"]))

    if any(issue.severity == "error" for issue in result.issues):
        if isinstance(frontmatter.get("name"), str):
            result.name = frontmatter["name"].strip() or result.name
        result.issues = dedupe_issues(result.issues)
        return result

    skill_name = str(frontmatter["name"]).strip()
    result.name = skill_name
    description = str(frontmatter["description"]).strip()

    result.issues.extend(lint_description(description))
    if include_body_checks:
        result.issues.extend(lint_body(skill_name, body, body_start_line))

    result.issues = dedupe_issues(result.issues)
    return result


def summary(results: list[SkillResult]) -> tuple[int, int]:
    error_count = sum(1 for result in results if any(issue.severity == "error" for issue in result.issues))
    warning_count = sum(
        1
        for result in results
        if not any(issue.severity == "error" for issue in result.issues)
        and any(issue.severity == "warning" for issue in result.issues)
    )
    return error_count, warning_count


def render_text(results: list[SkillResult], errors_only: bool) -> str:
    lines: list[str] = []
    scanned = len(results)
    error_count, warning_count = summary(results)
    lines.append(f"Scanned {scanned} skills: {error_count} error(s), {warning_count} warning group(s)")

    for result in results:
        if errors_only and result.status != "ERROR":
            continue
        lines.append(f"[{result.status}] {result.name}")
        if not result.issues:
            continue
        for issue in result.issues:
            prefix = f"{issue.severity.upper()} {issue.code}"
            if issue.line is not None:
                lines.append(f"  - {prefix} (line {issue.line}): {issue.message}")
            else:
                lines.append(f"  - {prefix}: {issue.message}")
    return "\n".join(lines)


def render_json(results: list[SkillResult], errors_only: bool) -> str:
    filtered = [
        result
        for result in results
        if not errors_only or any(issue.severity == "error" for issue in result.issues)
    ]
    scanned = len(results)
    error_count, warning_count = summary(results)
    payload = {
        "scanned": scanned,
        "errors": error_count,
        "warnings": warning_count,
        "skills": [
            {
                "name": result.name,
                "path": result.path,
                "status": result.status,
                "issues": [asdict(issue) for issue in result.issues],
            }
            for result in filtered
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main() -> int:
    args = parse_args()
    target = Path(args.path).expanduser().resolve()
    skill_files = collect_skill_files(target)

    if not skill_files:
        print(f"No SKILL.md files found under {target}", file=sys.stderr)
        return 1

    results = [
        lint_skill_file(skill_md, strict=args.strict, include_body_checks=args.include_body_checks)
        for skill_md in skill_files
    ]

    if args.format == "json":
        print(render_json(results, args.errors_only))
    else:
        print(render_text(results, args.errors_only))

    has_error = any(any(issue.severity == "error" for issue in result.issues) for result in results)
    has_warning = any(any(issue.severity == "warning" for issue in result.issues) for result in results)

    if has_error:
        return 1
    if args.fail_on_warnings and has_warning:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
