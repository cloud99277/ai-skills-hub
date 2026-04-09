---
name: add-provider
description: Quickly add or update a Codex provider from a base URL and API key. Use when the user wants a fast provider setup or update, gives an OpenAI-compatible endpoint, or asks to make a provider visible in model aliases. Prefer `codex-provider-bootstrap` when the request also includes full bootstrap, alias conventions, or credential persistence details.
---

# Add Provider

Run the script directly.

```bash
python3 scripts/add_provider.py --base-url "https://xxx/v1" --api-key "sk-xxxx"
```

Optional:

```bash
python3 scripts/add_provider.py \
  --base-url "https://xxx/v1" \
  --api-key "sk-xxxx" \
  --name "xxx" \
  --short-alias "cxx"
```

Then run:

```bash
source ~/.bashrc
```
