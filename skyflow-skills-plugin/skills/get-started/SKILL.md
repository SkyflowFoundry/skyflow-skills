---
name: get-started
description: Use at the very start of any Skyflow project — when a user is new to Skyflow, is bootstrapping an integration or proof of concept, doesn't know which API/SDK/skill to reach for, or hasn't yet set up their account, environment (trial/sandbox/production), base URLs, or credentials. The front door that orients the user and hands off to the right Skyflow skill.
---

# Get Started with Skyflow

The front door for a new Skyflow integration or POC. Your job is to get the user from "I have (or want) a Skyflow account" to "I'm working in the right skill, against the right environment, with credentials handled safely" — fast.

Skyflow is a data privacy vault: you store sensitive data (PII, PHI, PCI) in Skyflow, get back tokens, and keep raw secrets out of your own systems. This skill doesn't do the integration itself — it **routes** to the skill that does.

## Run this flow

Work through these in order. **Skip any step the user has already answered** — don't re-interrogate. Present choices as pick-lists (offer the options, let them choose) rather than open questions.

1. **Account & environment** — do they have an account? Trial, sandbox, or production? This sets the base URLs and how careful to be.
2. **Credentials** — get a token in place *securely*, without it ever touching the chat.
3. **Goal** — what are they actually trying to do? Propose the options.
4. **Mode** — educational/collaborative, or get-it-done?
5. **Hand off** — route to the right skill(s), API, SDK, and docs.

---

## Step 1 — Account & environment

Ask: **"Do you already have a Skyflow account?"**

- **No account** → point them to the free trial: <https://www.skyflow.com/try-skyflow>. A trial is the fastest way to start. Come back here once they're signed in.
- **Has an account** → find out which *type*, because it drives every base URL and vault URL you'll use. Easiest tell: look at the browser URL while signed in to Studio.

| Account type | Studio URL looks like | Management (API) base URL | Vault URL pattern |
| --- | --- | --- | --- |
| **Trial** | `try.skyflow.com/...` | `https://manage.skyflowapis.com` | `https://<clusterId>.vault.skyflowapis.com` |
| **Sandbox** | `<account>.skyflow-preview.com` | `https://manage.skyflowapis-preview.com` | `https://<clusterId>.vault.skyflowapis-preview.com` |
| **Production** | `<account>.skyflow.com` | `https://manage.skyflowapis.com` | `https://<clusterId>.vault.skyflowapis.com` |

**The `-preview` suffix is the sandbox tell.** Trial and production both run on `skyflowapis.com`.

> **Golden rule:** don't guess the URLs. Copy the exact **Management URL** and **Vault URL** from Studio → *vault menu icon → View vault details*. That view also has your **Account ID**, **Workspace ID**, and **Vault ID**. The table above is the usual mapping; Studio is the source of truth.

Record for the session: account type, Management base URL, Vault URL, Account ID, Vault ID.

Full detail, per-environment cautions, and how to find each ID → [environments.md](environments.md).

---

## Step 2 — Credentials (handle with care)

The quickest credential to start with is a **personal access / API bearer token** from Studio: **top-right profile (account) menu → Generate API Bearer Token**.

**Never ask the user to paste the token into the chat.** Tokens are secrets — in a shared or logged session, and especially in sandbox/production, a pasted token is a leaked token. Instead, have them place it in the environment and read it from there:

```bash
# Add to your shell profile (e.g. ~/.zshrc), then restart the terminal.
# These names match the Skyflow MCP plugins, so setting them once wires those up too.
export SKYFLOW_BEARER_TOKEN="your-token-here"
export SKYFLOW_ACCOUNT_ID="your-account-id-here"
```

Confirm it's set **without printing it**:

```bash
[ -n "$SKYFLOW_BEARER_TOKEN" ] && echo "token is set" || echo "token is NOT set"
```

For a project, a **gitignored `.env`** works too — just make sure `.env` is in `.gitignore` before writing anything to it.

Match the credential to the environment:

