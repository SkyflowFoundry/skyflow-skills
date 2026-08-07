# Java SDK Migration: V1 to V2

Detailed guide for migrating the Skyflow Java SDK from V1 to V2.

## Package Update

Update your Maven or Gradle dependency to the latest version:

**Maven:**
```xml
<dependency>
    <groupId>com.skyflow</groupId>
    <artifactId>skyflow-java</artifactId>
    <version>2.x.x</version>  <!-- Use latest V2 version -->
</dependency>
```

**Gradle:**
```groovy
implementation 'com.skyflow:skyflow-java:2.x.x'  // Use latest V2 version
```

## Import Changes

### V1 Imports

```java
import com.skyflow.Skyflow;
import com.skyflow.config.SkyflowConfiguration;
import com.skyflow.vault.InsertOptions;
import com.skyflow.vault.TokenProvider;
import com.skyflow.serviceaccount.Token;
import com.skyflow.errors.SkyflowException;
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
```

### V2 Imports

```java
import com.skyflow.Skyflow;
import com.skyflow.config.Credentials;
import com.skyflow.config.VaultConfig;
import com.skyflow.enums.Env;
import com.skyflow.enums.LogLevel;
import com.skyflow.enums.TokenMode;
import com.skyflow.vault.data.InsertRequest;
import com.skyflow.vault.data.InsertResponse;
import java.util.ArrayList;
import java.util.HashMap;
```

## Authentication Migration

### V1: TokenProvider Implementation

```java
import com.skyflow.vault.TokenProvider;
import com.skyflow.serviceaccount.Token;
import com.skyflow.serviceaccount.ResponseToken;
import com.skyflow.errors.SkyflowException;

static class DemoTokenProvider implements TokenProvider {
    @Override
    public String getBearerToken() throws Exception {
        ResponseToken res = null;
        try {
            String filePath = "<YOUR_CREDENTIALS_FILE_HERE>";
            res = Token.generateBearerToken(filePath);
        } catch (SkyflowException e) {
            e.printStackTrace();
        }
        return res.getAccessToken();
    }
}
```

### V2: Multiple Authentication Options

#### Option 1: API Key

```java
Credentials credentials = new Credentials();
credentials.setApiKey("<YOUR_API_KEY>");
```

#### Option 2: Environment Variable (Recommended)

```java
// Set SKYFLOW_CREDENTIALS environment variable with your credentials JSON
// The SDK will automatically read from this env var
Credentials credentials = new Credentials();
// No explicit credential setting needed - SDK reads from env
```

#### Option 3: Credentials File Path

```java
Credentials credentials = new Credentials();
credentials.setPath("<YOUR_CREDENTIALS_FILE_PATH>");
```

#### Option 4: Stringified JSON

```java
Credentials credentials = new Credentials();
credentials.setCredentialsString("<YOUR_CREDENTIALS_STRING>");
```

#### Option 5: Bearer Token

```java
Credentials credentials = new Credentials();
credentials.setToken("<BEARER_TOKEN>");
```

**Notes:**
- Use only ONE authentication method
- API Key or Environment Variables are recommended for production
- Secure storage of credentials is essential

## Client Initialization Migration

### V1 Initialization

```java
import com.skyflow.Skyflow;
import com.skyflow.config.SkyflowConfiguration;

// DemoTokenProvider class is an implementation of the TokenProvider interface
DemoTokenProvider demoTokenProvider = new DemoTokenProvider();

SkyflowConfiguration skyflowConfig = new SkyflowConfiguration(
    "<VAULT_ID>",
    "<VAULT_URL>",
    demoTokenProvider
);

Skyflow skyflowClient = Skyflow.init(skyflowConfig);
```

### V2 Initialization (Builder Pattern)

```java
import com.skyflow.Skyflow;
import com.skyflow.config.Credentials;
import com.skyflow.config.VaultConfig;
import com.skyflow.enums.Env;
import com.skyflow.enums.LogLevel;

// Configure credentials
Credentials credentials = new Credentials();
credentials.setPath("<YOUR_CREDENTIALS_FILE_PATH>");

// Configure vault
VaultConfig vaultConfig = new VaultConfig();
vaultConfig.setVaultId("<YOUR_VAULT_ID>");      // Same as V1
vaultConfig.setClusterId("<YOUR_CLUSTER_ID>");  // Extract from V1 vaultUrl
vaultConfig.setEnv(Env.PROD);                   // or Env.DEV, Env.STAGE
vaultConfig.setCredentials(credentials);         // Associate credentials

// Set up Skyflow credentials (fallback when vault has no credentials)
Credentials skyflowCredentials = new Credentials();
skyflowCredentials.setPath("<YOUR_CREDENTIALS_FILE_PATH>");

// Create Skyflow client using builder pattern
Skyflow skyflowClient = Skyflow.builder()
    .setLogLevel(LogLevel.DEBUG)              // Instance-specific log level
    .addVaultConfig(vaultConfig)              // Add vault configuration
    .addSkyflowCredentials(skyflowCredentials) // Add general Skyflow credentials
    .build();
```

