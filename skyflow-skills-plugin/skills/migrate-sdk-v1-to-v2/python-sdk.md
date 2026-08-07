# Python SDK Migration: V1 to V2

Detailed guide for migrating the Skyflow Python SDK from V1 to V2.

## Package Update

| V1 | V2 |
|----|-----|
| `pip install skyflow` | `pip install skyflow` (same package, new major version) |

```bash
# Update to V2
pip install --upgrade skyflow
```

## Import Changes

### V1 Imports

```python
from skyflow.vault import Client, Configuration, InsertOptions
from skyflow.service_account import generate_bearer_token, is_expired
```

### V2 Imports

```python
from skyflow import Skyflow, Env, LogLevel
from skyflow.vault.data import InsertRequest, InsertResponse
from skyflow.vault.tokens import TokenMode
```

## Authentication Migration

### V1: Token Provider Function

```python
# V1: User-defined function to provide access token
def token_provider():
    global bearer_token
    if not is_expired(bearer_token):
        return bearer_token
    bearer_token, _ = generate_bearer_token('<YOUR_CREDENTIALS_FILE_PATH>')
    return bearer_token
```

### V2: Multiple Authentication Options

#### Option 1: API Key

```python
credentials = {
    'api_key': '<YOUR_API_KEY>'
}
```

#### Option 2: Environment Variable (Recommended)

```python
# Set SKYFLOW_CREDENTIALS environment variable with your credentials JSON
# The SDK will automatically read from this env var
# No credentials dict needed - just don't pass credentials
```

#### Option 3: Credentials File Path

```python
credentials = {
    'path': '<PATH_TO_CREDENTIALS_JSON>'
}
```

#### Option 4: Stringified JSON

```python
credentials = {
    'credentials_string': '<YOUR_CREDENTIALS_STRING>'
}
```

#### Option 5: Bearer Token

```python
credentials = {
    'token': '<YOUR_BEARER_TOKEN>'
}
```

**Notes:**
- Use only ONE authentication method
- API Key or Environment Variables are recommended for production
- Secure storage of credentials is essential

## Client Initialization Migration

### V1 Initialization

```python
from skyflow.vault import Client, Configuration

# V1: Simple configuration object
config = Configuration('<VAULT_ID>', '<VAULT_URL>', token_provider)
client = Client(config)
```

### V2 Initialization (Builder Pattern)

```python
from skyflow import Skyflow, Env, LogLevel

# V2: Builder pattern with vault config
client = (
    Skyflow.builder()
    .add_vault_config({
        'vault_id': '<VAULT_ID>',      # Same as V1
        'cluster_id': '<CLUSTER_ID>',  # Extract from V1 vault_url
        'env': Env.PROD,               # or Env.SANDBOX
        'credentials': credentials      # Individual vault credentials
    })
    .add_skyflow_credentials(credentials)  # Default credentials
    .set_log_level(LogLevel.INFO)          # Instance-specific log level
    .build()
)
```

### Extracting cluster_id from vault_url

| V1 vault_url | V2 cluster_id |
|--------------|---------------|
| `https://abc123.vault.skyflowapis.com` | `abc123` |
| `https://my-cluster.vault.skyflowapis.com` | `my-cluster` |

### Multi-Vault Configuration (V2 New Feature)

```python
client = (
    Skyflow.builder()
    .add_vault_config({
        'vault_id': 'vault-1',
        'cluster_id': 'cluster-a',
        'env': Env.PROD,
        'credentials': credentials
    })
    .add_vault_config({
        'vault_id': 'vault-2',
        'cluster_id': 'cluster-a',
        'env': Env.PROD
    })
    .add_skyflow_credentials(credentials)  # Used when vault has no individual credentials
    .set_log_level(LogLevel.ERROR)
    .build()
)

# Access specific vault
response = client.vault('vault-1').insert(insert_request)
```

## Insert Operation Migration

### V1 Insert

```python
# V1: Dict-based request with separate options
response = client.insert(
    {
        'records': [
            {
                'table': 'cards',
                'fields': {
                    'cardNumber': '4111111111111111',
                    'cvv': '123',
                },
            }
        ]
    },
    InsertOptions(True),  # tokens=True
)

# V1 Response structure
# {
#     'records': [
#         {
#             'table': 'cards',
#             'fields': {
#                 'cardNumber': 'token-uuid-1',
#                 'cvv': 'token-uuid-2',
#                 'skyflow_id': 'record-uuid'
#             },
#             'request_index': 0
#         }
#     ]
# }
```

### V2 Insert

```python
from skyflow.vault.data import InsertRequest

# Prepare data
insert_data = [
    {
        'card_number': '4111111111111111',
        'cvv': '123',
    },
]

# Create request with options as constructor parameters
insert_request = InsertRequest(
    table='cards',
    values=insert_data,
    return_tokens=True,      # Optional: Get tokens for inserted data
    continue_on_error=True   # Optional: Continue on partial errors
)

# Execute insert
response = client.vault('<VAULT_ID>').insert(insert_request)

# V2 Response structure
# InsertResponse(
#     inserted_fields=[
#         {
#             'skyflow_id': 'a8f3ed5d-55eb-4f32-bf7e-2dbf4b9d9097',
#             'card_number': '5479-4229-4622-1393'
#         }
#     ],
#     errors=[]
# )
```

### Key Insert Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Request format | `{'records': [{'table', 'fields'}]}` | `InsertRequest(table=, values=)` |
| Table location | Inside each record dict | Constructor parameter |
| Options | Separate `InsertOptions(True)` | Constructor params: `return_tokens=`, `continue_on_error=` |
| Response tokens | Under `fields` key | Directly in `inserted_fields` |
| Skyflow ID | `fields.skyflow_id` | `skyflow_id` at record level |

