# Skyflow Environments & Base URLs

Your Skyflow account type decides which base URLs you talk to and how careful you should be. Get this right first — pointing an integration at the wrong environment is one of the most common early mistakes.

## Identify your account type

Sign in to Studio and look at the URL in your browser:

| Browser URL | Account type |
| --- | --- |
| `try.skyflow.com/...` | **Trial** |
| `<account>.skyflow-preview.com` | **Sandbox** |
| `<account>.skyflow.com` (not `try`, not `-preview`) | **Production** |

If you're not sure, the **`-preview` suffix means sandbox**. Trial and production both live on `skyflow.com` / `skyflowapis.com`.

## Base URL matrix

| Account type | Management (API) base URL | Vault URL pattern | Docs |
| --- | --- | --- | --- |
| **Trial** | `https://manage.skyflowapis.com` | `https://<clusterId>.vault.skyflowapis.com` | `docs.skyflow.com` |
| **Sandbox** | `https://manage.skyflowapis-preview.com` | `https://<clusterId>.vault.skyflowapis-preview.com` | `docs.skyflow-preview.com` |
| **Production** | `https://manage.skyflowapis.com` | `https://<clusterId>.vault.skyflowapis.com` | `docs.skyflow.com` |

- **Management API** (create vaults, manage schemas/policies, auth) uses the `manage.*` host.
- **Data & Detect APIs** (insert, tokenize, detokenize, de-identify) use your **vault URL** — the per-vault `<clusterId>.vault.*` host.
- `<clusterId>` is the subdomain of your vault URL (e.g. for `https://ebfc9bee4242.vault.skyflowapis.com`, the cluster ID is `ebfc9bee4242`).

> **Always confirm the exact URLs from Studio.** This table is the usual mapping, but Studio is the source of truth — copy the real values rather than reconstructing them from memory.

## Find your IDs and URLs in Studio

In Studio, open a vault and click the **vault menu icon → View vault details**. That panel gives you:

- **Vault URL** — the base for Data and Detect API calls
- **Vault ID** — identifies the vault in API paths
- **Account ID** — sent as the `X-SKYFLOW-ACCOUNT-ID` header on many Management calls
- **Workspace ID** — needed when creating vaults

Suggested environment variables for local work (these names line up with the Skyflow MCP plugins):

```bash
export MANAGEMENT_URL=https://manage.skyflowapis.com   # or ...-preview.com for sandbox
export SKYFLOW_ACCOUNT_ID=<account-id>
export WORKSPACE_ID=<workspace-id>
export VAULT_ID=<vault-id>
export VAULT_URL=<vault-url>
export SKYFLOW_BEARER_TOKEN=<token>   # see credentials.md
```

## Per-environment guidance

### Trial
- **Purpose:** learning, demos, quick POCs. Time-limited.
- **Data:** synthetic/test data only — never real customer PII.
- **Credentials:** a personal access token in a local `.env` or env var is fine.
- **Mindset:** move fast, treat everything as disposable.

### Sandbox (`-preview`)
- **Purpose:** pre-production development and staging against a stable environment.
- **Data:** test data only. Still no real PII.
- **Credentials:** personal access token works; begin moving to a **service account** as the integration matures.
- **Mindset:** build it the way you'll ship it, but it's still safe to break.

### Production
- **Purpose:** real users, real sensitive data.
- **Data:** real PII/PHI/PCI — handle accordingly. Never log raw values.
- **Credentials:** **service account or least-privilege API key**, short-lived bearer tokens generated server-side, secrets stored in a secrets manager. No personal tokens.
- **Mindset:** highest caution. Confirm before any write, config change, or credential rotation. Get a security review before launch (see the `plan-skyflow-implementation` skill).

## Common mistakes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` on every call | Token from a different environment, or expired | Regenerate a token for the environment you're targeting |
| Calls hit the wrong data / vault | Mixed `skyflowapis.com` and `skyflowapis-preview.com` hosts | Use one environment's hosts consistently; copy URLs from Studio |
| `404` on Management calls | Wrong `manage.*` host for your account type | Sandbox uses `manage.skyflowapis-preview.com`; trial/prod use `manage.skyflowapis.com` |
| Vault operations fail | Using the Management host for Data/Detect calls | Data & Detect use the **vault URL**, not `manage.*` |