| Environment | Recommended credential |
| --- | --- |
| Trial / POC | Personal access token (fastest to get going) |
| Sandbox | Personal access token is fine; start moving to a service account |
| Production | Service account or **API key** with least privilege; generate short-lived bearer tokens server-side; use a secrets manager |

**Non-negotiables:** never paste tokens into chat, commit them, or echo them into logs; never send real customer PII to a trial/sandbox; the higher the environment, the more caution.

Token types, secure provisioning options, and MCP wiring → [credentials.md](credentials.md).

---

## Step 3 — What do you want to do?

Propose these options and let the user pick (they can combine):

- **A. Explore what's possible** — learn the concepts, kick the tires, see a working example.
- **B. Plan a full implementation** — design the vault, data model, and integration before building.
- **C. Build a POC / prototype** — get something working fast, correctness over polish.
- **D. Build a production-ready integration** — do it properly: security, access controls, real credentials.
- **E. A specific task** — e.g. create a vault, collect data in the browser, tokenize records, de-identify text/LLM data, or migrate an existing SDK.

---

## Step 4 — Pick a working mode

Offer both, and adapt for the rest of the session:

- 🎓 **Educational / collaborative** — explain the *why*, go step by step, surface options and trade-offs, confirm understanding before moving on. Best for first-timers and anyone learning Skyflow.
- ⚡ **Get-it-done** — minimize back-and-forth, choose sensible defaults, execute end-to-end, then report what you did. Best when the user knows Skyflow or just wants the result.

Get-it-done still **pauses before anything irreversible or production-facing** (writing real data, changing production config, rotating credentials).

---

## Step 5 — Hand off to the right skill

Match the goal to the skill and load it. All skills below ship in this same `skyflow-skills` plugin.

| You want to… | Start here (skill) | Also useful |
| --- | --- | --- |
| Plan a full implementation / architecture | **plan-skyflow-implementation** | create-vault, call-rest-apis |
| Create or design a vault (schema, tokenization, redaction) | **create-vault** | call-rest-apis |
| Call the Skyflow REST APIs directly (curl/HTTP) | **call-rest-apis** | skyflow-developer-mcp |
| Integrate a Node.js / backend service | **quickstart-node** | call-rest-apis, migrate-sdk-v1-to-v2 |
| Collect sensitive data in the browser (Elements) | **quickstart-js-browser** | create-vault |
| De-identify PII in text or protect LLM prompts (Detect) | **call-rest-apis** (Detect) | skyflow-runtime-mcp |
| Upgrade an existing V1 SDK integration | **migrate-sdk-v1-to-v2** | — |
| Look things up live (docs, resources, skills) | **skyflow-developer-mcp** (MCP plugin) | — |

**Typical first-timer path:** explore → `plan-skyflow-implementation` → `create-vault` → a quickstart (`quickstart-node` or `quickstart-js-browser`) → `call-rest-apis` as you build.

### Companion MCP plugins (optional)

The skills work standalone. For live access, pair with:

- **skyflow-developer-mcp** — Skyflow docs, skills, and integration resources on demand. Most users want this. Reads `SKYFLOW_BEARER_TOKEN` and `SKYFLOW_ACCOUNT_ID` (the same vars from Step 2).
- **skyflow-runtime-mcp** — on-demand de-identification of PII in text via the Detect APIs. Add only if you need it.

Install: `/plugin marketplace add SkyflowFoundry/claude` then `/plugin install skyflow-developer-mcp@skyflow-marketplace`.

---

## Guardrails (apply throughout)

- **Secrets stay out of the transcript.** Never request, print, or commit a token; read it from the environment.
- **Right environment, right data.** Trial and sandbox are for test data only — never real customer PII.
- **Escalate caution with the environment.** Production actions get confirmed first, always.
- **Confirm URLs from Studio**, don't hardcode from memory.
- **When unsure which skill fits, ask** — this skill is a router, not the destination.

## Related documentation

- [environments.md](environments.md) — account types, base URLs, finding your IDs, per-environment guidance
- [credentials.md](credentials.md) — token types, secure local setup, what never to do
- Skyflow docs: <https://docs.skyflow.com> · API authentication: <https://docs.skyflow.com/docs/fundamentals/api-authentication>
