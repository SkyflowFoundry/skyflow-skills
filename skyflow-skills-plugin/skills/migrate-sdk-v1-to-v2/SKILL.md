---
name: migrate-sdk-v1-to-v2
description: Guide migration from Skyflow V1 SDKs to V2, covering authentication changes, client initialization, request/response structures, and SDK-specific patterns.
---

# Migrate Skyflow SDK from V1 to V2

This skill guides you through migrating from Skyflow V1 SDKs to the new V2 SDKs. V2 introduces significant improvements including TypeScript support, multiple authentication options, multi-vault support, and enhanced error handling.

## Why Migrate to V2?

| Feature | V1 | V2 |
|---------|----|----|
| Type Safety | Limited or separate type packages | Native type support (TypeScript, type hints) |
| Authentication Options | Service account / token provider only | API Key, Env Var, Credentials File, JSON String, Bearer Token |
| Multi-Vault Support | Separate client per vault | Single client, multiple vaults |
| Log Levels | Global setting | Instance-specific |
| Error Details | Basic (code, description) | Enhanced (http_status, grpc_code, request_ID, details) |
| Vault Configuration | `vaultURL` | `clusterId`-based |
| Request Building | Plain objects / JSON | Typed request classes or builder pattern |
| Data Structures | Third-party JSON libraries | Native language collections |

## Migration Workflow

```
1. Discover ─> 2. Understand ─> 3. Migrate ─> 4. Test ─> 5. Verify
     │              │                │            │           │
     ├─ Find V1     ├─ Review        ├─ Update    ├─ Unit     ├─ Integration
     │  usage       │  breaking      │  imports   │  tests    │  tests
     ├─ Inventory   │  changes       ├─ Update    ├─ Access   ├─ Production
     │  code        ├─ Plan          │  auth      │  control  │  validation
     └─ Document    │  updates       ├─ Update    │  tests    │
        patterns    │                │  requests  │           │
                    │                └─ Update    │           │
                    │                   errors    │           │
```

## Phase 1: Discover Existing V1 Usage

Before migrating, inventory all V1 SDK usage in your codebase.

### V1 Identification Patterns

| SDK | V1 Import Pattern | V1 Initialization Pattern |
|-----|-------------------|---------------------------|
| Node.js | `require('skyflow-node')` | `Skyflow.init({ vaultID, vaultURL, getBearerToken })` |
| Python | `from skyflow.vault import Client, Configuration` | `Client(Configuration(vault_id, vault_url, token_provider))` |
| Java | `import com.skyflow.Skyflow` | `Skyflow.init(new SkyflowConfiguration(vaultId, vaultUrl, tokenProvider))` |
| Go | `import "github.com/skyflowapi/skyflow-go/skyflow/client"` | `Skyflow.Init(common.Configuration{VaultID, VaultURL, TokenProvider})` |

### Discovery Checklist

- [ ] Search for V1 import statements
- [ ] Identify all client initialization points
- [ ] List all API operations (insert, get, detokenize, etc.)
- [ ] Document authentication method currently used
- [ ] Note any custom error handling patterns
- [ ] Identify test files that need updating

Use [templates/code-inventory.md](templates/code-inventory.md) to document findings.

## Phase 2: Understand Breaking Changes

### Authentication Changes

V2 supports multiple authentication methods:

| Auth Method | Description | When to Use |
|-------------|-------------|-------------|
| **API Key** | Direct API key authentication | Simple backend services |
| **Environment Variable** | `SKYFLOW_CREDENTIALS` env var | CI/CD pipelines, containers |
| **Credentials File** | Path to credentials JSON file | Local development |
| **Stringified JSON** | Credentials as JSON string | Secrets managers |
| **Bearer Token** | Pre-generated bearer token | Frontend apps, short-lived tokens |

### Client Initialization Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Vault Location | `vaultURL: 'https://xxx.vault.skyflowapis.com'` | `clusterId: 'xxx'` |
| Multiple Vaults | Separate client instance per vault | Single client with `vaultConfigs` array |
| Log Level | Global setting | Per-instance via `logLevel` config |
| Type Safety | Separate type packages or none | Native types (TypeScript, type hints, generics) |
| Context (Go) | Not required | `context.Context` required for all operations |

