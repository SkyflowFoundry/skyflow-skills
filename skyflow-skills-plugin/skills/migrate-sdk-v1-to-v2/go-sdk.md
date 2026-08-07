# Go SDK Migration: V1 to V2

Detailed guide for migrating the Skyflow Go SDK from V1 to V2.

## Package Update

| V1 | V2 |
|----|-----|
| `github.com/skyflowapi/skyflow-go` | `github.com/skyflowapi/skyflow-go/v2` |

```bash
# Update to V2
go get github.com/skyflowapi/skyflow-go/v2
```

## Import Changes

### V1 Imports

```go
import (
    Skyflow "github.com/skyflowapi/skyflow-go/skyflow/client"
    "github.com/skyflowapi/skyflow-go/skyflow/common"
    saUtil "github.com/skyflowapi/skyflow-go/serviceaccount/util"
)
```

### V2 Imports

```go
import (
    "context"
    "fmt"
    "github.com/skyflowapi/skyflow-go/v2/client"
    "github.com/skyflowapi/skyflow-go/v2/utils/common"
    "github.com/skyflowapi/skyflow-go/v2/utils/logger"
)
```

## Authentication Migration

### V1: Token Provider Function

```go
package main

import (
    "fmt"
    saUtil "github.com/skyflowapi/skyflow-go/serviceaccount/util"
)

var bearerToken = ""

func GetSkyflowBearerToken() (string, error) {
    filePath := "<file_path>"
    if saUtil.IsExpired(bearerToken) {
        newToken, err := saUtil.GenerateBearerToken(filePath)
        if err != nil {
            return "", err
        } else {
            bearerToken = newToken.AccessToken
            return bearerToken, nil
        }
    }
    return bearerToken, nil
}
```

### V2: Multiple Authentication Options

#### Option 1: API Key

```go
skyflowCredentials := common.Credentials{
    ApiKey: "<YOUR_API_KEY>",
}
```

#### Option 2: Environment Variable (Recommended)

```go
// Set SKYFLOW_CREDENTIALS environment variable with your credentials JSON
// The SDK will automatically read from this env var
skyflowCredentials := common.Credentials{}
```

#### Option 3: Credentials File Path

```go
skyflowCredentials := common.Credentials{
    Path: "<YOUR_CREDENTIALS_FILE_PATH>",
}
```

#### Option 4: Stringified JSON

```go
skyflowCredentials := common.Credentials{
    CredentialsString: "<YOUR_CREDENTIALS_STRING>",
}
```

#### Option 5: Bearer Token

```go
skyflowCredentials := common.Credentials{
    Token: "<BEARER_TOKEN>",
}
```

## Client Initialization Migration

### V1 Initialization

```go
import (
    Skyflow "github.com/skyflowapi/skyflow-go/skyflow/client"
    "github.com/skyflowapi/skyflow-go/skyflow/common"
)

configuration := common.Configuration{
    VaultID:       "<vault_id>",       // ID of the vault
    VaultURL:      "<vault_url>",      // URL of the vault
    TokenProvider: GetSkyflowBearerToken, // Token provider function
}

skyflowClient := Skyflow.Init(configuration)
```

### V2 Initialization (Functional Options Pattern)

```go
import (
    "context"
    "fmt"
    "github.com/skyflowapi/skyflow-go/v2/client"
    "github.com/skyflowapi/skyflow-go/v2/utils/common"
    "github.com/skyflowapi/skyflow-go/v2/utils/logger"
)

func main() {
    // Configure credentials
    creds := common.Credentials{
        Path: "<YOUR_CREDENTIALS_FILE_PATH>",
    }

    // Configure vault
    vaultConfig := common.VaultConfig{
        VaultId:     "<VAULT_ID>",
        ClusterId:   "<CLUSTER_ID>",  // Extracted from V1 VaultURL
        Env:         common.PROD,      // or common.DEV, common.STAGE
        Credentials: creds,
    }

    // Build vault configs array
    var vaultConfigs []common.VaultConfig
    vaultConfigs = append(vaultConfigs, vaultConfig)

    // Create Skyflow client with functional options
    skyflowClient, err := client.NewSkyflow(
        client.WithVaults(vaultConfigs...),
        client.WithCredentials(creds),       // Default credentials
        client.WithLogLevel(logger.ERROR),   // Instance-specific log level
    )

    if err != nil {
        fmt.Println("Error initializing client:", err)
        return
    }
}
```

