# Skyflow Skills

> [!WARNING]
> This is an experimental project in development. This project is not supported and offered under an MIT license.

Skyflow's **skills** for AI agents — guided workflows for getting started, vault creation, REST API guidance, SDK migration, implementation planning, and SDK quickstarts.

The skills follow the open [Agent Skills](https://agentskills.io/specification) format, and the plugin ships manifests for several agent hosts from one source of truth.

This repo contains **skills only**. It ships no MCP servers, opens no network connections, and requires no environment variables or credentials — which makes it straightforward to review and allowlist. The Skyflow MCP servers for Claude Code live in a separate marketplace, [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude).

- [Skyflow Skills](#skyflow-skills)
  - [What's in this repo](#whats-in-this-repo)
  - [Supported hosts](#supported-hosts)
  - [Install in Claude Code](#install-in-claude-code)
  - [Install in Cursor or Grok Bot](#install-in-cursor-or-grok-bot)
  - [Install in other agents](#install-in-other-agents)
  - [Standalone Skill Downloads](#standalone-skill-downloads)
  - [For administrators: allowlisting this marketplace](#for-administrators-allowlisting-this-marketplace)
  - [Looking for the MCP servers?](#looking-for-the-mcp-servers)
  - [Learn More](#learn-more)
  - [Contributing](#contributing)

## What's in this repo

| Plugin | What it does | Environment variables | Docs |
| ------ | ------------ | --------------------- | ---- |
| `skyflow-skills` | Guided Skyflow workflows (getting started, vault creation, REST API guidance, SDK migration, implementation planning, SDK quickstarts) | None | [README](skyflow-skills-plugin/README.md) |

## Supported hosts

| Host | Manifest | How to install |
| ---- | -------- | -------------- |
| Agent Plugins hosts (vendor-neutral) | [`skyflow-skills-plugin/plugin.json`](skyflow-skills-plugin/plugin.json) ([Agent Plugins 1.0.0](https://agent-plugins.org/specification)) | Point the host at the `skyflow-skills-plugin/` directory |
| Claude Code | [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) and [`skyflow-skills-plugin/.claude-plugin/plugin.json`](skyflow-skills-plugin/.claude-plugin/plugin.json) | [Install in Claude Code](#install-in-claude-code) |
| Cursor and Grok Bot | [`.cursor-plugin/marketplace.json`](.cursor-plugin/marketplace.json) plus the Agent Plugins manifest | [Install in Cursor or Grok Bot](#install-in-cursor-or-grok-bot) |
| Any Agent Skills harness | Each `skills/<name>/SKILL.md` | [Standalone Skill Downloads](#standalone-skill-downloads) |

## Install in Claude Code

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

## Install in Cursor or Grok Bot

Grok Bot installs plugins through the same marketplace and format as Cursor, so the steps are the same in both.

1. Open **Settings → Plugins**.
2. Paste `https://github.com/SkyflowFoundry/skyflow-skills` into the **Search or Paste Link** box.
3. Select **skyflow-skills** and click **Add**.

The plugin needs no environment variables and no sign-in. The agent invokes the relevant skill automatically when it fits what you're working on.

To test local changes in Cursor, copy the plugin folder (not the repo root) and reload the window:

```sh
mkdir -p ~/.cursor/plugins/local
rm -rf ~/.cursor/plugins/local/skyflow-skills
cp -R skyflow-skills-plugin ~/.cursor/plugins/local/skyflow-skills
```

Then run **Developer: Reload Window** and check that the skills appear under **Customize**.

## Install in other agents

Hosts that support the vendor-neutral [Agent Plugins](https://agent-plugins.org/specification) format can load `skyflow-skills-plugin/` directly because its root `plugin.json` targets Agent Plugins 1.0.0. Hosts that only support [Agent Skills](https://agentskills.io/specification) can use the [standalone skill downloads](#standalone-skill-downloads).

## Standalone Skill Downloads

A plugin install is the easiest way to get the skills. If you instead want a single skill as a portable file — to drop into another project, share, or use with a different Agent Skills-compatible harness — each skill is also published as a standalone `.zip` on the [Releases page](https://github.com/SkyflowFoundry/skyflow-skills/releases/latest).

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

This section applies to Claude Code. Because this marketplace contains only skills and no MCP servers, you can authorize it on its own without granting access to any MCP endpoints. To restrict your organization to this marketplace, add it to [`strictKnownMarketplaces`](https://code.claude.com/docs/en/settings#strictknownmarketplaces) in managed settings:

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

The Skyflow MCP servers (`skyflow-developer-mcp` and `skyflow-runtime-mcp`) are published for Claude Code from a separate marketplace so they can be reviewed and authorized independently:

```sh
/plugin marketplace add SkyflowFoundry/claude
```

See [`SkyflowFoundry/claude`](https://github.com/SkyflowFoundry/claude) for details.

## Learn More

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Plugins specification](https://agent-plugins.org/specification)
- [Claude Code plugins documentation](https://code.claude.com/docs/en/plugins)
- [Cursor plugins documentation](https://cursor.com/docs/plugins)

## Contributing

For developers who want to contribute to these skills, see [CONTRIBUTING.md](CONTRIBUTING.md).
