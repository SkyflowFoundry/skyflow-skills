---
name: quickstart-js-browser
description: Set up a standalone front-end project using Vite and the skyflow-js SDK to collect sensitive data with Skyflow Elements (secure iframe-based input fields). Use when building a browser-based form that tokenizes credit card numbers, PII, or other sensitive data. Relevant for skyflow-js, Skyflow Elements, secure iframe inputs, client-side tokenization with Skyflow, or setting up a Vite project with Skyflow.
---

# Quickstart: Skyflow Elements with Vite

Set up a standalone front-end project using Vite to collect
sensitive data with Skyflow Elements from the `skyflow-js` SDK.

Skyflow Elements are secure, pre-built iframe-based input fields.
Sensitive data typed into these fields never touches your
application code — it goes directly to your Skyflow vault and
returns tokens.

## Prerequisites

- Node.js (LTS recommended)
- A Skyflow vault with at least one table and columns for the
  data you want to collect
- A bearer token for vault access (from your Skyflow dashboard
  or a token generation endpoint)

## Steps

### 1) Scaffold the project

```sh
mkdir skyflow-elements-demo
cd skyflow-elements-demo
npm init -y
```

Add the following fields to the generated `package.json` (merge with existing content):

```json
{
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

### 2) Install dependencies

```sh
npm install skyflow-js
npm install -D vite typescript
```

### 3) Add Vite config

Create `vite.config.ts` at the project root:

```ts
import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
  },
});
```

### 4) Configure TypeScript

Create `tsconfig.json` at the project root:

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

Create `src/vite-env.d.ts` so TypeScript understands Vite's `import.meta.env`:

```ts
/// <reference types="vite/client" />
```

### 5) Configure environment variables

Create `.env.local` at the project root:

```sh
# Your Skyflow vault ID (found in Skyflow Studio under vault settings)
VITE_SKYFLOW_VAULT_ID=your_vault_id_here

# Your Skyflow vault URL (e.g. https://ebfc9bee4242.vault.skyflowapis.com)
VITE_SKYFLOW_VAULT_URL=https://your-vault-url.vault.skyflowapis.com

# A bearer token for vault access (for demo/development only — see production notes below)
VITE_SKYFLOW_BEARER_TOKEN=your_bearer_token_here
```

> **Note:** Bearer tokens expire after ~60 minutes. For development, you can paste a fresh token here. For production, use a token endpoint instead (see Production Hardening below).

### 6) Create the HTML page

Create `index.html` at the project root. Skyflow Elements render as iframes — mount targets **must have an explicit height** or the iframes default to 0px and are invisible:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Skyflow Elements Demo</title>
    <style>
      body {
        font-family: system-ui, sans-serif;
        max-width: 480px;
        margin: 2rem auto;
        padding: 0 1rem;
      }

      .field-label {
        display: block;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
      }

      /* Each element mount point needs explicit height */
      .skyflow-element {
        height: 40px;
        margin-bottom: 0.75rem;
      }

      #status {
        margin-top: 1rem;
        padding: 0.75rem;
        border-radius: 4px;
        display: none;
      }
      #status.success {
        display: block;
        background: #d4edda;
        color: #155724;
      }
      #status.error {
        display: block;
        background: #f8d7da;
        color: #721c24;
      }
    </style>
  </head>
  <body>
    <h1>Skyflow Elements Demo</h1>

    <!-- Mount points for Skyflow Elements — customize these for your schema.
         Note: labels use aria-label approach since iframe elements
         cannot be associated via the "for" attribute. -->
    <div>
      <span class="field-label">Card number</span>
      <div
        id="field-1"
        class="skyflow-element"
        role="group"
        aria-label="Card number"
      ></div>
    </div>

    <div>
      <span class="field-label">Cardholder name</span>
      <div
        id="field-2"
        class="skyflow-element"
        role="group"
        aria-label="Cardholder name"
      ></div>
    </div>

    <div>
      <span class="field-label">Expiration month</span>
      <div
        id="field-3"
        class="skyflow-element"
        role="group"
        aria-label="Expiration month"
      ></div>
    </div>

    <div>
      <span class="field-label">Expiration year</span>
      <div
        id="field-4"
        class="skyflow-element"
        role="group"
        aria-label="Expiration year"
      ></div>
    </div>

    <button type="button" id="submit">Collect</button>
    <div id="status"></div>

    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

### 7) Create the client entry

Create `src/main.ts`:

```ts
import Skyflow from "skyflow-js";

// ---------------------------------------------------------------------------
// Environment variables
// ---------------------------------------------------------------------------
const vaultID = import.meta.env.VITE_SKYFLOW_VAULT_ID as string | undefined;
const vaultURL = import.meta.env.VITE_SKYFLOW_VAULT_URL as string | undefined;
const bearerToken = import.meta.env.VITE_SKYFLOW_BEARER_TOKEN as
  | string
  | undefined;