### Extracting ClusterId from VaultURL

| V1 VaultURL | V2 ClusterId |
|-------------|--------------|
| `https://abc123.vault.skyflowapis.com` | `abc123` |
| `https://my-cluster.vault.skyflowapis.com` | `my-cluster` |

### Multi-Vault Configuration (V2 New Feature)

```go
creds1 := common.Credentials{Path: "<CREDENTIALS_FILE_PATH_1>"}
creds2 := common.Credentials{Path: "<CREDENTIALS_FILE_PATH_2>"}

vaultConfig1 := common.VaultConfig{
    VaultId:     "<VAULT_ID_1>",
    ClusterId:   "<CLUSTER_ID_1>",
    Env:         common.PROD,
    Credentials: creds1,
}

vaultConfig2 := common.VaultConfig{
    VaultId:     "<VAULT_ID_2>",
    ClusterId:   "<CLUSTER_ID_2>",
    Env:         common.PROD,
    Credentials: creds2,
}

var vaultConfigs []common.VaultConfig
vaultConfigs = append(vaultConfigs, vaultConfig1, vaultConfig2)

skyflowClient, err := client.NewSkyflow(
    client.WithVaults(vaultConfigs...),
    client.WithLogLevel(logger.DEBUG),
)

// Access specific vault
service, _ := skyflowClient.Vault("<VAULT_ID_1>")
```

### Key Initialization Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Pattern | `Skyflow.Init(configuration)` | `client.NewSkyflow(options...)` |
| Vault Location | `VaultURL` | `ClusterId` |
| Multiple Vaults | Separate client per vault | Single client with `WithVaults()` |
| Log Level | Global | `WithLogLevel()` per instance |
| Credentials | `TokenProvider` function | `common.Credentials` struct |

## Insert Operation Migration

### V1 Insert

```go
import (
    Skyflow "github.com/skyflowapi/skyflow-go/skyflow/client"
    "github.com/skyflowapi/skyflow-go/skyflow/common"
)

// Build records using maps
var records = make(map[string]interface{})

var record = make(map[string]interface{})
record["table"] = "<your_table_name>"

var fields = make(map[string]interface{})
fields["<field_name>"] = "<field_value>"
record["fields"] = fields

var recordsArray []interface{}
recordsArray = append(recordsArray, record)
records["records"] = recordsArray

// Upsert options
var upsertArray []common.UpsertOptions
var upsertOption = common.UpsertOptions{
    Table:  "<table_name>",
    Column: "<column_name>",
}
upsertArray = append(upsertArray, upsertOption)

// Insert options
options := common.InsertOptions{
    Tokens:          true,        // Return tokens
    Upsert:          upsertArray, // Upsert support
    ContinueOnError: true,        // Continue on partial errors
}

res, err := skyflowClient.Insert(records, options)

// V1 Response structure
// {
//     "Records": [
//         {
//             "table": "cards",
//             "fields": {
//                 "skyflow_id": "16419435-aa63-4823-aae7-19c6a2d6a19f",
//                 "cardNumber": "f3907186-e7e2-466f-91e5-48e12c2bcbc1",
//                 "cvv": "1989cb56-63da-4482-a2df-1f74cd0dd1a5"
//             }
//         }
//     ]
// }
```

### V2 Insert

```go
// Get vault service
service, serviceError := skyflowClient.Vault("<VAULT_ID>")
if serviceError != nil {
    fmt.Println(serviceError)
    return
}

ctx := context.TODO()

// Build values using native Go data structures
values := make([]map[string]interface{}, 0)
values = append(values, map[string]interface{}{
    "<COLUMN_NAME_1>": "<COLUMN_VALUE_1>",
})
values = append(values, map[string]interface{}{
    "<COLUMN_NAME_2>": "<COLUMN_VALUE_2>",
})

// Optional: BYOT tokens
tokens := make([]map[string]interface{}, 0)
tokens = append(tokens, map[string]interface{}{
    "<COLUMN_NAME_1>": "<TOKEN_VALUE_1>",
})

// Create insert request and options
insertRequest := common.InsertRequest{
    Table:  "<TABLE_NAME>",
    Values: values,
}

insertOptions := common.InsertOptions{
    ContinueOnError: false,
    ReturnTokens:    true,
    TokenMode:       common.DISABLE,  // or common.ENABLE for BYOT
    Upsert:          "<UPSERT_COLUMN>",
    Tokens:          tokens,          // Required when TokenMode is ENABLE
}

// Execute insert
insert, err := service.Insert(ctx, insertRequest, insertOptions)

if err != nil {
    fmt.Println("Error occurred:", *err)
} else {
    fmt.Println("Response:", insert)
}

// V2 Response structure
// {
//     "InsertedFields": [
//         {
//             "card_number": "5484-7829-1702-9110",
//             "request_index": "0",
//             "skyflow_id": "9fac9201-7b8a-4446-93f8-5244e1213bd1",
//             "cardholder_name": "b2308e2a-c1f5-469b-97b7-1f193159399b"
//         }
//     ],
//     "Errors": []
// }
```

