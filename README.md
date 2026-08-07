# Skyflow Skills for Claude Code

> [!WARNING]
> This is an experimental project in development. This project is not supported and offered under an MIT license.

A Claude Code plugin marketplace that publishes Skyflow's **skills** — guided workflows for getting started, vault creation, REST API guidance, SDK migration, implementation planning, and SDK quickstarts.

This marketplace contains **skills only**. It ships no MCP servers, opens no network connections, and requires no environment variables or credentials — which makes it straightforward to review and allowlist. The Skyflow MCP servers live in a separate marketplace, [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude).

- [Skyflow Skills for Claude Code](#skyflow-skills-for-claude-code)
  - [What's in this marketplace](#whats-in-this-marketplace)
  - [Quick Start](#quick-start)
  - [Standalone Skill Downloads](#standalone-skill-downloads)
  - [For administrators: allowlisting this marketplace](#for-administrators-allowlisting-this-marketplace)
  - [Looking for the MCP servers?](#looking-for-the-mcp-servers)
  - [Learn More](#learn-more)
  - [Contributing](#contributing)

## What's in this marketplace

| Plugin | What it does | Environment variables | Docs |
| ------ | ------------ | --------------------- | ---- |
| `skyflow-skills` | Guided Skyflow workflows (getting started, vault creation, REST API guidance, SDK migration, implementation planning, SDK quickstarts) | None | [README](skyflow-skills-plugin/README.md) |

## Quick Start

> **Note:** You must have Claude Code installed first. If you haven't installed it yet, see the [Claude Code installation guide](https://code.claude.com/docs/en/overview).

1. Open Claude Code:

   ```sh
   claude
   ```

2. Add the marketplace:

   ```sh
   /plugin marketplace add SkyflowFoundry/skyflow-skills
   ```

3. Install the skills plugin:

   ```sh
   /plugin install skyflow-skills@skyflow-skills-marketplace
   ```

The `skyflow-skills` plugin needs no environment variables. Each skill is available as a slash command in the form `/skyflow-skills:<skill-name>`, and Claude also invokes the relevant skill automatically when it fits what you're working on.

## Standalone Skill Downloads

The `skyflow-skills` plugin is the easiest way to get the skills in Claude Code. If you instead want a single skill as a portable file — to drop into another project, share, or use with a different Agent Skills-compatible harness — each skill is also published as a standalone `.zip` on the [Releases page](https://github.com/SkyflowFoundry/skyflow-skills/releases/latest).

Each archive unzips to a self-contained skill folder (`<skill-name>/SKILL.md` plus its resources). To install one manually:

```sh
# Download the latest build of a skill (stable URL always points at the newest release)
curl -L -O https://github.com/SkyflowFoundry/skyflow-skills/releases/latest/download/create-vault.zip

# Unzip into your user skills directory (or a project's .claude/skills/)
unzip create-vault.zip -d ~/.claude/skills/
```

Available skills: `call-rest-apis`, `create-vault`, `get-started`, `migrate-sdk-v1-to-v2`, `plan-skyflow-implementation`, `quickstart-js-browser`, `quickstart-node`. A `SHA256SUMS.txt` is attached to each release so you can verify downloads.

> These zips are build artifacts generated from the same skills in this repo — the plugin and the standalone downloads are always in sync.

## For administrators: allowlisting this marketplace

Because this marketplace contains only skills and no MCP servers, you can authorize it on its own without granting access to any MCP endpoints. To restrict your organization to this marketplace, add it to [`strictKnownMarketplaces`](https://code.claude.com/docs/en/settings#strictknownmarketplaces) in managed settings:

```json
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "SkyflowFoundry/skyflow-skills" }
  ]
}
```

To also register it automatically so users don't have to run `/plugin marketplace add`, pair it with [`extraKnownMarketplaces`](https://code.claude.com/docs/en/settings#extraknownmarketplaces):

```json
{
  "extraKnownMarketplaces": {
    "skyflow-skills-marketplace": {
      "source": { "source": "github", "repo": "SkyflowFoundry/skyflow-skills" }
    }
  },
  "enabledPlugins": {
    "skyflow-skills@skyflow-skills-marketplace": true
  }
}
```

## Looking for the MCP servers?

The Skyflow MCP servers (`skyflow-developer-mcp` and `skyflow-runtime-mcp`) are published from a separate marketplace so they can be reviewed and authorized independently:

```sh
/plugin marketplace add SkyflowFoundry/claude
```

See [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude) for details.

## Learn More

For complete documentation on Claude Code plugins, see the [Claude Code Plugins documentation](https://code.claude.com/docs/en/plugins).

## Contributing

For developers who want to contribute to these skills, see [CONTRIBUTING.md](CONTRIBUTING.md).
