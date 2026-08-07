# Unique columns and upsert

The Skyflow Data Privacy Vault lets you specify columns as `unique` in the schema and then use values in that column to identify existing records. Every value you insert must be unique within the column once you enable uniqueness for a column. When you want to capture data in the vault, you can make a request to the Skyflow API and include an `upsert` value. Upsert uses the unique column value to verify if a record already exists. If the record doesn't exist, upsert inserts a new record. If the record does exist, upsert updates the record with new values.

## Columns with a unique constraint

The uniqueness of columns enhances your vault schema by eliminating the chance of duplicating data. For instance, consider a table that stores employee data. Each record has a name, date of birth, and phone number, but those values aren't unique, as there can be multiple records with the same name or date of birth.

<Frame caption="Figure 1: Employee data table">
  \| FirstName | LastName | DateOfBirth | PhoneNumber | | --- | --- | --- | --- |
  \| Ashley | Rogers | 1/21/2001 | 123-456-7890 | | Travis | Rogers | 5/5/2001 |
  456-789-0123 | | Michelle | Wilson | 1/21/2001 | 789-012-3456 |
</Frame>

By adding a new column, employeeID, you can enable a uniqueness constraint and enforce that values in this column are unique to each record.

<Frame caption="Figure 2: Employee data table with a uniqueness constraint">
  \| FirstName | LastName | DateOfBirth | PhoneNumber | EmployeeID | | --- | ---
  \| --- | --- | --- | | Ashley | Rogers | 1/21/2001 | 123-456-7890 | 2A1B | |
  Travis | Rogers | 5/5/2001 | 456-789-0123 | 3C4D | | Michelle | Wilson |
  1/21/2001 | 789-012-3456 | 5E6F |
</Frame>

If your request has a unique value that duplicates an existing value, the Insert Record API call fails, returns an error message, and doesn't insert the data. However, if you want to update the existing value, you can do so in one call using upsert. Similarly, if you want to retrieve a record with a unique value, you can use the unique value in your [Get Records by Unique](/api/data/records/get-records) call.

### Create a column with a uniqueness constraint

You can enable uniqueness on any number of columns in a table and specify one column and value to use in your API requests. With your input, your vault automatically updates, inserts, or rejects requests based on the uniqueness constraint of a column and the unique value you identified in your API call.

<Note>
  You can't add the unique constraint to columns with existing data. If you have
  an existing column that you want to make unique, you'll need to add a new
  column with the unique constraint and migrate your data to the new column.
</Note>

<Tabs>
  <Tab title="Studio" language="Studio">
    1. From your Studio dashboard, click **Create a vault**.
    2. Select the option for **Start from Scratch**.
    3. After your vault schema opens, press the tab **New Column**.
    4. Search for or select the **Skyflow Data Types** you want to capture.
    5. On the configuration screen, turn on **Unique** to enable the setting.

    <Frame caption="Figure 3: Create a new column with a unique constraint">
      <img src="https://files.buildwithfern.com/https://skyflow.docs.buildwithfern.com/2026-01-29T19:01:40.110Z/assets/images/columns-unique-setting.gif" alt="Enabling the Unique setting for a new column in Studio." />
    </Frame>
  </Tab>

  <Tab title="API" language="API">
    Set environment variables by updating the following command with your values and running it in a terminal:

    ```bash
    export ACCOUNT_ID=$ACCOUNT_ID
    export WORKSPACE_ID=$WORKSPACE_ID
    export MANAGEMENT_URL=$MANAGEMENT_URL
    export TOKEN=$TOKEN
    ```

    ```bash
    curl -s -X POST "$MANAGEMENT_URL/v1/vaults" \
     -H "Content-Type: application/json" \
     -H "X-SKYFLOW-ACCOUNT-ID: $ACCOUNT_ID" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
         "name": "Custom vault",
         "description": "A custom vault containing a column with a uniqueness constraint.",
         "vaultSchema": {
             "schemas": [

                 {
                    "ID": "b4fa1e03d9d34e5c9d66c70083432b47",
                    "name": "employee_data",
                    "parentSchemaProperties": null,
                    "fields": [
                        {
                            "name": "skyflow_id",
                            "datatype": "DT_STRING",
                            "isArray": false,
                            "tags": [
                                {
                                    "name": "skyflow.options.default_dlp_policy",
                                    "values": [
                                        "PLAIN_TEXT"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.operation",
                                    "values": [
                                        "ALL_OP"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.sensitivity",
                                    "values": [
                                        "LOW"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.data_type",
                                    "values": [
                                        "skyflow.SkyflowID"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.description",
                                    "values": [
                                        "Skyflow-defined Primary Key"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.display_name",
                                    "values": [
                                        "Skyflow ID"
                                    ]
                                }
                            ],
                            "properties": null,
                            "index": 0
                        },
                        {
                            "name": "employee_name",
                            "datatype": "DT_STRING",
                            "isArray": false,
                            "tags": [
                                {
                                    "name": "skyflow.options.default_dlp_policy",
                                    "values": [
                                        "REDACT"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.operation",
                                    "values": [
                                        "ALL_OP"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.default_token_policy",
                                    "values": [
                                        "DETERMINISTIC_UUID"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.description",
                                    "values": [
                                        "Name of employee"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.display_name",
                                    "values": [
                                        "employee_name"
                                    ]
                                }
                            ],
                            "properties": null,
                            "index": 0
                        },
                        {
                            "name": "ein",
                            "datatype": "DT_STRING",
                            "isArray": false,
                            "isUnique": true,
                            "tags": [
                                {
                                    "name": "skyflow.options.default_dlp_policy",
                                    "values": [
                                        "REDACT"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.operation",
                                    "values": [
                                        "ALL_OP"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.default_token_policy",
                                    "values": [
                                        "DETERMINISTIC_UUID"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.description",
                                    "values": [
                                        "Employee ID number"
                                    ]
                                },
                                {
                                    "name": "skyflow.options.display_name",
                                    "values": [
                                        "ein"
                                    ]
                                }

                            ],
                            "properties": null,
                            "index": 0
                        }
                    ],
                    "childrenSchemas": [],
                    "schemaTags": [],
                    "properties": null
                }
            ],
            "tags": []
        },
        "workspaceID": "'"$WORKSPACE_ID"'"
    }'
    ```
  </Tab>
