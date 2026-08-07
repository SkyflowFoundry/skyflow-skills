# Detect API (PII Detection & De-identification)

The Detect API automatically identifies and redacts PII in text and documents using ML-based entity detection.

**Base URL**: `https://{clusterID}.vault.skyflowapis.com`

**Authentication**: Bearer token required

**OpenAPI Spec**: See [detect.openapi.json](detect.openapi.json) for complete request/response schemas

## API Versions

The Detect API has two versions:

- **v1** (`/v1/detect/...`) — Generally available. Uses `snake_case` fields and a per-request `vault_id` plus inline options.
- **v2** (`/v2/detect/...`) — **In beta and feature-flagged.** Uses `camelCase` fields and a reusable Detect **configuration** (via `configurationId` or an inline `configuration` object). See [V2 Endpoints (beta)](#v2-endpoints-beta) below.

Both versions cover the same operations (de-identify/re-identify strings and files, guardrails, and run status). Use v1 unless you specifically need the v2 configuration-based workflow.

---

## DEIDENTIFY TEXT - Detect and Replace PII

**Endpoint**: `POST /v1/detect/deidentify/string`
**Operation**: `deidentify_string`

Scans text for PII and replaces with tokens or placeholders.

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v1/detect/deidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Contact John at john@example.com or 555-123-4567",
    "entity_types": ["EMAIL", "PHONE_NUMBER", "NAME"],
    "token_type": "ENTITY_UNIQUE_COUNTER"
  }'
```

**Response**:
```json
{
  "processed_text": "Contact <NAME_1> at <EMAIL_1> or <PHONE_NUMBER_1>",
  "entities": [
    {
      "type": "NAME",
      "value": "John",
      "location": {"start": 8, "end": 12},
      "confidence": 0.95,
      "token": "<NAME_1>"
    },
    {
      "type": "EMAIL",
      "value": "john@example.com",
      "location": {"start": 16, "end": 32},
      "confidence": 0.99,
      "token": "<EMAIL_1>"
    }
  ]
}
```

**Token Types**:

| Type | Description | Example |
|------|-------------|---------|
| `ENTITY_ONLY` | Simple replacement | `<EMAIL>` |
| `ENTITY_UNIQUE_COUNTER` | With counter | `<EMAIL_1>`, `<EMAIL_2>` |
| `VAULT_TOKEN` | Stores in vault, returns Skyflow tokens | `tok_abc123` |

---

## REIDENTIFY TEXT - Restore Original PII

**Endpoint**: `POST /v1/detect/reidentify/string`
**Operation**: `reidentify_string`

Restores original values from de-identified text using entity mappings.

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v1/detect/reidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "processed_text": "Contact <NAME_1> at <EMAIL_1>",
    "entities": [
      {"type": "NAME", "token": "<NAME_1>", "value": "John"},
      {"type": "EMAIL", "token": "<EMAIL_1>", "value": "john@example.com"}
    ]
  }'
```

**Response**:
```json
{
  "text": "Contact John at john@example.com"
}
```

---

## DEIDENTIFY FILE - Process Documents

**Endpoint**: `POST /v1/detect/deidentify/file`
**Operation**: `deidentify_file`

Processes documents (PDF, images) to detect and redact PII. Returns an async run ID; poll `GET /v1/detect/runs/{run_id}` for the result.

```bash
# Submit file for processing
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v1/detect/deidentify/file" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf" \
  -F 'entity_types=["NAME","SSN","EMAIL"]' \
  -F "masking_method=REDACT" \
  -F "output_processed_image=true"
```

**Response** (async):
```json
{
  "request_id": "abc-123-def-456",
  "status": "PROCESSING"
}
```

**Check Status**:
```bash
curl -X GET "https://$CLUSTER_ID.vault.skyflowapis.com/v1/detect/runs/abc-123-def-456" \
  -H "Authorization: Bearer $TOKEN"
```

**Completed Response**:
```json
{
  "request_id": "abc-123-def-456",
  "status": "COMPLETED",
  "processed_file_url": "https://...",
  "entities": [
    {
      "type": "NAME",
      "value": "John Doe",
      "confidence": 0.95,
      "page": 1,
      "bounding_box": {...}
    }
  ]
}
```