### Extracting clusterId from vaultUrl

| V1 vaultUrl | V2 clusterId |
|-------------|--------------|
| `https://abc123.vault.skyflowapis.com` | `abc123` |
| `https://my-cluster.vault.skyflowapis.com` | `my-cluster` |

### Multi-Vault Configuration (V2 New Feature)

```java
// First vault credentials
Credentials credentials1 = new Credentials();
credentials1.setPath("<CREDENTIALS_FILE_PATH_1>");

// Second vault credentials
Credentials credentials2 = new Credentials();
credentials2.setPath("<CREDENTIALS_FILE_PATH_2>");

// Configure first vault
VaultConfig vaultConfig1 = new VaultConfig();
vaultConfig1.setVaultId("<VAULT_ID_1>");
vaultConfig1.setClusterId("<CLUSTER_ID_1>");
vaultConfig1.setEnv(Env.PROD);
vaultConfig1.setCredentials(credentials1);

// Configure second vault
VaultConfig vaultConfig2 = new VaultConfig();
vaultConfig2.setVaultId("<VAULT_ID_2>");
vaultConfig2.setClusterId("<CLUSTER_ID_2>");
vaultConfig2.setEnv(Env.PROD);
vaultConfig2.setCredentials(credentials2);

// Create client with multiple vaults
Skyflow skyflowClient = Skyflow.builder()
    .setLogLevel(LogLevel.ERROR)
    .addVaultConfig(vaultConfig1)
    .addVaultConfig(vaultConfig2)
    .addSkyflowCredentials(skyflowCredentials)
    .build();

// Access specific vault
InsertResponse response = skyflowClient.vault("<VAULT_ID_1>").insert(insertRequest);
```

### Key Initialization Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Pattern | `Skyflow.init(config)` | `Skyflow.builder()...build()` |
| Vault Location | `vaultUrl` | `clusterId` |
| Multiple Vaults | Separate client per vault | Single client with multiple `addVaultConfig()` |
| Log Level | Global | `setLogLevel()` per instance |
| Credentials | `TokenProvider` interface | `Credentials` class with setters |

## Insert Operation Migration

### V1 Insert

```java
import org.json.simple.JSONObject;
import org.json.simple.JSONArray;

// Build records using JSON objects
JSONObject recordsJson = new JSONObject();
JSONArray recordsArrayJson = new JSONArray();

JSONObject recordJson = new JSONObject();
recordJson.put("table", "cards");

JSONObject fieldsJson = new JSONObject();
fieldsJson.put("cardNumber", "4111111111111111");
fieldsJson.put("cvv", "123");

recordJson.put("fields", fieldsJson);
recordsArrayJson.add(recordJson);
recordsJson.put("records", recordsArrayJson);

try {
    JSONObject insertResponse = skyflowClient.insert(recordsJson);
    System.out.println(insertResponse);
} catch (SkyflowException exception) {
    System.out.println(exception);
}

// V1 Response structure
// {
//     "records": [
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

```java
import com.skyflow.vault.data.InsertRequest;
import com.skyflow.vault.data.InsertResponse;
import com.skyflow.enums.TokenMode;
import java.util.ArrayList;
import java.util.HashMap;

// Build values using native Java data structures
ArrayList<HashMap<String, Object>> values = new ArrayList<>();
HashMap<String, Object> record = new HashMap<>();
record.put("card_number", "4111111111111111");
record.put("cvv", "123");
values.add(record);

// Optional: BYOT tokens
ArrayList<HashMap<String, Object>> tokens = new ArrayList<>();
HashMap<String, Object> token = new HashMap<>();
token.put("card_number", "<TOKEN_VALUE>");
tokens.add(token);

// Build insert request using builder pattern
InsertRequest insertRequest = InsertRequest.builder()
    .table("<TABLE_NAME>")
    .values(values)
    .continueOnError(true)      // Continue on partial errors
    .returnTokens(true)         // Return tokens in response
    .tokenMode(TokenMode.DISABLE) // or TokenMode.ENABLE for BYOT
    .tokens(tokens)             // Required when TokenMode is ENABLE
    .build();

