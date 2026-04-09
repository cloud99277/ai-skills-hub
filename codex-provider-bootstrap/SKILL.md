---
name: codex-provider-bootstrap
description: Fully bootstrap a Codex local provider from an OpenAI-compatible endpoint, including alias setup and credential persistence in `~/.codex/auth.json`. Use when the user wants to add or switch a provider and also needs durable local configuration, `codexx-*` model aliases, or a complete bootstrap flow rather than a quick one-off update.
---

# Codex Provider Bootstrap

Run the automation script and avoid manual editing unless repair is needed.

## Workflow

1. Collect inputs:
- Required: `base_url`, `api_key`
- Optional: `provider_name` (auto-derived from URL host if omitted), `short_alias`

2. Run script:
```bash
python3 scripts/add_provider.py \
  --base-url "https://arena.exe.xyz/v1" \
  --api-key "sk-xxxx" \
  --name "arena" \
  --short-alias "cxa"
```

3. Confirm results:
- Provider block exists in `~/.codex/config.toml`
- Env key exists in `~/.codex/auth.json`
- Alias `codexx-<name>` exists in `~/.bashrc`
- `models` command can display it (it reads `alias codexx-...`)

4. Apply shell changes:
```bash
source ~/.bashrc
```

## Default decisions

- Infer `provider_name` from URL hostname first label (for example `arena` from `arena.exe.xyz`).
- Write provider with `wire_api = "responses"`.
- Store key as `<PROVIDER>_API_KEY` in `~/.codex/auth.json` where provider name is uppercased and `-` becomes `_`.
- Add `alias codexx-<name>='codex --local-provider <name> --dangerously-bypass-approvals-and-sandbox'`.
- If `--short-alias` is provided, add `alias <short_alias>='codexx-<name>'`.

## Repair Mode

If files already contain the provider, run the script again. It performs upsert for:
- `[model_providers.<name>]` block in `config.toml`
- Key entry in `auth.json`
- Alias lines in `.bashrc`
