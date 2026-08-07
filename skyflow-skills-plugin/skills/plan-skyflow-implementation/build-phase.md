# Phase 2: Build - Detailed Guide

The Build phase implements your Skyflow integration. During this phase, you'll set up authentication, configure access controls, integrate SDKs, and test your implementation.

## Authentication Setup

### Authentication Methods

| Method | Use Case | Security Level | Token Lifetime |
|--------|----------|----------------|----------------|
| **Service Account** | Backend services | High | 60 minutes (auto-refresh) |
| **Bearer Token** | Development/testing | Medium | 60 minutes |
| **API Key** | Legacy integrations | Lower | Long-lived |

**Recommendation:** Use service accounts for all production workloads.

### Service Account Setup

#### Step 1: Create Service Account in Studio

1. Navigate to Settings > Service Accounts
2. Click "Create Service Account"
3. Provide a descriptive name (e.g., `backend-prod`, `data-pipeline`)
4. Assign appropriate roles
5. Download the credentials JSON file

#### Step 2: Secure Credentials Storage

**Never store credentials in:**
- Source code
- Environment variables in version control
- Client-side code
- Logs or error messages

**Recommended storage:**
- AWS Secrets Manager
- HashiCorp Vault
- Google Secret Manager
- Azure Key Vault
- Environment variables (set at deployment time)

#### Step 3: Implement Token Generation

**Node.js Example:**

```javascript
const { Skyflow, generateBearerToken } = require('skyflow-node');

// Load credentials from secure storage
const credentials = JSON.parse(process.env.SKYFLOW_CREDENTIALS);

async function getToken() {
  const token = await generateBearerToken(credentials);
  return token.accessToken;
}
```

**Python Example:**

```python
from skyflow import Skyflow, Env
from skyflow.service_account import generate_bearer_token
import json
import os

# Load credentials from secure storage
credentials = json.loads(os.environ['SKYFLOW_CREDENTIALS'])

def get_token():
    token, _ = generate_bearer_token(credentials)
    return token
```

### Bearer Token Endpoint (for Frontend)

If your frontend needs to call Skyflow directly, create a backend endpoint that provides scoped bearer tokens:

```javascript
// Express.js example
app.get('/api/skyflow-token', authenticate, async (req, res) => {
  try {
    const token = await generateBearerToken(credentials, {
      // Scope token to specific roles if needed
      roles: ['vault-viewer']
    });
    res.json({ accessToken: token.accessToken });
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate token' });
  }
});
```

## Roles and Policies

### Understanding Skyflow Access Control

Skyflow uses a combination of roles and policies:

- **Roles**: Define a set of permissions that can be assigned to users/service accounts
- **Policies**: Fine-grained rules that control access to specific data

### Default Roles

| Role | Capabilities |
|------|--------------|
| **Vault Owner** | Full access, manage users, see plain text |
| **Vault Editor** | Create, update, delete records with default redaction |
| **Vault Viewer** | Read-only access with default redaction |

### Creating Custom Roles

Custom roles allow precise control over permissions. Common patterns:

#### Pattern: Data Entry Role

```
Capabilities:
- CREATE records in specified tables
- TOKENIZATION of inserted values
- READ own records (optional)

No access to:
- DETOKENIZATION
- DELETE
- Other tables
```

#### Pattern: Support Agent Role

```
Capabilities:
- READ all records with MASKED redaction
- DETOKENIZATION for specific fields (e.g., last 4 of phone)

No access to:
- CREATE, UPDATE, DELETE
- Full detokenization
```

#### Pattern: Analytics Role

```
Capabilities:
- QUERY with aggregations
- READ with REDACTED values

No access to:
- DETOKENIZATION
- Individual record access
```

### Policy Expression Examples

Policies use Skyflow's policy language to define access rules:

#### Allow read with masked redaction:

```policy
ALLOW READ ON customers.* WITH REDACTION = MASKED
```

#### Allow detokenization for specific fields:

```policy
ALLOW DETOKENIZATION ON customers.email WITH REDACTION = PLAIN_TEXT
ALLOW DETOKENIZATION ON customers.phone WITH REDACTION = MASKED
```

#### Allow create and tokenization:

```policy
ALLOW CREATE ON customers.*
ALLOW TOKENIZATION ON customers.*
```

#### Deny access to specific columns:

```policy
DENY READ ON customers.ssn
DENY DETOKENIZATION ON customers.ssn
```

### Access Control Planning Checklist

- [ ] List all user/service types that need vault access
- [ ] For each type, define required operations (read, write, delete)
- [ ] Determine redaction level for each type
- [ ] Identify fields requiring detokenization access
- [ ] Create role for each user type
- [ ] Write policies for fine-grained control
- [ ] Test each role's access in development

## Server-Side Integration

### SDK Installation

#### Node.js

```bash
npm install skyflow-node
```

#### Python

```bash
pip install skyflow
```

#### Java (Maven)

