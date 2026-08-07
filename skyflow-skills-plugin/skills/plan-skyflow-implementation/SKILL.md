---
name: plan-skyflow-implementation
description: Guide users through planning a complete Skyflow implementation, from requirements assessment through production launch, using the Define-Build-Go Live framework.
---

# Plan Your Skyflow Implementation

This skill helps you create a comprehensive implementation plan for Skyflow. It guides users through a structured three-phase approach that covers requirements assessment, technical integration, and production readiness.

## Overview

Implementing Skyflow involves three main phases:

| Phase | Focus | Duration | Key Outputs |
|-------|-------|----------|-------------|
| **Define** | Requirements, schema design | 1-2 weeks | Data inventory, vault schema, environment setup |
| **Build** | Integration, testing | 2-4 weeks | SDK integration, access controls, test coverage |
| **Go Live** | Production readiness | 1-2 weeks | Security review, data migration, launch |

```
Phase 1: Define          Phase 2: Build              Phase 3: Go Live
─────────────────────────────────────────────────────────────────────────
  Data Assessment    -->   Authentication      -->   Security Review
  Schema Design      -->   SDK Integration     -->   Data Migration
  Environment Setup  -->   Access Controls     -->   Launch
                     -->   Testing             -->   Monitoring
```

## Quick Start

When helping users plan their Skyflow implementation, gather this information:

### Essential Questions

| Question | Why It Matters |
|----------|----------------|
| What sensitive data do you need to protect? | Determines schema design and compliance requirements |
| What's your tech stack (languages, frameworks)? | Guides SDK selection and integration patterns |
| When do you need to go live? | Establishes timeline and phase durations |
| What compliance requirements apply? | Identifies GDPR, HIPAA, PCI-DSS, CCPA needs |
| Do you have existing sensitive data to migrate? | Affects go-live planning |

### Use Case Classification

| Use Case | Primary Features | Typical Timeline |
|----------|-----------------|------------------|
| **Payment Processing** | Card tokenization, PCI compliance | 4-6 weeks |
| **Healthcare/PHI** | HIPAA compliance, audit logging | 6-8 weeks |
| **Identity/KYC** | Document storage, verification | 4-6 weeks |
| **AI/LLM Data** | De-identification, Detect API | 3-4 weeks |
| **General PII** | Customer data protection | 3-5 weeks |

See [use-case-patterns.md](use-case-patterns.md) for detailed patterns.

## Phase 1: Define

The Define phase establishes your foundation. See [define-phase.md](define-phase.md) for detailed guidance.

### 1.1 Assess Data Requirements

**Goal**: Identify all sensitive data that Skyflow will protect.

#### Data Inventory Checklist

- [ ] List all PII/PHI/PCI data fields you collect
- [ ] Map data sources (forms, APIs, imports, third parties)
- [ ] Map data destinations (storage, analytics, third parties)
- [ ] Identify who needs access to what data
- [ ] Document compliance requirements (GDPR, HIPAA, PCI-DSS, CCPA)

#### Data Classification

| Category | Examples | Typical Handling |
|----------|----------|------------------|
| **PII** | Names, emails, addresses, SSN | Tokenization + redaction |
| **PHI** | Medical records, diagnoses | Tokenization + HIPAA compliance tags |
| **PCI** | Card numbers, CVV | Tokenization + transient tokens for CVV |
| **NPI** | Bank accounts, financial data | Tokenization + audit logging |

### 1.2 Design Vault Schema

**Goal**: Create an optimized schema for your data.

#### Schema Design Checklist

- [ ] Identify tables and relationships
- [ ] Define fields with appropriate data types
- [ ] Configure tokenization policies per field
- [ ] Set redaction/masking rules
- [ ] Add compliance tags
- [ ] Configure validation rules
- [ ] Plan unique constraints for upsert operations

#### Tokenization Decision Tree

```
Is the data format important downstream?
├── Yes --> Format-preserving tokens
│   └── Need same token for same value?
│       ├── Yes --> DETERMINISTIC_FPT
│       └── No  --> FORMAT_PRESERVING_TOKEN
└── No --> UUID-based tokens
    └── Need same token for same value?
        ├── Yes --> DETERMINISTIC_UUID
        └── No  --> NON_DETERMINISTIC_UUID
            └── Temporary storage? --> NON_DETERMINISTIC_TRANSIENT_UUID
```

