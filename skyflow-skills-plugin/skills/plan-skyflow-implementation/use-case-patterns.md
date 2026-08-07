# Use Case Patterns

This guide provides pre-built implementation patterns for common Skyflow use cases. Use these patterns as starting points and customize based on your specific requirements.

## Payment Processing (PCI)

### Overview

| Aspect | Details |
|--------|---------|
| **Primary Compliance** | PCI-DSS |
| **Data Types** | Card numbers, CVV, expiration dates |
| **Typical Timeline** | 4-6 weeks |
| **Key Features** | Tokenization, transient CVV storage, format-preserving tokens |

### Recommended Schema

```json
{
  "name": "payments_vault",
  "vaultSchema": {
    "schemas": [
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
            "name": "expiry_month",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["PLAIN_TEXT"]}
            ]
          },
          {
            "name": "expiry_year",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["PLAIN_TEXT"]}
            ]
          },
          {
            "name": "cardholder_name",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PII"]}
            ]
          }
        ]
      },
      {
        "name": "transactions",
        "fields": [
          {
            "name": "card_skyflow_id",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]}
            ]
          },
          {
            "name": "amount",
            "datatype": "DT_FLOAT32",
            "tags": [
              {"name": "skyflow.options.operation", "values": ["AGGREGATION"]}
            ]
          },
          {
            "name": "status",
            "datatype": "DT_STRING"
          }
        ]
      }
    ]
  }
}
```

### Integration Pattern

```
User Browser                  Your Backend                    Skyflow                    Payment Processor
    │                              │                             │                              │
    │ 1. Enter card details        │                             │                              │
    │ (via Skyflow Elements)       │                             │                              │
    │─────────────────────────────>│                             │                              │
    │                              │                             │                              │
    │                              │ 2. Collect & tokenize       │                              │
    │                              │─────────────────────────────>│                              │
    │                              │                             │                              │
    │                              │ 3. Return tokens            │                              │
    │                              │<─────────────────────────────│                              │
    │                              │                             │                              │
    │ 4. Return tokens             │                             │                              │
    │<─────────────────────────────│                             │                              │
    │                              │                             │                              │
    │ 5. Submit payment            │                             │                              │
    │─────────────────────────────>│                             │                              │
    │                              │                             │                              │
    │                              │ 6. Process via Connection   │                              │
    │                              │─────────────────────────────>│                              │
    │                              │                             │ 7. Detokenize & forward      │
    │                              │                             │─────────────────────────────>│
    │                              │                             │                              │
```

### PCI Compliance Checklist

- [ ] Card data never touches your servers (use Skyflow Elements)
- [ ] CVV stored transiently (15-minute TTL max)
- [ ] Card numbers tokenized with format-preserving tokens
- [ ] Access to plain card numbers strictly limited
- [ ] Audit logging enabled for all card access
- [ ] Annual PCI assessment scheduled

### Access Control Matrix

| Role | Cards Table | Transactions Table | Detokenize |
|------|-------------|-------------------|------------|
| Frontend (collection) | Insert | - | No |
| Backend (processing) | Read (masked) | Insert, Read | Via Connection only |
| Support | Read (masked) | Read | Last 4 only |
| Admin | Full | Full | Yes (audited) |

---

## Healthcare (HIPAA/PHI)

### Overview

| Aspect | Details |
|--------|---------|
| **Primary Compliance** | HIPAA |
| **Data Types** | Medical records, SSN, insurance info |
| **Typical Timeline** | 6-8 weeks |
| **Key Features** | Audit logging, strict access controls, data retention |

### Recommended Schema

```json
{
  "name": "healthcare_vault",
  "vaultSchema": {
    "schemas": [
      {
        "name": "patients",
        "fields": [
          {
            "name": "first_name",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PHI"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
            ]
          },
          {
            "name": "last_name",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PHI"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
            ]
          },
          {
            "name": "date_of_birth",
            "datatype": "DT_DATE",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PHI"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
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
              {"name": "skyflow.options.personal_information_type", "values": ["PHI", "PII"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
            ]
          },
          {
            "name": "medical_record_number",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.configuration_tags", "values": ["UNIQUE"]},
              {"name": "skyflow.options.operation", "values": ["EXACT_MATCH"]}
            ]
          }
        ]
      },
      {
        "name": "medical_records",
        "fields": [
          {
            "name": "patient_skyflow_id",
            "datatype": "DT_STRING"
          },
          {
            "name": "diagnosis",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PHI"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
            ]
          },
          {
            "name": "treatment_notes",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PHI"]},
              {"name": "skyflow.options.privacy_law", "values": ["HIPAA"]}
            ]
          },
          {
            "name": "provider_id",
            "datatype": "DT_STRING"
          },
          {
            "name": "visit_date",
            "datatype": "DT_DATETIME"
          }
        ]
      }
    ]
  }
}
```

### HIPAA Compliance Checklist

- [ ] All PHI fields tagged with HIPAA compliance
- [ ] Audit logging enabled for all data access
- [ ] Role-based access control implemented
- [ ] Minimum necessary access principle applied
- [ ] Business Associate Agreement (BAA) with Skyflow
- [ ] Data retention policies configured
- [ ] Breach notification procedures documented