**Form Fields**:
- `file`: Binary file content
- `entity_types`: JSON array of types to detect (optional, detects all if omitted)
- `masking_method`: `REDACT`, `MASK`, or `REPLACE` (default: `REDACT`)
- `output_processed_image`: Return redacted file (default: `true`)
- `output_ocr_text`: Return extracted text (default: `false`)

---

# V2 Endpoints (beta)

> **Note**: The v2 API is **in beta and feature-flagged**. Endpoints, fields, and behavior are subject to change. Contact Skyflow to have v2 enabled for your account.

The v2 API keeps the same set of operations as v1 but changes the request/response shape:

- Fields use **`camelCase`** (`processedText`, `entityType`, `startIndex`, `runId`) instead of v1's `snake_case`.
- De-identify operations reference a reusable **Detect configuration** — pass either a `configurationId` (ID of a saved configuration) **or** an inline `configuration` object. Only one is required.
- File operations describe the input with `dataSource` + `value` + `dataFormat` instead of a nested `file` object.
- Enum values (status, output type) are **UPPERCASE** (`SUCCESS`, `IN_PROGRESS`, `FAILED`, `BASE64`, `SKYFLOW_ID`, `PRESIGNED_URL`).
- Responses include a `metrics` object (size, word/character count, pages, slides, duration).

| Operation | Method | Endpoint | Operation ID |
| --- | --- | --- | --- |
| De-identify String | POST | `/v2/detect/deidentify/string` | `deidentify_string_v2` |
| De-identify File | POST | `/v2/detect/deidentify/file` | `deidentify_file_v2` |
| Re-identify String | POST | `/v2/detect/reidentify/string` | `reidentify_string_v2` |
| Re-identify File | POST | `/v2/detect/reidentify/file` | `reidentify_file_v2` |
| Check Guardrails | POST | `/v2/detect/guardrails` | `check_guardrails_v2` |
| Get Detect Run | GET | `/v2/detect/runs/{runId}` | `get_run_v2` |

---

## DEIDENTIFY STRING (v2)

**Endpoint**: `POST /v2/detect/deidentify/string`
**Operation**: `deidentify_string_v2`

Provide either `configurationId` or an inline `configuration` — only one is required.

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/deidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My name is John Doe, and my email is johndoe@acme.com.",
    "configurationId": "'"$CONFIGURATION_ID"'"
  }'
```

**Request fields**:
- `text` (required): Text to de-identify.
- `configurationId` (required unless `configuration` is provided): ID of the Detect configuration to use.
- `configuration` (required unless `configurationId` is provided): Inline Detect configuration object (see [Configurations](#configurations-v2)).

**Response**:
```json
{
  "processedText": "My name is [NAME_1] and my email is [EMAIL_ADDRESS_1].",
  "entities": [
    {
      "token": "NAME_1",
      "value": "John Doe",
      "location": {
        "startIndex": 11,
        "endIndex": 19,
        "startIndexProcessed": 11,
        "endIndexProcessed": 19
      },
      "entityType": "NAME",
      "entityScores": { "NAME": 0.9152 }
    },
    {
      "token": "EMAIL_ADDRESS_1",
      "value": "johndoe@acme.com",
      "location": {
        "startIndex": 36,
        "endIndex": 52,
        "startIndexProcessed": 36,
        "endIndexProcessed": 53
      },
      "entityType": "EMAIL_ADDRESS",
      "entityScores": { "EMAIL_ADDRESS": 0.8955 }
    }
  ],
  "metrics": { "size": 0.05, "wordCount": 10, "characterCount": 53 }
}
```

---

## DEIDENTIFY FILE (v2)

**Endpoint**: `POST /v2/detect/deidentify/file`
**Operation**: `deidentify_file_v2`

Async operation — returns a `runId`. Poll `GET /v2/detect/runs/{runId}` for the result.

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/deidentify/file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "BASE64",
    "value": "'"$BASE64_DATA"'",
    "dataFormat": "pdf",
    "configurationId": "'"$CONFIGURATION_ID"'"
  }'
```

