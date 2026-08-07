# Node.js SDK Migration: V1 to V2

Detailed guide for migrating the Skyflow Node.js SDK from V1 to V2.

## Package Update

| V1 | V2 |
|----|-----|
| `npm install skyflow-node` | `npm install skyflow-node` (same package, new major version) |

V2 has native TypeScript support - separate `@types` packages are no longer needed.

```bash
# Update to V2
npm install skyflow-node@latest
```

## Import Changes

### V1 Imports

```javascript
const Skyflow = require('skyflow-node');
// or
const { Skyflow } = require('skyflow-node');
```

### V2 Imports

```typescript
import {
  Skyflow,
  Credentials,
  VaultConfig,
  SkyflowConfig,
  Env,
  LogLevel,
  // Request classes
  InsertRequest,
  GetRequest,
  DetokenizeRequest,
  // Options classes
  InsertOptions,
  GetOptions,
  // Response types
  InsertResponse,
  GetResponse,
  DetokenizeResponse
} from 'skyflow-node';
```

## Authentication Migration

### V1: Bearer Token Function

```javascript
// V1: Pass a function that returns a bearer token
const auth = function () {
  return new Promise((resolve, reject) => {
    resolve(process.env.VAULT_BEARER_TOKEN);
  });
};

const client = Skyflow.init({
  vaultID: 'your-vault-id',
  vaultURL: 'https://your-cluster.vault.skyflowapis.com',
  getBearerToken: auth
});
```

### V2: Multiple Authentication Options

#### Option 1: API Key

```typescript
import { Credentials } from 'skyflow-node';

const credentials: Credentials = {
  apiKey: '<YOUR_SKYFLOW_API_KEY>'
};
```

#### Option 2: Environment Variable (Recommended)

```typescript
// Set SKYFLOW_CREDENTIALS environment variable with your credentials JSON
// The SDK will automatically read from this env var
const credentials: Credentials = {};  // Empty - SDK reads from env
```

#### Option 3: Credentials File Path

```typescript
const credentials: Credentials = {
  path: '<YOUR_CREDENTIALS_FILE_PATH>'
};
```

#### Option 4: Stringified JSON

```typescript
const credentials: Credentials = {
  credentialsString: JSON.stringify({
    clientID: '...',
    clientName: '...',
    keyID: '...',
    tokenURI: '...',
    privateKey: '...'
  })
};
```

#### Option 5: Bearer Token

```typescript
const credentials: Credentials = {
  token: '<YOUR_BEARER_TOKEN>'
};
```

## Client Initialization Migration

### V1 Initialization

```javascript
const client = Skyflow.init({
  vaultID: 'your-vault-id',
  vaultURL: 'https://your-cluster.vault.skyflowapis.com',
  getBearerToken: auth
});
```

### V2 Initialization

```typescript
import { Credentials, VaultConfig, SkyflowConfig, Env, LogLevel, Skyflow } from 'skyflow-node';

// Step 1: Configure credentials
const credentials: Credentials = {
  apiKey: '<YOUR_API_KEY>'
};

// Step 2: Configure vault(s)
const primaryVaultConfig: VaultConfig = {
  vaultId: '<YOUR_VAULT_ID>',      // Same as V1 vaultID
  clusterId: '<YOUR_CLUSTER_ID>',  // Extract from V1 vaultURL
  env: Env.PROD,                   // or Env.SANDBOX
  credentials: credentials         // Can override per-vault
};

// Step 3: Configure Skyflow client
const skyflowConfig: SkyflowConfig = {
  vaultConfigs: [primaryVaultConfig],
  skyflowCredentials: credentials,  // Default credentials
  logLevel: LogLevel.INFO           // Instance-specific log level
};

// Step 4: Initialize client
const skyflowClient: Skyflow = new Skyflow(skyflowConfig);
```

### Extracting clusterId from vaultURL

| V1 vaultURL | V2 clusterId |
|-------------|--------------|
| `https://abc123.vault.skyflowapis.com` | `abc123` |
| `https://my-cluster.vault.skyflowapis.com` | `my-cluster` |

### Multi-Vault Configuration (V2 New Feature)