if (!vaultID) throw new Error("Missing VITE_SKYFLOW_VAULT_ID in .env.local");
if (!vaultURL) throw new Error("Missing VITE_SKYFLOW_VAULT_URL in .env.local");
if (!vaultURL.startsWith("https://"))
  throw new Error("VITE_SKYFLOW_VAULT_URL must start with https://");
if (!bearerToken)
  throw new Error("Missing VITE_SKYFLOW_BEARER_TOKEN in .env.local");

// ---------------------------------------------------------------------------
// Initialize the Skyflow client
// ---------------------------------------------------------------------------
// getBearerToken must be a function returning a Promise<string>.
// The SDK calls this automatically whenever it needs to authenticate.
//
// DEMO: return a static token from env vars (fine for development).
// PRODUCTION: fetch a fresh token from your backend (see Production Hardening).
const skyflow = Skyflow.init({
  vaultID,
  vaultURL,
  getBearerToken: async () => bearerToken,
  options: {
    logLevel: Skyflow.LogLevel.DEBUG, // verbose logging during development
    env: Skyflow.Env.DEV, // DEV exposes values in event callbacks for debugging
  },
});

// ---------------------------------------------------------------------------
// Create a Collect container and elements
// ---------------------------------------------------------------------------
// A COLLECT container gathers sensitive input and sends it directly to your
// Skyflow vault. The response contains tokens — your app never sees raw values.
const container = skyflow.container(Skyflow.ContainerType.COLLECT);

// Style overrides for validation states (applied inside the iframe)
const inputStyles = {
  base: { color: "#1d1d1d" },
  complete: { color: "#4caf50" },
  invalid: { color: "#d32f2f" },
  focus: { borderColor: "#1a73e8" },
};

// ┌─────────────────────────────────────────────────────────────────────────┐
// │ CUSTOMIZE: replace table/column names to match YOUR vault schema.      │
// │                                                                        │
// │ The element types below are for a credit card collection form.         │
// │ Available types include:                                               │
// │   CARD_NUMBER, CARDHOLDER_NAME, CVV,                                   │
// │   EXPIRATION_DATE, EXPIRATION_MONTH, EXPIRATION_YEAR,                  │
// │   PIN, INPUT_FIELD (generic — for SSN, email, etc.)                    │
// └─────────────────────────────────────────────────────────────────────────┘
const cardNumber = container.create({
  table: "credit_cards",
  column: "card_number",
  type: Skyflow.ElementType.CARD_NUMBER,
  inputStyles,
  placeholder: "4111 1111 1111 1111",
});

const cardholderName = container.create({
  table: "credit_cards",
  column: "cardholder_name",
  type: Skyflow.ElementType.CARDHOLDER_NAME,
  inputStyles,
  placeholder: "Jane Doe",
});

const expiryMonth = container.create({
  table: "credit_cards",
  column: "expiry_month",
  type: Skyflow.ElementType.EXPIRATION_MONTH,
  inputStyles,
  placeholder: "MM",
});

const expiryYear = container.create({
  table: "credit_cards",
  column: "expiry_year",
  type: Skyflow.ElementType.EXPIRATION_YEAR,
  inputStyles,
  placeholder: "YY",
});

// ---------------------------------------------------------------------------
// Mount elements to the DOM
// ---------------------------------------------------------------------------
cardNumber.mount("#field-1");
cardholderName.mount("#field-2");
expiryMonth.mount("#field-3");
expiryYear.mount("#field-4");

// ---------------------------------------------------------------------------
// Element event listeners — useful for debugging and validation feedback
// ---------------------------------------------------------------------------
// READY fires when the iframe has loaded and the element is interactive.
[cardNumber, cardholderName, expiryMonth, expiryYear].forEach((el, i) => {
  el.on(Skyflow.EventName.READY, () => {
    console.log(`[Skyflow] Element #field-${i + 1} ready`);
  });

  // CHANGE fires on every keystroke — state includes isValid, isEmpty, isFocused.
  // In DEV mode, state.value contains the actual value for debugging.
  el.on(Skyflow.EventName.CHANGE, (state: Record<string, unknown>) => {
    console.log(`[Skyflow] Element #field-${i + 1} changed:`, state);
  });
});

// ---------------------------------------------------------------------------
// Collect handler
// ---------------------------------------------------------------------------
const submitButton = document.querySelector<HTMLButtonElement>("#submit")!;
const statusDiv = document.querySelector<HTMLDivElement>("#status")!;

submitButton.addEventListener("click", async () => {
  statusDiv.className = "";
  statusDiv.textContent = "";

  try {
    const response = await container.collect({ tokens: true });
    console.log("[Skyflow] Collect response:", response);
    statusDiv.className = "success";
    statusDiv.textContent = "Tokens created successfully — check the console.";
  } catch (err) {
    console.error("[Skyflow] Collect error:", err);
    statusDiv.className = "error";
    statusDiv.textContent = `Collection failed — ${err instanceof Error ? err.message : "check the console for details."}`;
  }
});
```

### 8) Run and verify

Start the dev server:

```sh
npm run dev
```

Open `http://localhost:5173` in your browser and verify:

