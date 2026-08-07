# Management API (Vault Administration)

The Management API handles vault administration: creating vaults, managing schemas, configuring policies, and accessing audit logs.

**Base URL**: `https://manage.skyflowapis.com/v1`

**Authentication**: Bearer token with management permissions

**OpenAPI Spec**: See [management.openapi.json](management.openapi.json) for complete request/response schemas

---

## GET BEARER TOKEN

**Endpoint**: `POST /v1/auth/sa/oauth/token`
**Operation**: `AuthenticationService_GetAuthToken`

Generates a Bearer token for authenticating with Skyflow APIs. This endpoint does not require an existing Authorization header - it's the starting point for API authentication.

**How it works**: You create a signed JWT assertion using your service account credentials, then exchange it for a bearer token.

```bash
curl -X POST "https://manage.skyflowapis.com/v1/auth/sa/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": "<your-signed-jwt>"
  }'
```

**Response**:

```json
{
  "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer"
}
```

**Request Body**:

| Field | Required | Description |
| ----- | -------- | ----------- |
| `grant_type` | Yes | Must be `urn:ietf:params:oauth:grant-type:jwt-bearer` |
| `assertion` | Yes | Signed JWT containing: `iss` (client ID), `key` (key ID), `aud` (audience URL), `exp` (expiry), `sub` (client ID) |
| `scope` | No | Subset of roles: `"role:<roleID1> role:<roleID2>"` |

**Creating the JWT Assertion**:

The `assertion` JWT must include these claims:

- `iss`: Your service account's client ID
- `key`: Your key ID
- `aud`: `https://manage.skyflowapis.com`
- `exp`: Expiration timestamp (typically 1 hour from now)
- `sub`: Your service account's client ID

Sign the JWT with your service account's private key using RS256.

**Using the Token**:

Include in subsequent API requests:

```text
Authorization: Bearer {accessToken}
```

Tokens are typically valid for 60 minutes. Cache and reuse until near expiry.

---

## LIST VAULTS

**Endpoint**: `GET /v1/vaults`
**Operation**: `list-vaults`

Returns all vaults accessible to the authenticated user.

```bash
curl -X GET "https://manage.skyflowapis.com/v1/vaults?limit=25&offset=0" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID"
```

**Response**:

```json
{
  "vaults": [
    {
      "ID": "vault_id_123",
      "name": "Production Vault",
      "url": "https://example.vault.skyflowapis.com",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 10
}
```

**Query Parameters**:

- `filterOps.name`: Filter by vault name
- `filterOps.status`: Filter by status (`ACTIVE`, `PENDING`, `CREATED`, `DELETED`, etc.)
- `filterOps.type`: Filter by vault type (`PII_DATA`, `PAYMENT`, `CUSTOMER_IDENTITY`, etc.)
- `sortOps.orderBy`: Sort order (`ASCENDING` or `DESCENDING`)
- `limit`: Results per page (default: 25)
- `offset`: Pagination offset
- `fetchMetadataOnly`: If `true`, returns only vault ID, name, description, status, namespace

---

## CREATE VAULT

**Endpoint**: `POST /v1/vaults`
**Operation**: `create-vault`

Creates a new vault. You can create from a template or with a custom schema.

### Create from Template

```bash
curl -X POST "https://manage.skyflowapis.com/v1/vaults" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vault",
    "description": "Production PII vault",
    "templateID": "TEMPLATE_ID",
    "workspaceID": "WORKSPACE_ID"
  }'
```

### Create with Custom Schema

```bash
curl -X POST "https://manage.skyflowapis.com/v1/vaults" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vault",
    "description": "Custom vault with PII table",
    "workspaceID": "WORKSPACE_ID",
    "vaultSchema": {
      "schemas": [
        {
          "name": "users",
          "fields": [
            {"name": "skyflow_id", "datatype": "DT_STRING"},
            {"name": "email", "datatype": "DT_STRING"},
            {"name": "ssn", "datatype": "DT_STRING"}
          ]
        }
      ]
    }
  }'
```

**Response**:

```json
{
  "ID": "v123abc456"
}
```

**Request Body** (choose ONE of templateID or vaultSchema):

- `name`\* (string): Vault name (no spaces or underscores)
- `description` (string): Vault description
- `workspaceID`\* (string): Workspace to create the vault in
- `templateID` (string): Template ID to create from (use GET /v1/vault-templates to list)
- `vaultSchema` (object): Custom schema with tables and fields
- `owners` (array): Members to assign as vault owners

**Available Templates**: `QUICKSTART`, `PAYMENT`, `PII_DATA`, `CUSTOMER_IDENTITY`, `PLAID`

---

## CREATE POLICY

**Endpoint**: `POST /v1/policies`
**Operation**: `PolicyAuthoringService_CreatePolicy`

Creates access control policies for a specified resource (vault, workspace, etc.).

```bash
curl -X POST "https://manage.skyflowapis.com/v1/policies" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "read_pii_policy",
    "displayName": "Read PII Policy",
    "description": "Allow reading PII with redaction",
    "resource": {
      "ID": "VAULT_ID",
      "type": "VAULT"
    },
    "ruleParams": [
      {
        "name": "read_users_email",
        "columnRuleParams": {
          "vaultID": "VAULT_ID",
          "columns": ["users.email", "users.phone"],
          "action": "READ",
          "effect": "ALLOW",
          "redaction": "MASKED"
        }
      }
    ],
    "activated": true
  }'
```

**Resource Types**: `VAULT`, `WORKSPACE`, `ACCOUNT`, `SERVICE_ACCOUNT`, `RECORD`, `TOKEN`

**Actions**: `READ`, `WRITE`, `DELETE`, `TOKENIZE`, `DETOKENIZE`

**Effects**: `ALLOW`, `DENY`

---

## GET AUDIT EVENTS

**Endpoint**: `GET /v1/audit/events`
**Operation**: `AuditService_ListAuditEvents`

Retrieves audit trail of vault and account operations.

```bash
curl -X GET "https://manage.skyflowapis.com/v1/audit/events?filterOps.accountID=$ACCOUNT_ID&filterOps.startTime=2024-01-01T00:00:00Z&filterOps.endTime=2024-01-31T23:59:59Z&limit=100" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID"
```

**Response**:

```json
{
  "events": [
    {
      "context": {
        "changeID": "change_123",
        "requestID": "req_456",
        "actor": "user_id",
        "actorType": "USER",
        "ipAddress": "192.168.1.1"
      },
      "actionType": "CREATE",
      "resourceType": "RECORD",
      "responseCode": 200,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Query Parameters** (required marked with \*):

- `filterOps.accountID`\*: Account ID to filter events
- `filterOps.startTime`: Start timestamp (SQL format)
- `filterOps.endTime`: End timestamp (SQL format)
- `filterOps.vaultID`: Filter by vault ID
- `filterOps.actionType`: `CREATE`, `READ`, `UPDATE`, `DELETE`, `LIST`, `EXECUTE`
- `filterOps.resourceType`: `VAULT`, `RECORD`, `TOKEN`, `USER`, `SERVICE_ACCOUNT`, `POLICY`
- `filterOps.context.actor`: Filter by user or service account ID
- `limit`: Results per page (default: 25)
- `offset`: Pagination offset
