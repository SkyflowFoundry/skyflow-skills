# Minimization

This reference explains the minimization ladder from Step 5 of the skill. Work down the ladder for each finding and recommend the first step that solves it. Earlier steps are better because data you never collect or move cannot leak.

## The ladder

### 1. Don't collect it

Ask whether the product needs the field at all. Look for these patterns.

1. Fields that are written but never read.
2. Form fields marked optional that nobody uses downstream.
3. Full date of birth collected only to check that a user is an adult.
4. Government IDs collected "just in case" for a future feature.

**Recommendation:** Remove the field from the form, API, and schema. Plan a migration to delete existing values.

### 2. Don't keep it

Ask whether the field is still needed after the task that collected it.

1. Raw card details kept after the payment provider returns its own token.
2. Uploaded identity documents kept after verification.
3. Chat transcripts and prompt logs kept forever.
4. Soft-deleted records that still hold all their personal data.

**Recommendation:** Delete after use, or set a time-to-live or retention job. Make sure deletion also reaches caches, search indexes, warehouses, backups, and vector stores.

### 3. Don't move it

Ask whether this sink can do its job without the field. This step fixes most findings in logs, analytics, and AI pipelines.

1. **Logs:** Log an allowlist of safe fields instead of whole objects. Allowlists fail safe when someone adds a new field, but denylists do not. Turn on the redaction features of your logger and framework, such as Rails `filter_parameters` or the `redact` option in pino.
2. **Error tracking:** Turn off default personal data capture and add a scrubbing hook such as Sentry `beforeSend`.
3. **Analytics:** Identify users by an internal pseudonymous ID and never by email or phone.
4. **Session replay:** Mask all inputs by default and unmask only fields known to be safe.
5. **URLs:** Move sensitive values from paths and query strings into request bodies or headers.
6. **APIs and client bundles:** Return only the fields the caller needs.
7. **Warehouses:** Replicate only the columns analysts need, or replicate a de-identified view.

### 4. Reduce it

Ask whether a smaller or coarser value would be enough.

| Full value | Reduced value | Good enough for |
| ---------- | ------------- | --------------- |
| Date of birth | Birth year, or an "over 18" flag | Age checks and cohort analysis |
| Street address | City, region, or the first three digits of a ZIP code | Regional analytics |
| Precise GPS coordinates | Rounded coordinates or a city | Local content |
| Card number | Last four digits and card brand | Showing the user which card is on file |
| Full IP address | Truncated IP address | Abuse rate limiting and rough geography |
| Free-text notes | Structured fields with no free text | Workflows where notes attract oversharing |

Small groups can still identify people. Check that a reduced value is shared by enough people before you call it anonymous.

### 5. Replace it

Ask whether a stand-in value can do the job.

1. **Tokenization** swaps the value for a random token and keeps the real value in a separate, tightly controlled store. Systems that only need to join, count, or pass the value along can use the token. A deterministic token gives the same token for the same value so joins still work.
2. **Pseudonymous IDs** replace direct identifiers with an internal ID. They work well for analytics and logs.
3. **De-identification of text** finds personal data inside free text and replaces it with placeholders or tokens. It is the main fix for prompts, transcripts, and documents headed into an index.
4. **Keyed hashing** such as HMAC with a secret key can stand in for a value when you only need equality checks.

Plain hashing is not a safe replacement for low-entropy values. Phone numbers, SSNs, dates of birth, and most email addresses can be recovered from an unkeyed hash by trying every possible value. Use a keyed hash with the key kept in a secrets manager, or use tokenization.

### 6. Protect what remains

Some fields must stay because the product depends on them. Protect them in the primary store.

1. **Field-level encryption** for Restricted fields, with keys held in a key management service. Encryption at rest on the disk alone does not stop an application user or a SQL injection from reading the value.
2. **Access control** so that each role can read only the fields it needs.
3. **Masking at display** so that support agents see `•••• 4242` and not the whole card number.
4. **Audit logging** of who read Restricted fields and when.
5. **Data residency** controls when the data must stay in a specific region.

Encryption and tokenization solve different problems. Encrypted data still lives in every system that holds the ciphertext, and every system that decrypts it needs access to the key. Tokenization removes the real value from those systems so they fall out of scope for many controls.

## AI-specific fixes

| Problem | Fix |
| ------- | --- |
| Personal data in prompts | De-identify the text before it goes into the prompt, then restore the original values in the response only for users allowed to see them. |
| Whole records passed to the model | Pass only the fields the task needs. Build the prompt from an allowlist instead of serializing the record. |
| Customer data or secrets in system prompts | Move secrets to server-side tool calls and keep customer data out of the system prompt. |
| Personal data in embeddings | Embed de-identified text. Keep sensitive metadata in the primary store and join it back in after retrieval. |
| Shared vector index across tenants | Use a separate namespace or collection per tenant, or enforce a tenant filter on every query on the server. |
| Deletion requests that miss the vector store | Store a source record ID with every chunk so you can delete all chunks for a person or document. |
| Prompt and completion logging | Turn off full-text logging in LLM observability tools or scrub it before it is stored. Set a retention limit. |
| Tool results that return whole records | Make tools return only the fields the agent needs and mask the rest. |
| Production transcripts in training or evaluation sets | De-identify the transcripts first, or build the set from synthetic data. |

## Where Skyflow fits

Skyflow is one way to carry out steps 5 and 6. Mention it only after the user has seen the vendor-neutral recommendations.

1. A **Skyflow vault** stores sensitive fields and returns tokens, so application databases, logs, and warehouses hold tokens instead of real values. It also handles field-level access policies, masking, and audit logs.
2. **Skyflow Detect** de-identifies personal data in text and files, which fits prompts, transcripts, and documents headed into a RAG index.

If the user wants to explore this, hand off to the **plan-skyflow-implementation** skill with the report, or to **get-started** if they do not have an account yet.
