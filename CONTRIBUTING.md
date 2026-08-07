# Contributing to Skyflow Skills for Claude Code

This guide is for developers who want to contribute to or extend the Skyflow skills.

## Repository Structure

This repository is a Claude Code plugin marketplace that publishes a single, skills-only plugin:

```
/
├── README.md                             # Marketplace overview
├── .claude-plugin/
│   └── marketplace.json                  # Marketplace configuration (lists the skyflow-skills plugin)
└── skyflow-skills-plugin/                # Skills plugin (no MCP servers)
    ├── .claude-plugin/
    │   └── plugin.json                   # Plugin metadata
    ├── README.md                         # Plugin docs
    └── skills/                           # Agent skills
        ├── call-rest-apis/
        │   └── SKILL.md
        ├── create-vault/
        │   └── SKILL.md
        ├── get-started/
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

This marketplace contains skills only. The Skyflow MCP server plugins are maintained separately in the [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude) marketplace so that skills and MCP servers can be reviewed, authorized, and versioned independently.

## Marketplace Configuration

The `.claude-plugin/marketplace.json` file at the root defines the marketplace and lists available plugins:

- `name`: The marketplace identifier (`skyflow-skills-marketplace`). This must be distinct from the `skyflow-marketplace` in `SkyflowFoundry/claude`, because Claude Code registers only one marketplace per name.
- `owner`: Marketplace owner information
- `plugins`: Array of plugin definitions with name, source path, and description. This marketplace lists a single plugin: `skyflow-skills`.

A plugin's `name` must match the `name` in its own `.claude-plugin/plugin.json`, and `source` is a path relative to the repository root (e.g. `./skyflow-skills-plugin`).

## Plugin Structure

The `skyflow-skills-plugin/` directory is a standard skills plugin:

- `.claude-plugin/plugin.json`: Plugin metadata (name, version, author, description)
- `skills/`: Agent skills, each in its own directory with a `SKILL.md` file

Each plugin also carries its own `README.md` at its root documenting installation; the root [README.md](README.md) is a marketplace overview that links to it.

A plugin only requires `.claude-plugin/plugin.json`. (`commands/`, `agents/`, and `hooks/` are also supported by Claude Code but are not currently used in this repo.)

## Adding New Skills

Skills are guided workflows that help Claude assist users with Skyflow tasks. They provide structured documentation, examples, and references that Claude can use when helping users implement features.

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

1. **Plugin** — installed via the marketplace (`/plugin install skyflow-skills@skyflow-skills-marketplace`).
2. **Standalone zips** — one portable `.zip` per skill, published as GitHub Release assets for use in other projects or harnesses.

The zips are build artifacts. They are **not** committed to the repo (`dist/` is gitignored), so the plugin/marketplace install is never affected.

### CI workflows

- **`.github/workflows/validate-skills.yml`** — runs on pull requests that touch skills. It checks every `SKILL.md` has valid frontmatter (`name` matches the directory, lowercase-hyphen, ≤64 chars; `description` present, ≤1024 chars).
- **`.github/workflows/package-skills.yml`** — runs on a pushed version tag (`v*`) or manual dispatch. It validates, zips each skill into `dist/<skill>.zip`, generates `dist/SHA256SUMS.txt`, and attaches everything to the matching GitHub Release.

### Cutting a release

1. Bump `version` in `skyflow-skills-plugin/.claude-plugin/plugin.json`.
2. Tag and push: `git tag v0.6.0 && git push origin v0.6.0`. The package workflow creates the release and uploads the zips automatically.

Alternatively, trigger the **Package skills** workflow manually (Actions tab → *Run workflow*); it defaults the tag to `v<plugin.json version>`.

### Building locally

```sh
python3 .github/scripts/validate-skills.py   # validate frontmatter
bash   .github/scripts/package-skills.sh      # build dist/*.zip + SHA256SUMS.txt
```

## Learn More

For complete documentation on Claude Code plugins, see the [Claude Code Plugins documentation](https://code.claude.com/docs/en/plugins).
