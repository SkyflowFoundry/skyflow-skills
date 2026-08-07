# Phase 3: Go Live - Detailed Guide

The Go Live phase prepares your Skyflow implementation for production. During this phase, you'll complete a security review, migrate any existing data, and launch your integration.

## Production Readiness

### Production Environment Setup

#### Step 1: Create Production Vault

Your production vault should mirror your development schema:

```bash
# Download schema from development vault in Studio
# Upload to production environment

# Or use Management API
curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
  -H "X-SKYFLOW-ACCOUNT-ID: $PROD_ACCOUNT_ID" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @production-schema.json
```

#### Step 2: Create Production Service Accounts

Create separate service accounts for production:

| Account | Purpose | Permissions |
|---------|---------|-------------|
| `prod-backend` | Main application backend | Insert, read, tokenize |
| `prod-worker` | Background jobs | Insert, update, tokenize |
| `prod-analytics` | Reporting/analytics | Read with aggregations |
| `prod-admin` | Emergency access | Full access (use sparingly) |

**Security practices:**
- Never share credentials between environments
- Use separate accounts for different services
- Implement credential rotation policy

#### Step 3: Configure Production Access Controls

Replicate your tested roles and policies:

1. Export policies from development
2. Review and adjust for production requirements
3. Apply to production vault
4. Test with production credentials

### Production Configuration Checklist

- [ ] Production vault created with correct schema
- [ ] Production service accounts created
- [ ] Production credentials stored in secrets manager
- [ ] Roles and policies applied and tested
- [ ] Environment variables configured for production
- [ ] Production URLs updated in application config

### Infrastructure Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **Network** | HTTPS outbound to Skyflow APIs | Whitelist `*.skyflowapis.com` |
| **Secrets** | Secure credential storage | Secrets manager recommended |
| **Logging** | Centralized logging | Ensure no PII in logs |
| **Monitoring** | API call monitoring | Track latency, errors |
| **Alerting** | Error rate alerts | Alert on auth failures, rate limits |

## Security Review

Before going live, complete a thorough security review. See [security-checklist.md](security-checklist.md) for the complete checklist.

### Pre-Review Preparation

Prepare documentation for your security review:

1. **Architecture diagram** showing data flows
2. **Access control matrix** listing all roles and permissions
3. **Data inventory** showing all sensitive data fields
4. **Integration documentation** describing SDK usage
5. **Security controls** implemented in your application

### Security Review Areas

#### 1. Credential Management

| Check | Status | Notes |
|-------|--------|-------|
| No hardcoded credentials in source code | | |
| Credentials stored in secrets manager | | |
| Service account credentials rotated regularly | | |
| Bearer tokens short-lived (60 min) | | |
| Token refresh implemented correctly | | |

#### 2. Access Control

| Check | Status | Notes |
|-------|--------|-------|
| Principle of least privilege applied | | |
| Roles segregated by responsibility | | |
| Detokenization restricted appropriately | | |
| No overly permissive policies | | |
| Service accounts have minimal required permissions | | |

#### 3. Data Handling

| Check | Status | Notes |
|-------|--------|-------|
| No PII in application logs | | |
| No PII in error messages | | |
| No PII in URLs/query parameters | | |
| Proper redaction in all responses | | |
| Tokens stored instead of plain text | | |

#### 4. Transport Security

| Check | Status | Notes |
|-------|--------|-------|
| All API calls over HTTPS | | |
| Certificate validation enabled | | |
| No sensitive data in request URLs | | |
| TLS 1.2+ enforced | | |

#### 5. Application Security

| Check | Status | Notes |
|-------|--------|-------|
| Input validation on all user inputs | | |
| Output encoding for XSS prevention | | |
| Rate limiting handled with retry logic | | |
| Error handling doesn't leak info | | |

### Skyflow Security Review

Contact Skyflow for a security review before production launch:

1. Schedule review with your Skyflow contact
2. Share architecture documentation
3. Walk through integration implementation
4. Address any findings
5. Obtain approval for production

### Common Security Findings

