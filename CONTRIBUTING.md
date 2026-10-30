# Contributing to Skyflow Skills

This guide is for developers who want to contribute to or extend the Skyflow skills.

## Repository Structure

This repository publishes a single, skills-only plugin to several agent hosts from one source of truth. Each host reads its own manifest, and every manifest points at the same `skills/` directory:

```
/
├── README.md                             # Repo overview and per-host install steps
├── .claude-plugin/
│   └── marketplace.json                  # Claude Code marketplace (lists the skyflow-skills plugin)
├── .cursor-plugin/
│   └── marketplace.json                  # Cursor and Grok Bot marketplace (lists the skyflow-skills plugin)
├── .github/
│   ├── schemas/                          # Vendored Agent Plugins schema used by CI
│   ├── scripts/                          # Validators and the skill packager
│   └── workflows/                        # CI
└── skyflow-skills-plugin/                # Skills plugin (no MCP servers)
    ├── plugin.json                       # Agent Plugins 1.0.0 manifest (vendor-neutral, used by Cursor and Grok Bot)
    ├── .claude-plugin/
    │   └── plugin.json                   # Claude Code manifest
    ├── README.md                         # Plugin docs
    ├── assets/
    │   ├── logo.svg                      # Square logo (referenced by the Cursor marketplace entry)
    │   └── logo.png                      # 1024 × 1024 PNG export of logo.svg for hosts and forms that need a raster image
    └── skills/                           # Agent Skills
        ├── call-rest-apis/
        │   └── SKILL.md
        ├── create-vault/
        │   └── SKILL.md
        ├── get-started/
        │   └── SKILL.md
        ├── inventory-sensitive-data/
        │   └── SKILL.md
        ├── migrate-sdk-v1-to-v2/
        │   └── SKILL.md
        ├── plan-skyflow-implementation/
        │   └── SKILL.md
        ├── quickstart-js-browser/
        │   └── SKILL.md
        └── quickstart-node/
            └── SKILL.md
```

This repo contains skills only. The Skyflow MCP server plugins for Claude Code are maintained separately in the [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude) marketplace so that skills and MCP servers can be reviewed, authorized, and versioned independently.

## Standards

The repo follows two open standards wherever a host allows it:

