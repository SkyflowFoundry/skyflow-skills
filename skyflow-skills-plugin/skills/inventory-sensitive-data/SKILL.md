---
name: inventory-sensitive-data
description: Inventory the sensitive data in a codebase, database schema, or AI pipeline and review it for data minimization. Finds PII, PHI, payment, financial, and secret fields, traces where they flow (logs, analytics, error trackers, caches, third-party APIs, LLM prompts, embeddings, and vector stores), and produces a prioritized report with minimization fixes. Needs no Skyflow account. Use when a user asks what personal or sensitive data their app handles, where PII might be leaking, whether an LLM, RAG, or agent feature exposes customer data, how to prepare for a privacy or security review, or how to build a data inventory before planning a Skyflow implementation.
---

# Inventory Sensitive Data

This skill helps you find the sensitive data in a system and see where it goes. You read the code and schemas, list every sensitive field, trace each one to the places it is stored or sent, and recommend ways to collect, keep, and move less of it. The result is a report the user can act on right away.

The skill works without a Skyflow account and without any network access. It only needs the code or a description of the system. Skyflow comes up only at the end, as one option among several for protecting what remains.

## Overview

| Step | What you do | Reference |
| ---- | ----------- | --------- |
| 1 | Agree on scope and goal | This file |
| 2 | Find where sensitive data is defined | [discovery-patterns.md](discovery-patterns.md) |
| 3 | Classify each field | This file |
| 4 | Trace each field to its sinks | [sinks.md](sinks.md) |
| 5 | Review each flow for minimization | [minimization.md](minimization.md) |
| 6 | Write the report | [templates/inventory-report.md](templates/inventory-report.md) |
| 7 | Hand off | This file |

## Prerequisites

1. A workspace that contains the code, schemas, or pipeline definitions to review. If there is no code, the user can describe the system and you can run the same steps as an interview.
2. A way to search files. Prefer `rg` (ripgrep) and fall back to `grep -rEn` when it is not installed.

No account, credentials, or environment variables are needed.

## Guardrails

Apply these throughout the review.

