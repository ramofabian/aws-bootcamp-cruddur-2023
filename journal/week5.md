# Week 5 — DynamoDB and Serverless Caching
## Mandatory tasks
### Watched Week 5 - Data Modelling (Live Stream)
:white_check_mark: DONE.
### Watched Ashish's Week 5 - DynamoDB Considerations
:white_check_mark: DONE.
### Implement Schema Load Script
:white_check_mark: DONE. I didn't have any issue to follow Andre's instructions.

To implement the schema load script, it is requiered the following steps:
1. Switch on the containers and make sure dynamoDB  container is working.
2. Create `schema-load` python script.

```python
#!/usr/bin/env python3

import boto3
import sys

attrs = {
    'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
    if "prod" in sys.argv[1]:
        attrs = {}

ddb = boto3.client('dynamodb', **attrs)

table_name = 'cruddur-messages'

# Creating table
response = ddb.create_table(
    TableName=table_name,
    AttributeDefinitions=[
        {
            'AttributeName': 'pk',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'sk',
            'AttributeType': 'S'
        },
    ],
    KeySchema=[
        {
            'AttributeName': 'pk',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'sk',
            'KeyType': 'RANGE'
        },
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    },
)
print(response)
```

3. Create `list-tables` script to see if the table has been cretaed.

```bash
#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="list-tables"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

#Check if the conection URL is prod or dev
if [ "$1" = "prod" ]; then
    ENDPOINT_URL=""
else
    ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

#get the list of tables via AWS command
aws dynamodb list-tables $ENDPOINT_URL \
--query TableNames \
--output table
```

4. Create `drop` script to make the table removal.

```bash
#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="Drop"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

# ./db/ddb/drop cruddur-messages prod

#Check if the conection URL is prod or dev
if [ -z "$1" ]; then
    echo "No TABLE_NAME argument supplied eg ./db/ddb/drop cruddur-messages prod"
    exit 1
fi

TABLE_NAME=$1

if [ "$2" = "prod" ]; then
    ENDPOINT_URL=""
else
    ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

echo "Deleting table: $TABLE_NAME"

#get the list of tables via AWS command
aws dynamodb delete-table $ENDPOINT_URL \
--table-name $TABLE_NAME
```

<p align="center"><img src="assets/week5/dynamodb_loading_schema.png" alt="accessibility text"></p>

### Implement Seed Script
### Implement Scan Script
### Implement Pattern Scripts for Read and List Conversations
### Implement Update Cognito ID Script for Postgres Database
### Implement (Pattern A) Listing Messages in Message Group into Application
### Implement (Pattern B) Listing Messages Group into Application
### Implement (Pattern C) Listing Messages Group into Application
### Implement (Pattern D) Listing Messages Group into Application
### Implement (Pattern E) Listing Messages Group into Application