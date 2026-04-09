#!/usr/bin/env python3
"""Add or update a Codex third-party provider + profile aliases.

This script upserts 4 places:
1) ~/.codex/config.toml model_providers block
2) ~/.codex/config.toml profiles block
3) ~/.codex/auth.json API key
4) ~/.bashrc alias codexx-<provider> (and optional short alias)
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def normalize_provider_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9-]", "-", name.strip().lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError("provider name resolved to empty")
    return slug


def infer_provider_name(base_url: str) -> str:
    host = urlparse(base_url).hostname or ""
    if not host:
        raise ValueError(f"invalid base URL: {base_url}")
    first = host.split(".")[0]
    return normalize_provider_name(first)


def ensure_v1_url(base_url: str) -> str:
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    return url


def upsert_provider_block(config_path: Path, provider: str, base_url: str, env_var: str) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

    block = (
        f"[model_providers.{provider}]\n"
        f"name = \"{provider}\"\n"
        f"base_url = \"{base_url}\"\n"
        "wire_api = \"responses\"\n"
        f"api_key_env_var = \"{env_var}\"\n"
    )

    pattern = re.compile(
        rf"(?ms)^\[model_providers\.{re.escape(provider)}\]\n.*?(?=^\[|\Z)"
    )

    if pattern.search(text):
        updated = pattern.sub(block + "\n", text)
    else:
        sep = "\n" if text.endswith("\n") or not text else "\n\n"
        updated = text + sep + block

    config_path.write_text(updated, encoding="utf-8")


def upsert_profile_block(config_path: Path, provider: str, model: str, reasoning_effort: str) -> None:
    text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""

    block = (
        f"[profiles.{provider}]\n"
        f"model = \"{model}\"\n"
        f"model_provider = \"{provider}\"\n"
        f"model_reasoning_effort = \"{reasoning_effort}\"\n"
    )

    pattern = re.compile(
        rf"(?ms)^\[profiles\.{re.escape(provider)}\]\n.*?(?=^\[|\Z)"
    )

    if pattern.search(text):
        updated = pattern.sub(block + "\n", text)
    else:
        sep = "\n" if text.endswith("\n") or not text else "\n\n"
        updated = text + sep + block

    config_path.write_text(updated, encoding="utf-8")


def upsert_auth_key(auth_path: Path, env_var: str, api_key: str) -> None:
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    if auth_path.exists():
        raw = auth_path.read_text(encoding="utf-8").strip()
        data = json.loads(raw) if raw else {}
    else:
        data = {}

    if not isinstance(data, dict):
        raise ValueError(f"unexpected JSON structure in {auth_path}")

    data[env_var] = api_key
    auth_path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def upsert_alias_line(bashrc_path: Path, alias_name: str, alias_value: str) -> None:
    bashrc_path.parent.mkdir(parents=True, exist_ok=True)
    lines = bashrc_path.read_text(encoding="utf-8").splitlines() if bashrc_path.exists() else []

    target = f"alias {alias_name}='{alias_value}'"
    pattern = re.compile(rf"^alias\s+{re.escape(alias_name)}=")

    replaced = False
    new_lines = []
    for line in lines:
        if pattern.match(line):
            if not replaced:
                new_lines.append(target)
                replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        new_lines.append(target)

    bashrc_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Add/update Codex provider and models-visible alias")
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible provider URL")
    parser.add_argument("--api-key", required=True, help="Provider API key")
    parser.add_argument("--name", help="Provider name, default derived from URL host")
    parser.add_argument("--short-alias", help="Optional extra alias, e.g. cxa")
    parser.add_argument("--model", default="gpt-5.4", help="Model for generated profile")
    parser.add_argument(
        "--reasoning-effort",
        default="xhigh",
        help="Reasoning effort for generated profile",
    )
    parser.add_argument("--config", default="~/.codex/config.toml")
    parser.add_argument("--auth", default="~/.codex/auth.json")
    parser.add_argument("--bashrc", default="~/.bashrc")
    args = parser.parse_args()

    base_url = ensure_v1_url(args.base_url)
    provider = normalize_provider_name(args.name) if args.name else infer_provider_name(base_url)
    env_var = f"{provider.upper().replace('-', '_')}_API_KEY"

    config_path = Path(args.config).expanduser()
    auth_path = Path(args.auth).expanduser()
    bashrc_path = Path(args.bashrc).expanduser()

    upsert_provider_block(config_path, provider, base_url, env_var)
    upsert_profile_block(config_path, provider, args.model, args.reasoning_effort)
    upsert_auth_key(auth_path, env_var, args.api_key)

    upsert_alias_line(
        bashrc_path,
        f"codexx-{provider}",
        f"codex --profile {provider} --dangerously-bypass-approvals-and-sandbox",
    )

    if args.short_alias:
        short = normalize_provider_name(args.short_alias).replace("-", "")
        upsert_alias_line(bashrc_path, short, f"codexx-{provider}")

    print(f"provider: {provider}")
    print(f"base_url: {base_url}")
    print(f"env_var: {env_var}")
    print(f"profile: {provider}")
    print(f"model: {args.model}")
    print(f"reasoning_effort: {args.reasoning_effort}")
    print(f"command: codexx-{provider}")
    if args.short_alias:
        print(f"short_alias: {normalize_provider_name(args.short_alias).replace('-', '')}")
    print("run: source ~/.bashrc")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