### Access Control Matrix

| Role | Patients | Medical Records | Detokenize |
|------|----------|-----------------|------------|
| Physician | Read (plain text) | Read, Insert (plain text) | Yes (own patients) |
| Nurse | Read (masked) | Read (masked) | Limited fields |
| Admin Staff | Read (masked) | - | No |
| Billing | Limited fields | Limited fields | Insurance only |
| Auditor | Metadata only | Metadata only | No |

---

## Identity & KYC

### Overview

| Aspect | Details |
|--------|---------|
| **Primary Compliance** | KYC/AML regulations |
| **Data Types** | Government IDs, addresses, documents |
| **Typical Timeline** | 4-6 weeks |
| **Key Features** | Document storage, verification workflows |

### Recommended Schema

```json
{
  "name": "identity_vault",
  "vaultSchema": {
    "schemas": [
      {
        "name": "persons",
        "fields": [
          {
            "name": "full_name",
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
              {"name": "skyflow.options.configuration_tags", "values": ["UNIQUE"]},
              {"name": "skyflow.options.operation", "values": ["EXACT_MATCH"]}
            ]
          },
          {
            "name": "phone",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
              {"name": "skyflow.options.find_pattern", "values": ["^(.*)([0-9]{4})$"]},
              {"name": "skyflow.options.replace_pattern", "values": ["***-***-${2}"]}
            ]
          },
          {
            "name": "date_of_birth",
            "datatype": "DT_DATE",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]}
            ]
          }
        ]
      },
      {
        "name": "identifiers",
        "fields": [
          {
            "name": "person_skyflow_id",
            "datatype": "DT_STRING"
          },
          {
            "name": "id_type",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.validation.predefinedvalues", "values": ["PASSPORT", "DRIVERS_LICENSE", "SSN", "NATIONAL_ID"]}
            ]
          },
          {
            "name": "id_number",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
              {"name": "skyflow.options.find_pattern", "values": ["^(.*)(.{4})$"]},
              {"name": "skyflow.options.replace_pattern", "values": ["****${2}"]},
              {"name": "skyflow.options.sensitivity", "values": ["HIGH"]}
            ]
          },
          {
            "name": "expiry_date",
            "datatype": "DT_DATE"
          },
          {
            "name": "verification_status",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.validation.predefinedvalues", "values": ["PENDING", "VERIFIED", "REJECTED", "EXPIRED"]}
            ]
          }
        ]
      },
      {
        "name": "documents",
        "fields": [
          {
            "name": "person_skyflow_id",
            "datatype": "DT_STRING"
          },
          {
            "name": "document_type",
            "datatype": "DT_STRING"
          },
          {
            "name": "document_file",
            "datatype": "DT_FILE",
            "tags": [
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]}
            ]
          },
          {
            "name": "uploaded_at",
            "datatype": "DT_DATETIME"
          }
        ]
      }
    ]
  }
}
```

### KYC Workflow

```
1. User Onboarding
   └─> Collect identity info via Skyflow Elements
       └─> Store tokenized, return tokens

2. Document Upload
   └─> Upload ID documents to Skyflow (DT_FILE)
       └─> Store securely, return document token

3. Verification
   └─> Send to verification service via Connection
       └─> Skyflow detokenizes and forwards
       └─> Receive verification result

4. Ongoing Access
   └─> Display masked data to support
   └─> Full access only for compliance team
```

---

## AI/LLM Data Protection

### Overview

| Aspect | Details |
|--------|---------|
| **Primary Use** | Protect PII in LLM workflows |
| **Data Types** | Any text containing PII |
| **Typical Timeline** | 3-4 weeks |
| **Key Features** | Detect API, de-identification, re-identification |

### Integration Pattern

```
User Input               Your Application             Skyflow Detect            LLM Provider
    │                           │                           │                        │
    │ "My SSN is 123-45-6789"   │                           │                        │
    │──────────────────────────>│                           │                        │
    │                           │                           │                        │
    │                           │ 1. Detect & de-identify   │                        │
    │                           │──────────────────────────>│                        │
    │                           │                           │                        │
    │                           │ 2. "My SSN is [SSN_1]"   │                        │
    │                           │<──────────────────────────│                        │
    │                           │                           │                        │
    │                           │ 3. Send de-identified     │                        │
    │                           │───────────────────────────────────────────────────>│
    │                           │                           │                        │
    │                           │ 4. LLM response with [SSN_1]                       │
    │                           │<───────────────────────────────────────────────────│
    │                           │                           │                        │
    │                           │ 5. Re-identify response   │                        │
    │                           │──────────────────────────>│                        │
    │                           │                           │                        │
    │                           │ 6. Original values restored                        │
    │                           │<──────────────────────────│                        │
    │                           │                           │                        │
    │ Response with real SSN    │                           │                        │
    │<──────────────────────────│                           │                        │
```

### Detect API Usage

**De-identify text before sending to LLM:**

