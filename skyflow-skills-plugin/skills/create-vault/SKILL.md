---
name: create-vault
description: Create Skyflow vaults programmatically using the Management API, including schema design, template selection, and configuration of tokenization, redaction, and compliance settings.
---

# Create a Skyflow Vault

This skill guides you through creating Skyflow vaults programmatically using an API-first approach. Skyflow vaults securely store and protect sensitive data with built-in tokenization, redaction, and compliance controls.

## Overview

There are three approaches to creating a vault:

| Approach | When to Use | Method |
|----------|-------------|--------|
| **Template-based** | Quick start with standard use cases | List templates via API, then create vault with `templateID` |
| **Custom Schema** | You have a prepared schema definition | Create vault with `vaultSchema` JSON |
| **From Scratch** | Build iteratively, start minimal | Use `scratch-template.json` as starting point |

## Prerequisites

1. **Skyflow account**: [Sign up for a free trial](https://www.skyflow.com/try-skyflow) if needed

2. **Bearer token**: Generate via Studio (Account icon > Generate API Bearer Token) or use service account authentication

3. **Required tools**: Terminal with `bash`, `curl`, and `jq`

4. **Environment variables**: Set these before running API commands:

```bash
export MANAGEMENT_URL=https://manage.skyflowapis.com  # or https://manage.skyflowapis-preview.com for staging
export ACCOUNT_ID=<your-account-id>
export WORKSPACE_ID=<your-workspace-id>
export TOKEN=<your-bearer-token>
```

To find your Account ID and Workspace ID: In Studio, click **vault menu icon > View vault details**.

## Workflow

```
1. Choose Approach ─> 2. Prepare Schema ─> 3. Create Vault ─> 4. Verify ─> 5. Access Controls
       │                    │                    │
       ├─ Template          ├─ Tables            Note: Access controls
       ├─ Custom JSON       ├─ Fields            require Studio UI
       └─ From Scratch      └─ Tags (tokenization, DLP, validation)
```

## Step 1: Choose a Creation Approach

### Option A: Use a Template

List available templates:

```bash
curl -s -X GET "$MANAGEMENT_URL/v1/vault-templates?accountID=$ACCOUNT_ID" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN"
```

Available templates:

| Template | Tables | Relational | Use Case |
|----------|--------|------------|----------|
| Quickstart | 2 | No | Demo/testing (credit_cards, persons) |
| Payment | 7 | Yes | Payment processing |
| PIIData | 1 | No | General PII fields |
| CustomerIdentity | 4 | Yes | Customer data management |
| Plaid | 14 | No | Banking/financial integration |

Create vault with template:

```bash
export TEMPLATE_ID=<template-id-from-list>
export VAULT_NAME=<your-vault-name>

curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "'"$VAULT_NAME"'",
    "description": "Vault description",
    "templateID": "'"$TEMPLATE_ID"'",
    "workspaceID": "'"$WORKSPACE_ID"'"
  }'
```

### Option B: Use a Custom Schema

Create vault with your own schema JSON:

```bash
curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @schema.json
```

Where `schema.json` contains your vault schema (see Step 2 for structure).

### Option C: Start from Scratch

Use `vault-samples/scratch-template.json` as a minimal starting point, then modify as needed.

## Step 2: Design Your Vault Schema

### Schema Structure

```json
{
  "name": "my_vault",
  "description": "Vault description",
  "vaultSchema": {
    "schemas": [
      {
        "name": "table_name",
        "fields": [
          {
            "name": "field_name",
            "datatype": "DT_STRING",
            "tags": [...]
          }
        ],
        "childrenSchemas": []
      }
    ],
    "tags": []
  },
  "workspaceID": "<workspace-id>"
}
```

### Data Types

| Type | Constant | Description |
|------|----------|-------------|
| String | `DT_STRING` | Text data |
| Integer | `DT_INT32` | 32-bit integer |
| Float | `DT_FLOAT32` | 32-bit floating point |
| Boolean | `DT_BOOL` | true/false |
| Date | `DT_DATE` | Date (YYYY-MM-DD) |
| DateTime | `DT_DATETIME` | Timestamp |
| Time | `DT_TIME` | Time value |
| File | `DT_FILE` | Binary file data |
| Enum | Use with `predefinedvalues` tag | Enumerated values |

### Naming Rules

- Use **lowercase** alphanumeric characters, underscores, and hyphens only
- No spaces in vault names
- Avoid SQL reserved keywords (SELECT, FROM, WHERE, etc.)
- Avoid policy reserved keywords

## Step 3: Configure Field Tags

Tags define field behaviors for tokenization, redaction, validation, and compliance.

### Tokenization Tags

**Tag:** `skyflow.options.default_token_policy`

| Value | Description |
|-------|-------------|
| `DETERMINISTIC_UUID` | Same value always generates same UUID token |
| `DETERMINISTIC_FPT` | Same value generates same format-preserving token |
| `FORMAT_PRESERVING_TOKEN` | Token matches regex format |
| `RANDOM_TOKEN` | Random token, not derived from data |
| `NON_DETERMINISTIC_UUID` | Different UUID each time |
| `NON_DETERMINISTIC_TRANSIENT_UUID` | Temporary token with TTL |

For format-preserving tokens, also set:
- `skyflow.options.format_preserving_regex` - Regex defining token format

For transient tokens, also set:
- `skyflow.options.ttl` - Time-to-live in minutes (1-20160, default 60)

### Redaction (DLP) Tags

**Tag:** `skyflow.options.default_dlp_policy`

| Value | Description |
|-------|-------------|
| `PLAIN_TEXT` | No redaction (use only for non-sensitive fields) |
| `REDACT` | Completely redacted (shows "REDACTED") |
| `MASK` | Partially masked based on find/replace patterns |

For masking, also set:
- `skyflow.options.find_pattern` - Regex to find values to mask
- `skyflow.options.replace_pattern` - Replacement pattern (e.g., `XXX${1}XX${2}`)

### Validation Tags

| Tag | Description |
|-----|-------------|
| `skyflow.validation.regular_exp` | Regex pattern for input validation |
| `skyflow.validation.predefinedvalues` | List of allowed enum values |

### Compliance Tags

| Tag | Values |
|-----|--------|
| `skyflow.options.sensitivity` | `HIGH`, `MEDIUM`, `LOW` |
| `skyflow.options.identifiability` | `HIGH_IDENTIFIABILITY`, `MODERATE_IDENTIFIABILITY`, `LOW_IDENTIFIABILITY` |
| `skyflow.options.privacy_law` | `GDPR`, `CCPA`, `HIPAA`, `COPPA`, `GLBA` |
| `skyflow.options.personal_information_type` | `PII`, `PHI`, `PCI`, `NPI` |

### Configuration Tags

**Tag:** `skyflow.options.configuration_tags`

| Value | Description |
|-------|-------------|
| `UNIQUE` | Values must be unique |
| `NOT_NULL` | Field cannot be null |
| `NULLABLE` | Field can be null |
| `INDEX` | Field is indexed |
| `PRIMARY_KEY` | Primary key field |
| `FOREIGN_KEY` | Foreign key reference |

### Encrypted Operations

**Tag:** `skyflow.options.operation`

| Value | Enables |
|-------|---------|
| `EXACT_MATCH` | Equality queries (`WHERE email = 'x'`) |
| `AGGREGATION` | AVG, COUNT, MAX, MIN, SUM |
| `ORDER` | Comparison operators, ORDER BY |
| `ALL_OP` | All operations (not encrypted - use only for non-sensitive data) |

### Example: SSN Field with Full Configuration

```json
{
  "name": "ssn",
  "datatype": "DT_STRING",
  "tags": [
    { "name": "skyflow.options.data_type", "values": ["skyflow.SSN"] },
    { "name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_FPT"] },
    { "name": "skyflow.options.format_preserving_regex", "values": ["^[0-9]{3}-[0-9]{2}-([0-9]{4})$"] },
    { "name": "skyflow.options.default_dlp_policy", "values": ["MASK"] },
    { "name": "skyflow.options.find_pattern", "values": ["^[0-9]{3}([- ])?[0-9]{2}([- ])?([0-9]{4})$"] },
    { "name": "skyflow.options.replace_pattern", "values": ["XXX${1}XX${2}${3}"] },
    { "name": "skyflow.validation.regular_exp", "values": ["^$|^([0-9]{3}-?[0-9]{2}-?[0-9]{4})$"] },
    { "name": "skyflow.options.sensitivity", "values": ["HIGH"] },
    { "name": "skyflow.options.privacy_law", "values": ["GDPR", "CCPA", "HIPAA"] },
    { "name": "skyflow.options.personal_information_type", "values": ["PII"] },
    { "name": "skyflow.options.operation", "values": ["EXACT_MATCH"] }
  ]
}
```

## Step 4: Create the Vault

Run the API call from Step 1 (template or custom schema approach). The response returns the `vaultID` on success.

## Step 5: Verify and Test

### Get Vault Details

```bash
export VAULT_ID=<vault-id-from-create-response>

curl -s -X GET "$MANAGEMENT_URL/v1/vaults/$VAULT_ID/" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

### Update Vault Schema

```bash
curl -s -X PATCH "$MANAGEMENT_URL/v1/vaults/$VAULT_ID" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "vaultSchema": {
      "schemas": [...],
      "tags": [...]
    }
  }'
