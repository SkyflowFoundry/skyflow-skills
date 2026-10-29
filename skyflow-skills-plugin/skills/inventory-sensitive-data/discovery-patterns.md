# Discovery Patterns

This reference lists where sensitive data is usually declared and how to search for it. Every pattern here is deliberately loose. Expect false positives and confirm each hit by reading the surrounding code.

## Where to look first

Read the files that declare data shapes before you search application code.

| Artifact | Where it usually lives | Signals to look for |
| -------- | ---------------------- | ------------------- |
| SQL migrations and schemas | `migrations/`, `db/`, `*.sql`, `db/schema.rb`, `alembic/versions/`, Flyway `V*__*.sql` | `CREATE TABLE`, `ADD COLUMN` |
| ORM models | `models.py`, `app/models/`, `entities/`, `schema.prisma`, `*.entity.ts` | Django `models.Model`, SQLAlchemy `Column(` or `mapped_column(`, TypeORM `@Column`, Prisma `model`, Mongoose `new Schema(`, Drizzle `pgTable(`, JPA `@Entity`, GORM `gorm:"` tags |
| API contracts | `openapi.*`, `swagger.*`, `*.graphql`, `*.proto`, `*.avsc`, `*.schema.json` | Property names and `format: email` or similar |
| Validators and DTOs | `schemas/`, `dto/`, `validators/`, `types/` | Pydantic `BaseModel`, Zod `z.object(`, Joi `Joi.object(`, class-validator `@IsEmail` and `@IsPhoneNumber`, `EmailStr` |
| Forms and client inputs | `components/`, `templates/`, `views/` | `<input>` names and `autocomplete` values |
| Mobile apps | `Info.plist`, `AndroidManifest.xml` | iOS `NS*UsageDescription` keys and Android `android.permission.*` entries |
| Data pipelines | dbt `models/` and `schema.yml`, Airflow `dags/`, Spark jobs | Column lists and `SELECT *` from user tables |
| AI assets | `prompts/`, `*.prompt`, `*.j2`, `*.jinja`, `evals/`, `datasets/`, `*.jsonl` | Prompt templates, document loaders, and training or evaluation records |
| Committed data | `fixtures/`, `seeds/`, `seed.*`, `*.csv`, `*.xlsx`, `*.parquet`, `*.ipynb`, `*.sql` dumps, `.env*` | Real-looking records and secrets |

Notebook output cells deserve a close look because they often hold printed rows from a real database.

## Search setup

Exclude dependencies and build output on every search. With ripgrep:

```bash
RG_EXCLUDES=(-g '!node_modules' -g '!vendor' -g '!third_party' -g '!.venv' -g '!venv' -g '!dist' -g '!build' -g '!.next' -g '!coverage' -g '!*.lock' -g '!package-lock.json' -g '!*.min.js')
```

Also exclude any vendored SDK or third-party documentation you find in the repo. It is full of example card numbers and placeholder tokens that are not the project's data.

Without ripgrep, use `grep -rEn -i` with `--exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build`.

### Ignored and hidden files

Ripgrep skips hidden files and anything in `.gitignore` by default, so the searches above never see `.env` files. Run one extra pass that lists ignored and hidden files that hold secrets or data:

```bash
rg -l --hidden --no-ignore -g '!.git' "${RG_EXCLUDES[@]}" -g '.env*' -g '*.pem' -g '*.key' -g '*.p12' -g '*.sqlite' -g '*.db' -g '*.csv' --files
```

A gitignored file that only exists on this machine is a lower risk than a committed one. Check which ones are tracked with `git ls-files -- '.env*'`. Inspect any of them with the safe procedures below.

## Reading sensitive files safely

Reading a schema or model is safe because it holds field names and not values. Reading fixtures, `.env` files, notebooks, or lines that matched a value pattern can print real values into the transcript. Use these forms instead.

| Need | Command |
| ---- | ------- |
| See which keys an `.env` file defines | `sed -E 's/^([^=#]+)=.*/\1=[REDACTED]/' .env` |
| See matched lines with the values masked | `rg -n -r '[REDACTED]' -e '<pattern>' <path>` |
| Count matches per file | `rg -c -e '<pattern>' .` |
| Find commits that ever added or removed a match | `git log --all --oneline -G '<pattern>'` |
| Find the history of a deleted or ignored file | `git log --all --oneline -- <path>` |

The `git log` forms print commit IDs and subjects only. Do not add `-p` because a patch shows the values. A secret that appears only in git history is still exposed to anyone with a clone, so record it as a finding and recommend rotation.

When a sink search prints a line that contains a literal secret or personal value, rerun it with `-r '[REDACTED]'` and a value pattern before you quote it.

## Field-name patterns

Run each pattern with `rg -n -i "${RG_EXCLUDES[@]}" -e '<pattern>' .` to see the lines. Add `-c` first to get a count per file when the repo is large. The patterns match `snake_case`, `kebab-case`, and `camelCase` names because the search is case-insensitive.