**Request fields**:
- `dataSource` (required): `BASE64` (base64-encoded file string), `SKYFLOW_ID` (reference a file by vault ID), or `PRESIGNED_URL` (S3 presigned URL of the input file).
- `value` (required): File data corresponding to the `dataSource` type.
- `dataFormat` (required): Input file format. One of `mp3`, `wav`, `pdf`, `txt`, `csv`, `json`, `jpg`, `jpeg`, `tif`, `tiff`, `png`, `bmp`, `xls`, `xlsx`, `doc`, `docx`, `ppt`, `pptx`, `xml`, `dcm`, `jsonl`, `zip`, `gif`.
- `configurationId` (required unless `configuration` is provided): ID of the Detect configuration to use.
- `configuration` (required unless `configurationId` is provided): Inline Detect configuration object.

**Response**:
```json
{ "runId": "$RUN_ID" }
```

---

## GET DETECT RUN (v2)

**Endpoint**: `GET /v2/detect/runs/{runId}`
**Operation**: `get_run_v2`

Poll for the status and output of an async file operation. Requires the `vaultId` query parameter.

```bash
curl -X GET "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/runs/$RUN_ID?vaultId=$VAULT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response**:
```json
{
  "status": "SUCCESS",
  "outputType": "PRESIGNED_URL",
  "output": [
    { "processedFile": "$REDACTED_TEXT_URL", "processedFileType": "REDACTED_TEXT" },
    { "processedFile": "$ENTITIES_URL", "processedFileType": "ENTITIES" }
  ],
  "message": "De-identification completed successfully."
}
```

- `status`: `UNKNOWN`, `FAILED`, `SUCCESS`, or `IN_PROGRESS`.
- `outputType`: `BASE64`, `SKYFLOW_ID`, or `PRESIGNED_URL`.
- `output[]`: Each entry has `processedFile`, `processedFileType`, and optional `processedFileExtension`.

---

## REIDENTIFY STRING (v2)

**Endpoint**: `POST /v2/detect/reidentify/string`
**Operation**: `reidentify_string_v2`

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/reidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vaultId": "'"$VAULT_ID"'",
    "text": "My name is [NAME_1], and my email is [EMAIL_ADDRESS_1]."
  }'
```

**Request fields**:
- `vaultId` (required): ID of the vault used for de-identification.
- `text` (required): Text to re-identify.
- `redactionLevel` (optional): Array of replacement patterns applied to entity types during re-identification.

**Response**:
```json
{ "processedText": "My name is John Doe, and my email is johndoe@acme.com." }
```

---

## REIDENTIFY FILE (v2)

**Endpoint**: `POST /v2/detect/reidentify/file`
**Operation**: `reidentify_file_v2`

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/reidentify/file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSource": "BASE64",
    "value": "'"$BASE64_DATA"'",
    "dataFormat": "txt",
    "vaultId": "'"$VAULT_ID"'"
  }'
```

**Request fields**:
- `dataSource` (required): `BASE64`, `SKYFLOW_ID`, or `PRESIGNED_URL`.
- `value` (required): File data corresponding to the `dataSource` type.
- `dataFormat` (required): Input file format (same set as De-identify File).
- `vaultId` (required): ID of the vault used for de-identification.
- `redactionLevel` (optional): Array of replacement patterns applied to entity types during re-identification.

**Response**:
```json
{
  "status": "SUCCESS",
  "outputType": "BASE64",
  "output": [
    {
      "processedFile": "$PROCESSED_FILE",
      "processedFileType": "REIDENTIFIED_FILE",
      "processedFileExtension": "txt"
    }
  ]
}
```

---

## CHECK GUARDRAILS (v2)

**Endpoint**: `POST /v2/detect/guardrails`
**Operation**: `check_guardrails_v2`

Checks text for toxicity and denied topics to preserve safety and compliance with usage policies.

```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/guardrails" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vaultId": "'"$VAULT_ID"'",
    "text": "I love to play cricket.",
    "checkToxicity": true,
    "denyTopics": ["sports"]
  }'