```xml
<dependency>
  <groupId>com.skyflow</groupId>
  <artifactId>skyflow-java</artifactId>
  <version>1.x.x</version>
</dependency>
```

#### Go

```bash
go get github.com/skyflowapi/skyflow-go
```

### SDK Initialization

#### Node.js

```javascript
const { Skyflow } = require('skyflow-node');

const client = Skyflow.init({
  vaultID: process.env.VAULT_ID,
  vaultURL: process.env.VAULT_URL,
  getBearerToken: async () => {
    // Return your token
    return await getToken();
  }
});
```

#### Python

```python
from skyflow import Skyflow, Env, LogLevel

client = Skyflow.init({
    'vaultID': os.environ['VAULT_ID'],
    'vaultURL': os.environ['VAULT_URL'],
    'getBearerToken': get_token
})
```

### Common Operations

#### Insert Records (Tokenize)

```javascript
// Node.js
const response = await client.insert({
  records: [
    {
      table: 'customers',
      fields: {
        first_name: 'John',
        last_name: 'Doe',
        email: 'john@example.com',
        ssn: '123-45-6789'
      }
    }
  ]
});

// Response contains tokens
// {
//   records: [
//     {
//       skyflow_id: 'abc-123',
//       tokens: {
//         first_name: 'tok_xxx',
//         email: 'tok_yyy',
//         ssn: '123-45-tok_zzz'  // Format-preserving
//       }
//     }
//   ]
// }
```

#### Get Records (with Redaction)

```javascript
const response = await client.get({
  records: [
    {
      table: 'customers',
      ids: ['abc-123'],
      redaction: 'MASKED'  // or 'PLAIN_TEXT', 'REDACTED'
    }
  ]
});
```

#### Detokenize

```javascript
const response = await client.detokenize({
  records: [
    { token: 'tok_xxx' },
    { token: 'tok_yyy' }
  ]
});

// Returns plain text values
// {
//   records: [
//     { value: 'John' },
//     { value: 'john@example.com' }
//   ]
// }
```

#### Query Records

```javascript
const response = await client.query({
  query: 'SELECT * FROM customers WHERE email = ?',
  params: ['tok_email_token']  // Use tokenized value for queries
});
```

### Integration Patterns

#### Pattern 1: Tokenize on Write

Replace sensitive data with tokens at the point of collection:

```javascript
// Before: Storing PII directly
await db.insert({ name: userData.name, email: userData.email });

// After: Tokenize first, store tokens
const skyflowResponse = await skyflowClient.insert({
  records: [{ table: 'customers', fields: userData }]
});
const tokens = skyflowResponse.records[0].tokens;
await db.insert({ name: tokens.name, email: tokens.email });
```

#### Pattern 2: Detokenize on Read

Retrieve plain text only when authorized and needed:

```javascript
// Fetch tokenized data from your database
const user = await db.getUser(userId);

// Detokenize for authorized display
const plaintext = await skyflowClient.detokenize({
  records: [
    { token: user.name },
    { token: user.email }
  ]
});
```

#### Pattern 3: Proxy Through Connections

Use Skyflow Connections to keep PII out of your systems entirely:

```javascript
// Configure connection to third-party API
const connection = await skyflowClient.invokeConnection({
  connectionURL: 'https://api.thirdparty.com/endpoint',
  methodName: 'POST',
  requestBody: {
    // Skyflow automatically detokenizes before sending
    card_number: '{tok_card_token}'
  }
});
```

## Client-Side Integration

### Frontend SDK Selection

| Framework | Package | Installation |
|-----------|---------|--------------|
| React | `skyflow-react-js` | `npm install skyflow-react-js` |
| JavaScript | `skyflow-js` | `npm install skyflow-js` |
| React Native | `skyflow-react-native` | `npm install skyflow-react-native` |

### React Integration

#### Step 1: Create Token Provider

```javascript
// src/skyflow/tokenProvider.js
const tokenProvider = async () => {
  const response = await fetch('/api/skyflow-token', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${userToken}` }
  });
  const data = await response.json();
  return data.accessToken;
};

export default tokenProvider;
```

#### Step 2: Configure Skyflow Provider

```javascript
// src/App.js
import { SkyflowProvider } from 'skyflow-react-js';
import tokenProvider from './skyflow/tokenProvider';

const skyflowConfig = {
  vaultID: process.env.REACT_APP_VAULT_ID,
  vaultURL: process.env.REACT_APP_VAULT_URL,
  getBearerToken: tokenProvider
};

function App() {
  return (
    <SkyflowProvider config={skyflowConfig}>
      <YourApp />
    </SkyflowProvider>
  );
}
```

#### Step 3: Use Skyflow Elements for Collection

```javascript
import {
  CardNumberElement,
  ExpirationDateElement,
  CVVElement,
  useSkyflow
} from 'skyflow-react-js';