</Tabs>

## Upsert

Upsert is a single-step operation that combines two common requests: update a record if it exists, or if it doesn't, insert a new record. When you make a request to insert a record, upsert accepts a column with a uniqueness constraint and a unique value in that column. If the value matches a record in your table, the upsert operation updates the existing record with the values you provided in the request body. If the value doesn't exist, upsert inserts the given values.

### Upsert records

You can make upsert calls via an API or an SDK.

<Tabs>
  <Tab title="API" language="API">
    Set environment variables by updating the following command with your values and running it in a terminal:

    ```bash
    export ACCOUNT_ID=$ACCOUNT_ID
    export TOKEN=$TOKEN
    export VAULT_URL=$VAULT_URL
    export VAULT_ID=$VAULT_ID
    export TABLE_NAME=$TABLE_NAME
    ```

    ```bash
    curl -s -X POST \
      "$VAULT_URL/v1/vaults/$VAULT_ID/$TABLE_NAME" \
      -H "Authorization: Bearer $TOKEN" \
      -H "content-type: application/json" \
      -d '{
        "records": [
            {
                "fields": {
                    "ein": "2A1B",
                    "employee_name": "Ashley Rogers",
                    "Department": "English"
                }
            }
        ],
        "tokenization": true,
        "upsert": "ein"
    }'
    ```

    Skyflow returns tokens for the record you just inserted.

    ```json
    {
      "records": [
        {
          "table": "employees",
          "fields": {
            "ein": "1989cb56-63a-4482-adf-1f74cd1a5",
            "employee_name": "f37186-e7e2-466f-91e5-48e2bcbc1"
          }
        }
      ]
    }
    ```
  </Tab>

  <Tab title="JavaScript SDK" language="JavaScript SDK">
    The [Node.JS SDK](https://github.com/skyflowapi/skyflow-node#insert) closely resembles the following JavaScript SDK example.

    ```js
    const records = {
      records: [
        {
          table: "string", // Table name for record insertion.
          fields: {
            column1: "value", // Column names should match vault column names.
            //...additional fields here.
          },
        },
        // ...additional records here.
      ],
    };

    const options = {
      tokens: true, // Indicates whether to return tokens for the inserted data. Defaults to 'true.'
      upsert: [
        // Upsert operations support in the vault.
        {
          table: "string", // Table name.
          column: "value", // Unique column in the table.
        },
      ],
    };

    skyflowClient.insert(records, options);
    ```
  </Tab>
</Tabs>

## Next steps

Unique columns and upsert requests are powerful features that help to eliminate the risk of duplicating records and let you perform inserts or updates in one call. Continue exploring [data privacy vaults](/docs/vaults/create-a-vault#create-a-vault), or learn more about integrating this solution with [client-side SDKs](/docs/sdks/handling-data-client-side).
