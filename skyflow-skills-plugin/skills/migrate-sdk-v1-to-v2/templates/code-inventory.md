# V1 SDK Code Inventory

Use this template to inventory all Skyflow V1 SDK usage before starting migration.

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | [Your project] |
| **Date** | [Date] |
| **Completed By** | [Name] |

---

## SDK Information

| Field | Value |
|-------|-------|
| **SDK Language** | [Node.js / Python / Java / Go] |
| **V1 Package Name** | [e.g., skyflow-node] |
| **V1 Version Installed** | [e.g., 1.x.x] |
| **Target V2 Version** | [e.g., 2.x.x] |

---

## Authentication

### Current Method

- [ ] Service Account (credentials JSON file)
- [ ] Bearer Token (pre-generated)
- [ ] Custom token provider function
- [ ] Other: ____________________

### Credentials Location

| Storage Method | Path / Variable Name |
|----------------|----------------------|
| File path | |
| Environment variable | |
| Secrets manager | |
| Hardcoded (needs fixing!) | |

### Token Provider Code Location

| File | Line(s) | Function Name | Notes |
|------|---------|---------------|-------|
| | | | |

---

## Client Initialization

### Vault Configuration

| Setting | Current V1 Value | V2 Equivalent |
|---------|------------------|---------------|
| vaultID | | (same) |
| vaultURL | | clusterId: |
| getBearerToken / tokenProvider | | credentials: |

### Initialization Code Locations

| File | Line(s) | Notes |
|------|---------|-------|
| | | |
| | | |

---

## Operations Inventory

### Insert Operations

| File | Line(s) | Table(s) | Fields Inserted | Options Used |
|------|---------|----------|-----------------|--------------|
| | | | | tokens: true/false |
| | | | | |
| | | | | |

### Get Operations

| File | Line(s) | Table(s) | Redaction | Query by ID/Column |
|------|---------|----------|-----------|-------------------|
| | | | MASKED / PLAIN_TEXT / etc. | |
| | | | | |

### Detokenize Operations

| File | Line(s) | Token Source | Redaction | Notes |
|------|---------|--------------|-----------|-------|
| | | | | |
| | | | | |

### Update Operations

| File | Line(s) | Table(s) | Fields Updated | Notes |
|------|---------|----------|----------------|-------|
| | | | | |

### Delete Operations

| File | Line(s) | Table(s) | Notes |
|------|---------|----------|-------|
| | | | |

### Query Operations

| File | Line(s) | Query Type | Tables | Notes |
|------|---------|------------|--------|-------|
| | | | | |

---

## Response Handling Patterns

### Field Access Patterns

| File | Line(s) | Access Pattern | V2 Update Needed |
|------|---------|----------------|------------------|
| | | `response.records[0].fields.X` | Yes - update to V2 structure |
| | | `response.records[0].tokens.X` | Yes - tokens in main response |
| | | | |

### Token Extraction

| File | Line(s) | Current Pattern | Notes |
|------|---------|-----------------|-------|
| | | | |

---

## Error Handling Patterns

### Try/Catch Blocks

| File | Line(s) | Error Properties Used | Custom Logic |
|------|---------|----------------------|--------------|
| | | error.code, error.description | |
| | | | |

### Error Logging

| File | Line(s) | What's Logged | Update for request_ID? |
|------|---------|---------------|------------------------|
| | | | Yes / No |
| | | | |

### Custom Error Classes/Handlers

| File | Class/Function Name | Notes |
|------|---------------------|-------|
| | | |

---

## Test Files

### Unit Tests

| Test File | What It Tests | V1 Mocks/Stubs Used |
|-----------|---------------|---------------------|
| | | |
| | | |

### Integration Tests

| Test File | Operations Tested | Test Vault Used |
|-----------|-------------------|-----------------|
| | | |
| | | |

### Test Utilities

| File | Purpose | V1-specific Code |
|------|---------|------------------|
| | Mock client setup | |
| | Test data factories | |

---

## Configuration Files

| File | Skyflow-related Config | Notes |
|------|------------------------|-------|
| | vaultURL, vaultID | |
| | credentials path | |
| | | |

---

## Dependencies

### Direct SDK Dependencies

| Package | Current Version | V2 Version |
|---------|-----------------|------------|
| | | |

### Type Definition Packages (if applicable)

| Package | Version | Remove in V2? |
|---------|---------|---------------|
| @types/skyflow-node | | Yes - built into V2 |
| | | |

---

## Summary

| Category | Count | Notes |
|----------|-------|-------|
| Files with V1 SDK usage | | |
| Client initialization points | | |
| Insert operations | | |
| Get operations | | |
| Detokenize operations | | |
| Update operations | | |
| Delete operations | | |
| Error handling blocks | | |
| Test files | | |

---

## Migration Priority

Rank files by migration priority based on criticality and dependencies.

| Priority | File | Reason | Dependencies |
|----------|------|--------|--------------|
| 1 (High) | | Core functionality | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 (Low) | | | |

---

## Multi-Vault Assessment

Does your application need multi-vault support?

- [ ] **No** - Single vault is sufficient
- [ ] **Yes** - Need to access multiple vaults

If yes, list vaults:

| Vault ID | Current vaultURL | Purpose |
|----------|------------------|---------|
| | | |
| | | |

---

## Notes

[Additional observations, concerns, or questions discovered during inventory]