### 1.3 Set Up Environment

**Goal**: Prepare your Skyflow account and development environment.

#### Environment Setup Checklist

- [ ] Create Skyflow account (sandbox for development)
- [ ] Note Account ID and Workspace ID
- [ ] Generate API credentials (bearer token or service account)
- [ ] Set up environment variables
- [ ] Create development vault
- [ ] Install required tools (curl, jq, SDK packages)

## Phase 2: Build

The Build phase implements your integration. See [build-phase.md](build-phase.md) for detailed guidance.

### 2.1 Authentication Setup

**Goal**: Establish secure authentication for your application.

#### Authentication Decision Tree

```
Where will Skyflow operations run?
├── Backend only --> Service account authentication
│   └── Store credentials in: secrets manager, env vars
├── Frontend only --> Bearer tokens (generated by backend)
│   └── Implement: token endpoint, token refresh
└── Both --> Hybrid approach
    ├── Backend: service account
    └── Frontend: bearer tokens from backend
```

#### Authentication Checklist

- [ ] Create service account in Studio
- [ ] Download and securely store credentials JSON
- [ ] Implement token generation (never expose credentials to frontend)
- [ ] Configure token refresh logic

### 2.2 Roles and Policies

**Goal**: Define who can access what data and how.

#### Access Control Matrix Template

| Role | Read | Write | Delete | Detokenize | Redaction Level |
|------|------|-------|--------|------------|-----------------|
| Admin | All | All | All | Yes | PLAIN_TEXT |
| Editor | All | All | No | No | MASKED |
| Viewer | All | No | No | No | REDACTED |
| Service | Specific | Specific | No | Specific | MASKED |

#### Policy Planning Checklist

- [ ] Map user roles to vault access needs
- [ ] Identify redaction requirements per role
- [ ] Define detokenization permissions
- [ ] Create custom policies for fine-grained control
- [ ] Test policies in development environment

### 2.3 Server-Side Integration

**Goal**: Integrate Skyflow into your backend services.

#### SDK Selection

| Language | SDK Package | Install Command |
|----------|-------------|-----------------|
| Node.js | `skyflow-node` | `npm install skyflow-node` |
| Python | `skyflow` | `pip install skyflow` |
| Java | `skyflow-java` | Maven/Gradle dependency |
| Go | `skyflow-go` | `go get github.com/skyflowapi/skyflow-go` |

#### Integration Patterns

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **Tokenize on write** | Protect data at ingestion | Insert API, store tokens |
| **Proxy through Skyflow** | Keep PII out of your systems | Connections API |
| **Detokenize on read** | Authorized access to PII | Detokenize API |
| **De-identify text** | LLM/AI data protection | Detect API |

### 2.4 Client-Side Integration

**Goal**: Securely collect sensitive data from users.

#### Frontend SDK Selection

| Framework | SDK Package | Use Case |
|-----------|-------------|----------|
| React | `skyflow-react-js` | Web forms, SPAs |
| React Native | `skyflow-react-native` | Mobile apps |
| JavaScript | `skyflow-js` | Vanilla JS, other frameworks |
| iOS | `Skyflow-iOS` | Native iOS apps |
| Android | `skyflow-android` | Native Android apps |

#### Client Integration Checklist

- [ ] Implement bearer token endpoint on backend
- [ ] Install frontend SDK
- [ ] Configure Skyflow provider with token function
- [ ] Build secure collection forms using Skyflow Elements
- [ ] Handle collection responses (tokens)
- [ ] Implement error handling

### 2.5 Testing and Validation

**Goal**: Verify your integration works correctly.

#### Test Scenarios

| Test | What to Validate |
|------|------------------|
| Insert and tokenize | Records created, tokens returned |
| Retrieve with redaction | Correct redaction applied per role |
| Detokenize | Authorized users get plain text |
| Access control | Unauthorized requests are blocked |
| Rate limiting | Retry logic handles rate limits |
| Error handling | Graceful failure modes |

## Phase 3: Go Live

The Go Live phase prepares for production. See [go-live-phase.md](go-live-phase.md) for detailed guidance.