| Finding | Risk | Remediation |
|---------|------|-------------|
| Credentials in environment files committed to git | High | Remove from repo, rotate credentials, use secrets manager |
| PII logged in application logs | High | Audit all log statements, filter sensitive fields |
| Overly permissive service account | Medium | Create role-specific accounts with minimal permissions |
| Missing rate limit handling | Medium | Implement exponential backoff retry |
| Bearer tokens cached too long | Medium | Implement proper token refresh logic |

## Data Migration

### Migration Strategy Selection

| Strategy | Use Case | Complexity | Risk |
|----------|----------|------------|------|
| **Big Bang** | Replace all data at once | Medium | Higher |
| **Incremental** | Migrate data in batches | Higher | Lower |
| **Dual Write** | Write to both systems during transition | Higher | Lower |
| **New Data Only** | Only new data goes to Skyflow | Low | Lowest |

### Migration Planning

#### Step 1: Inventory Existing Data

Document all sensitive data that needs migration:

| Data Source | Record Count | Fields | Priority |
|-------------|--------------|--------|----------|
| | | | |

#### Step 2: Define Token Mapping

For existing tokens or IDs, decide how to handle:

| Scenario | Approach |
|----------|----------|
| No existing tokens | Generate new Skyflow tokens |
| Existing tokens | Import with `tokenStrict` to preserve tokens |
| Need correlation | Use deterministic tokens for matching |

#### Step 3: Create Migration Scripts

**Batch Insert Example (Node.js):**

```javascript
const BATCH_SIZE = 25;  // Skyflow limit

async function migrateData(records) {
  const batches = chunkArray(records, BATCH_SIZE);

  for (const batch of batches) {
    try {
      const response = await skyflowClient.insert({
        records: batch.map(record => ({
          table: 'customers',
          fields: record
        }))
      });

      // Store token mapping
      for (let i = 0; i < response.records.length; i++) {
        await saveTokenMapping(
          batch[i].original_id,
          response.records[i].skyflow_id,
          response.records[i].tokens
        );
      }
    } catch (error) {
      // Log failed batch for retry
      await logFailedBatch(batch, error);
    }
  }
}
```

**Preserving Existing Tokens:**

```javascript
// If you have existing tokens to preserve
const response = await skyflowClient.insert({
  records: [{
    table: 'customers',
    fields: {
      email: 'john@example.com'
    }
  }],
  tokenStrict: true,  // Ensures consistent token generation
  tokens: [{
    email: 'your-existing-token'  // Preserve this token
  }]
});
```

### Migration Execution

#### Pre-Migration Checklist

- [ ] Migration scripts tested against sandbox
- [ ] Token mapping storage configured
- [ ] Rollback procedure documented
- [ ] Data validation queries prepared
- [ ] Monitoring in place for migration job

#### During Migration

1. **Start with small batch** - Validate before full migration
2. **Monitor progress** - Track records migrated, errors
3. **Validate continuously** - Spot check migrated data
4. **Keep logs** - Record all operations for audit

#### Post-Migration Validation

```javascript
// Validate migration completeness
async function validateMigration() {
  const sourceCount = await getSourceRecordCount();
  const skyflowCount = await getSkyflowRecordCount();

  if (sourceCount !== skyflowCount) {
    throw new Error(`Count mismatch: ${sourceCount} vs ${skyflowCount}`);
  }

  // Spot check random records
  const sampleIds = await getRandomSourceIds(100);
  for (const id of sampleIds) {
    const sourceRecord = await getSourceRecord(id);
    const skyflowRecord = await getSkyflowRecord(id);

    // Compare non-sensitive fields directly
    // Compare sensitive fields via detokenization
  }
}
```

### Migration Checklist

- [ ] Data inventory complete
- [ ] Token mapping strategy defined
- [ ] Migration scripts developed and tested
- [ ] Small batch migration successful
- [ ] Full migration executed
- [ ] Post-migration validation passed
- [ ] Application updated to use Skyflow tokens
- [ ] Old data securely archived or deleted

## Launch

### Pre-Launch Checklist

#### Technical Readiness

- [ ] All tests passing in production environment
- [ ] Production vault contains migrated data (if applicable)
- [ ] Application configured for production Skyflow
- [ ] Monitoring and alerting active
- [ ] Logs streaming correctly (no PII)

#### Operational Readiness

