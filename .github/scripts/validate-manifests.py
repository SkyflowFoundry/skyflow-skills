#!/usr/bin/env python3
"""Validate the plugin and marketplace manifests for every supported host.

The plugin ships one manifest per host format:

- skyflow-skills-plugin/plugin.json             Agent Plugins 1.0.0 (vendor-neutral)
- skyflow-skills-plugin/.claude-plugin/plugin.json   Claude Code
- .claude-plugin/marketplace.json               Claude Code marketplace
- .cursor-plugin/marketplace.json               Cursor and Grok Bot marketplace

The Agent Plugins manifest is checked against the vendored 1.0.0 schema. The
other manifests must agree with it on the fields they share so that a version
bump or rename can't land in one host and miss the others.

Exit code 0 = all valid, 1 = one or more problems (details printed).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

PLUGIN_DIR = Path("skyflow-skills-plugin")
AGENT_PLUGIN = PLUGIN_DIR / "plugin.json"
CLAUDE_PLUGIN = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
CLAUDE_MARKETPLACE = Path(".claude-plugin/marketplace.json")
CURSOR_MARKETPLACE = Path(".cursor-plugin/marketplace.json")
SCHEMA = Path(".github/schemas/agent-plugins-1.0.0-plugin.schema.json")

# Fields that every plugin manifest must keep identical to plugin.json.
SHARED_FIELDS = ("name", "version", "description", "author", "license")


def load(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: missing")
        return None
    except json.JSONDecodeError as e:
        errors.append(f"{path}: invalid JSON ({e})")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path}: top level must be a JSON object")
        return None
    return data


def check_marketplace(path: Path, plugin: dict, errors: list[str]) -> None:
    market = load(path, errors)
    if market is None:
        return
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin["name"]]
    if len(entries) != 1:
        errors.append(f"{path}: expected one entry named `{plugin['name']}`, found {len(entries)}")
        return
    entry = entries[0]
    source = entry.get("source")
    if not isinstance(source, str) or Path(source).resolve() != PLUGIN_DIR.resolve():
        errors.append(f"{path}: `{plugin['name']}` source must be `./{PLUGIN_DIR}`")
    if entry.get("description") != plugin.get("description"):
        errors.append(f"{path}: `{plugin['name']}` description differs from {AGENT_PLUGIN}")
    logo = entry.get("logo")
    if isinstance(logo, str) and not logo.startswith(("http://", "https://")):
        if not (PLUGIN_DIR / logo).is_file():
            errors.append(f"{path}: `{plugin['name']}` logo `{logo}` not found under {PLUGIN_DIR}")
    version = market.get("metadata", {}).get("version")
    if version is not None and version != plugin.get("version"):
        errors.append(f"{path}: metadata.version `{version}` differs from {AGENT_PLUGIN}")


def main() -> int:
    errors: list[str] = []

    schema = load(SCHEMA, errors)
    plugin = load(AGENT_PLUGIN, errors)
    if schema is not None and plugin is not None:
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(plugin), key=str):
            where = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{AGENT_PLUGIN}: {where}: {err.message}")

    claude = load(CLAUDE_PLUGIN, errors)
    if plugin is not None and claude is not None:
        for field in SHARED_FIELDS:
            if claude.get(field) != plugin.get(field):
                errors.append(f"{CLAUDE_PLUGIN}: `{field}` differs from {AGENT_PLUGIN}")

    if plugin is not None and isinstance(plugin.get("name"), str):
        check_marketplace(CLAUDE_MARKETPLACE, plugin, errors)
        check_marketplace(CURSOR_MARKETPLACE, plugin, errors)

    if errors:
        print("Manifest validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"All manifests valid and in sync ({plugin['name']} {plugin.get('version')}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