**Extracting clusterId from vaultURL:**
- V1 vaultURL: `https://<clusterId>.vault.skyflowapis.com`
- V2 clusterId: `<clusterId>` (just the subdomain portion)

### Request Structure Changes

V2 uses typed request classes instead of plain objects. The exact syntax varies by SDK:

| SDK | V1 Request Pattern | V2 Request Pattern |
|-----|--------------------|--------------------|
| Node.js | `{ records: [{ table, fields }] }` | `new InsertRequest(table, values)` |
| Python | `{ 'records': [{ 'table', 'fields' }] }` | `InsertRequest(table=, values=, return_tokens=)` |
| Java | `JSONObject` with records array | `InsertRequest.builder().table().values().build()` |
| Go | `map[string]interface{}` with records | `common.InsertRequest{Table: , Values: }` |

**Key pattern changes:**
- Table name moves from inside each record to a top-level parameter
- Options move from separate class to request constructor/builder
- Response uses `insertedFields` instead of `records[].fields`

### Response Structure Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Insert Response | `response.records[0].fields.fieldName` | `response.insertedFields[0].fieldName` |
| Token Access | `response.records[0].tokens` key | Tokens included directly in response |
| Error Access | `error.code`, `error.description` | `error.http_status`, `error.grpc_code`, `error.request_ID`, `error.details` |

### Error Structure Changes

V2 provides significantly enhanced error information for debugging:

| V1 Error Property | V2 Error Property | Description |
|-------------------|-------------------|-------------|
| `code` | `http_code` / `httpCode` | HTTP status code |
| `description` | `message` | Error message |
| - | `http_status` / `httpStatus` | HTTP status string |
| - | `grpc_code` / `grpcCode` | gRPC error code |
| - | `request_id` / `requestId` | Unique request ID for support |
| - | `details` | Array of detailed error info |

> **Note:** Property naming varies by SDK (snake_case vs camelCase). See SDK-specific guides.

## Phase 3: Migrate Code

### Migration Steps

1. **Update package version** - Install V2 SDK via package manager
2. **Update imports** - Change to V2 import patterns
3. **Update authentication** - Choose appropriate auth method, update credentials config
4. **Update client initialization** - Change `vaultURL` to `clusterId`, add `vaultConfigs`
5. **Update request construction** - Replace plain objects with request classes
6. **Update response handling** - Use V2 response structure
7. **Update error handling** - Leverage new error properties

### SDK-Specific Migration Guides

See the detailed guide for your SDK:

| SDK | Guide | V2 Design Pattern |
|-----|-------|-------------------|
| Node.js | [node-sdk.md](node-sdk.md) | Class-based with native TypeScript |
| Python | [python-sdk.md](python-sdk.md) | Builder pattern (`Skyflow.builder()`) |
| Java | [java-sdk.md](java-sdk.md) | Builder pattern with fluent API |
| Go | [go-sdk.md](go-sdk.md) | Functional options pattern |

Each guide includes complete before/after code examples, migration checklists, and SDK-specific considerations.

## Phase 4: Test Migration

### Test Categories

| Category | What to Test |
|----------|--------------|
| Unit Tests | SDK initialization, request building, error parsing |
| Integration Tests | Full CRUD operations against test vault |
| Access Control | All roles can perform authorized operations |
| Error Handling | Correct error details extracted and logged |

### Test Checklist

- [ ] Insert operations return expected tokens
- [ ] Get operations return correctly structured responses
- [ ] Detokenize operations work with new request format
- [ ] Error handling captures enhanced error details
- [ ] Multi-vault operations work (if applicable)
- [ ] Log levels function as expected

## Phase 5: Verify in Production

### Pre-Production Checklist

- [ ] All tests passing in staging
- [ ] Production vault configured
- [ ] Service accounts/credentials set up for production
- [ ] Monitoring configured for errors
- [ ] Rollback plan documented

### Production Verification

- [ ] Deploy to subset of traffic if possible
- [ ] Monitor error rates
- [ ] Verify all operations succeed
- [ ] Check logs for unexpected warnings
- [ ] Confirm request_ID tracking works

