# Data Inventory Worksheet

Use this worksheet to inventory all sensitive data in your system before designing your Skyflow vault schema.

---

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | |
| **Date** | |
| **Completed By** | |

---

## Part 1: Sensitive Data Identification

### What sensitive data do you collect?

Check all that apply and list specific fields:

#### Personal Identifiable Information (PII)

- [ ] **Names**
  - Fields: ________________________________________________
  - Example: first_name, last_name, full_name

- [ ] **Email addresses**
  - Fields: ________________________________________________
  - Example: email, work_email, personal_email

- [ ] **Phone numbers**
  - Fields: ________________________________________________
  - Example: phone, mobile, work_phone

- [ ] **Physical addresses**
  - Fields: ________________________________________________
  - Example: street, city, state, zip, country

- [ ] **Date of birth**
  - Fields: ________________________________________________

- [ ] **Government IDs (SSN, Tax ID, etc.)**
  - Fields: ________________________________________________
  - Example: ssn, tax_id, national_id

- [ ] **Driver's license / Passport**
  - Fields: ________________________________________________
  - Example: dl_number, passport_number

- [ ] **Other PII**
  - Fields: ________________________________________________

#### Payment Card Information (PCI)

- [ ] **Credit/debit card numbers**
  - Fields: ________________________________________________

- [ ] **Card verification value (CVV/CVC)**
  - Fields: ________________________________________________

- [ ] **Card expiration date**
  - Fields: ________________________________________________

- [ ] **Cardholder name**
  - Fields: ________________________________________________

- [ ] **Bank account numbers**
  - Fields: ________________________________________________

- [ ] **Routing numbers**
  - Fields: ________________________________________________

#### Protected Health Information (PHI)

- [ ] **Medical record numbers**
  - Fields: ________________________________________________

- [ ] **Diagnoses / Conditions**
  - Fields: ________________________________________________

- [ ] **Treatment information**
  - Fields: ________________________________________________

- [ ] **Prescription information**
  - Fields: ________________________________________________

- [ ] **Insurance information**
  - Fields: ________________________________________________

- [ ] **Provider information**
  - Fields: ________________________________________________

#### Non-Public Personal Information (NPI)

- [ ] **Financial account information**
  - Fields: ________________________________________________

- [ ] **Investment information**
  - Fields: ________________________________________________

- [ ] **Income / Salary information**
  - Fields: ________________________________________________

#### Other Sensitive Data

- [ ] **Biometric data**
  - Fields: ________________________________________________

- [ ] **Authentication credentials**
  - Fields: ________________________________________________

- [ ] **Document images/files**
  - Fields: ________________________________________________

- [ ] **Other**
  - Fields: ________________________________________________

---

## Part 2: Data Sources

### Where does sensitive data enter your system?

| Source Type | Description | Data Fields Collected |
|-------------|-------------|----------------------|
| User Forms | | |
| Mobile App | | |
| API Integrations | | |
| File Uploads | | |
| Third-party Services | | |
| Data Imports | | |
| Other | | |

---

## Part 3: Data Storage

### Where is sensitive data currently stored?

| Storage Location | Type | Data Fields Stored | Encryption? |
|-----------------|------|-------------------|-------------|
| Primary Database | [e.g., PostgreSQL] | | [ ] Yes [ ] No |
| Cache | [e.g., Redis] | | [ ] Yes [ ] No |
| File Storage | [e.g., S3] | | [ ] Yes [ ] No |
| Logs | | | [ ] Yes [ ] No |
| Third-party SaaS | | | [ ] Yes [ ] No |
| Other | | | [ ] Yes [ ] No |

---

## Part 4: Data Processing

### Which systems process sensitive data?

| System/Service | Purpose | Data Fields Accessed | Access Level |
|---------------|---------|---------------------|--------------|
| Backend API | | | Read / Write / Both |
| Worker Jobs | | | Read / Write / Both |
| Analytics | | | Read / Write / Both |
| Reporting | | | Read / Write / Both |
| Third-party APIs | | | Read / Write / Both |
| Other | | | Read / Write / Both |

---

## Part 5: Data Destinations

### Where does sensitive data leave your system?

| Destination | Purpose | Data Fields Sent | Method |
|-------------|---------|-----------------|--------|
| Email Provider | | | API / Webhook |
| Payment Processor | | | API / Webhook |
| Analytics Platform | | | API / Webhook |
| Third-party APIs | | | API / Webhook |
| Reports/Exports | | | File / API |
| Other | | | |

---

## Part 6: Data Access

### Who needs access to sensitive data?

| Role | Data Fields Needed | Purpose | Access Level |
|------|-------------------|---------|--------------|
| | | | Full / Masked / Redacted |
| | | | Full / Masked / Redacted |
| | | | Full / Masked / Redacted |
| | | | Full / Masked / Redacted |
| | | | Full / Masked / Redacted |

---

## Part 7: Compliance Requirements

### Which regulations apply to your data?

- [ ] **PCI-DSS** (Payment card data)
  - Scope: ________________________________________________

- [ ] **HIPAA** (US healthcare data)
  - Scope: ________________________________________________

- [ ] **GDPR** (EU personal data)
  - Scope: ________________________________________________

- [ ] **CCPA** (California consumer data)
  - Scope: ________________________________________________

- [ ] **SOC 2** (Service organization controls)
  - Scope: ________________________________________________

- [ ] **Other**
  - Regulation: ____________________________________________
  - Scope: ________________________________________________

### Compliance requirements by data field:

| Data Field | Regulations | Retention Period | Deletion Required |
|------------|-------------|------------------|-------------------|
| | | | [ ] Yes [ ] No |
| | | | [ ] Yes [ ] No |
| | | | [ ] Yes [ ] No |

---

## Part 8: Data Field Details

### Complete this table for each sensitive data field:

| Field Name | Data Type | Category | Tokenization | Redaction | Queryable | Unique |
|------------|-----------|----------|--------------|-----------|-----------|--------|
| | String/Int/Date/File | PII/PHI/PCI/NPI | Det/Non-det/FPT | Mask/Redact/Plain | Yes/No | Yes/No |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

**Legend:**
- **Tokenization**: Det = Deterministic, Non-det = Non-deterministic, FPT = Format-preserving
- **Redaction**: Mask = Partial masking, Redact = Full redaction, Plain = No redaction

---

## Part 9: Summary

### Data Inventory Summary

| Category | Field Count | Compliance Impact |
|----------|-------------|-------------------|
| PII | | |
| PHI | | |
| PCI | | |
| NPI | | |
| **Total** | | |

### Key Decisions Needed

1. [ ] Tokenization strategy for each field
2. [ ] Redaction rules for each role
3. [ ] Retention policies
4. [ ] Access control matrix
5. [ ] Migration approach for existing data

### Next Steps

- [ ] Review inventory with stakeholders
- [ ] Design vault schema based on inventory
- [ ] Create access control matrix
- [ ] Plan data migration (if applicable)

---

## Notes

[Additional notes, questions, or concerns about the data inventory]
