# Contributing to API Documentation

Step-by-step guide for adding new operations to the API guides.

## 1. Identify the Source

Locate the OpenAPI spec for the API you're documenting:

| API Guide           | OpenAPI Spec              |
| ------------------- | ------------------------- |
| `management-api.md` | `management.openapi.json` |
| `vault-api.md`      | `data.openapi.json`       |
| `detect-api.md`     | `detect.openapi.json`     |

## 2. Find the Operation

Search the OpenAPI spec for the endpoint:

```bash
# Find all available endpoints
grep -E '"\/v1\/[^"]+": \{' management.openapi.json

# Find a specific operation's details
grep -A 50 '"operationId": "create-vault"' management.openapi.json
```

Key fields to extract:

- **Path**: The endpoint URL (e.g., `/v1/vaults`)
- **Method**: GET, POST, PUT, DELETE
- **operationId**: The operation name for reference
- **parameters**: Query params, path params, headers
- **requestBody**: Schema reference for POST/PUT bodies
- **responses**: Expected response schemas

## 3. Validate Before Documenting

Before adding an operation, verify:

- [ ] Endpoint path exists in the OpenAPI spec
- [ ] HTTP method matches
- [ ] All documented parameters exist in spec
- [ ] Parameter names match exactly (e.g., `filterOps.accountID` not `account_id`)
- [ ] Required parameters are marked
- [ ] Request body schema matches spec

## 4. Document Structure

Follow this format for each operation:

````markdown
## OPERATION NAME - Brief Description

**Endpoint**: `METHOD /v1/path/{param}`
**Operation**: `operationId`

One-sentence description of what this operation does.

```bash
curl -X METHOD "https://base.url/v1/path" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "field": "value"
  }'
```
````

**Response**:

```json
{
  "field": "value"
}
```

**Parameters** (or **Query Parameters** / **Request Body**):

- `param1`_: Description (required marked with _)
- `param2`: Description

---

````

## 5. Information Checklist

Include for each operation:

| Element | Required | Notes |
|---------|----------|-------|
| Section header | Yes | `## VERB NAME - Description` |
| Endpoint | Yes | Full path with method |
| Operation | Yes | operationId from spec |
| Description | Yes | 1-2 sentences |
| curl example | Yes | Working example with variables |
| Response example | Yes | Representative JSON |
| Parameters | Yes | All params with types/descriptions |
| Enums/Options | If applicable | List valid values |

## 6. Style Guidelines

- Use `$VARIABLE` for user-specific values in curl examples
- Mark required parameters with `*`
- List enum values inline: `` `VALUE1`, `VALUE2`, `VALUE3` ``
- Keep descriptions concise
- Group related parameters logically
- Reference the OpenAPI spec for complete schemas

## 7. Verify Your Addition

After adding:

1. Cross-check endpoint path against OpenAPI spec
2. Verify all parameter names match exactly
3. Confirm operationId is correct
4. Test curl example structure (syntax check)
5. Ensure response matches schema structure

## Example: Adding a New Operation

1. Find in spec:
```json
"/v1/vaults/{ID}": {
  "get": {
    "operationId": "get-vault",
    "summary": "Get Vault",
    ...
  }
}
````

2. Document:

````markdown
## GET VAULT

**Endpoint**: `GET /v1/vaults/{ID}`
**Operation**: `get-vault`

Returns details for a specific vault.

```bash
curl -X GET "https://manage.skyflowapis.com/v1/vaults/$VAULT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID"
```
````

...

```

```