- [ ] Runbook documented for common issues
- [ ] On-call team briefed on Skyflow integration
- [ ] Escalation path to Skyflow support defined
- [ ] Rollback procedure documented and tested

#### Business Readiness

- [ ] Stakeholders notified of launch plan
- [ ] Success criteria defined
- [ ] Go/no-go decision made

### Launch Approaches

#### Approach 1: Big Bang

Switch all traffic to Skyflow at once.

**Pros:** Simple, clean cutover
**Cons:** Higher risk, all-or-nothing

**Steps:**
1. Deploy updated application
2. Switch configuration to production Skyflow
3. Monitor closely for 24-48 hours

#### Approach 2: Staged Rollout

Gradually increase traffic to Skyflow.

**Pros:** Lower risk, can catch issues early
**Cons:** More complex, requires traffic splitting

**Steps:**
1. Deploy with feature flag
2. Enable for 1% of traffic
3. Monitor and increase gradually (1% → 5% → 25% → 50% → 100%)

#### Approach 3: Canary Deployment

Test with specific user segments first.

**Pros:** Real user validation, controlled blast radius
**Cons:** Requires user segmentation capability

**Steps:**
1. Identify canary user group (internal users, beta testers)
2. Enable Skyflow for canary group
3. Gather feedback and metrics
4. Expand to all users

### Launch Day Checklist

#### Morning of Launch

- [ ] Verify production systems are healthy
- [ ] Confirm team availability for monitoring
- [ ] Review rollback procedure
- [ ] Final go/no-go call

#### During Launch

- [ ] Deploy changes per rollout plan
- [ ] Monitor error rates closely
- [ ] Watch API latency metrics
- [ ] Track key business metrics
- [ ] Be ready to rollback if issues arise

#### Post-Launch

- [ ] Confirm all systems stable
- [ ] Review any errors that occurred
- [ ] Document lessons learned
- [ ] Celebrate success!

### Rollback Procedure

If issues arise, be prepared to rollback:

1. **Identify the issue** - Is it Skyflow-related or application-related?
2. **Assess severity** - Can users work around it?
3. **Decision** - Rollback or hotfix?

**Rollback steps:**

```bash
# If using feature flags
disable_skyflow_feature_flag()

# If using deployment rollback
kubectl rollout undo deployment/app
# or
heroku rollback
# or
revert to previous deployment
```

**Post-rollback:**
1. Communicate to stakeholders
2. Investigate root cause
3. Fix issue in development
4. Plan re-launch

## Post-Launch

### Monitoring

Set up ongoing monitoring for:

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| API error rate | > 1% | Investigate errors |
| API latency (p99) | > 500ms | Check for issues |
| Authentication failures | Any | Check credentials |
| Rate limit hits | > 10/min | Review usage patterns |

### Ongoing Operations

#### Regular Tasks

| Task | Frequency | Owner |
|------|-----------|-------|
| Credential rotation | Monthly | DevOps |
| Access review | Quarterly | Security |
| Schema review | As needed | Engineering |
| Performance review | Monthly | Engineering |

#### Support Resources

- **Skyflow Support:** support@skyflow.com (for production issues)
- **Documentation:** docs.skyflow.com
- **Status Page:** skyflow.statuspage.io

### Success Metrics

Track these metrics to measure implementation success:

| Metric | Target | Current |
|--------|--------|---------|
| Data breach incidents | 0 | |
| Compliance audit findings | 0 | |
| API availability | 99.9% | |
| Mean time to resolution | < 1 hour | |

## Go Live Phase Completion Checklist

- [ ] Production vault created and configured
- [ ] Production service accounts created
- [ ] Security review completed and approved
- [ ] Data migration completed (if applicable)
- [ ] Application deployed to production
- [ ] Monitoring and alerting active
- [ ] Runbook documented
- [ ] Rollback procedure tested
- [ ] Launch executed successfully
- [ ] Post-launch validation complete

Congratulations on going live with Skyflow!

## Related Documentation

- [security-checklist.md](security-checklist.md) - Complete security review checklist
- [templates/implementation-plan.md](templates/implementation-plan.md) - Implementation plan template
- [Skyflow Status Page](https://skyflow.statuspage.io/) - Real-time status updates