```javascript
const response = await fetch('https://detect.skyflowapis.com/v1/detect/deidentify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: userInput,
    // Entities to detect and replace
    entities: ['PERSON_NAME', 'EMAIL', 'PHONE', 'SSN', 'CREDIT_CARD']
  })
});

const { deidentifiedText, entities } = await response.json();
// deidentifiedText: "Hello, my name is [PERSON_1] and my email is [EMAIL_1]"
// entities: mapping of placeholders to tokens
```

**Re-identify response from LLM:**

```javascript
const reidentifyResponse = await fetch('https://detect.skyflowapis.com/v1/detect/reidentify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: llmResponse,
    entities: entities  // From de-identify response
  })
});

const { reidentifiedText } = await reidentifyResponse.json();
// Original values restored in response
```

### Supported Entity Types

| Entity | Examples | Use Case |
|--------|----------|----------|
| `PERSON_NAME` | John Smith | Customer names in prompts |
| `EMAIL` | john@example.com | Contact information |
| `PHONE` | (555) 123-4567 | Phone numbers |
| `SSN` | 123-45-6789 | Social security numbers |
| `CREDIT_CARD` | 4111-1111-1111-1111 | Card numbers |
| `ADDRESS` | 123 Main St | Physical addresses |
| `DATE_OF_BIRTH` | 01/15/1990 | Birthdates |

### LLM Protection Checklist

- [ ] Detect API integrated before LLM calls
- [ ] Entity types configured for your data
- [ ] Re-identification implemented for responses
- [ ] Tokens stored for audit/compliance
- [ ] Fallback handling for detection failures
- [ ] Logging excludes PII

---

## General PII Protection

### Overview

| Aspect | Details |
|--------|---------|
| **Primary Compliance** | GDPR, CCPA |
| **Data Types** | Customer data, employee data |
| **Typical Timeline** | 3-5 weeks |
| **Key Features** | Tokenization, access control, data subject rights |

### Recommended Schema

```json
{
  "name": "pii_vault",
  "vaultSchema": {
    "schemas": [
      {
        "name": "customers",
        "fields": [
          {
            "name": "first_name",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PII"]},
              {"name": "skyflow.options.privacy_law", "values": ["GDPR", "CCPA"]}
            ]
          },
          {
            "name": "last_name",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]},
              {"name": "skyflow.options.personal_information_type", "values": ["PII"]},
              {"name": "skyflow.options.privacy_law", "values": ["GDPR", "CCPA"]}
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
              {"name": "skyflow.options.configuration_tags", "values": ["UNIQUE"]},
              {"name": "skyflow.options.operation", "values": ["EXACT_MATCH"]},
              {"name": "skyflow.options.privacy_law", "values": ["GDPR", "CCPA"]}
            ]
          },
          {
            "name": "phone",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["MASK"]},
              {"name": "skyflow.options.find_pattern", "values": ["^(.*)([0-9]{4})$"]},
              {"name": "skyflow.options.replace_pattern", "values": ["***-***-${2}"]}
            ]
          },
          {
            "name": "address",
            "datatype": "DT_STRING",
            "tags": [
              {"name": "skyflow.options.default_token_policy", "values": ["DETERMINISTIC_UUID"]},
              {"name": "skyflow.options.default_dlp_policy", "values": ["REDACT"]}
            ]
          }
        ]
      }
    ]
  }
}
```

### GDPR/CCPA Compliance Checklist

- [ ] All PII fields tagged with applicable privacy laws
- [ ] Data subject access request (DSAR) process implemented
- [ ] Right to deletion supported
- [ ] Data portability export available
- [ ] Consent management integrated
- [ ] Data retention policies configured
- [ ] Cross-border transfer controls in place

### Data Subject Rights Implementation

#### Right to Access (DSAR)

```javascript
// Export all data for a user
async function handleDSAR(userId) {
  const records = await skyflowClient.get({
    records: [{
      table: 'customers',
      ids: [userId],
      redaction: 'PLAIN_TEXT'  // Full access for data subject
    }]
  });

  return formatForExport(records);
}
```

#### Right to Deletion

```javascript
// Delete user data
async function handleDeletionRequest(userId) {
  await skyflowClient.delete({
    records: [{
      table: 'customers',
      ids: [userId]
    }]
  });

  // Log deletion for compliance
  await logDeletionEvent(userId);
}
```

---

## Choosing the Right Pattern

| If You Need | Use This Pattern |
|-------------|------------------|
| Credit card storage | Payment Processing (PCI) |
| Medical data | Healthcare (HIPAA/PHI) |
| User verification | Identity & KYC |
| LLM/AI protection | AI/LLM Data Protection |
| Customer data | General PII Protection |

### Combining Patterns

Many implementations combine multiple patterns. For example:

- **E-commerce**: Payment + General PII
- **Healthcare portal**: Healthcare + Payment
- **Fintech**: Payment + Identity + General PII
- **AI assistants**: AI/LLM + any other pattern

When combining patterns, create separate tables for each data type and apply the appropriate compliance tags and access controls to each.