```

**Note:** You cannot rename or change a column's data type if it contains data. You can always add new columns.

## Step 6: Configure Access Controls

Access control configuration **requires Studio UI**. Navigate to your vault and click **Access** in the side navigation.

### Default Roles

| Role | Permissions |
|------|-------------|
| **Vault Owner** | Full access including plain text reads, manage service accounts/roles/policies |
| **Vault Editor** | Create, update, delete records with default redaction |
| **Vault Viewer** | Read-only with default redaction |

For custom roles and policies, see Data Governance documentation.

## Sample Schemas

Reference these samples in `vault-samples/` for common patterns:

| Sample | Use Case | Description |
|--------|----------|-------------|
| `quickstart.json` | Demo/testing | 2 tables (credit_cards, persons) with comprehensive tag examples |
| `payment.json` | Payment processing | 7 relational tables for full payment flow |
| `customer_identity.json` | Customer data | 4 relational tables (persons, identifiers, contacts, organizations) |
| `pii_data.json` | General PII | Single table with common PII fields |
| `plaid.json` | Banking integration | 14 tables for Plaid API compatibility |
| `scratch-template.json` | Starting point | Minimal blank template |

## Schema Validation

- Maximum schema size: **15 MB**
- JSON format required
- Every table automatically includes a `skyflow_id` primary key field
- At least one table required

Use `vault-schema-schemas/catalogue-vault-schema.json` for JSONSchema validation.

## Studio-Only Operations

These operations currently require the Studio UI:

- Creating custom roles and policies
- Managing service accounts
- Viewing audit logs
- Initial bearer token generation (manual)
- Visual drag-and-drop schema editing

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired token | Regenerate bearer token |
| 400 Bad Request | Invalid schema JSON | Validate against JSONSchema |
| 409 Conflict | Vault name already exists | Use a unique vault name |
| Reserved keyword error | SQL/policy keyword in name | Rename table or column |
| Cannot modify column | Column contains data | Create a new column instead |

## Related Documentation

- [vault-settings.md](vault-settings.md) - Complete tag reference with all 28+ configuration options
- [unique-columns-upsert.md](unique-columns-upsert.md) - Unique column constraints and upsert operations
- [create-a-vault.md](create-a-vault.md) - Full Skyflow documentation on vault creation
