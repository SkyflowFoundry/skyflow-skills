# Sensitive Data Inventory: [Project name]

This report must not contain any sensitive values. Cite files, lines, and field names only.

| Field | Value |
| ----- | ----- |
| **Scope** | [Repository, service, directory, or feature reviewed] |
| **Goal** | [General check, AI feature, audit preparation, or pre-Skyflow inventory] |
| **Date** | |
| **Commit** | [Commit SHA reviewed] |
| **Method** | Static review of code and schemas. No application was run and no database was queried. |
| **Not covered** | [Directories, services, or sinks that were skipped and why] |

---

## Summary

[Two or three sentences on the overall picture.]

**AI features reviewed:** [List the AI features the product uses, or write "None found".]

| Category | Entries | Confirmed | Suspected or inferred |
| -------- | ------- | --------- | --------------------- |
| Identity | | | |
| Contact | | | |
| Government ID | | | |
| Payment card | | | |
| Financial | | | |
| Health | | | |
| Special category | | | |
| Location and device | | | |
| Children's data | | | |
| Credentials and secrets | | | |

### Top findings

1. [Most important finding with its severity and the fix]
2.
3.

---

## Part 1: Sensitive fields

| # | Field | Data type | Defined at | Category | Tier | Status | Entry points | Stored in |
| - | ----- | --------- | ---------- | -------- | ---- | ------ | ------------ | --------- |
| F1 | `users.email` | String | `db/schema.sql:12` | Contact | Confidential | Confirmed | Sign-up form, CRM import | Postgres `users` |
| F2 | | | | | | | | |

**Tier:** Restricted, Confidential, or Internal. **Status:** Confirmed, Suspected, Inferred (from the product's purpose rather than a field), or History only (removed from the code but still in git history).

---

## Part 2: Findings

Most findings are flows to a sink. Findings about collecting or keeping too much go here too, with `Collection` or `Retention` in the sink column.

| # | Finding | Fields | Sink | Location | Severity | Reference | Recommendation |
| - | ------- | ------ | ---- | -------- | -------- | --------- | -------------- |
| S1 | Request bodies logged on sign-up | F1 | Application logs | `src/routes/signup.ts:40` | Medium | | Log an allowlist of fields |
| S2 | | | | | | | |

**Severity:** High, Medium, or Low. **Reference:** an OWASP risk ID with a link where one applies.

---

## Part 3: Minimization plan

List the fixes in the order you recommend doing them. Name the ladder step each fix uses.

| Order | Fix | Findings | Ladder step | Effort |
| ----- | --- | -------- | ----------- | ------ |
| 1 | | | Don't collect, Don't keep, Don't move, Reduce, Replace, or Protect | Small, Medium, or Large |
| 2 | | | | |

---

## Part 4: Likely regulatory scope

This section is not legal advice. It lists regulations the compliance or legal team may want to confirm.

| Regulation | Why it may apply | Fields |
| ---------- | ---------------- | ------ |
| [For example PCI DSS] | [For example card numbers are stored] | |

---

## Part 5: Open questions

1. [Questions the code could not answer, such as model provider retention terms or who can read the warehouse]
2.

---

## Part 6: Carrying this into a Skyflow plan

Complete this part only if the user wants to plan a Skyflow implementation. The **plan-skyflow-implementation** skill uses a data inventory worksheet, and each part of this report fills one or more of its parts.

| This report | Data inventory worksheet |
| ----------- | ------------------------ |
| Part 1 field, data type, and category | Part 1 (Sensitive Data Identification) and Part 8 (Data Field Details) |
| Part 1 entry points | Part 2 (Data Sources) |
| Part 1 stored in | Part 3 (Data Storage) |
| Part 2 findings with sinks inside the system | Part 4 (Data Processing) |
| Part 2 findings with sinks outside the system | Part 5 (Data Destinations) |
| Part 4 regulatory scope | Part 7 (Compliance Requirements) |

The worksheet's Part 6 (Data Access) needs input from the user about roles, because the code rarely shows who should see what.