function PaymentForm() {
  const { container } = useSkyflow();

  const handleSubmit = async () => {
    try {
      const response = await container.collect();
      // response contains tokens, not plain text
      console.log('Tokens:', response);
      // Send tokens to your backend
      await savePaymentMethod(response.records[0].tokens);
    } catch (error) {
      console.error('Collection failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardNumberElement table="cards" column="card_number" />
      <ExpirationDateElement table="cards" column="expiry" />
      <CVVElement table="cards" column="cvv" />
      <button type="submit">Save Card</button>
    </form>
  );
}
```

### Skyflow Elements

Skyflow Elements are pre-built UI components that securely collect sensitive data:

| Element | Purpose | Returns |
|---------|---------|---------|
| `CardNumberElement` | Credit card number input | Format-preserving token |
| `ExpirationDateElement` | Card expiry date | Token |
| `CVVElement` | Card CVV input | Transient token |
| `InputElement` | Generic text input | Token |
| `PinElement` | PIN input | Token |

**Benefits of Elements:**
- Sensitive data never touches your frontend code
- PCI compliance simplified
- Built-in validation and formatting
- Accessible and customizable

### Revealing Data

To display tokenized data to users:

```javascript
import { RevealElement, useSkyflow } from 'skyflow-react-js';

function CardDisplay({ cardToken }) {
  return (
    <RevealElement
      token={cardToken}
      redaction="MASKED"  // Shows: **** **** **** 1234
    />
  );
}
```

## Testing and Validation

### Test Environment Setup

1. Use sandbox/development vault (never production data in tests)
2. Create test service account with appropriate permissions
3. Generate test data that mimics production patterns

### Test Categories

#### Unit Tests

Mock Skyflow SDK to test your application logic:

```javascript
// Jest example
jest.mock('skyflow-node', () => ({
  Skyflow: {
    init: () => ({
      insert: jest.fn().mockResolvedValue({
        records: [{ skyflow_id: 'test-id', tokens: { email: 'tok_test' } }]
      }),
      detokenize: jest.fn().mockResolvedValue({
        records: [{ value: 'test@example.com' }]
      })
    })
  }
}));
```

#### Integration Tests

Test against sandbox vault:

```javascript
describe('Skyflow Integration', () => {
  it('should insert and retrieve record', async () => {
    // Insert
    const insertResponse = await client.insert({
      records: [{ table: 'customers', fields: testData }]
    });
    expect(insertResponse.records[0].skyflow_id).toBeDefined();

    // Retrieve
    const getResponse = await client.get({
      records: [{
        table: 'customers',
        ids: [insertResponse.records[0].skyflow_id]
      }]
    });
    expect(getResponse.records[0]).toBeDefined();
  });
});
```

#### Access Control Tests

Verify permissions work correctly:

```javascript
describe('Access Control', () => {
  it('should deny detokenization for viewer role', async () => {
    const viewerClient = createClientWithRole('viewer');

    await expect(
      viewerClient.detokenize({ records: [{ token: 'tok_xxx' }] })
    ).rejects.toThrow(/unauthorized/i);
  });

  it('should allow detokenization for admin role', async () => {
    const adminClient = createClientWithRole('admin');

    const response = await adminClient.detokenize({
      records: [{ token: 'tok_xxx' }]
    });
    expect(response.records[0].value).toBeDefined();
  });
});
```

### Test Checklist

#### Functional Tests

- [ ] Insert records and receive tokens
- [ ] Retrieve records with correct redaction
- [ ] Detokenize with authorized account
- [ ] Query records using tokens
- [ ] Update existing records
- [ ] Delete records

#### Security Tests

- [ ] Unauthorized detokenization is blocked
- [ ] Incorrect role cannot access restricted data
- [ ] Rate limiting works correctly
- [ ] Token expiration handled gracefully

#### Error Handling Tests

- [ ] Invalid token format handled
- [ ] Network errors handled with retry
- [ ] Expired credentials trigger refresh
- [ ] Validation errors returned clearly

#### Performance Tests

- [ ] Bulk insert within acceptable time
- [ ] Query response time acceptable
- [ ] Concurrent requests handled

## Build Phase Completion Checklist

Before moving to Go Live phase, ensure:

- [ ] Service accounts created and credentials secured
- [ ] Token generation/refresh implemented
- [ ] Roles and policies configured
- [ ] Backend SDK integrated
- [ ] Frontend SDK integrated (if applicable)
- [ ] Skyflow Elements implemented for collection
- [ ] All CRUD operations tested
- [ ] Access control tests passing
- [ ] Error handling implemented
- [ ] Retry logic implemented for rate limits
- [ ] Logging configured (no PII in logs)

## Next Steps

Once the Build phase is complete, proceed to [go-live-phase.md](go-live-phase.md) to prepare for production.

## Related Documentation

- [security-checklist.md](security-checklist.md) - Security review preparation
- **rest-apis** skill - Detailed API reference
- [Skyflow SDK Documentation](https://docs.skyflow.com/sdks/)