// Execute insert
try {
    InsertResponse response = skyflowClient.vault("<VAULT_ID>").insert(insertRequest);
    System.out.println(response.getInsertedFields());
} catch (Exception e) {
    System.out.println(e.getMessage());
}

// V2 Response structure
// {
//     "insertedFields": [
//         {
//             "card_number": "5484-7829-1702-9110",
//             "request_index": "0",
//             "skyflow_id": "9fac9201-7b8a-4446-93f8-5244e1213bd1",
//             "cvv": "b2308e2a-c1f5-469b-97b7-1f193159399b"
//         }
//     ],
//     "errors": []
// }
```

### Key Insert Changes

| Aspect | V1 | V2 |
|--------|----|----|
| Data Structure | Third-party JSONObject | Native ArrayList/HashMap |
| Request Format | JSON with `records` array | `InsertRequest.builder()` |
| Table Location | Inside each JSON record | `.table()` builder method |
| Options | Separate `InsertOptions` class | Builder methods on request |
| Response | JSON with `records[].fields` | `InsertResponse` with `insertedFields` |

## Request Options Migration

### V1 Options (Separate Class)

```java
import com.skyflow.vault.InsertOptions;

InsertOptions insertOptions = new InsertOptions(true);  // tokens = true

JSONObject response = skyflowClient.insert(records, insertOptions);
```

### V2 Options (Builder Pattern)

```java
InsertRequest insertRequest = InsertRequest.builder()
    .table("<TABLE_NAME>")
    .values(values)
    .continueOnError(false)       // Stop on first error
    .returnTokens(false)          // Do not return tokens
    .tokenMode(TokenMode.DISABLE) // Disable BYOT
    .upsert("<UPSERT_COLUMN>")    // Column for upsert logic
    .build();
```

### Available Builder Methods

| Method | Type | Description |
|--------|------|-------------|
| `.table(String)` | Required | Table name |
| `.values(ArrayList)` | Required | Data to insert |
| `.returnTokens(boolean)` | Optional | Return tokens in response |
| `.continueOnError(boolean)` | Optional | Continue on partial errors |
| `.upsert(String)` | Optional | Column name for upsert logic |
| `.tokenMode(TokenMode)` | Optional | BYOT mode (ENABLE/DISABLE) |
| `.tokens(ArrayList)` | Optional | Token values when BYOT enabled |

## Error Handling Migration

### V1 Error Handling

```java
import com.skyflow.errors.SkyflowException;

