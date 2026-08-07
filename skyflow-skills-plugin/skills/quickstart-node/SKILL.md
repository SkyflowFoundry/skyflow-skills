---
name: quickstart-node
description: A quickstart guide for setting up a Node.js project with the skyflow-node SDK.
---

# Quickstart: Node.js with skyflow-node

This guide describes a standard setup for a new Node.js project using TypeScript with ES modules and the skyflow-node SDK. ESLint and Prettier are optional.

## Prerequisites

- Node.js (LTS recommended)
- npm (comes with Node.js)
- TypeScript
- skyflow-node

## Steps

### 1) Initialize the project

```sh
mkdir my-skyflow-project
cd my-skyflow-project
npm init -y
```

### 2) Install required dependencies

```sh
npm install skyflow-node
npm install -D typescript @types/node
```

### 3) Create a TypeScript config

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": ".",
    "strict": true,
    "types": ["node"],
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["index.ts"]
}
```

### 4) Add the entry file

Create `index.ts`:

```ts
import {
  Skyflow, // Vault client
  isExpired, // JWT auth helpers
  LogLevel, // logging options
  Credentials,
} from "skyflow-node";

const credentials: Credentials = {
  token: "<BEARER_TOKEN>",
};
```

### 5) Set package type and scripts

Update `package.json`:

```json
{
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

### 6) Build and run

```sh
npm run build
npm start
```

## Optional: ESLint and Prettier

1) Install tools

```sh
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin prettier eslint-config-prettier
```

2) Add ESLint config

Create `.eslintrc.cjs`:

```js
module.exports = {
  root: true,
  env: {
    node: true,
    es2020: true,
  },
  parser: "@typescript-eslint/parser",
  parserOptions: {
    sourceType: "module",
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  ignorePatterns: ["dist/"],
};
```

3) Add Prettier config

Create `.prettierrc`:

```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100
}
```

4) Add scripts

Update `package.json`:

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts",
    "format": "prettier --write ."
  }
}
```

## Optional: CSpell

1) Install CSpell

```sh
npm install -D cspell
```

2) Add a repo dictionary

Create `cspell.json`:

```json
{
  "version": "0.2",
  "ignorePaths": [
    "node_modules",
    "dist",
    "package-lock.json"
  ],
  "words": [
    "skyflow"
  ]
}
```

3) Add a script

Update `package.json`:

```json
{
  "scripts": {
    "spellcheck": "cspell --config cspell.json \"**/*\""
  }
}
```

4) Run spellcheck

```sh
npm run spellcheck
```
