# Vault settings

When you create a vault or edit a vault's schema, there are various settings (represented as `tags` in the [Management API](/api/management)) that define field behaviors. Available settings follow.

## Accepted values

**Tag:** `skyflow.validation.predefinedvalues`

Values that an enum field should accept.

You can use this tag multiple times on a single field.

### Values

A string.

### Data types

* enum

## Allowed file types

**Tag:** `skyflow.options.allowed_file_types`

Restricts the types of files that can be uploaded to a file column based on actual file content, not just the file extension. This provides protection against spoofed or renamed files by validating the file's true MIME type during upload.

When configured, the system validates uploaded files by:

1. Detecting the actual file type from the file's binary signature (MIME sniffing)
2. Comparing the detected type against the allowed list
3. Verifying that the file extension matches the actual content type

If a file doesn't match the allowed types or the extension doesn't match the actual file type, the upload is rejected.

<Note>
  You can only configure allowed file types on empty columns. Once a column
  contains data, you can't modify this setting.
</Note>

### Values \[#allowed-file-types-values]

A subset of MIME type strings following the [IANA Media Types](https://www.iana.org/assignments/media-types/media-types.xhtml) standard format (`type/subtype`). Supported MIME types:

{/*Based on https://github.com/gabriel-vasile/mimetype/blob/master/supported_mimes.md, but only documenting MIME types we've actively tested.*/}

| File type                 | Value                                                                       |
| ------------------------- | --------------------------------------------------------------------------- |
| Gzip compressed files     | `application/gzip`                                                          |
| JSON files                | `application/json`                                                          |
| PDF documents             | `application/pdf`                                                           |
| Windows executable files  | `application/vnd.microsoft.portable-executable`                             |
| PowerPoint PPTX files     | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| PowerPoint PPT files      | `application/vnd.ms-powerpoint`                                             |
| Excel XLSX files          | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`         |
| Excel XLS files           | `application/vnd.ms-excel`                                                  |
| Word DOCX files           | `application/vnd.openxmlformats-officedocument.wordprocessingml.document`   |
| Word DOC files            | `application/msword`                                                        |
| SQLite database files     | `application/vnd.sqlite3`                                                   |
| Java applet files         | `application/x-java-applet`                                                 |
| ZIP archive files         | `application/zip`                                                           |
| FLAC audio files          | `audio/flac`                                                                |
| MP3 audio files           | `audio/mpeg`                                                                |
| WAV audio files           | `audio/wav`                                                                 |
| GIF image files           | `image/gif`                                                                 |
| TIFF image files          | `image/tiff`                                                                |
| HEIC image files          | `image/heic`                                                                |
| JPEG image files          | `image/jpeg`, \`image/jpg                                                   |
| PNG image files           | `image/png`                                                                 |
| WebP image files          | `image/webp`                                                                |
| HTML files                | `text/html`                                                                 |
| Plain text files          | `text/plain`                                                                |
| MP4 video files           | `video/mp4`                                                                 |
| QuickTime MOV video files | `video/quicktime`                                                           |

### Data types \[#allowed-file-types-data-types]

* file

### Example

```json
{
  "name": "document",
  "datatype": "DT_FILE",
  "tags": [
    {
      "name": "skyflow.options.allowed_file_types",
      "values": ["application/pdf", "image/png", "image/jpeg"]
    }
  ]
}
```

## Column group

**Tag:** `skyflow.options.column_group`

A column-level option to specify the [column group](/docs/tokenization/column-groups) that the column belongs to. If not specified, each column belongs to its own column group with the schema `$tableName.$columnName`. For example, the `state` column in a `persons` table has a default column group of `persons.state`.

All columns in a column group need to have the same values for the following options:

* [Default token policy](#default-token-policy)
* [Find pattern](#find-pattern)
* [Format-preserving regular expression](#format-preserving-regular-expression)
* [Redaction](#redaction)
* [Regular expression validation](#regular-expression-validation)
* [Replace pattern](#replace-pattern)

### Values \[#values]

A string.

## Configuration tags

**Tag:** `skyflow.options.configuration_tags`

Tags for properties of a field.

You can use this tag multiple times on a single field.

### Values \[#values1]

| Value         | Data types                                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `INDEX`       | <ul> <li> date </li> <li> datetime </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `FOREIGN_KEY` | <ul> <li> string </li> </ul>                                                                                                         |
| `META_DATA`   | <ul> <li> bool </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> </ul>                     |
| `NOT_NULL`    | <ul> <li> bool </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> </ul>                     |
| `NULLABLE`    | <ul> <li> bool </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> </ul>                     |
| `PRIMARY_KEY` | <ul> <li> string </li> </ul>                                                                                                         |
| `UNIQUE`      | <ul> <li> date </li> <li> datetime </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |

## Data type

**Tag:** `skyflow.options.data_type`

The type of data the field stores.

### Values \[#values2]

* `bool`
* `date`
* `datetime`
* `enum`
* `file`
* `float32`
* `int32`
* `json`
* `string`
* `time`

## Default token policy

**Tag:** `skyflow.options.default_token_policy`

The type of tokenization to use for the associated field.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values3]

| Value                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Data types                                                                                                                                                           |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DETERMINISTIC_FPT`                     | A persistent, format-preserving token for a given value. A [regular expression](/docs/vaults/vault-settings#format-preserving-regular-expression) can to structure the token format. If a regular expression isn't specified, the format is inferred based on the value. <br /><br /> For example, "\<[bwe09f@fg7d8.com](mailto:bwe09f@fg7d8.com)>" can be a token for "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>" in a given vault and for a given a regular expression.                                                                                                                           | <ul> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> string </li> <li> time </li> </ul>                                                     |
| `DETERMINISTIC_UUID`                    | A token that is a persistent UUID for a given value. All occurrences of this value generate the same token. <br /><br /> For example, "c7db3f3a-5d01-4a98-961e-9cbdb6241b0d" can be a token for "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>" in a given vault.                                                                                                                                                                                                                                                                                                                                       | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `FORMAT_PRESERVING_TOKEN`               | A token that follows the default [regular expression](/docs/vaults/vault-settings#format-preserving-regular-expression) specified for the field. <br /><br /> For example, "bwe09f\@fg7d8.tu8" can be a token for "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>".                                                                                                                                                                                                                                                                                                                                      | <ul> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> string </li> <li> time </li> </ul>                                                     |
| `NON_DETERMINISTIC_FPT`                 | A format-preserving token for a given \`value. All occurrences of a given value generate different tokens. A [regular expression](/docs/vaults/vault-settings#format-preserving-regular-expression) can structure the token format. If a regular expression isn't specified, the format is inferred based on the value. <br /><br /> For example, "\<[bwe09f@fg7d8.com](mailto:bwe09f@fg7d8.com)>" and "\<[nv63kl@s8021h.com](mailto:nv63kl@s8021h.com)>" can be tokens for different instances of "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>" in a given vault and for a given regular expression. | <ul> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> string </li> <li> time </li> </ul>                                                     |
| `NON_DETERMINISTIC_TRANSIENT_UUID`      | A non-deterministic UUID token that expires after the specified [time-to-live (TTL)](#time-to-live) elapses. <br /><br /> Transient field values are available through [Detokenize](/api/data/tokens/detokenize) until the field's TTL elapses, even if the record containing the value was deleted. Transient field values aren't available through the [Get Record](/api/data/records/get-record-by-id).                                                                                                                                                                                                 | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `NON_DETERMINISTIC_UUID`                | A token that is a random UUID. All occurrences of a given value generate different tokens. <br /><br /> For example, "c7db3f3a-5d01-4a98-961e-9cbdb6241b0d" and "2df82555-3a48-48ad-ac4b-2b89a1a99c0e" can be tokens for different instances of "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>".                                                                                                                                                                                                                                                                                                        | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `RANDOM_TOKEN`                          | A token that isn't derived from original data. <br /><br /> For example, "bwe09ffg7d8tu8pd" can be a token for "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>".                                                                                                                                                                                                                                                                                                                                                                                                                                         | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `DETERMINISTIC_PRESERVE_LEFT_6_RIGHT_4` | A persistent token for a given value that preserves the left-6 and right-4 digits of a credit card number. Only works with columns formatted as the Credit Card data type. All occurrences of this value generate the same token. <br /><br /> For example, "7234565843691234" can be a token for "7234567899871234" in a given vault. <br /><br /> **Note:** This token policy limits the token space to 1 million possible combinations, which may negatively impact performance of token generation. To learn more, contact Skyflow.                                                                    | <ul> <li> Credit Card </li> </ul>                                                                                                                                    |
| `DETERMINISTIC_PRESERVE_EMAIL_DOMAIN`   | A persistent token for a given value that preserves the domain and the top level domain (TLD) of an email address. Only works with columns formatted as the Email data type. All occurrences of this value generate the same token. <br /><br /> For example, "\<[c7db3f3a5d014a98961@gmail.com](mailto:c7db3f3a5d014a98961@gmail.com)>" can be a token for "\<[johndoe@gmail.com](mailto:johndoe@gmail.com)>" in a given vault. **Note:** This token type is not generally available. Contact Skyflow support for more information.                                                                       | <ul> <li> Email </li> </ul>                                                                                                                                          |

## Description

**Tag:** `skyflow.options.description`

Information about the field.

### Values \[#values4]

A string.

### Data types \[#data-types1]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Encrypted operations

**Tag:** `skyflow.options.operation`

Operations enabled for encrypted data.

You can use this tag multiple times on a single field.

### Values \[#values5]

| Value         | Description                                                                                                                                    | Data types                                                                                                                                                           |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ALL_OP`      | **Warning:** Don't use for fields that contain sensitive data. <br /><br /> Enables all operations by not keeping data encrypted at all times. | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `AGGREGATION` | Enables queries like `SELECT AVERAGE(age) FROM users`.                                                                                         | <ul> <li> int32 </li> </ul>                                                                                                                                          |
| `EXACT_MATCH` | Enables queries like `SELECT * FROM users WHERE email = \"johndoe@mail.com\"`.                                                                 | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `ORDER`       | Enables queries like `SELECT * FROM users WHERE age > 40`.                                                                                     | <ul> <li> date </li> <li> datetime </li> <li> int32 </li> <li> time </li> </ul>                                                                                      |

## Find pattern

**Tag:** `skyflow.options.find_pattern`

The regular expression to find values to [mask](/docs/vaults/vault-settings#redaction) in a field.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values6]

A regular expression.

### Data types \[#data-types2]

* date
* datetime
* enum
* string
* time

## Format-preserving regular expression

**Tag:** `skyflow.options.format_preserving_regex`

The regular expression used when generating [tokens](/docs/vaults/vault-settings#default-token-policy). If not specified,
tokens formats are based on the input structure and length.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values7]

A regular expression.

### Data types \[#data-types3]

* date
* datetime
* enum
* string
* time

## Identifiability

**Tag:** `skyflow.options.identifiability`

A tag for how personally identifiable the field's data is.

You can use this tag multiple times on a single field.

### Values \[#values8]

| Value                      | Description                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `HIGH_IDENTIFIABILITY`     | Data that can uniquely identify the person, such as name, address, or email.                                             |
| `MODERATE_IDENTIFIABILITY` | Data that can identify a person relatively easily when combined with other data but cannot uniquely identify the person. |
| `LOW_IDENTIFIABILITY`      | Data that can't easily identify a person.                                                                                |
| `UNKNOWN_IDENTIFIABILITY`  | Data that has an unknown level of identifiability.                                                                       |

### Data types \[#data-types4]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Index

**Tag:** `skyflow.options.index`

Specifies whether or not the field is indexed.

### Values \[#values9]

* `true`
* `false`

### Data types \[#data-types5]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Not null

**Tag:** `skyflow.options.not_null`

Specifies whether or not the field is nullable.

### Values \[#values10]

* `true`
* `false`

### Data types \[#data-types6]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Personal information type

**Tag:** `skyflow.options.personal_information_type`

A tag for the type of personal information in the field.

You can use this tag multiple times on a single field.

### Values \[#values11]

| Value | Description                                                                                                                                                                                                       |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NPI` | Nonpublic personal information (NPI) is personally identifiable financial information provided by a consumer to a financial institution, resulting from any transaction with the consumer.                        |
| `PCI` | Payment Card Industry Data Security Standard (PCI DSS) is a set of requirements intended to ensure that all companies that process, store, or transmit credit card information maintain a secure environment.     |
| `PHI` | Protected health information (PHI) is the term given to health data created, received, stored, or transmitted by HIPAA-covered entities and their business associates.                                            |
| `PII` | Personally Identifiable Information (PII) can be used to distinguish or trace an individual's identity, either alone or when combined with other information that is linked or linkable to a specific individual. |

### Data types \[#data-types7]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Privacy law

**Tag:** `skyflow.options.privacy_law`

A tag for privacy laws that are applicable to the field.

You can use this tag multiple times on a single field.

### Values \[#values12]

| Value                 | Description                                                                                                                                                                                                                                                                                 |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CCPA`                | The California Consumer Privacy Act (CCPA) is a state statute intended to enhance privacy rights and consumer protection for residents of California, United States.                                                                                                                        |
| `COPPA`               | The Children's Online Privacy Protection Act of 1998 (COPPA) is a federal law that imposes specific requirements on operators of websites and online services to protect the privacy of children under 13.                                                                                  |
| `GDPR`                | The General Data Protection Regulation (GDPR) is a regulation in EU law on data protection and privacy in the European Union and the European Economic Area.                                                                                                                                |
| `GLBA`                | The Gramm-Leach-Bliley Act (GLBA) requires financial institutions—companies that offer consumers financial products or services like loans, financial or investment advice, or insurance—to explain their information-sharing practices to their customers and to safeguard sensitive data. |
| `HIPAA`               | The Health Insurance Portability and Accountability Act of 1996 (HIPAA) is a federal law that required the creation of national standards to protect sensitive patient health information from being disclosed without the patient's consent or knowledge.                                  |
| `US_PRIVACY_ACTIVITY` | General United States-based privacy activity.                                                                                                                                                                                                                                               |
| `UNKNOWN_PRIVACY_LAW` |                                                                                                                                                                                                                                                                                             |

### Data types \[#data-types8]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Redaction

**Tag:** `skyflow.options.default_dlp_policy`

The redaction strategy for displaying the field's data.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values13]

| Value        | Description                                                                                                                                                                                                                                                                                                                                | Data types                                                                                                                                                           |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PLAIN_TEXT` | Data isn't redacted and appears in plain text. Only use this setting on non-sensitive fields. <br /><br /> For example, "\<[johndoe@acme.com](mailto:johndoe@acme.com)>" appears as "\<[johndoe@acme.com](mailto:johndoe@acme.com)>".                                                                                                      | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> file </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul> |
| `REDACT`     | Data is completely redacted. <br /><br /> For example, "\<[johndoe@acme.com](mailto:johndoe@acme.com)>" appears as "REDACTED".                                                                                                                                                                                                             | <ul> <li> bool </li> <li> date </li> <li> datetime </li> <li> enum </li> <li> float32 </li> <li> int32 </li> <li> string </li> <li> time </li> </ul>                 |
| `MASK`       | Data is partially redacted based on the associated [Find pattern](/docs/vaults/vault-settings#find-pattern) and [Replace pattern](/docs/vaults/vault-settings#replace-pattern). <br /><br /> For example, "\<[johndoe@acme.com](mailto:johndoe@acme.com)>" might appear "\*\*\*@acme.com" given the appropriate Find and Replace patterns. | <ul> <li> date </li> <li> datetime </li> <li> enum </li> <li> string </li> <li> time </li> </ul>                                                                     |

## Regular expression validation

**Tag:** `skyflow.validation.regular_exp`

Regular expressions that determine if input values are valid and accepted for the field.

You can use this tag multiple times on a single field.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values14]

A regular expression.

## Replace pattern

**Tag:** `skyflow.options.replace_pattern`

The regular expression to replace found values in a [masked](/docs/vaults/vault-settings#redaction) field.

<Note>
  All fields in a [column group](#column-group) need to have the same value for
  this setting.
</Note>

### Values \[#values15]

A regular expression.

### Data types \[#data-types9]

* date
* datetime
* enum
* string
* time

## Sensitivity

**Tag:** `skyflow.options.sensitivity`

A tag for the sensitivity level of a field's data. The greater the harm caused by the data being compromised or disclosed, the higher its sensitivity.

You can use this tag multiple times on a single field.

### Values \[#values16]

* `HIGH`
* `MEDIUM`
* `LOW`

### Data types \[#data-types10]

* bool
* date
* datetime
* enum
* file
* float32
* int32
* string
* time

## Time to live (TTL) \[#time-to-live]

**Tag:** `skyflow.options.ttl`

The amount of time (in minutes) to elapse before a [transient](/docs/vaults/vault-settings#default-token-policy) field's value expires.

Min: `1` minute. Max: `20160` minutes or 14 days. Default: `60` minutes.

### Values \[#values17]

An integer.

## Unique

**Tag:** `skyflow.options.unique`

Specifies whether or not values in the field must be unique and non-repeating.

### Values \[#values18]

* `true`
* `false`

### Data types \[#data-types11]

* date
* datetime
* float32
* int32
* string
* time