1. **[Agent Skills](https://agentskills.io/specification)** governs every `SKILL.md`. Frontmatter may only use the fields that spec defines (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`).
2. **[Agent Plugins 1.0.0](https://agent-plugins.org/specification)** governs `skyflow-skills-plugin/plugin.json`. Its schema is closed, so host-specific fields such as a logo or display name belong in that host's own manifest or marketplace entry instead.

Skill text must not assume a particular host. Refer to "the agent" rather than a product name, and when a step depends on where the agent runs (for example a local shell profile versus a hosted machine) cover both cases.

## Manifests

| File | Host | Notes |
| ---- | ---- | ----- |
| `skyflow-skills-plugin/plugin.json` | Agent Plugins hosts, Cursor, Grok Bot | Source of truth for `name`, `version`, `description`, `author`, and `license` |
| `skyflow-skills-plugin/.claude-plugin/plugin.json` | Claude Code | Must match the fields above |
| `.claude-plugin/marketplace.json` | Claude Code | `name` is `skyflow-skills-marketplace`. It must stay distinct from the `skyflow-marketplace` in `SkyflowFoundry/claude` because Claude Code registers only one marketplace per name. |
| `.cursor-plugin/marketplace.json` | Cursor, Grok Bot | Lets the hosts find the plugin in its subdirectory when you paste the repo link. Its entry also carries the `logo` because the Agent Plugins schema has no logo field. The path is relative to the plugin directory. |

In both marketplace files, each plugin entry's `name` must match the plugin manifest, `source` is a path relative to the repository root (`./skyflow-skills-plugin`), and `description` must match the plugin manifest. CI enforces all of this with `.github/scripts/validate-manifests.py`.

Each plugin also carries its own `README.md` at its root documenting installation; the root [README.md](README.md) is an overview that links to it.

### Logo

`skyflow-skills-plugin/assets/logo.svg` is the official white Skyflow wordmark from the brand kit centered on a `#403E6B` square plate. If you change it, re-export the PNG so the two stay identical:

```sh
magick -background none -density 288 skyflow-skills-plugin/assets/logo.svg -resize 1024x1024 -depth 8 -strip skyflow-skills-plugin/assets/logo.png
```

## Adding New Skills

Skills are guided workflows that help an agent assist users with Skyflow tasks. They provide structured documentation, examples, and references that the agent can use when helping users implement features.

### Skill Directory Structure

Create a new directory in `skyflow-skills-plugin/skills/` with the following structure:

```
skyflow-skills-plugin/skills/your-skill-name/
├── SKILL.md                    # Main skill file (required)
├── supporting-doc.md           # Additional documentation (optional)
├── samples/                    # Sample files (optional)
│   ├── example-1.json
│   └── example-2.json
└── schemas/                    # Validation schemas (optional)
    └── schema.json
```

### SKILL.md Format

The main skill file must include a YAML frontmatter header followed by the skill content:

```markdown
---
name: your-skill-name
description: Brief description of what the skill helps users accomplish.
---

# Skill Title

Overview paragraph explaining the purpose.

## Prerequisites
## Step 1: First Step
## Step 2: Second Step
...
## Troubleshooting
## Related Documentation
```

### Best Practices

#### Structure and Organization

- Keep the skill name lowercase with hyphens (e.g., `create-vault`, `detect-pii`)
- Start with an Overview section explaining what the skill accomplishes
- Include a Prerequisites section with required accounts, tokens, and tools
- Use numbered steps for the main workflow
- End with Troubleshooting and Related Documentation sections

#### API-First Approach

- Prefer API examples over Studio UI instructions where possible
- Include complete, copy-pastable curl commands with environment variables
- Document required environment variables at the start
- Note explicitly when Studio UI is required for certain operations

#### Documentation Quality

- Use tables for reference information (data types, tag values, templates)
- Include realistic examples showing complete configurations
- Link to supporting documentation files for detailed references
- Keep the main SKILL.md scannable; put comprehensive details in supporting docs

#### Supporting Files

- Place sample schemas/configs in a `samples/` or descriptive subdirectory
- Include validation schemas (JSONSchema) when applicable
- Use relative links to reference supporting files from SKILL.md
- Provide samples for common use cases (e.g., quickstart, payment, PII)

#### Example Field Configuration

When documenting configurable options, show a complete example:

```json
{
  "name": "email",
  "datatype": "DT_STRING",
  "tags": [
    { "name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"] },
    { "name": "skyflow.options.default_dlp_policy", "values": ["MASK"] },
    { "name": "skyflow.validation.regular_exp", "values": ["^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"] }
  ]
}
```

### Updating the README

After creating a new skill, add it to the Skills section in the plugin [README.md](skyflow-skills-plugin/README.md):

1. Add a subsection with the skill name as a heading
2. Write a paragraph describing what the skill does and its key features
3. Add a row to the skills table

## Packaging and Releasing Skills

Skills are distributed two ways from a single source of truth (the directories under `skyflow-skills-plugin/skills/`):

1. **Plugin** — installed through each host's marketplace or plugin settings (see the [README](README.md#supported-hosts)).
2. **Standalone zips** — one portable `.zip` per skill, published as GitHub Release assets for use in other projects or harnesses.

The zips are build artifacts. They are **not** committed to the repo (`dist/` is gitignored), so the plugin/marketplace install is never affected.

### CI workflows

- **`.github/workflows/validate-skills.yml`** — runs on pull requests that touch the plugin, the manifests, or the validators. It checks every `SKILL.md` has valid Agent Skills frontmatter (`name` matches the directory, lowercase-hyphen, ≤64 chars; `description` present, ≤1024 chars; no fields outside the spec). It also validates `plugin.json` against the Agent Plugins schema and checks that every manifest agrees on name, version, description, author, and license.
- **`.github/workflows/package-skills.yml`** — runs on a pushed version tag (`v*`) or manual dispatch. It validates, zips each skill into `dist/<skill>.zip`, generates `dist/SHA256SUMS.txt`, and attaches everything to the matching GitHub Release.

### Cutting a release

1. Bump `version` in `skyflow-skills-plugin/plugin.json`, `skyflow-skills-plugin/.claude-plugin/plugin.json`, and `metadata.version` in `.cursor-plugin/marketplace.json`. CI fails if they disagree.
2. Tag and push: `git tag v0.6.0 && git push origin v0.6.0`. The package workflow creates the release and uploads the zips automatically.

Alternatively, trigger the **Package skills** workflow manually (Actions tab → *Run workflow*); it defaults the tag to `v<plugin.json version>`.

### Building locally

```sh
pip install pyyaml jsonschema
python3 .github/scripts/validate-skills.py      # validate skill frontmatter
python3 .github/scripts/validate-manifests.py   # validate and cross-check manifests
bash    .github/scripts/package-skills.sh        # build dist/*.zip + SHA256SUMS.txt
```

## Learn More

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Plugins specification](https://agent-plugins.org/specification)
- [Claude Code plugins documentation](https://code.claude.com/docs/en/plugins)
- [Cursor plugins documentation](https://cursor.com/docs/plugins)
