#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
from pathlib import Path

HISTORY_FILE = Path.home() / ".codex" / "history.jsonl"
KEY_RE = re.compile(r"sk-[A-Za-z0-9_-]+")


def mask_text(text: str, max_len: int) -> str:
    masked = KEY_RE.sub("sk-***", (text or "").replace("\n", " ").strip())
    masked = re.sub(r"\s+", " ", masked)
    if len(masked) > max_len:
        return masked[: max_len - 3] + "..."
    return masked


def parse_history(path: Path):
    rows = []
    if not path.exists():
        raise FileNotFoundError(f"history file not found: {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            rows.append(obj)
        except json.JSONDecodeError:
            continue
    return rows


def fmt_ts(ts):
    try:
        ts_int = int(ts)
        return dt.datetime.fromtimestamp(ts_int, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    except Exception:
        return "invalid-ts"


def print_rows(rows, max_len=140, start_index=1):
    for i, row in enumerate(rows, start=start_index):
        ts = fmt_ts(row.get("ts"))
        sid = row.get("session_id", "")
        text = mask_text(row.get("text", ""), max_len)
        print(f"[{i:02d}] [{ts}] [{sid}] {text}")


def parse_utc_timestamp(s: str) -> int:
    # Expected format: YYYY-MM-DD HH:MM:SSZ
    t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%SZ")
    return int(t.replace(tzinfo=dt.timezone.utc).timestamp())


def cmd_recent(args):
    rows = parse_history(HISTORY_FILE)
    limit = max(1, args.limit)
    subset = rows[-limit:]
    print_rows(subset, max_len=args.max_len, start_index=1)


def cmd_around(args):
    rows = parse_history(HISTORY_FILE)
    target_ts = parse_utc_timestamp(args.timestamp)

    idx = None
    for i, row in enumerate(rows):
        try:
            if int(row.get("ts", -1)) == target_ts:
                idx = i
                break
        except Exception:
            continue

    if idx is None:
        print(f"timestamp not found: {args.timestamp}")
        return

    left = max(0, idx - max(0, args.before))
    right = min(len(rows), idx + max(0, args.after) + 1)
    window = rows[left:right]
    print_rows(window, max_len=args.max_len, start_index=left + 1)


def main():
    parser = argparse.ArgumentParser(description="Query Codex local conversation history")
    sub = parser.add_subparsers(dest="command", required=True)

    p_recent = sub.add_parser("recent", help="Show recent records")
    p_recent.add_argument("--limit", type=int, default=20)
    p_recent.add_argument("--max-len", type=int, default=140)
    p_recent.set_defaults(func=cmd_recent)

    p_around = sub.add_parser("around", help="Show records around exact UTC timestamp")
    p_around.add_argument("--timestamp", required=True, help='UTC timestamp, e.g. "2026-03-03 15:12:09Z"')
    p_around.add_argument("--before", type=int, default=4)
    p_around.add_argument("--after", type=int, default=6)
    p_around.add_argument("--max-len", type=int, default=180)
    p_around.set_defaults(func=cmd_around)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