```

**Request fields**:
- `vaultId` (required): ID of the vault.
- `text` (required): Text to check against guardrails (max 500,000 characters).
- `checkToxicity` (optional, default `true`): If `true`, checks for toxicity.
- `denyTopics` (optional): List of topics to deny (max 100 items, each up to 60 characters).

**Response**:
```json
{
  "text": "I love to play cricket.",
  "toxic": false,
  "deniedTopic": true,
  "validation": "FAILED"
}
```

- `validation`: `PASSED` or `FAILED`.

> **Beta caveat**: The v2 guardrails **schema** uses `camelCase` (`checkToxicity`, `denyTopics`, `deniedTopic`) and uppercase `validation` values, as documented above. Some examples in the beta OpenAPI spec still show `snake_case` (`check_toxicity`, `deny_topics`, `denied_topic`) and lowercase `validation`. If a request fails, confirm the expected casing with your Skyflow contact until the beta spec is finalized.

---

## Configurations (v2)

De-identify operations in v2 use a reusable **Detect configuration** instead of passing options on every request. Reference a saved configuration by `configurationId`, or send an inline `configuration` object.

A configuration is bound to a vault and can describe detection settings and file/media handling. Minimal inline example:

```json
{
  "configuration": {
    "name": "my-detect-config",
    "vaultId": "$VAULT_ID",
    "detect": { }
  }
}
```

Key fields:
- `vaultId` (required): ID of the vault the configuration applies to.
- `name`, `description`: Human-readable identifiers.
- `detect`: Detection and de-identification settings.
- `fileMapping`: Mappings for source and de-identified file locations.
- `media`: Media (audio/document/image) handling options.

See `DetectConfigV2` in [detect.openapi.json](detect.openapi.json) for the complete configuration schema.

---

# Migrating from v1 to v2

> **Note**: v2 is **in beta and feature-flagged**. Keep v1 in place until v2 is enabled for your account and validated against your workloads. The two versions can run side by side — migrate one operation at a time.

## Endpoint mapping

| Operation | v1 | v2 |
| --- | --- | --- |
| De-identify string | `POST /v1/detect/deidentify/string` | `POST /v2/detect/deidentify/string` |
| De-identify file | `POST /v1/detect/deidentify/file` | `POST /v2/detect/deidentify/file` |
| Re-identify string | `POST /v1/detect/reidentify/string` | `POST /v2/detect/reidentify/string` |
| Re-identify file | `POST /v1/detect/reidentify/file` | `POST /v2/detect/reidentify/file` |
| Check guardrails | `POST /v1/detect/guardrails` | `POST /v2/detect/guardrails` |
| Get detect run | `GET /v1/detect/runs/{run_id}` | `GET /v2/detect/runs/{runId}` |

The v1 category- and type-specific de-identify file endpoints (`/v1/detect/deidentify/file/document`, `/file/image`, `/file/audio`, `/file/document/pdf`, etc.) are **consolidated** in v2: use the single `POST /v2/detect/deidentify/file` and drive file-type behavior through the Detect **configuration** (`media` / `fileMapping`) instead.

## What changes

1. **Options move into a configuration.** v1 passes `vault_id` plus inline options on every request. v2 replaces this with a reusable Detect configuration — send a `configurationId` **or** an inline `configuration` object. (Re-identify and guardrails still take `vaultId` directly.)
2. **Fields are `camelCase`.** All request/response fields switch from `snake_case` to `camelCase`.
3. **File inputs are flattened.** The nested `file: { base64, data_format }` object becomes three top-level fields: `dataSource` (`BASE64` \| `SKYFLOW_ID` \| `PRESIGNED_URL`), `value`, and `dataFormat`.
4. **Enum values are UPPERCASE.** `status` (`SUCCESS`, `IN_PROGRESS`, `FAILED`, `UNKNOWN`), `outputType`, and processed-file types are uppercase in v2. Note `outputType` **replaces** v1's `efs_path` with `PRESIGNED_URL`.
5. **New `metrics` object.** String responses now return `metrics` (`size`, `wordCount`, `characterCount`, and for files `pages`/`slides`/`duration`). In v1, `word_count`/`character_count` were top-level fields.
6. **A couple of response shapes changed** (see the field reference below) — notably re-identify string's output field and re-identify file's `output` container.

## Field name reference

Common renames (v1 → v2):

| v1 (`snake_case`) | v2 (`camelCase`) |
| --- | --- |
| `vault_id` | `vaultId` (or a `configurationId` for de-identify) |
| `processed_text` | `processedText` |
| `entity_type` | `entityType` |
| `entity_scores` | `entityScores` |
| `start_index` / `end_index` | `startIndex` / `endIndex` |
| `start_index_processed` / `end_index_processed` | `startIndexProcessed` / `endIndexProcessed` |
| `word_count` / `character_count` (top-level) | `metrics.wordCount` / `metrics.characterCount` |
| `run_id` | `runId` |
| `output_type` | `outputType` |
| `processed_file` / `processed_file_type` | `processedFile` / `processedFileType` |
| `processed_file_extension` | `processedFileExtension` |
| `check_toxicity` / `deny_topics` / `denied_topic` | `checkToxicity` / `denyTopics` / `deniedTopic` (see guardrails caveat) |

Shape changes to watch for:
- **Re-identify string** — the result field is renamed from `text` (v1) to `processedText` (v2).
- **Re-identify file** — `output` changes from a single object (v1) to an **array** of file outputs (v2).
- **Processed-file types** — lowercase in v1 (`redacted_text`, `entities`, `reidentified_file`) become uppercase in v2 (`REDACTED_TEXT`, `ENTITIES`, `REIDENTIFIED_FILE`).

## Before / after example

De-identify a string.

**v1**:
```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v1/detect/deidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vault_id": "'"$VAULT_ID"'",
    "text": "My name is John Doe, and my email is johndoe@acme.com."
  }'