1. **Stay read-only.** Do not change code, configuration, or data until the user approves a specific fix.
2. **Never copy sensitive values.** Cite the file, line, and field name instead. If you find real-looking personal data or a secret, describe its type and location and do not repeat the value in the chat or the report. Read `.env` files, fixtures, and value matches with the masking commands in [discovery-patterns.md](discovery-patterns.md#reading-sensitive-files-safely) so the values never reach your own tool output either.
3. **Report secrets by location only.** A committed API key or private key is a finding on its own. Recommend rotating it because removing it from the latest commit does not remove it from git history.
4. **Do not move data to scan it.** Do not run the application, query production databases, or send code or data to an outside service as part of the review. Sample a database only if the user asks and only against non-production data.
5. **Separate evidence from guesses.** Mark a field **Confirmed** when the code shows it holds sensitive data. Mark it **Suspected** when only its name suggests it.
6. **Do not give legal advice.** The regulation hints in this skill help the user brief their compliance or legal team. They are not a determination of what applies.
7. **Say what you skipped.** In a large codebase, review the most important paths first and list what you did not cover.

## Step 1: Agree on scope and goal

Ask the user two questions and skip any they have already answered.

1. **What should I review?** Offer these choices.
   1. The whole repository.
   2. One service, package, or directory.
   3. A schema or data model file.
   4. One AI feature, such as a chatbot, RAG search, or agent.
2. **What is the review for?** Offer these choices.
   1. A general privacy or security check.
   2. Launching or hardening an AI feature.
   3. Preparing for an audit or compliance review.
   4. Building a data inventory before planning a Skyflow implementation.

The goal decides what to emphasize. An AI feature review spends most of its time on prompts, retrieval, and model logging. A pre-Skyflow inventory needs every field classified because the vault schema is built from it.

Before you start, tell the user that the review is read-only and that the report will not contain any sensitive values.

## Step 2: Find where sensitive data is defined

Start with the places that declare data shapes, because one schema hit is worth more than a hundred grep matches in application code. Look in this order.

1. Database schemas, migrations, and ORM models.
2. API contracts such as OpenAPI, GraphQL, and protobuf files, plus request validators and DTOs.
3. Forms and client input fields.
4. Data pipelines, warehouse models, and ETL jobs.
5. AI assets such as prompt templates, document loaders, and evaluation or fine-tuning datasets.
6. Seed data, fixtures, notebooks, and committed data files.

Then run the field-name and value searches. Finish with a pass over ignored and hidden files such as `.env` and a check of git history, because the default searches skip both. The file paths, search patterns, safe ways to read sensitive files, and false-positive traps are in [discovery-patterns.md](discovery-patterns.md).

Record each sensitive field with the file and line where it is defined.

## Step 3: Classify each field

Give each field a category and a tier.

| Category | Examples |
| -------- | -------- |
| **Identity** | Full name, date of birth, photo |
| **Contact** | Email, phone, postal address |
| **Government ID** | SSN, national ID, passport, driver's license, tax ID |
| **Payment card** | Card number (PAN), CVV, expiry, cardholder name |
| **Financial** | Bank account, routing number, IBAN, income, credit score |
| **Health** | Diagnoses, medications, medical record number, insurance member ID |
| **Special category** | Race or ethnicity, religion, sexual orientation, union membership, genetic or biometric data |
| **Location and device** | Precise geolocation, IP address, device ID, advertising ID |
| **Children's data** | Any personal data about users who may be minors |
| **Credentials and secrets** | Passwords, security answers, API keys, session tokens, private keys |

| Tier | Meaning | Typical members |
| ---- | ------- | --------------- |
| **Restricted** | Exposure causes direct harm or triggers breach notification | Government IDs, card data, health data, special category data, credentials |
| **Confidential** | Exposure harms privacy and usually needs notice or consent | Contact details, precise location, financial details, date of birth |
| **Internal** | Low risk alone but identifying when combined | Internal user IDs, coarse location, account timestamps |

Combinations raise the tier. A ZIP code alone is Internal but a ZIP code together with a birth date and gender can identify a person.

The product's purpose can also raise the tier. Being a user of a dating, health, religious, or LGBTQ+ app can reveal a special category trait even when no field stores it. Record this as a Suspected inference and say what it is inferred from.

## Step 4: Trace each field to its sinks

For each Restricted or Confidential field, follow it from where it enters the system to every place it is written, sent, logged, or shown. A sink is any place the data ends up outside its primary store. The most common sinks are these.

1. Application logs, URLs, and query strings.
2. Error trackers, session replay, analytics, and tracing tools.
3. Caches, queues, search indexes, warehouses, and exports.
4. Third-party APIs, email, and SMS.
5. Browser and mobile storage.
6. LLM prompts, system prompts, embeddings, vector stores, agent memory, and LLM observability tools.
7. Test fixtures, seed data, and notebooks.

[sinks.md](sinks.md) lists the code signals for each sink and why it matters.

Record each flow as a finding with the field, the sink, the file and line, and a severity. Fields that are collected or kept without need are findings too, even when they never reach a sink.

| Severity | Use when |
| -------- | -------- |
| **High** | Restricted data reaches a sink that is broadly readable, held by a third party, or hard to delete. Examples are plaintext card numbers in logs, health data in an LLM prompt, and a committed secret. |
| **Medium** | Confidential data reaches such a sink, or Restricted data reaches a sink with partial controls. Examples are email addresses sent to analytics and unmasked inputs in session replay. |
| **Low** | Internal data in a sink, or a flow that is already well controlled but could be tighter. |

## Step 5: Review each flow for minimization

For each finding, work down this ladder and stop at the first step that solves the problem.

1. **Don't collect it.** Does the system need this field at all?
2. **Don't keep it.** Can it be deleted after use or given a retention limit?
3. **Don't move it.** Can this sink do its job without the field?
4. **Reduce it.** Would a truncated, generalized, or partial value be enough?
5. **Replace it.** Can a token, pseudonym, or de-identified version stand in for it?
6. **Protect what remains.** Apply encryption, access control, masking, and audit logging.

[minimization.md](minimization.md) explains each step with techniques, examples, and the traps to avoid. It also covers the AI-specific fixes for prompts, embeddings, and agent memory.

## Step 6: Write the report

Fill in [templates/inventory-report.md](templates/inventory-report.md). Ask the user where to save it and suggest `docs/sensitive-data-inventory.md`. Do not commit it unless the user asks.

The report must list the scope and what was skipped. Each finding needs a file and line and a recommendation. Lead the summary with the three to five findings that matter most.

## Step 7: Hand off

Offer the user these next steps and let them choose.

1. **Fix the top findings now.** Propose the specific changes for the High findings and make them only after the user approves each one.
2. **Plan how to protect the data that must stay.** If the user wants to evaluate Skyflow, the **plan-skyflow-implementation** skill picks up this report as its data inventory. The last section of the report template maps each part to that skill's worksheet. Users without an account can start with the **get-started** skill.
3. **Stop here.** The report stands on its own and can go to a security or compliance team.

## Troubleshooting

| Problem | What to do |
| ------- | ---------- |
| Searches return thousands of hits | Search schemas and models first. Exclude `node_modules`, `vendor`, `dist`, `build`, lockfiles, and generated code. |
| No schema exists because the store is schemaless | Use request validators, API types, and the code that writes documents to infer the shape. |
| Field names are generic, such as `data` or `payload` | Follow the writes to see what goes into them, and mark the field Suspected until you know. |
| The codebase is a monorepo | Review one service at a time and write one findings table per service. |
| Encrypted columns show up | They still count. Record them as protected and check where the decrypted value goes. |
| The user has no code to share | Run the steps as an interview. Ask what each form, table, and integration holds, and mark every field Suspected. |

## Related documentation

1. [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) covers personal data leaking through LLM inputs and outputs.
2. [OWASP LLM07:2025 System Prompt Leakage](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/) covers sensitive data and secrets placed in system prompts.
3. [OWASP LLM08:2025 Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) covers RAG and vector store risks.
4. [OWASP GenAI Data Security Risks and Mitigations 2026](https://genai.owasp.org/resource/owasp-genai-data-security-risks-mitigations-2026/) is a broader guide to data security in AI systems.
5. The **plan-skyflow-implementation** skill turns this inventory into a Skyflow vault schema and implementation plan.
