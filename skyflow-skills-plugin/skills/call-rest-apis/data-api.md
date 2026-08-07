# Data API

The Data API handles all data operations: inserting, retrieving, updating, and deleting sensitive data with automatic tokenization.

**Base URL**: `https://{vaultURL}/v1/vaults/{vaultID}`

**Authentication**: Bearer token required in all requests

**OpenAPI Spec**: See [data.openapi.json](data.openapi.json) for complete request/response schemas

## Common Headers

```
Authorization: Bearer {token}
Content-Type: application/json
X-Skyflow-Account-ID: {accountID}  # optional, for audit logs
```

---

## INSERT - Store and Tokenize Data

**Endpoint**: `POST /v1/vaults/{vaultID}/{tableName}`
**Operation**: `insert_records`

Inserts records and returns tokens for sensitive fields.

```bash
curl -X POST "https://$VAULT_URL/v1/vaults/$VAULT_ID/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [{
      "fields": {
        "email": "user@example.com",
        "ssn": "123-45-6789"
      }
    }],
    "tokenization": true
  }'
```

**Response**:
```json
{
  "records": [{
    "skyflow_id": "f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d",
    "tokens": {
      "email": "token_1234abcd",
      "ssn": "token_5678efgh"
    }
  }]
}
```

**Parameters**:
- `tokenization` (boolean): Return tokens for fields
- `continueOnError` (boolean): Continue processing on partial failures

---

## GET BY ID - Retrieve Data

**Endpoint**: `GET /v1/vaults/{vaultID}/{tableName}`
**Operation**: `get_records`

Retrieves records by Skyflow ID with configurable redaction.

```bash
curl -X GET "https://$VAULT_URL/v1/vaults/$VAULT_ID/users?skyflow_ids=id1,id2&redaction=MASKED" \
  -H "Authorization: Bearer $TOKEN"
```

**Response**:
```json
{
  "records": [{
    "fields": {
      "skyflow_id": "id1",
      "email": "user@example.com",
      "ssn": "XXX-XX-6789"
    }
  }]
}
```

**Query Parameters**:
- `skyflow_ids`: Comma-separated Skyflow IDs
- `redaction`: `PLAIN_TEXT`, `MASKED`, `REDACTED`, or `DEFAULT`
- `fields`: Comma-separated field names to retrieve

---

## DETOKENIZE - Retrieve Original Values

**Endpoint**: `POST /v1/vaults/{vaultID}/detokenize`
**Operation**: `detokenize`

Converts tokens back to original values (requires permissions).

```bash
curl -X POST "https://$VAULT_URL/v1/vaults/$VAULT_ID/detokenize" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "detokenizationParameters": [
      {"token": "token_1234abcd", "redaction": "PLAIN_TEXT"}
    ]
  }'
```

**Response**:
```json
{
  "records": [{
    "token": "token_1234abcd",
    "value": "user@example.com"
  }]
}
```

---

## UPDATE - Modify Existing Records

**Endpoint**: `PUT /v1/vaults/{vaultID}/{tableName}/{skyflow_id}`
**Operation**: `update_record`

Updates specific fields in an existing record. The record ID is specified in the URL path.

```bash
curl -X PUT "https://$VAULT_URL/v1/vaults/$VAULT_ID/users/f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "record": {
      "fields": {
        "email": "newemail@example.com"
      }
    },
    "tokenization": true
  }'
```

**Response**:

```json
{
  "skyflow_id": "f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d",
  "tokens": {
    "email": "token_newabcd1234"
  }
}
```

**Request Body**:

- `record.fields` (object): Field values to update
- `tokenization` (boolean): Return tokens for updated fields

---

## DELETE - Remove Records

**Endpoint**: `DELETE /v1/vaults/{vaultID}/{tableName}`
**Operation**: `delete_records`

Permanently removes records from the vault.

```bash
curl -X DELETE "https://$VAULT_URL/v1/vaults/$VAULT_ID/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skyflow_ids": [
      "f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d",
      "a1b2c3d4-5678-90ab-cdef-1234567890ab"
    ]
  }'
```

**Response**:

```json
{
  "RecordIDResponse": [
    "f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d",
    "a1b2c3d4-5678-90ab-cdef-1234567890ab"
  ]
}
```

**Request Body**:

- `skyflow_ids` (array): Skyflow IDs of records to delete. Use `["*"]` to delete all records in the table.

---

## QUERY - SQL Queries

**Endpoint**: `POST /v1/vaults/{vaultID}/query`
**Operation**: `execute_query`

Executes SQL SELECT queries against vault data. Returns up to 25 records per query.

```bash
curl -X POST "https://$VAULT_URL/v1/vaults/$VAULT_ID/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM users WHERE skyflow_id = \"f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d\""
  }'
```

**Response**:

```json
{
  "records": [
    {
      "fields": {
        "skyflow_id": "f8d8c7e4-63c7-4361-a89e-4e9a07e1ae9d",
        "email": "user@example.com",
        "ssn": "XXX-XX-6789"
      }
    }
  ]
}
```

**Request Body**:

- `query` (string): SQL SELECT query with inline values

**Supported SQL**:

- Commands: `SELECT`
- Operators: `>`, `<`, `=`, `AND`, `OR`, `NOT`, `LIKE`, `ILIKE`, `NULL`, `NOT NULL`
- Keywords: `FROM`, `JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN`, `WHERE`, `OFFSET`, `LIMIT`
- Functions: `AVG()`, `SUM()`, `COUNT()`, `MIN()`, `MAX()`, `REDACTION()`

---

## Redaction Levels

| Level | Description |
|-------|-------------|
| `PLAIN_TEXT` | Unmasked data (requires permissions) |
| `MASKED` | Partially masked (e.g., `XXX-XX-6789`) |
| `REDACTED` | Fully redacted (e.g., `*********`) |
| `DEFAULT` | Uses field's default redaction policy |
