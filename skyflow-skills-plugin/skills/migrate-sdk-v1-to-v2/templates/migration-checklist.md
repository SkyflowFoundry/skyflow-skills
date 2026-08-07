# SDK Migration Checklist

Use this template to track your V1 to V2 SDK migration progress.

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | [Your project] |
| **SDK** | [Node.js / Python / Java / Go] |
| **V1 Version** | [e.g., 1.x.x] |
| **V2 Target Version** | [e.g., 2.x.x] |
| **Migration Start Date** | [Date] |
| **Target Completion** | [Date] |
| **Owner** | [Name] |

---

## Phase 1: Discovery

- [ ] Searched codebase for V1 import statements
- [ ] Inventoried all files using Skyflow SDK
- [ ] Documented current authentication method
- [ ] Listed all operations used (insert, get, detokenize, etc.)
- [ ] Identified custom error handling patterns
- [ ] Found all test files requiring updates
- [ ] Completed code inventory template

### Files to Migrate

| File Path | Operations Used | Priority | Status |
|-----------|-----------------|----------|--------|
| | | High / Medium / Low | Pending / In Progress / Done |
| | | | |
| | | | |
| | | | |

---

## Phase 2: Preparation

- [ ] Read V2 migration guide for my SDK
- [ ] Understood all breaking changes
- [ ] Planned authentication approach for V2
- [ ] Determined if multi-vault support needed
- [ ] Created feature branch for migration
- [ ] Set up test environment

### Authentication Decision

| Current V1 Method | Chosen V2 Method | Reason |
|-------------------|------------------|--------|
| [e.g., Bearer token function] | [e.g., API Key] | [Simplicity, security, etc.] |

---

## Phase 3: Migration

### Package Updates

- [ ] Updated package.json / requirements.txt / pom.xml / go.mod
- [ ] Installed V2 package
- [ ] Removed obsolete type packages (if applicable)
- [ ] Verified no version conflicts

### Authentication

- [ ] Selected credential type
- [ ] Updated credential initialization
- [ ] Tested authentication works
- [ ] Updated any token refresh logic (if applicable)

### Client Initialization

- [ ] Extracted `clusterId` from V1 `vaultURL`: ____________________
- [ ] Updated initialization code pattern
- [ ] Configured `vaultConfigs` array
- [ ] Set appropriate `logLevel`
- [ ] Configured multiple vaults (if needed)

### Operations Migration

#### Insert Operations
- [ ] Updated to V2 request class pattern
- [ ] Updated options configuration
- [ ] Updated response handling
- [ ] Tested insert operations

#### Get Operations
- [ ] Updated to V2 request class pattern
- [ ] Updated options configuration
- [ ] Updated response handling
- [ ] Tested get operations

#### Detokenize Operations
- [ ] Updated to V2 request class pattern
- [ ] Updated response handling
- [ ] Tested detokenize operations

#### Other Operations (Update, Delete, etc.)
- [ ] Updated to V2 patterns
- [ ] Tested all operations

### Error Handling

- [ ] Updated catch blocks for new error structure
- [ ] Access `http_status` / `http_code` instead of `code`
- [ ] Access `message` instead of `description`
- [ ] Log `request_ID` for debugging support
- [ ] Handle `details` array for granular errors
- [ ] Updated error logging/reporting

---

## Phase 4: Testing

### Unit Tests

- [ ] Updated test mocks for V2 patterns
- [ ] All unit tests passing
- [ ] Added tests for new V2 features (if using)

### Integration Tests

- [ ] Updated integration tests
- [ ] All integration tests passing
- [ ] Tested against sandbox/dev vault

### Manual Testing

- [ ] Insert operations return expected tokens
- [ ] Get operations return correctly structured responses
- [ ] Detokenize operations work with new format
- [ ] Error handling captures enhanced error details
- [ ] Multi-vault operations work (if applicable)
- [ ] Log levels function as expected

---

## Phase 5: Deployment

### Pre-Production

- [ ] Code review completed
- [ ] All tests passing
- [ ] Merged to staging branch
- [ ] Tested in staging environment
- [ ] Performance validated
- [ ] Monitoring configured

### Production

- [ ] Deployed to production
- [ ] Verified all operations succeed
- [ ] Monitored error rates
- [ ] Checked logs for warnings
- [ ] Confirmed `request_ID` tracking works
- [ ] Migration complete

---

## Issues Encountered

| Issue | Resolution | Date |
|-------|------------|------|
| | | |
| | | |
| | | |

---

## Rollback Plan

In case of critical issues:

1. **Immediate rollback steps:**
   - [ ] Revert to previous deployment
   - [ ] Verify V1 code is operational
   - [ ] Monitor for stability

2. **Investigation:**
   - [ ] Capture error logs with `request_ID`
   - [ ] Document reproduction steps
   - [ ] Contact Skyflow support if needed

---

## Notes

[Additional notes, learnings, or recommendations for future migrations]
