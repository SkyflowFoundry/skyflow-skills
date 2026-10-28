# Skyflow Credentials — Secure Setup

Every Skyflow API call needs a bearer token in an `Authorization: Bearer <token>` header. This guide covers the token types, how to get one, and — most importantly — how to handle it without leaking it.

## The one rule that matters most

**A token is a secret. It never belongs in the chat, a commit, or a log.**

- Do **not** ask the user to paste their token into the conversation.
- Do **not** print it, echo it, or write it into a file that gets committed.
- Read it from the **environment** (or a gitignored `.env`) instead.
- The higher the environment (trial → sandbox → production), the more this matters. A leaked production token can expose real customer data.

If a token ever does end up in the transcript or a shared log, treat it as compromised: **rotate/revoke it in Studio immediately.**

## Token types

| Type | Where it comes from | Lifetime | Best for |
| --- | --- | --- | --- |
| **Personal access / API bearer token** | Studio → top-right profile (account) menu → *Generate API Bearer Token* | Short-lived (typically ~60 min) | Getting started, trials, POCs. Tied to your user. |
| **API key** | Studio (service account settings) | Long-lived, revocable | Long-lived programmatic/backend access with least privilege |
| **Service account + generated bearer token** | Download a credentials JSON; sign a JWT assertion and exchange it for a bearer token server-side | Bearer token short-lived; you regenerate as needed | Production. Credentials never leave your backend. |

For getting started, the **personal access token** is the fastest path. For anything production-facing, move to a **service account** or a least-privilege **API key**. See the `call-rest-apis` skill for how to exchange a service account JWT assertion for a bearer token, and the `plan-skyflow-implementation` skill for the auth decision tree.

## Get a personal access token

1. Sign in to Skyflow Studio (the right environment — see [environments.md](environments.md)).
2. Click the **profile / account icon in the top-right**.
3. Choose **Generate API Bearer Token**.
4. Copy the token — you'll place it in your environment below, not into the chat.

Because these tokens expire (~60 min), you'll regenerate periodically during development. For anything longer-lived, use an API key or a service account.

## Provide the token securely (pick one)

### Option 1 — The agent host's secret store (hosted or cloud agents)

Some agents run on a hosted or cloud machine rather than the user's own computer. Those hosts usually offer a secure way to store secrets — a secret field, a secrets setting, or similar — that injects the value as an environment variable. Use it with the names `SKYFLOW_BEARER_TOKEN` and `SKYFLOW_ACCOUNT_ID`, and have the user enter the value there themselves. Don't append secrets to a shell profile on a hosted machine.

### Option 2 — Shell environment variable (recommended for local dev)

Add to your shell profile (e.g. `~/.zshrc` on macOS), then **restart the terminal**. If you also use a Skyflow MCP server plugin, it reads these same names:

```bash
echo 'export SKYFLOW_BEARER_TOKEN="your-token-here"' >> ~/.zshrc
echo 'export SKYFLOW_ACCOUNT_ID="your-account-id-here"' >> ~/.zshrc
```

Verify **without printing the secret**:

```bash
[ -n "$SKYFLOW_BEARER_TOKEN" ] && echo "SKYFLOW_BEARER_TOKEN is set" || echo "SKYFLOW_BEARER_TOKEN is NOT set"
```

### Option 3 — Gitignored `.env` file (project-local)

1. Confirm `.env` is in `.gitignore` **before** creating it:
   ```bash
   grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
   ```
2. Put the token in `.env`:
   ```bash
   SKYFLOW_BEARER_TOKEN=your-token-here
   SKYFLOW_ACCOUNT_ID=your-account-id-here
   ```
3. Load it with your framework's env loader (`dotenv`, Vite's `import.meta.env`, etc.). Never hardcode the token in source.

### Option 4 — Secrets manager (production)

Store credentials in a secrets manager (AWS Secrets Manager, GCP Secret Manager, Vault, etc.) and inject them at runtime. Use a **service account** to generate short-lived bearer tokens on the backend — the raw credentials never reach a frontend or a developer's laptop.

## Using the token in requests

```bash
curl -s "$VAULT_URL/v1/vaults/$VAULT_ID/persons" \
  -H "Authorization: Bearer $SKYFLOW_BEARER_TOKEN"
```

The agent should reference `$SKYFLOW_BEARER_TOKEN` in commands rather than the literal value, so the secret stays out of the command it prints.

## Frontend note

Browser/mobile SDKs must **never** hold a service account or long-lived key. They call your backend for a **short-lived bearer token** via a `getBearerToken()` function. See the `quickstart-js-browser` skill's "Production Hardening" section for the token-endpoint pattern.

## Checklist

- [ ] Token stored in the agent host's secret store, an env var, a gitignored `.env`, or a secrets manager — never in the chat
- [ ] `.env` is in `.gitignore` (if using a file)
- [ ] Token matches the target environment (trial/sandbox/production)
- [ ] Production uses a service account or least-privilege API key, not a personal token
- [ ] No token, credential, or real PII appears in logs, commits, or the transcript