```typescript
const skyflowConfig: SkyflowConfig = {
  vaultConfigs: [
    { vaultId: 'vault-1', clusterId: 'cluster-a', env: Env.PROD },
    { vaultId: 'vault-2', clusterId: 'cluster-a', env: Env.PROD },
    { vaultId: 'vault-3', clusterId: 'cluster-b', env: Env.SANDBOX }
  ],
  skyflowCredentials: credentials,
  logLevel: LogLevel.ERROR
};

const client = new Skyflow(skyflowConfig);

// Access specific vault
const vault1Response = await client.vault('vault-1').insert(request);
const vault2Response = await client.vault('vault-2').insert(request);
```

## Insert Operation Migration

### V1 Insert

```javascript
const result = await client.insert({
  records: [
    {
      fields: {
        card_number: '4111111111111111',
        expiry_date: '11/22',
        fullname: 'John Doe'
      },
      table: 'cards'
    }
  ]
});

// V1 Response structure
// {
//   "records": [
//     {
//       "table": "cards",
//       "fields": {
//         "card_number": "token-uuid-1",
//         "expiry_date": "token-uuid-2"
//       }
//     }
//   ]
// }
```

### V2 Insert

```typescript
import { InsertRequest, InsertOptions, InsertResponse } from 'skyflow-node';

// Prepare data
const insertData: Record<string, unknown>[] = [
  {
    card_number: '4111111111111111',
    expiry_date: '11/22',
    fullname: 'John Doe'
  }
];

// Create request
const insertReq: InsertRequest = new InsertRequest(
  'cards',      // table name
  insertData    // array of records
);

// Configure options (optional)
const insertOptions: InsertOptions = new InsertOptions();
insertOptions.setReturnTokens(true);      // Get tokens for inserted data
insertOptions.setContinueOnError(true);   // Continue on partial errors

// Execute insert
const response: InsertResponse = await skyflowClient
  .vault('<VAULT_ID>')
  .insert(insertReq, insertOptions);

// V2 Response structure
// InsertResponse {
//   insertedFields: [
//     {
//       skyflowId: 'record-uuid',
//       card_number: 'token-uuid-1',
//       expiry_date: 'token-uuid-2',
//       fullname: 'token-uuid-3'
//     }
//   ],
//   errors: null
// }
```

### Key Insert Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Request format | `{ records: [{ table, fields }] }` | `new InsertRequest(table, data)` |
| Table location | Inside each record | Constructor parameter |
| Options | `{ options: { tokens: true } }` | `InsertOptions` class with setters |
| Response tokens | Nested under `tokens` key | Directly in `insertedFields` |
| Skyflow ID | `fields.skyflow_id` | `skyflowId` at record level |

## Get Operation Migration

### V1 Get

```javascript
const result = await client.get({
  records: [
    {
      ids: ['skyflow-id-1', 'skyflow-id-2'],
      table: 'cards',
      redaction: 'MASKED'
    }
  ]
});

// Access fields
const cardNumber = result.records[0].fields.card_number;
```

### V2 Get

```typescript
import { GetRequest, GetOptions, GetResponse } from 'skyflow-node';

// Create request
const getReq: GetRequest = new GetRequest(
  'cards',
  ['skyflow-id-1', 'skyflow-id-2']  // Skyflow IDs
);

// Configure options
const getOptions: GetOptions = new GetOptions();
getOptions.setRedaction('MASKED');

// Execute get
const response: GetResponse = await skyflowClient
  .vault('<VAULT_ID>')
  .get(getReq, getOptions);

// Access response
const records = response.data;
const cardNumber = records[0].card_number;
```

## Detokenize Operation Migration

### V1 Detokenize

```javascript
const result = await client.detokenize({
  records: [
    { token: 'token-1' },
    { token: 'token-2', redaction: 'PLAIN_TEXT' }
  ]
});

// Access values
const value1 = result.records[0].value;
```

### V2 Detokenize

```typescript
import { DetokenizeRequest, DetokenizeResponse } from 'skyflow-node';

// Create request
const detokenizeReq: DetokenizeRequest = new DetokenizeRequest([
  'token-1',
  'token-2'
]);

// Execute detokenize
const response: DetokenizeResponse = await skyflowClient
  .vault('<VAULT_ID>')
  .detokenize(detokenizeReq);

// Access response
const values = response.detokenizedFields;
```

## Error Handling Migration

### V1 Error Handling

```javascript
try {
  await client.insert(request);
} catch (error) {
  console.log('Error code:', error.code);
  console.log('Description:', error.description);
}
```

### V2 Error Handling