| Category | Pattern |
| -------- | ------- |
| Identity | `(first\|last\|full\|middle\|given\|family\|maiden\|legal)[_-]?name\|date[_-]?of[_-]?birth\|birth[_-]?date\|birthday\|\bdob\b\|\bgender\b` |
| Contact | `e[_-]?mail\|phone\|mobile[_-]?(number\|no)\|msisdn\|street\|address[_-]?line\|postal[_-]?code\|zip[_-]?code\|zipcode` |
| Government ID | `\bssn\b\|social[_-]?security\|national[_-]?id\|tax[_-]?id\|\bitin\b\|passport\|driver'?s?[_-]?licen[cs]e\|aadhaar\|\bnric\b` |
| Payment card | `card[_-]?(number\|num\|no)\b\|cc[_-]?(number\|num)\|credit[_-]?card\|\bcvv2?\b\|\bcvc2?\b\|card[_-]?holder\|exp(iry\|iration)[_-]?(date\|month\|year)` |
| Financial | `\biban\b\|routing[_-]?(number\|no)\|account[_-]?(number\|num\|no)\b\|sort[_-]?code\|salary\|income\|credit[_-]?score` |
| Health | `diagnos[ie]s\|icd[_-]?10\|medication\|prescription\|allerg(y\|ies)\|\bmrn\b\|medical[_-]?record\|patient\|insurance[_-]?(id\|number)\|member[_-]?id` |
| Special category | `\brace\b\|ethnicity\|religion\|sexual[_-]?orientation\|union[_-]?member\|biometric\|fingerprint\|face[_-]?(id\|embedding\|template)\|genetic` |
| Location and device | `latitude\|longitude\|\blat\b\|\blng\b\|geo[_-]?location\|ip[_-]?addr\|remote[_-]?addr\|x-forwarded-for\|device[_-]?id\|\bidfa\b\|\bgaid\b\|advertising[_-]?id\|\bimei\b` |
| Credentials and secrets | `password\|passwd\|secret\|api[_-]?key\|access[_-]?token\|refresh[_-]?token\|private[_-]?key\|security[_-]?(question\|answer)` |

The `\|` in the table is an escaped pipe for Markdown. Type a plain `|` in the shell.

### Form autocomplete values

HTML `autocomplete` tokens are a strong signal because they state what a field holds. Search with:

```bash
rg -n -i "${RG_EXCLUDES[@]}" -e "autocomplete=[\"'{](cc-|bday|sex|tel|email|name|given-name|family-name|street-address|address-line|postal-code|one-time-code|current-password|new-password)" .
```

### Mobile permissions

```bash
rg -n "${RG_EXCLUDES[@]}" -e 'NS[A-Za-z]+UsageDescription' -e 'android\.permission\.(ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION|READ_CONTACTS|READ_SMS|READ_PHONE_STATE|BODY_SENSORS|CAMERA|RECORD_AUDIO)' .
```

## Value patterns

Value searches find real or realistic data in fixtures, notebooks, logs, and committed files. **Never print the matched values.** Use `-c` or `-l` to get only counts or file names, or use `-r '[REDACTED]'` to print the line with the match masked.

```bash
rg -n "${RG_EXCLUDES[@]}" -r '[REDACTED]' -e '<pattern>' .
```

| What | Pattern | Notes |
| ---- | ------- | ----- |
| Email address | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | Ignore `example.com`, `example.org`, and `test` domains |
| US SSN | `\b\d{3}-\d{2}-\d{4}\b` | Also matches some dates and IDs, so read the context |
| Card-like number | `\b(?:\d[ -]?){12,18}\d\b` | Filter with the Luhn check below |
| IBAN | `\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b` | Noisy in minified code |
| Phone in E.164 form | `\+[1-9]\d{7,14}\b` | Misses local formats |
| IPv4 address | `\b(?:\d{1,3}\.){3}\d{1,3}\b` | Ignore private ranges and version strings |
| AWS access key ID | `\b(AKIA\|ASIA)[0-9A-Z]{16}\b` | A High finding when present |
| Private key | `-----BEGIN [A-Z ]*PRIVATE KEY-----` | A High finding when present |
| JWT | `\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | May hold personal claims as well as being a credential |
| Hardcoded secret | `(api[_-]?key\|secret\|token\|password)\s*[:=]\s*['"][^'"]{8,}['"]` | Use `-i` and skip obvious placeholders |
| Secret exposed to the client bundle | `(NEXT_PUBLIC_\|VITE_\|EXPO_PUBLIC_\|REACT_APP_\|NUXT_PUBLIC_\|PUBLIC_)[A-Z0-9_]*(KEY\|SECRET\|TOKEN\|PASSWORD)` | Variables with these prefixes are compiled into code that ships to every user, so any real secret here is a High finding. Publishable keys meant for the client are fine. |

Test card numbers published by payment providers (such as numbers starting with `4111 1111`) are expected in tests. Report them only if they appear outside test code.

### Luhn check without printing numbers

This pipeline prints only the file and line of each card-like number that passes the Luhn check:

```bash
rg -o -n --with-filename "${RG_EXCLUDES[@]}" '\b(?:\d[ -]?){12,18}\d\b' . | python3 -c '
import sys
def luhn(s):
    d = [int(c) for c in s if c.isdigit()][::-1]
    return sum(x if i % 2 == 0 else (x * 2 - 9 if x > 4 else x * 2) for i, x in enumerate(d)) % 10 == 0
for line in sys.stdin:
    where, value = line.rstrip("\n").rsplit(":", 1)
    if luhn(value):
        print(where)
'
```

## False-positive traps

These names often mean something other than personal data. Read the code before you record them.

| Name | Often actually means |
| ---- | -------------------- |
| `name` | A product, file, or config name |
| `address` | A memory address, network address of a service, or blockchain address |
| `token` | A CSRF token, pagination cursor, or lexer token |
| `key` | A map key, cache key, or React list key |
| `pin` | A pinned item or a GPIO pin |
| `pan` | Camera panning |
| `race` | A race condition |
| `patient` | A domain term in a demo app that holds no real data |
| `lat` and `lng` | A store or office location rather than a person's location |

A field that is only Suspected stays in the inventory with that label. Do not drop it just because you could not confirm it.