1. **Elements render** — you should see four input fields, not blank space. If fields are invisible, check that `.skyflow-element` has a height set.
2. **Console shows READY events** — open DevTools and look for `[Skyflow] Element #field-N ready` messages for each field. These confirm the iframes loaded and connected to your vault.
3. **Type a test card number** — use `4111 1111 1111 1111` (Visa test number). The input should turn green (the `complete` style) and the console should log the change event with `isValid: true`.
4. **Click Collect** — fill all fields and click the button. On success, the console logs the response containing `skyflow_id` and token values for each field. The status area turns green.
5. **Check the Network tab** — you should see a request to your vault URL. A `200` response confirms data was tokenized and stored.

### 9) Verification checklist

Use this checklist to confirm everything is working:

- [ ] `npm run dev` starts without errors
- [ ] All four element iframes render with correct height
- [ ] Console shows `[Skyflow] Element #field-N ready` for each element
- [ ] Typing in card number shows the card brand icon (Visa, Mastercard, etc.)
- [ ] Invalid input (e.g. `1234`) turns the text red (`invalid` style)
- [ ] Valid input (e.g. `4111 1111 1111 1111`) turns the text green (`complete` style)
- [ ] Collect with valid data returns tokens in the console and shows green status
- [ ] Collect with invalid/missing data shows an error and red status
- [ ] No sensitive values appear in your application code or network requests (only in the Skyflow iframe)

## Production Hardening

Before deploying, make these changes:

**1) Switch to production mode** — in `Skyflow.init()` options:

```ts
options: {
  logLevel: Skyflow.LogLevel.ERROR,
  env: Skyflow.Env.PROD,  // masks values in event callbacks
}
```

**2) Fetch tokens from your backend** — replace the static `getBearerToken` with a fetch call to your token endpoint:

```ts
getBearerToken: async () => {
  const response = await fetch("/api/skyflow-token");
  if (!response.ok) throw new Error("Failed to fetch Skyflow token");
  const { accessToken } = await response.json();
  return accessToken;
},
```

Your backend should use a Skyflow service account to generate short-lived bearer tokens. See the Skyflow documentation on bearer token generation for details.

**3) Build for production:**

```sh
npm run build
npm run preview  # serves the built output locally for testing
```

## Integrating into an Existing Project

If you're adding Skyflow Elements to an existing app instead of starting fresh:

- **Already using Vite (or another bundler)?** Skip the Vite setup — just `npm install skyflow-js` and add the client code to your existing entry point.
- **Have a backend server (Express, Fastify, etc.)?** You can serve the built output as static files:
  ```ts
  // Example: Express serving the Vite build output
  app.use(express.static(path.resolve("dist")));
  ```
- **Using a framework (React, Vue, Svelte)?** Mount Skyflow Elements inside a component's `useEffect` / `onMounted` / `onMount` lifecycle hook. Each element's `.mount()` call targets a ref or DOM selector within your component.

## Troubleshooting

| Symptom                                | Likely cause                       | Fix                                                                                    |
| --------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------- |
| Elements are invisible (0 height)      | Mount target `<div>` has no height | Add explicit `height` via CSS to the mount containers                                  |
| `skyflow is not defined`               | SDK not bundled                    | Ensure you're using a bundler (Vite) — `skyflow-js` is an npm module, not a CDN script |
| `401 Unauthorized` on collect          | Bearer token expired or invalid    | Generate a fresh token (they expire after ~60 min)                                     |
| CORS errors in console                 | Wrong vault URL or missing HTTPS   | Verify `VITE_SKYFLOW_VAULT_URL` matches your vault and starts with `https://`          |
| Collect returns validation errors      | Required fields empty or invalid   | Check element `CHANGE` events for `isValid: false` before collecting                   |
| `Missing VITE_SKYFLOW_*` error on load | Env vars not set                   | Create `.env.local` with all three variables; restart the dev server after changes     |

## Notes

- `skyflow-js` is distributed as an npm module — a bundler like Vite is required. It cannot be loaded via a plain `<script>` tag.
- Skyflow Elements support three container types: `COLLECT` (gather input), `REVEAL` (display tokenized data), and `COMPOSABLE` (multiple elements in a single iframe). This quickstart uses `COLLECT`.
- For non-card data (SSNs, emails, addresses), use `Skyflow.ElementType.INPUT_FIELD` — it supports custom regex validation and input masking via the `format` and `translation` options.
- Custom validation rules (`REGEX_MATCH_RULE`, `LENGTH_MATCH_RULE`, `ELEMENT_VALUE_MATCH_RULE`) can be added to any element via the `validations` array.
