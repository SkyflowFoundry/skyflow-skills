# Sinks

A sink is any place sensitive data ends up outside its primary store. This reference lists the common sinks, the code signals that reveal them, and why each one matters. Use it in Step 4 of the skill.

For every Restricted or Confidential field, search for the field name next to the signals below. Then follow any variable that holds the whole record, because most leaks come from logging or sending an entire object rather than one field.

## Logs and URLs

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Application logs | `console.log(user)`, `logger.info(req.body)`, `print(record)`, `log.Printf("%+v", u)`, `JSON.stringify(req.body)` inside a log call, f-strings that include a field | Logs are copied to many tools, kept for a long time, and readable by most engineers |
| Request logging middleware | `morgan`, `pino-http`, `express-winston`, Django `LOGGING` with request bodies, Rails `filter_parameters` that is missing fields | Logs every request body or URL without anyone choosing to |
| SQL and ORM query logging with parameter values | SQLAlchemy `echo=True`, Sequelize `logQueryParameters: true`, Hibernate TRACE logging on `org.hibernate.orm.jdbc.bind` (Hibernate 6) or `org.hibernate.type.descriptor.sql` (Hibernate 5), Prisma query event handlers that log `params`, Django `django.db.backends` logging at `DEBUG` | Logs bound parameter values in plaintext. Plain query logging such as Hibernate `show_sql` prints `?` placeholders and is a lower risk. |
| URLs and query strings | Routes such as `/users/:email`, `GET` forms, redirects that carry fields in the query string | URLs land in access logs, browser history, proxies, and `Referer` headers |
| Debug mode | Django `DEBUG = True`, verbose error pages, stack traces returned to clients, SDK options such as `debug: true` or a development environment flag left on in production config, log level `DEBUG` in production | Error pages and debug logs can show request data and local variables |

## Observability and product tools

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Error tracking | Sentry `setUser`, `sendDefaultPii: true`, `send_default_pii=True`, breadcrumbs, a missing `beforeSend` scrubber, Bugsnag or Rollbar metadata | Error events capture request bodies, user objects, and local variables |
| Product analytics | `analytics.identify(email`, `track('...', { email })`, Mixpanel `people.set`, PostHog `identify`, Amplitude `setUserId(email)`, `gtag` user properties | Sends data to a third party, often keyed on email instead of an internal ID |
| Session replay | FullStory, LogRocket, Hotjar, Microsoft Clarity, PostHog recordings, Sentry Replay | Records what users type and see unless masking is configured, so check for `maskAllInputs` and similar settings |
| Tracing and APM | OpenTelemetry span attributes such as `db.statement` or request bodies, Datadog, New Relic, Honeycomb | Spans can capture full queries and payloads |
| Tag managers | Google Tag Manager containers, `dataLayer.push` with user fields | Lets non-engineers add new data flows without a code review |

## Data stores and pipelines

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Caches | Redis or Memcached `set` of whole user objects, HTTP caches of personalized responses | Caches are often unencrypted and have no access control per record |
| Queues and event streams | Kafka, SQS, Pub/Sub, RabbitMQ, or EventBridge payloads, outbound webhooks | Payloads are copied to every consumer and kept for the topic's retention period |
| Search indexes | Elasticsearch, OpenSearch, Algolia, Typesense, Meilisearch document mappings | Indexes copy fields into another system with its own access rules |
| Warehouses and ETL | Snowflake, BigQuery, Redshift, dbt models, Fivetran or Airbyte connectors, CDC tools such as Debezium | Replicates whole tables to a place many analysts can query |
| Files and exports | CSV or PDF exports, S3 or GCS uploads, report generators, database backups | Files are easy to download, forward, and forget |

## Outbound integrations

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Email and SMS | SendGrid, Postmark, SES, Twilio, or Mailgun calls and their templates | Messages are stored by the provider and the recipient's mailbox |
| Third-party APIs | CRM, support desk, KYC, payment, or marketing API calls such as Salesforce, HubSpot, Zendesk, Intercom, or Stripe | Each one is a new copy of the data under another company's controls |
| Feature flags and experiments | LaunchDarkly, Statsig, or Optimizely user context objects | Flag SDKs often send the whole user context to the vendor |

## Client side

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Browser storage | `localStorage`, `sessionStorage`, IndexedDB, non-`HttpOnly` cookies | Readable by any script on the page, including third-party scripts |
| Mobile storage | `UserDefaults`, `SharedPreferences`, SQLite files, and caches outside the Keychain or Keystore | Stored unencrypted on the device and included in some backups |
| Client bundles | API responses that return more fields than the UI shows, and environment variables with a public prefix such as `NEXT_PUBLIC_`, `VITE_`, or `EXPO_PUBLIC_` | Data the UI hides is still visible in the network tab, and public variables are readable in the shipped code |

## AI and LLM sinks

These sinks are newer and are often missed in reviews. Give them extra time when the goal is an AI feature.

An AI feature here means AI that the product itself uses or ships. AI coding tools that developers use on the repository, such as assistant rule files or MCP server configs, are not product features. Check their config files for committed secrets and record those under credentials instead.

| Sink | Code signals | Why it matters | OWASP reference |
| ---- | ------------ | -------------- | --------------- |
| Prompts | `chat.completions.create`, `responses.create`, `messages.create`, LangChain `PromptTemplate`, LlamaIndex query engines, Vercel AI SDK `generateText` or `streamText`, templates that interpolate a user record or `JSON.stringify(customer)` | The model provider receives and may retain the data, and the model may repeat it to the wrong user | [LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) |
| System prompts | System or developer messages that embed customer data, internal records, or secrets | Users can often get the model to reveal its system prompt | [LLM07:2025](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/) |
| RAG ingestion and embeddings | Document loaders, chunkers, `embeddings.create`, and vector stores such as pgvector, Pinecone, Chroma, Weaviate, Qdrant, Milvus, or FAISS, plus the metadata stored with each chunk | Embedded text can be retrieved by anyone who can query the index, and deletion requests rarely reach it | [LLM08:2025](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) |
| Retrieval filters | Queries to the vector store with no tenant or user filter, or one shared namespace for all customers | One customer's documents can be retrieved for another customer | [LLM08:2025](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) |
| Agent tools and memory | Tool functions that return whole records, persisted chat history, memory stores, LangGraph checkpointers | Tool results go into the context window and are often stored with the conversation | [LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) |
| LLM observability and gateways | LangSmith, Langfuse, Helicone, Arize Phoenix, Braintrust, Weights & Biases, or a proxy gateway that logs requests | These tools log full prompts and completions by default | [LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) |
| Fine-tuning and evaluation data | `*.jsonl` training files, evaluation sets, and golden datasets built from production transcripts | Data in training sets can be memorized by the model and is hard to remove | [LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) |
| Model outputs | Completions written to logs, shown to other users, or passed to tools | The model can echo sensitive input into places the input never reached directly | [LLM02:2025](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) |

Model providers have their own retention and training policies. Do not state what a provider does with data. Ask the user to confirm the terms of their own agreement and note it as an open question in the report.

## Test and development data

| Sink | Code signals | Why it matters |
| ---- | ------------ | -------------- |
| Fixtures and seeds | `fixtures/`, `seeds/`, factory files, snapshot tests | Real records copied for tests end up in every clone of the repository |
| Notebooks | `*.ipynb` files with output cells | Outputs often contain rows printed from a real database |
| Committed data files | `*.csv`, `*.xlsx`, `*.parquet`, SQL dumps | Git history keeps the data even after the file is deleted |
| Environment files | `.env`, `.env.local`, or config files committed with real values | Secrets in git history must be rotated |
