# Phase 1: Define - Detailed Guide

The Define phase establishes the foundation for your Skyflow implementation. During this phase, you'll assess your data requirements, design your vault schema, and set up your development environment.

## Data Requirements Assessment

### Data Discovery Process

Before designing your vault, thoroughly understand your data landscape:

#### Step 1: Inventory Sensitive Data

Use the [data inventory worksheet](templates/data-inventory.md) to document:

| Field Name | Data Type | Example | Source | Destination | Compliance |
|------------|-----------|---------|--------|-------------|------------|
| | | | | | |

**Common sensitive data types:**

| Category | Fields to Look For |
|----------|-------------------|
| **Identity** | Full name, SSN, date of birth, government IDs |
| **Contact** | Email, phone, physical address |
| **Financial** | Card numbers, bank accounts, routing numbers |
| **Health** | Medical records, diagnoses, prescriptions |
| **Authentication** | Passwords, security questions, biometrics |

#### Step 2: Map Data Flows

For each sensitive data field, document:

1. **Entry points**: Where does this data enter your system?
   - User forms
   - API integrations
   - File uploads
   - Third-party imports

2. **Storage locations**: Where is this data currently stored?
   - Databases
   - File systems
   - Caches
   - Logs

3. **Processing points**: What systems touch this data?
   - Backend services
   - Analytics pipelines
   - Third-party APIs
   - Reporting systems

4. **Exit points**: Where does this data leave your system?
   - User displays
   - API responses
   - Third-party integrations
   - Exports/reports

#### Step 3: Identify Compliance Requirements

| Regulation | Applies If | Key Requirements |
|------------|-----------|------------------|
| **GDPR** | EU residents' data | Right to erasure, consent, data minimization |
| **HIPAA** | US health information | Audit trails, access controls, encryption |
| **PCI-DSS** | Payment card data | Tokenization, restricted access, no CVV storage |
| **CCPA** | California residents' data | Right to know, right to delete, opt-out |
| **SOC 2** | Service organizations | Security, availability, confidentiality |

### Data Classification Framework

Classify each data field by sensitivity:

| Level | Definition | Examples | Skyflow Handling |
|-------|------------|----------|------------------|
| **Critical** | Breach causes severe harm | SSN, card numbers | Tokenize, full redaction, limited access |
| **High** | Breach causes significant harm | DOB, medical data | Tokenize, masked redaction |
| **Medium** | Breach causes moderate harm | Email, phone | Tokenize, partial redaction |
| **Low** | Minimal breach impact | Preferences | May not need tokenization |

## Vault Schema Design

### Schema Design Principles

1. **Start with your data model**: Mirror your application's data structure
2. **Plan for queries**: Consider how data will be accessed and searched
3. **Design for compliance**: Include necessary compliance tags
4. **Think about relationships**: Use relational tables for connected data
5. **Consider tokenization needs**: Match token types to use cases

### Schema Structure Overview

```json
{
  "name": "vault_name",
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
        "childrenSchemas": [],
        "schemaTags": []
      }
    ],
    "tags": []
  },
  "workspaceID": "<workspace-id>"
}
```

### Data Type Selection

| Your Data | Skyflow Type | Notes |
|-----------|--------------|-------|
| Text | `DT_STRING` | Most common, use for names, addresses, etc. |
| Numbers | `DT_INT32` | For counts, IDs (non-sensitive) |
| Decimals | `DT_FLOAT32` | For amounts, measurements |
| Yes/No | `DT_BOOL` | For flags, preferences |
| Dates | `DT_DATE` | For birthdates, expiration dates |
| Timestamps | `DT_DATETIME` | For event times, created/updated |
| Files | `DT_FILE` | For documents, images |

### Tokenization Strategy

Choose tokenization based on how tokens will be used:

#### Deterministic Tokens

**Use when:** You need the same token for the same value across records

- **DETERMINISTIC_UUID**: Random-looking UUID, same input = same output
- **DETERMINISTIC_FPT**: Format-preserving, same input = same output

**Examples:**
- Matching records across tables
- Deduplication
- Analytics on tokenized values

#### Non-Deterministic Tokens

**Use when:** Each tokenization should produce a unique token

- **NON_DETERMINISTIC_UUID**: Different token each time
- **FORMAT_PRESERVING_TOKEN**: Format-preserving, different each time
- **NON_DETERMINISTIC_TRANSIENT_UUID**: Temporary, auto-expires

