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

Notebook output cells deserve a close look because they often hold printed rows from a real database. Read them only with the safe procedures below.

## Search setup

Exclude dependencies and build output on every search. With ripgrep, define this array:

```bash
RG_EXCLUDES=(-g '!node_modules' -g '!vendor' -g '!third_party' -g '!.venv' -g '!venv' -g '!dist' -g '!build' -g '!.next' -g '!coverage' -g '!*.lock' -g '!package-lock.json' -g '!*.min.js')
```

Some hosts start a fresh shell for every command, which silently drops the array. Put the definition at the start of every command that uses it and join the two with `;`. In the commands below, `RG_EXCLUDES=(...)` stands for the full definition above.

Also exclude any vendored SDK or third-party documentation you find in the repo. It is full of example card numbers and placeholder tokens that are not the project's data.

Without ripgrep, use `grep -rEn -i` with `--exclude-dir=node_modules --exclude-dir=vendor --exclude-dir=dist --exclude-dir=build`. The field-name patterns below work in `grep -E` as written. The value patterns need the changes described under [Value patterns](#value-patterns).

### Ignored and hidden files

Ripgrep skips hidden files and anything in `.gitignore` by default, so the searches above never see `.env` files. Run one extra pass that lists ignored and hidden files that hold secrets or data:

```bash
RG_EXCLUDES=(...); rg -l --hidden --no-ignore -g '!.git' "${RG_EXCLUDES[@]}" -g '.env*' -g '*.pem' -g '*.key' -g '*.p12' -g '*.sqlite' -g '*.db' -g '*.csv' --files
```

A gitignored file that only exists on this machine is a lower risk than a committed one. Check which ones are tracked with `git ls-files -- '.env*' '*/.env*'`. Inspect any of them with the safe procedures below.

## Reading sensitive files safely

Reading a schema, model, or type definition is safe because it holds field names and not values. Reading fixtures, `.env` files, notebooks, application code, or lines that matched a value pattern can print real values into the transcript. Use these forms instead.

| Need | Command |
| ---- | ------- |
| List the keys an `.env` file defines without their values | `sed -nE 's/^[[:space:]]*(export[[:space:]]+)?([A-Za-z_][A-Za-z0-9_]*)[[:space:]]*=.*/\2/p' .env` |
| See where a field name appears without printing the rest of the line | `rg -n -o -i -e '<field-name pattern>' <path>` |
| See lines that match a value pattern with the values masked | `rg -n -r '[REDACTED]' -e '<value pattern>' <path>` |
| Count matches per file | `rg -c -e '<pattern>' .` |
| Count output cells per notebook | `rg -c '"output_type"' -g '*.ipynb' .` |
| Find commits that ever added or removed a match | `git log --all --oneline -G '<POSIX pattern>'` |
| Find the history of a deleted or ignored file | `git log --all --oneline -- <path>` |

The `-r '[REDACTED]'` form only protects you when the pattern matches the value itself. With a field-name pattern it masks the name and prints the value, so use `-o` for field names.

The `git log` forms print commit IDs and subjects only. Do not add `-p` because a patch shows the values. A secret that appears only in git history is still exposed to anyone with a clone, so record it as a finding and recommend rotation.

When a sink search prints a line that contains a literal secret or personal value, rerun it with `-o` or with `-r '[REDACTED]'` and a value pattern before you quote it.

## Field-name patterns

Run each pattern with `-o` so that only the matched name prints, not the rest of the line:

```bash
RG_EXCLUDES=(...); rg -n -o -i "${RG_EXCLUDES[@]}" -e '<pattern>' .
```

Add `-c` first to get a count per file when the repo is large. When a hit is in a schema, model, or type definition, open the file to judge the context. Elsewhere, judge it from the file name and the matched name.

The patterns match `snake_case`, `kebab-case`, and most `camelCase` names because the search is case-insensitive. Short tokens that collide with ordinary words are guarded with `[^a-zA-Z]` so they match only when a non-letter sits on at least one side. That keeps `ssn` from matching `className` while still matching `customer_ssn` and `userSsn`. The shortest tokens need a non-letter on both sides, so the [camelCase search](#camelcase-search-for-short-tokens) covers them separately.

| Category | Pattern |
| -------- | ------- |
| Identity | `(first\|last\|full\|middle\|given\|family\|maiden\|legal)[_-]?name\|date[_-]?of[_-]?birth\|birth[_-]?date\|birthday\|(^\|[^a-zA-Z])dob\|dob([^a-zA-Z]\|$)\|gender` |
| Contact | `e[_-]?mail\|phone\|mobile[_-]?(number\|num)\|msisdn\|street\|address[_-]?line\|postal[_-]?code\|zip[_-]?code\|zipcode` |
| Government ID | `(^\|[^a-zA-Z])ssn\|ssn([^a-zA-Z]\|$)\|social[_-]?security\|national[_-]?id\|tax[_-]?id\|(^\|[^a-zA-Z])itin([^a-zA-Z]\|$)\|passport\|drivers?[_-]?licen[cs]e\|aadhaar\|(^\|[^a-zA-Z])nric\|nric([^a-zA-Z]\|$)` |
| Payment card | `card[_-]?(number\|num)\|card[_-]?no([^a-zA-Z]\|$)\|cc[_-]?(number\|num)\|credit[_-]?card\|cvv\|cvc\|card[_-]?holder\|exp(iry\|iration)?[_-]?(date\|month\|year)` |
| Financial | `iban\|routing[_-]?(number\|num)\|account[_-]?(number\|num)\|account[_-]?no([^a-zA-Z]\|$)\|sort[_-]?code\|salary\|income\|credit[_-]?score` |
| Health | `diagnos[ie]s\|icd[_-]?10\|medication\|prescription\|allerg(y\|ies)\|mrn\|medical[_-]?record\|patient\|insurance[_-]?(id\|number)\|member[_-]?id` |
| Special category | `(^\|[^a-zA-Z])race([^a-zA-Z]\|$)\|ethnicity\|religion\|sexual[_-]?orientation\|union[_-]?member\|biometric\|fingerprint\|face[_-]?(id\|embedding\|template)\|genetic` |
| Location and device | `latitude\|longitude\|(^\|[^a-zA-Z])(lat\|lng)([^a-zA-Z]\|$)\|geo[_-]?location\|ip[_-]?addr\|remote[_-]?addr\|x-forwarded-for\|device[_-]?id\|idfa\|gaid\|advertising[_-]?id\|imei` |
| Credentials and secrets | `password\|passwd\|secret\|api[_-]?key\|access[_-]?token\|refresh[_-]?token\|private[_-]?key\|security[_-]?(question\|answer)` |

The `\|` in the table is an escaped pipe for Markdown. Type a plain `|` in the shell.

### camelCase search for short tokens

The tokens `itin`, `race`, `lat`, and `lng` need a non-letter on both sides, so the table misses names like `userLat`. Catch those with a case-sensitive search:

```bash
RG_EXCLUDES=(...); rg -n -o "${RG_EXCLUDES[@]}" -e '[a-z](Itin|Race|Lat|Lng)([^a-z]|$)' .
```

### Form autocomplete values

HTML `autocomplete` tokens are a strong signal because they state what a field holds. This search also catches section and billing prefixes such as `billing cc-number` and the JSX form `autoComplete={"email"}`:

```bash
RG_EXCLUDES=(...); rg -n -o -i "${RG_EXCLUDES[@]}" -e "autocomplete=\{?[\"']([a-z0-9-]+ )*(cc-|bday|sex|tel|email|name|given-name|family-name|street-address|address-line|postal-code|one-time-code|current-password|new-password)" .
```

### Mobile permissions

```bash
RG_EXCLUDES=(...); rg -n -o "${RG_EXCLUDES[@]}" -e 'NS[A-Za-z]+UsageDescription' -e 'android\.permission\.(ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION|READ_CONTACTS|READ_SMS|READ_PHONE_STATE|BODY_SENSORS|CAMERA|RECORD_AUDIO)' .
```

## Value patterns

Value searches find real or realistic data in fixtures, notebooks, logs, and committed files. **Never print the matched values.** Use `-c` or `-l` to get only counts or file names, or use `-r '[REDACTED]'` to print the line with the match masked.

```bash
RG_EXCLUDES=(...); rg -n "${RG_EXCLUDES[@]}" -r '[REDACTED]' -e '<pattern>' .
```

| What | Pattern | Notes |
| ---- | ------- | ----- |
| Email address | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | Ignore `example.com`, `example.org`, and `test` domains |
| US SSN | `\b\d{3}-\d{2}-\d{4}\b` | Also matches some dates and IDs, so read the masked context |
| Card-like number | `\b(?:\d[ -]?){12,18}\d\b` | Filter with the Luhn check below |
| IBAN | `\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b` | Noisy in minified code |
| Phone in E.164 form | `\+[1-9]\d{7,14}\b` | Misses local formats |
| IPv4 address | `\b(?:\d{1,3}\.){3}\d{1,3}\b` | Ignore private ranges and version strings |
| AWS access key ID | `\b(AKIA\|ASIA)[0-9A-Z]{16}\b` | A High finding when present |
| Private key | `-----BEGIN [A-Z ]*PRIVATE KEY-----` | A High finding when present |
| JWT | `\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` | May hold personal claims as well as being a credential |
| Hardcoded secret | See the command below | The pattern contains both quote characters |
| Secret exposed to the client bundle | `(NEXT_PUBLIC_\|VITE_\|EXPO_PUBLIC_\|REACT_APP_\|NUXT_PUBLIC_\|PUBLIC_)[A-Z0-9_]*(KEY\|SECRET\|TOKEN\|PASSWORD)` | Variables with these prefixes are compiled into code that ships to every user, so any real secret here is a High finding. Publishable keys meant for the client are fine. |

The hardcoded-secret pattern contains a single quote, so it needs double quotes in the shell:

```bash
RG_EXCLUDES=(...); rg -n -i "${RG_EXCLUDES[@]}" -r '[REDACTED]' -e "(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]" .
```

Skip obvious placeholders such as `changeme` or `your-key-here`.

### POSIX forms for git and grep

These patterns use `\d`, `\b`, and `(?:`, which ripgrep understands. `git log -G` and `grep -E` do not, and they fail silently or with an error. Convert a pattern before you use it with either tool.

1. Replace `\d` with `[0-9]`.
2. Remove `\b`.
3. Replace `(?:` with `(`.

For example, the SSN pattern becomes `[0-9]{3}-[0-9]{2}-[0-9]{4}`. On a machine with GNU grep you can use `grep -rPn` with the original pattern instead.

Test card numbers published by payment providers (such as numbers starting with `4111 1111`) are expected in tests. Report them only if they appear outside test code.

### Luhn check without printing numbers

This pipeline prints only the file and line of each card-like number that passes the Luhn check:

```bash
RG_EXCLUDES=(...); rg -o -n --with-filename "${RG_EXCLUDES[@]}" '\b(?:\d[ -]?){12,18}\d\b' . | python3 -c '
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