### 3.1 Production Readiness

**Goal**: Ensure your implementation is production-ready.

#### Production Readiness Checklist

- [ ] All development testing complete
- [ ] Service accounts created for production
- [ ] Production vault created with same schema
- [ ] Access controls configured and tested
- [ ] Monitoring and alerting set up
- [ ] Error handling comprehensive
- [ ] Retry logic implemented

### 3.2 Security Review

**Goal**: Validate security posture before launch.

See [security-checklist.md](security-checklist.md) for the complete security review checklist.

#### Security Review Areas

| Area | Key Checks |
|------|------------|
| **Credentials** | No hardcoded secrets, rotation policy |
| **Access Control** | Least privilege, role segregation |
| **Data Handling** | No PII in logs/errors, proper redaction |
| **Transport** | HTTPS everywhere, certificate validation |
| **Audit** | All access logged, logs secured |

### 3.3 Data Migration

**Goal**: Migrate existing sensitive data to Skyflow.

#### Migration Approaches

| Approach | Use Case | Complexity |
|----------|----------|------------|
| **Batch import** | One-time historical data | Medium |
| **Incremental sync** | Ongoing synchronization | High |
| **Cutover** | New data only, deprecate old | Low |

#### Migration Checklist

- [ ] Inventory existing sensitive data
- [ ] Plan token mapping strategy
- [ ] Create and test migration scripts
- [ ] Plan rollback procedure
- [ ] Execute migration
- [ ] Validate migrated data
- [ ] Update application to use tokens

### 3.4 Launch

**Goal**: Successfully launch your Skyflow integration.

#### Launch Checklist

- [ ] All tests passing
- [ ] Security review approved
- [ ] Data migration complete (if applicable)
- [ ] Monitoring active
- [ ] Runbook documented
- [ ] Rollback plan ready
- [ ] Go/no-go decision made
- [ ] Route live traffic to production vault

## Creating an Implementation Plan

When helping a user create their implementation plan, use the template at [templates/implementation-plan.md](templates/implementation-plan.md).

### Information to Gather

1. **Use case summary**: 2-3 sentences describing what they're building
2. **Data inventory**: List of sensitive data fields (use [templates/data-inventory.md](templates/data-inventory.md))
3. **Tech stack**: Languages, frameworks, deployment environment
4. **Timeline**: Target launch date and any hard deadlines
5. **Team**: Size and Skyflow experience level
6. **Constraints**: Compliance requirements, existing systems, budget

### Sample Timeline

```
Week 1-2: Define Phase
├── Week 1: Data assessment, compliance mapping
└── Week 2: Schema design, environment setup

Week 3-5: Build Phase
├── Week 3: Authentication, access control setup
├── Week 4: Backend SDK integration
└── Week 5: Frontend integration, testing

Week 6-7: Go Live Phase
├── Week 6: Security review, production setup
└── Week 7: Data migration, launch
```

## Related Documentation

- [define-phase.md](define-phase.md) - Detailed Define phase guidance
- [build-phase.md](build-phase.md) - Detailed Build phase guidance
- [go-live-phase.md](go-live-phase.md) - Detailed Go Live phase guidance
- [use-case-patterns.md](use-case-patterns.md) - Pre-built patterns for common use cases
- [security-checklist.md](security-checklist.md) - Security review checklist
- [templates/implementation-plan.md](templates/implementation-plan.md) - Plan template
- [templates/data-inventory.md](templates/data-inventory.md) - Data assessment worksheet

## Usage Instructions for Claude

When helping users plan their Skyflow implementation:

1. **Gather context**: Ask about use case, data types, tech stack, timeline
2. **Classify the project**: Match to use case patterns in [use-case-patterns.md](use-case-patterns.md)
3. **Create phased plan**: Generate Define/Build/Go Live milestones using the template
4. **Provide checklists**: Share relevant phase checklists from this document
5. **Reference detailed docs**: Link to phase-specific guidance as needed
6. **Iterate**: Refine plan based on user feedback and constraints

### Key Integrations

- Use the **create-vault** skill when ready to create the vault schema
- Use the **rest-apis** skill for API-specific questions during build phase
- Reference Skyflow documentation for latest SDK guides and API references