### Key Insert Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Data Structure | Third-party JSON objects | Native Go maps and slices |
| Request Format | `map[string]interface{}` with `records` | `common.InsertRequest` struct |
| Table Location | Inside each record map | `InsertRequest.Table` field |
| Options | `common.InsertOptions` with `Tokens` | `common.InsertOptions` with `ReturnTokens` |
| Upsert | `[]common.UpsertOptions` | `string` (column name) |
| Response | `Records[].fields` | `InsertedFields[]` |
| Context | Not required | `context.Context` required |

## Request Options Migration

### V1 Options

```go
var upsertArray []common.UpsertOptions
upsertArray = append(upsertArray, common.UpsertOptions{
    Table:  "<table_name>",
    Column: "<column_name>",
})

options := common.InsertOptions{
    Tokens:          true,        // Return tokens for inserted data
    Upsert:          upsertArray, // Upsert support
    ContinueOnError: true,        // Continue on partial errors
}
```

### V2 Options

```go
options := common.InsertOptions{
    ReturnTokens:    true,             // Return tokens for inserted data
    ContinueOnError: false,            // Stop on first error
    TokenMode:       common.DISABLE,   // BYOT mode (ENABLE/DISABLE)
    Upsert:          "<UPSERT_COLUMN>", // Column name for upsert
    Tokens:          tokens,           // Required when TokenMode is ENABLE
}
```

### Options Comparison

| V1 Field | V2 Field | Description |
|----------|----------|-------------|
| `Tokens` | `ReturnTokens` | Return tokens for inserted data |
| `Upsert` (array) | `Upsert` (string) | Column name for upsert logic |
| `ContinueOnError` | `ContinueOnError` | Continue on partial errors |
| - | `TokenMode` | BYOT mode (ENABLE/DISABLE) |
| - | `Tokens` | Token values when BYOT enabled |

## Error Handling Migration

### V1 Error Handling

```go
res, err := skyflowClient.Insert(records, options)
if err != nil {
    // V1 error structure
    // {
    //     "code": "<http_code>",
    //     "description": "<description>"
    // }
    fmt.Println("Error code:", err.Code)
    fmt.Println("Description:", err.Description)
}
```

### V2 Error Handling

```go
insert, err := service.Insert(ctx, insertRequest, insertOptions)
if err != nil {
    // V2 enhanced error structure
    // {
    //     "httpStatus": "<http_status>",
    //     "grpcCode": "<grpc_code>",
    //     "httpCode": "<http_code>",
    //     "message": "<message>",
    //     "requestId": "<request_id>",
    //     "details": ["<details>"]
    // }
    fmt.Println("HTTP Status:", err.HttpStatus)
    fmt.Println("HTTP Code:", err.HttpCode)
    fmt.Println("gRPC Code:", err.GrpcCode)
    fmt.Println("Message:", err.Message)
    fmt.Println("Request ID:", err.RequestId)  // Useful for Skyflow support

    // Detailed error breakdown
    for _, detail := range err.Details {
        fmt.Println("Detail:", detail)
    }
}
```

### Error Structure Comparison

| V1 Property | V2 Property | Description |
|-------------|-------------|-------------|
| `Code` | `HttpCode` | HTTP status code |
| `Description` | `Message` | Error message |
| - | `HttpStatus` | HTTP status string |
| - | `GrpcCode` | gRPC error code |
| - | `RequestId` | Unique request identifier |
| - | `Details` | Slice of detailed error messages |

## Migration Checklist for Go

### Package & Imports