**Examples:**
- Maximum security (can't correlate tokens)
- Temporary data (CVV, one-time codes)

### Redaction Strategy

Configure redaction based on who needs to see what:

| Redaction Type | Output Example | Use Case |
|----------------|----------------|----------|
| **PLAIN_TEXT** | `John Smith` | Authorized users only |
| **REDACT** | `REDACTED` | Default for most users |
| **MASK** | `J*** S****` | Support agents, partial visibility |

**Masking configuration:**

```json
{
  "name": "skyflow.options.default_dlp_policy",
  "values": ["MASK"]
},
{
  "name": "skyflow.options.find_pattern",
  "values": ["^(.{1})(.*)$"]
},
{
  "name": "skyflow.options.replace_pattern",
  "values": ["${1}****"]
}
```

### Field Configuration Checklist

For each sensitive field, decide:

- [ ] **Data type**: What type of data is this?
- [ ] **Tokenization**: Deterministic vs non-deterministic? Format-preserving?
- [ ] **Redaction**: How should unauthorized users see this?
- [ ] **Validation**: What regex validates input?
- [ ] **Uniqueness**: Should values be unique?
- [ ] **Nullable**: Is this field required?
- [ ] **Queryable**: Need to search/filter on this field?
- [ ] **Compliance tags**: GDPR, HIPAA, PCI applicability?

### Schema Examples by Use Case

#### Customer Profile Table

```json
{
  "name": "customers",
  "fields": [
    {
      "name": "first_name",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
        {"name": "skyflow.options.personal_information_type", "values": ["PII"]}
      ]
    },
    {
      "name": "email",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
        {"name": "skyflow.options.find_pattern", "values": ["^(.{2})(.*)(@.*)$"]},
        {"name": "skyflow.options.replace_pattern", "values": ["${1}***${3}"]},
        {"name": "skyflow.options.operation", "values": ["EXACT_MATCH"]},
        {"name": "skyflow.options.configuration_tags", "values": ["UNIQUE"]}
      ]
    },
    {
      "name": "ssn",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.data_type", "values": ["skyflow.SSN"]},
        {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_FPT"]},
        {"name": "skyflow.options.format_preserving_regex", "values": ["^[0-9]{3}-[0-9]{2}-([0-9]{4})$"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
        {"name": "skyflow.options.find_pattern", "values": ["^([0-9]{3})-([0-9]{2})-([0-9]{4})$"]},
        {"name": "skyflow.options.replace_pattern", "values": ["XXX-XX-${3}"]},
        {"name": "skyflow.options.sensitivity", "values": ["HIGH"]},
        {"name": "skyflow.options.privacy_law", "values": ["CCPA"]}
      ]
    }
  ]
}
```

#### Payment Card Table

```json
{
  "name": "cards",
  "fields": [
    {
      "name": "card_number",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.data_type", "values": ["skyflow.CardNumber"]},
        {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_FPT"]},
        {"name": "skyflow.options.format_preserving_regex", "values": ["^[0-9]{12}([0-9]{4})$"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
        {"name": "skyflow.options.find_pattern", "values": ["^([0-9]{4})[0-9]{8}([0-9]{4})$"]},
        {"name": "skyflow.options.replace_pattern", "values": ["${1} **** **** ${2}"]},
        {"name": "skyflow.options.personal_information_type", "values": ["PCI"]}
      ]
    },
    {
      "name": "cvv",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.data_type", "values": ["skyflow.CVV"]},
        {"name": "skyflow.options.default_token_policy", "values": ["NON_DETERMINISTIC_TRANSIENT_UUID"]},
        {"name": "skyflow.options.ttl", "values": ["15"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
        {"name": "skyflow.options.personal_information_type", "values": ["PCI"]}
      ]
    },
    {
      "name": "expiry_date",
      "datatype": "DT_STRING",
      "tags": [
        {"name": "skyflow.options.data_type", "values": ["skyflow.ExpirationDate"]},
        {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
        {"name": "skyflow.options.default_dlp_policy", "values": ["PLAIN_TEXT"]}
      ]
    }
  ]
}
```

## Environment Setup

### Account Setup Checklist

- [ ] Sign up for Skyflow account (sandbox for development)
- [ ] Verify email and complete account setup
- [ ] Note your Account ID (visible in Studio URL)
- [ ] Note your Workspace ID (visible in vault details)

### Credential Setup

#### Option A: Bearer Token (Quick Start)

1. In Studio, click your account icon
2. Select "Generate API Bearer Token"
3. Copy the token (valid for 60 minutes)

#### Option B: Service Account (Recommended for Development)

1. In Studio, navigate to Settings > Service Accounts
2. Click "Create Service Account"
3. Name it (e.g., "dev-service-account")
4. Download the credentials JSON
5. Store securely (never commit to version control)

### Environment Variables

Set these environment variables for API access:

```bash
# Skyflow API endpoints
export MANAGEMENT_URL=https://manage.skyflowapis.com
export VAULT_URL=https://ebfc9bee4242.vault.skyflowapis.com  # Your vault URL

# Account identifiers
export ACCOUNT_ID=<your-account-id>
export WORKSPACE_ID=<your-workspace-id>
export VAULT_ID=<your-vault-id>  # After vault creation

# Authentication
export TOKEN=<your-bearer-token>
# OR for service accounts:
export SKYFLOW_CREDENTIALS=/path/to/credentials.json
```

### Development Tools

Install these tools for API development:

```bash
# Required
brew install curl jq  # macOS
# apt-get install curl jq  # Linux

# Optional: Skyflow CLI (if available)
npm install -g @skyflow/cli
```

### Create Development Vault

Once environment is set up, create your development vault:

```bash
# Using template
curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "dev_vault",
    "description": "Development vault",
    "templateID": "<template-id>",
    "workspaceID": "'"$WORKSPACE_ID"'"
  }'

# Or with custom schema
curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
  -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @schema.json
```

## Define Phase Completion Checklist

Before moving to the Build phase, ensure:

- [ ] Data inventory complete (all sensitive fields documented)
- [ ] Data flows mapped (sources, storage, processing, destinations)
- [ ] Compliance requirements identified
- [ ] Vault schema designed
- [ ] Tokenization strategy defined for each field
- [ ] Redaction rules configured
- [ ] Skyflow account created and configured
- [ ] Development vault created
- [ ] API credentials obtained and stored securely
- [ ] Environment variables set

## Next Steps

Once the Define phase is complete, proceed to [build-phase.md](build-phase.md) to integrate Skyflow into your application.

## Related Documentation

- [templates/data-inventory.md](templates/data-inventory.md) - Data inventory worksheet
- [use-case-patterns.md](use-case-patterns.md) - Pre-built patterns for common use cases
- **create-vault** skill - Detailed vault creation guidance