## Common Migration Patterns

> **Note:** Examples below show Node.js/TypeScript syntax. See SDK-specific guides for exact syntax in your language.

### Pattern: Token Provider to Credentials Object

**V1:** Custom token provider function
```javascript
const auth = () => Promise.resolve(process.env.VAULT_BEARER_TOKEN);
const client = Skyflow.init({ vaultID, vaultURL, getBearerToken: auth });
```

**V2:** Credentials object with multiple auth options
```typescript
// Choose one authentication method
const credentials: Credentials = { apiKey: process.env.SKYFLOW_API_KEY };
// Or: { path: '/path/to/credentials.json' }
// Or: { token: 'bearer-token' }

const client = new Skyflow({ vaultConfigs: [{ vaultId, clusterId, credentials }] });
```

### Pattern: Single to Multi-Vault

**V1:** Separate client per vault
```javascript
const client1 = Skyflow.init({ vaultID: 'vault1', vaultURL: url1, getBearerToken });
const client2 = Skyflow.init({ vaultID: 'vault2', vaultURL: url2, getBearerToken });
```

**V2:** Single client with multiple vault configs
```typescript
const client = new Skyflow({
  vaultConfigs: [
    { vaultId: 'vault-1', clusterId: 'cluster-a', credentials },
    { vaultId: 'vault-2', clusterId: 'cluster-a', credentials }
  ]
});
// Access specific vault
await client.vault('vault-1').insert(request);
await client.vault('vault-2').get(request);
```

### Pattern: Records Array to Request Class

**V1:** Plain object with records array
```javascript
const response = await client.insert({
  records: [{ table: 'users', fields: { email: 'test@example.com' } }]
});
const token = response.records[0].fields.email;
```

**V2:** Typed request class, table as parameter
```typescript
const insertReq = new InsertRequest('users', [{ email: 'test@example.com' }]);
const response = await client.vault('vaultId').insert(insertReq);
const token = response.insertedFields[0].email;
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `vaultURL is not defined` | V1 initialization in V2 code | Use `clusterId` instead of `vaultURL` |
| `Cannot read property 'fields'` | V1 response access pattern | Use `insertedFields` instead of `records[].fields` |
| `Authentication failed` | Wrong auth method or credentials | Verify credentials match selected auth type |
| `Module not found` | Old import path | Update to V2 import pattern |
| `Records is not iterable` | V1 request format | Use V2 request classes/builder |
| `missing context parameter` (Go) | V2 requires context | Add `context.Context` to all operations |
| `JSONObject cannot be resolved` (Java) | V1 third-party JSON | Use native `ArrayList`/`HashMap` |
| `TokenProvider not found` | V1 auth interface removed | Use `Credentials` class/struct |

## Related Documentation

- [node-sdk.md](node-sdk.md) - Node.js SDK migration details
- [python-sdk.md](python-sdk.md) - Python SDK migration details
- [java-sdk.md](java-sdk.md) - Java SDK migration details
- [go-sdk.md](go-sdk.md) - Go SDK migration details
- [templates/migration-checklist.md](templates/migration-checklist.md) - Migration tracking template
- [templates/code-inventory.md](templates/code-inventory.md) - V1 usage discovery template

## Usage Instructions for Claude

When helping users migrate from V1 to V2:

1. **Identify the SDK** - Ask which SDK(s) they're using
2. **Assess scope** - How many files/modules use Skyflow?
3. **Link to SDK guide** - Direct to appropriate `{sdk}-sdk.md` file
4. **Use discovery template** - Help inventory V1 usage with `code-inventory.md`
5. **Provide code examples** - Show before/after for each change
6. **Track progress** - Use `migration-checklist.md` for larger migrations
7. **Test guidance** - Ensure tests are updated alongside code

### Key Questions to Ask

- Which Skyflow SDK(s) are you using?
- How many files/modules use the Skyflow SDK?
- What authentication method do you currently use?
- Do you need multi-vault support?
- What operations do you perform (insert, get, detokenize)?
- Do you have existing tests that need updating?