```typescript
try {
  await skyflowClient.vault('vault-id').insert(insertReq, insertOptions);
} catch (error) {
  // V2 enhanced error properties
  console.log('Message:', error.message);
  console.log('HTTP Status:', error.http_status);
  console.log('HTTP Code:', error.http_code);
  console.log('gRPC Code:', error.grpc_code);
  console.log('Request ID:', error.request_ID);  // Useful for debugging with Skyflow support

  // Detailed error breakdown
  if (error.details) {
    error.details.forEach((detail: string) => {
      console.log('Detail:', detail);
    });
  }
}
```

### Error Structure Comparison

| V1 Property | V2 Property | Description |
|-------------|-------------|-------------|
| `code` | `http_code` | HTTP status code |
| `description` | `message` | Error message |
| - | `http_status` | HTTP status string |
| - | `grpc_code` | gRPC error code |
| - | `request_ID` | Unique request identifier |
| - | `details` | Array of detailed error messages |

## TypeScript Support

V2 provides comprehensive TypeScript definitions. Key types:

```typescript
import {
  // Configuration
  Credentials,
  VaultConfig,
  SkyflowConfig,

  // Enums
  Env,
  LogLevel,

  // Requests
  InsertRequest,
  GetRequest,
  DetokenizeRequest,
  UpdateRequest,
  DeleteRequest,

  // Options
  InsertOptions,
  GetOptions,

  // Responses
  InsertResponse,
  GetResponse,
  DetokenizeResponse
} from 'skyflow-node';
```

## Migration Checklist for Node.js

### Package & Imports

- [ ] Update `package.json` to latest `skyflow-node`
- [ ] Run `npm install`
- [ ] Remove any `@types/skyflow-node` packages (now built-in)
- [ ] Update import statements to V2 pattern
- [ ] Add TypeScript types if using TypeScript

### Authentication

- [ ] Choose appropriate credential type for your use case
- [ ] Update credential initialization code
- [ ] Test authentication works
- [ ] Update any token refresh logic

### Client Initialization

- [ ] Extract `clusterId` from V1 `vaultURL`
- [ ] Update to `new Skyflow(config)` pattern
- [ ] Configure `vaultConfigs` array
- [ ] Set appropriate `logLevel`
- [ ] Configure multiple vaults if needed

### Insert Operations

- [ ] Replace object literals with `InsertRequest`
- [ ] Move table name to constructor parameter
- [ ] Use `InsertOptions` for configuration
- [ ] Update to `.vault('id').insert()` call pattern
- [ ] Update response access (no more nested `tokens` key)

### Get Operations

- [ ] Replace object literals with `GetRequest`
- [ ] Use `GetOptions` for redaction configuration
- [ ] Update to `.vault('id').get()` call pattern
- [ ] Update response field access

### Detokenize Operations

- [ ] Replace object literals with `DetokenizeRequest`
- [ ] Update to `.vault('id').detokenize()` call pattern
- [ ] Update response value access

### Error Handling

- [ ] Update catch blocks for new error structure
- [ ] Access `http_status` instead of `code`
- [ ] Access `message` instead of `description`
- [ ] Log `request_ID` for debugging support
- [ ] Handle `details` array for granular errors

### Testing

- [ ] Update unit test mocks for V2 patterns
- [ ] Update integration tests
- [ ] Verify all operations work in test environment
- [ ] Test error handling paths

## Quick Reference: V1 to V2 Mapping

| V1 Pattern | V2 Pattern |
|------------|------------|
| `Skyflow.init({...})` | `new Skyflow({...})` |
| `vaultURL: 'https://...'` | `clusterId: '...'` |
| `getBearerToken: fn` | `credentials: { apiKey }` or other auth option |
| `{ records: [{ table, fields }] }` | `new InsertRequest(table, [fields])` |
| `{ options: { tokens: true } }` | `new InsertOptions().setReturnTokens(true)` |
| `response.records[0].fields.email` | `response.insertedFields[0].email` |
| `error.code` | `error.http_code` or `error.http_status` |
| `error.description` | `error.message` |
| Global log level | `logLevel` in `SkyflowConfig` |

## Additional Resources

- [Skyflow Node.js SDK Documentation](https://docs.skyflow.com/sdks/skyflow-node/)
- [Node.js SDK GitHub Repository](https://github.com/skyflowapi/skyflow-node)
- [Node.js SDK npm Package](https://www.npmjs.com/package/skyflow-node)