- [ ] Update `go.mod` to use `github.com/skyflowapi/skyflow-go/v2`
- [ ] Run `go get github.com/skyflowapi/skyflow-go/v2`
- [ ] Update import paths to V2 structure
- [ ] Import `client`, `common`, and `logger` from V2 packages
- [ ] Remove `serviceaccount/util` imports

### Authentication

- [ ] Choose appropriate credential method for your use case
- [ ] Replace `TokenProvider` function with `common.Credentials` struct
- [ ] Remove `saUtil.GenerateBearerToken` and `saUtil.IsExpired` calls
- [ ] Test authentication works

### Client Initialization

- [ ] Extract `ClusterId` from V1 `VaultURL`
- [ ] Update to functional options pattern: `client.NewSkyflow(options...)`
- [ ] Use `client.WithVaults()` for vault configuration
- [ ] Set `Env` field (common.PROD, common.DEV, common.STAGE)
- [ ] Configure `client.WithLogLevel()` if needed
- [ ] Add multiple vaults if needed

### Insert Operations

- [ ] Replace map-based records with `common.InsertRequest` struct
- [ ] Move table name to `InsertRequest.Table` field
- [ ] Update `Tokens` to `ReturnTokens` in options
- [ ] Update `Upsert` from array to string
- [ ] Add `context.Context` parameter to all operations
- [ ] Update to `service.Insert(ctx, request, options)` pattern
- [ ] Update response access (`InsertedFields` instead of `Records[].fields`)

### Get Operations

- [ ] Update to `service.Get(ctx, request, options)` pattern
- [ ] Add `context.Context` parameter
- [ ] Update response field access

### Detokenize Operations

- [ ] Update to `service.Detokenize(ctx, request)` pattern
- [ ] Add `context.Context` parameter
- [ ] Update response value access

### Error Handling

- [ ] Update error checks for new error structure
- [ ] Access `HttpCode` instead of `Code`
- [ ] Access `Message` instead of `Description`
- [ ] Log `RequestId` for debugging support
- [ ] Handle `Details` slice for granular errors

### Testing

- [ ] Update unit test mocks for V2 patterns
- [ ] Update integration tests
- [ ] Verify all operations work in test environment
- [ ] Test error handling paths

## Quick Reference: V1 to V2 Mapping

| V1 Pattern | V2 Pattern |
|------------|------------|
| `Skyflow.Init(configuration)` | `client.NewSkyflow(options...)` |
| `common.Configuration{VaultURL: "..."}` | `common.VaultConfig{ClusterId: "..."}` |
| `TokenProvider: GetToken` | `Credentials: common.Credentials{...}` |
| `skyflowClient.Insert(records, options)` | `service.Insert(ctx, request, options)` |
| `common.InsertOptions{Tokens: true}` | `common.InsertOptions{ReturnTokens: true}` |
| `Upsert: []common.UpsertOptions{...}` | `Upsert: "<column_name>"` |
| `res.Records[0].Fields["email"]` | `res.InsertedFields[0]["email"]` |
| `err.Code` | `err.HttpCode` |
| `err.Description` | `err.Message` |
| Global log level | `client.WithLogLevel(logger.DEBUG)` |

## Go-Specific Considerations

### Context Usage

V2 requires `context.Context` for all vault operations:

```go
// Create context
ctx := context.TODO()
// or with timeout
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

// Use in operations
insert, err := service.Insert(ctx, request, options)
```

### Functional Options Pattern

V2 uses Go's functional options pattern for flexible client configuration:

```go
skyflowClient, err := client.NewSkyflow(
    client.WithVaults(vaultConfigs...),
    client.WithCredentials(creds),
    client.WithLogLevel(logger.DEBUG),
)
```

### Native Data Structures

V2 uses native Go types instead of third-party JSON libraries:

```go
// V2: Native Go maps and slices
values := []map[string]interface{}{
    {"card_number": "4111111111111111", "cvv": "123"},
}

request := common.InsertRequest{
    Table:  "cards",
    Values: values,
}
```

## Additional Resources

- [Skyflow Go SDK Documentation](https://docs.skyflow.com/sdks/skyflow-go/)
- [Go SDK GitHub Repository](https://github.com/skyflowapi/skyflow-go)
- [Go SDK pkg.go.dev](https://pkg.go.dev/github.com/skyflowapi/skyflow-go/v2)
- See [SKILL.md](SKILL.md) for complete migration workflow and concepts