try {
    JSONObject response = skyflowClient.insert(records);
} catch (SkyflowException e) {
    // V1 error structure
    // {
    //     "code": "<http_code>",
    //     "description": "<description>"
    // }
    System.out.println("Error code: " + e.getCode());
    System.out.println("Description: " + e.getDescription());
}
```

### V2 Error Handling

```java
try {
    InsertResponse response = skyflowClient.vault("<VAULT_ID>").insert(insertRequest);
} catch (Exception e) {
    // V2 enhanced error structure
    // {
    //     "httpStatus": "<http_status>",
    //     "grpcCode": <grpc_code>,
    //     "httpCode": <http_code>,
    //     "message": "<message>",
    //     "requestId": "<request_id>",
    //     "details": ["<details>"]
    // }
    System.out.println("HTTP Status: " + e.getHttpStatus());
    System.out.println("HTTP Code: " + e.getHttpCode());
    System.out.println("gRPC Code: " + e.getGrpcCode());
    System.out.println("Message: " + e.getMessage());
    System.out.println("Request ID: " + e.getRequestId());  // Useful for Skyflow support

    // Detailed error breakdown
    for (String detail : e.getDetails()) {
        System.out.println("Detail: " + detail);
    }
}
```

### Error Structure Comparison

| V1 Property | V2 Property | Description |
|-------------|-------------|-------------|
| `code` | `httpCode` | HTTP status code |
| `description` | `message` | Error message |
| - | `httpStatus` | HTTP status string |
| - | `grpcCode` | gRPC error code |
| - | `requestId` | Unique request identifier |
| - | `details` | List of detailed error messages |

## Migration Checklist for Java

### Package & Imports

- [ ] Update Maven/Gradle dependency to V2
- [ ] Remove `org.json.simple` imports (third-party JSON)
- [ ] Update import statements to V2 packages
- [ ] Import `Credentials`, `VaultConfig` from `com.skyflow.config`
- [ ] Import enums from `com.skyflow.enums`
- [ ] Import request classes from `com.skyflow.vault.data`

### Authentication

- [ ] Choose appropriate credential method for your use case
- [ ] Replace `TokenProvider` implementation with `Credentials` class
- [ ] Remove `Token.generateBearerToken()` calls
- [ ] Test authentication works

### Client Initialization

- [ ] Extract `clusterId` from V1 `vaultUrl`
- [ ] Update to builder pattern: `Skyflow.builder()...build()`
- [ ] Use `VaultConfig` class for vault configuration
- [ ] Set `Env` enum value (Env.PROD, Env.DEV, Env.STAGE)
- [ ] Configure `setLogLevel()` if needed
- [ ] Add multiple vaults with `addVaultConfig()` if needed

### Insert Operations

- [ ] Replace JSONObject/JSONArray with ArrayList/HashMap
- [ ] Use `InsertRequest.builder()` for request construction
- [ ] Move table name to `.table()` builder method
- [ ] Move options to builder methods (`.returnTokens()`, `.continueOnError()`)
- [ ] Update to `.vault("id").insert(request)` pattern
- [ ] Update response access (`getInsertedFields()` instead of JSON parsing)

### Get Operations

- [ ] Use appropriate request builder pattern
- [ ] Update to `.vault("id").get(request)` pattern
- [ ] Update response field access

### Detokenize Operations

- [ ] Use appropriate request builder pattern
- [ ] Update to `.vault("id").detokenize(request)` pattern
- [ ] Update response value access

### Error Handling

- [ ] Update catch blocks for new error structure
- [ ] Access `getHttpCode()` instead of `getCode()`
- [ ] Access `getMessage()` instead of `getDescription()`
- [ ] Log `getRequestId()` for debugging support
- [ ] Handle `getDetails()` list for granular errors

### Testing

- [ ] Update unit test mocks for V2 patterns
- [ ] Update integration tests
- [ ] Verify all operations work in test environment
- [ ] Test error handling paths

## Quick Reference: V1 to V2 Mapping

| V1 Pattern | V2 Pattern |
|------------|------------|
| `Skyflow.init(config)` | `Skyflow.builder()...build()` |
| `SkyflowConfiguration(vaultId, vaultUrl, tokenProvider)` | `VaultConfig` with setters + `Credentials` |
| `vaultUrl` | `clusterId` |
| `TokenProvider` interface | `Credentials` class |
| `JSONObject` / `JSONArray` | `ArrayList` / `HashMap` |
| `skyflowClient.insert(records, options)` | `skyflowClient.vault("id").insert(request)` |
| `InsertOptions(true)` | `InsertRequest.builder().returnTokens(true)` |
| `response.get("records")` | `response.getInsertedFields()` |
| `exception.getCode()` | `exception.getHttpCode()` |
| `exception.getDescription()` | `exception.getMessage()` |
| Global log level | `setLogLevel()` in builder |

## Java-Specific Considerations

### Builder Pattern

V2 extensively uses the builder pattern for cleaner, more readable code:

```java
// Request building with builder pattern
InsertRequest request = InsertRequest.builder()
    .table("cards")
    .values(values)
    .returnTokens(true)
    .continueOnError(false)
    .build();

// Client building with builder pattern
Skyflow client = Skyflow.builder()
    .setLogLevel(LogLevel.INFO)
    .addVaultConfig(vaultConfig)
    .addSkyflowCredentials(credentials)
    .build();
```

### Native Data Structures

V2 uses native Java collections instead of third-party JSON libraries:

```java
// V2: Native Java collections
ArrayList<HashMap<String, Object>> values = new ArrayList<>();
HashMap<String, Object> record = new HashMap<>();
record.put("card_number", "4111111111111111");
record.put("cvv", "123");
values.add(record);
```

### Fluent API

V2 supports method chaining for cleaner configuration:

```java
Skyflow client = Skyflow.builder()
    .setLogLevel(LogLevel.DEBUG)
    .addVaultConfig(config1)
    .addVaultConfig(config2)
    .addSkyflowCredentials(credentials)
    .build();
```

## Additional Resources

- [Skyflow Java SDK Documentation](https://docs.skyflow.com/sdks/skyflow-java/)
- [Java SDK GitHub Repository](https://github.com/skyflowapi/skyflow-java)
- [Java SDK Maven Central](https://search.maven.org/artifact/com.skyflow/skyflow-java)
- See [SKILL.md](SKILL.md) for complete migration workflow and concepts
