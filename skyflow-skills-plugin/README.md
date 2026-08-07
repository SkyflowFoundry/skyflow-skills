# Skyflow Skills

Guided Skyflow workflows for Claude Code. This plugin packages **skills** — structured documentation, sample schemas, and API examples that Claude can reference when helping you implement Skyflow features.

This plugin contains skills only. It does **not** connect to any MCP server and requires **no environment variables**. For live API access, pair it with the `skyflow-developer-mcp` plugin from the [Skyflow MCP marketplace](https://github.com/SkyflowFoundry/claude).

Part of the [Skyflow Skills marketplace](../README.md).

## Install

Add the Skyflow Skills marketplace:

```sh
/plugin marketplace add SkyflowFoundry/skyflow-skills
```

Install the plugin:

```sh
/plugin install skyflow-skills@skyflow-skills-marketplace
```

## Skills

Skills are guided workflows that help Claude assist you with common Skyflow tasks. They provide structured documentation, sample schemas, and API examples that Claude can reference when helping you implement Skyflow features.

Each skill is available as a slash command in the form `/skyflow-skills:<skill-name>`, and Claude will also invoke the relevant skill automatically when it fits what you're working on.

| Skill | Slash command |
| ----- | ------------- |
| Get Started with Skyflow | `/skyflow-skills:get-started` |
| Plan Skyflow Implementation | `/skyflow-skills:plan-skyflow-implementation` |
| Create Vault | `/skyflow-skills:create-vault` |
| Call REST APIs | `/skyflow-skills:call-rest-apis` |
| Migrate SDK V1 to V2 | `/skyflow-skills:migrate-sdk-v1-to-v2` |
| Quickstart: Node.js | `/skyflow-skills:quickstart-node` |
| Quickstart: JS Browser (Elements) | `/skyflow-skills:quickstart-js-browser` |

### Get Started with Skyflow

**Slash command:** `/skyflow-skills:get-started`

The **get-started** skill is the front door for a new Skyflow integration or POC. It orients new users and agents, then hands off to the right skill. It walks through four quick decisions — checking whether you have an account and whether it's a trial, sandbox, or production account (which drives the base URLs and how carefully to handle data), getting an API bearer token into your environment securely (never into the chat or logs), clarifying your goal (explore, plan, POC, or production-ready), and picking a working mode (educational/collaborative or get-it-done) — then routes you to the appropriate skill, API, SDK, and docs. Supporting references cover the account-type/base-URL matrix and secure credential setup.

### Plan Skyflow Implementation

**Slash command:** `/skyflow-skills:plan-skyflow-implementation`

The **plan-skyflow-implementation** skill guides you through planning a complete Skyflow implementation using the Define-Build-Go Live framework. It helps you assess requirements (data inventory, schema design, environment setup), plan technical integration (authentication, SDK integration, access controls, testing), and prepare for production (security review, data migration, launch). The skill includes use case classification, phase-specific checklists, tokenization decision trees, implementation templates, and security review guidance.

### Create Vault

**Slash command:** `/skyflow-skills:create-vault`

The **create-vault** skill guides you through creating Skyflow vaults programmatically using the Management API. It covers three approaches: using pre-built templates (Quickstart, Payment, PIIData, CustomerIdentity, Plaid), uploading a custom schema, or starting from scratch. The skill includes complete API examples for listing templates, creating vaults, and updating schemas, along with comprehensive documentation on configuring field tags for tokenization policies, redaction/DLP settings, validation rules, and compliance classifications (GDPR, CCPA, HIPAA, etc.). Sample vault schemas are provided for common use cases like payment processing, customer identity management, and PII storage.

### Call REST APIs

**Slash command:** `/skyflow-skills:call-rest-apis`

The **call-rest-apis** skill provides expertise on Skyflow REST APIs including management APIs, data APIs, and detect APIs. It covers API endpoints, request/response formats, authentication methods, and code examples. The skill includes an API quick reference table, OpenAPI specifications for data, detect, and management APIs, authentication guidance for bearer tokens and service accounts, error handling patterns, rate limiting information, and links to SDK documentation.

### Migrate SDK V1 to V2

**Slash command:** `/skyflow-skills:migrate-sdk-v1-to-v2`

The **migrate-sdk-v1-to-v2** skill guides you through migrating from Skyflow V1 SDKs to V2 SDKs. It covers authentication changes, client initialization updates, and request/response structure changes with SDK-specific migration patterns for Node.js, Python, Java, and Go. The skill includes V1 identification patterns, breaking changes documentation, a migration workflow, before/after code examples for common patterns, a troubleshooting guide, and test strategies.

### Quickstart: Node.js

**Slash command:** `/skyflow-skills:quickstart-node`

The **quickstart-node** skill sets up a new Node.js project with TypeScript, ES modules, and the `skyflow-node` SDK. It covers project initialization, TypeScript configuration, and package scripts, with optional steps for ESLint, Prettier, and CSpell.

### Quickstart: JS Browser (Elements)

**Slash command:** `/skyflow-skills:quickstart-js-browser`

The **quickstart-js-browser** skill sets up a standalone front-end project using Vite and the `skyflow-js` SDK to collect sensitive data with Skyflow Elements (secure, iframe-based input fields). It covers project scaffolding, Vite/TypeScript configuration, mounting Collect elements, handling validation and collect events, production hardening (token endpoints, env modes), and a troubleshooting guide.

## Learn More

For complete documentation on Claude Code plugins, see the [Claude Code Plugins documentation](https://code.claude.com/docs/en/plugins).