## Request Options Migration

### V1 Options (Separate Class)

```python
from skyflow.vault import InsertOptions

options = InsertOptions(
    tokens=True
)

response = client.insert(data, options)
```

### V2 Options (Constructor Parameters)

```python
from skyflow.vault.data import InsertRequest
from skyflow.vault.tokens import TokenMode

insert_request = InsertRequest(
    table='cards',
    values=insert_data,
    return_tokens=False,           # Do not return tokens
    continue_on_error=False,       # Stop on first error
    upsert='<UPSERT_COLUMN>',      # Column for upsert logic
    token_mode=TokenMode.DISABLE,  # Disable BYOT
    tokens='<TOKENS>'              # Tokens when TokenMode is ENABLE
)
```

### Available InsertRequest Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `table` | str | Table name (required) |
| `values` | list | Data to insert (required) |
| `return_tokens` | bool | Return tokens for inserted data |
| `continue_on_error` | bool | Continue inserting on partial errors |
| `upsert` | str | Column name for upsert logic |
| `token_mode` | TokenMode | BYOT mode (ENABLE/DISABLE) |
| `tokens` | str | Tokens when BYOT enabled |

## Error Handling Migration

### V1 Error Handling

```python
try:
    response = client.insert(data, options)
except Exception as error:
    print(f'Error code: {error.code}')
    print(f'Message: {error.message}')
```

### V2 Error Handling

```python
try:
    response = client.vault('vault-id').insert(insert_request)
except Exception as error:
    # V2 enhanced error properties
    print(f'HTTP Status: {error.http_status}')
    print(f'HTTP Code: {error.http_code}')
    print(f'gRPC Code: {error.grpc_code}')
    print(f'Message: {error.message}')
    print(f'Request ID: {error.request_id}')  # Useful for Skyflow support

    # Detailed error breakdown
    if error.details:
        for detail in error.details:
            print(f'Detail: {detail}')
```

### Error Structure Comparison

| V1 Property | V2 Property | Description |
|-------------|-------------|-------------|
| `code` | `http_code` | HTTP status code |
| `message` | `message` | Error message |
| - | `http_status` | HTTP status string |
| - | `grpc_code` | gRPC error code |
| - | `request_id` | Unique request identifier |
| - | `details` | List of detailed error messages |

## Migration Checklist for Python

### Package & Imports

- [ ] Update to latest `skyflow` package: `pip install --upgrade skyflow`
- [ ] Update import statements to V2 pattern
- [ ] Import `Skyflow`, `Env`, `LogLevel` from `skyflow`
- [ ] Import request classes from `skyflow.vault.data`

### Authentication

- [ ] Choose appropriate credential method for your use case
- [ ] Replace `token_provider` function with credentials dict
- [ ] Remove `generate_bearer_token` and `is_expired` imports
- [ ] Test authentication works

### Client Initialization

- [ ] Extract `cluster_id` from V1 `vault_url`
- [ ] Update to builder pattern: `Skyflow.builder()...build()`
- [ ] Use `add_vault_config()` for vault configuration
- [ ] Set `env` parameter (Env.PROD or Env.SANDBOX)
- [ ] Configure `set_log_level()` if needed
- [ ] Add multiple vaults if needed

### Insert Operations

- [ ] Replace dict-based requests with `InsertRequest`
- [ ] Move table name to constructor parameter
- [ ] Move options to constructor parameters (`return_tokens=`, `continue_on_error=`)
- [ ] Update to `.vault('id').insert()` call pattern
- [ ] Update response access (use `inserted_fields` instead of `records[0].fields`)

### Get Operations

- [ ] Replace dict-based requests with appropriate request class
- [ ] Update to `.vault('id').get()` call pattern
- [ ] Update response field access

### Detokenize Operations

- [ ] Replace dict-based requests with appropriate request class
- [ ] Update to `.vault('id').detokenize()` call pattern
- [ ] Update response value access

### Error Handling

- [ ] Update catch blocks for new error structure
- [ ] Access `http_code` instead of `code`
- [ ] Log `request_id` for debugging support
- [ ] Handle `details` list for granular errors

### Testing

- [ ] Update unit test mocks for V2 patterns
- [ ] Update integration tests
- [ ] Verify all operations work in test environment
- [ ] Test error handling paths

## Quick Reference: V1 to V2 Mapping

| V1 Pattern | V2 Pattern |
|------------|------------|
| `Configuration(vault_id, vault_url, token_provider)` | `Skyflow.builder().add_vault_config({...}).build()` |
| `vault_url='https://...'` | `cluster_id='...'` |
| `token_provider` function | `credentials` dict |
| `Client(config)` | `Skyflow.builder()...build()` |
| `client.insert({'records': [...]}, InsertOptions(True))` | `client.vault('id').insert(InsertRequest(...))` |
| `InsertOptions(tokens=True)` | `InsertRequest(..., return_tokens=True)` |
| `response['records'][0]['fields']['email']` | `response.inserted_fields[0]['email']` |
| `error.code` | `error.http_code` |
| `error.message` | `error.message` |
| Global log level | `set_log_level()` in builder |

## Additional Resources

- [Skyflow Python SDK Documentation](https://docs.skyflow.com/sdks/skyflow-python/)
- [Python SDK GitHub Repository](https://github.com/skyflowapi/skyflow-python)
- [Python SDK PyPI Package](https://pypi.org/project/skyflow/)
- See [SKILL.md](SKILL.md) for complete migration workflow and concepts