# -> { "processed_text": "...", "word_count": 10, "character_count": 53, "entities": [...] }
```

**v2**:
```bash
curl -X POST "https://$CLUSTER_ID.vault.skyflowapis.com/v2/detect/deidentify/string" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "configurationId": "'"$CONFIGURATION_ID"'",
    "text": "My name is John Doe, and my email is johndoe@acme.com."
  }'
# -> { "processedText": "...", "entities": [...], "metrics": { "wordCount": 10, "characterCount": 53 } }
```

## Migration checklist

- [ ] Confirm v2 is enabled for your account (beta / feature-flagged).
- [ ] Create a Detect **configuration** (capturing your v1 inline options) and note its `configurationId`, or build an inline `configuration`.
- [ ] Point requests at `/v2/detect/...`.
- [ ] Rename request fields to `camelCase`; flatten file inputs to `dataSource`/`value`/`dataFormat`.
- [ ] Update response parsing: `camelCase` fields, `metrics` object, uppercase enums, re-identify field/shape changes.
- [ ] For guardrails, verify field casing against the live endpoint (see the [beta caveat](#check-guardrails-v2)).
- [ ] Run v1 and v2 in parallel and diff outputs before cutting over.

---

## Supported Entity Types

| Category | Entity Types |
|----------|--------------|
| **Personal** | `NAME`, `PERSON`, `DATE_OF_BIRTH`, `DOB`, `AGE`, `GENDER` |
| **Contact** | `EMAIL`, `EMAIL_ADDRESS`, `PHONE`, `PHONE_NUMBER`, `ADDRESS`, `STREET_ADDRESS` |
| **Government IDs** | `SSN`, `SOCIAL_SECURITY_NUMBER`, `DRIVER_LICENSE`, `DRIVERS_LICENSE_NUMBER`, `PASSPORT`, `PASSPORT_NUMBER` |
| **Financial** | `CREDIT_CARD`, `CREDIT_CARD_NUMBER`, `US_BANK_ACCOUNT_NUMBER`, `ROUTING_NUMBER` |
| **Network** | `IP_ADDRESS`, `IPV4`, `IPV6` |

See the OpenAPI spec for the complete list of 50+ supported entity types.
