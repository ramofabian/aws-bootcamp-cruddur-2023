# Week 5 — DynamoDB and Serverless Caching
## Mandatory tasks
### Watched Week 5 - Data Modelling (Live Stream)
:white_check_mark: DONE.

DynamoDB Model :point_right: [link to file](https://lucid.app/lucidchart/8f58a19d-3821-4529-920f-5bb802d6c6a3/edit?invitationId=inv_e47bc316-9caa-4aee-940f-161e01e22715&page=0_0#)

DynamoDB Data Model :point_right: [link to file](https://docs.google.com/spreadsheets/d/1LrTC_y2X_YBEthFNlnwbo8TgxGlpHV3TCpM6XeVyiGg/edit#gid=0)
### Watched Ashish's Week 5 - DynamoDB Considerations
:white_check_mark: DONE.
### Implement Schema Load Script
:white_check_mark: DONE. I didn't have any issue to follow Andre's instructions.

To implement the schema load script, it is requiered the following steps:
1. Add `boto3` lib into `requirements.txt` within `backend-flask` folder. Then run the command `pip install -r requirements.txt`.
2. Switch on the containers and make sure dynamoDB  container is working.
2. Create `schema-load` python script and place it in `backend-flask/bin/ddb/`. This script will connect to local or remote DynamoDB database, then it will create a table called `cruddur-messages`.

```python
#!/usr/bin/env python3

import boto3
import sys

attrs = {
    'endpoint_url': 'http://localhost:8000'
}

# Checking if the prod word was entered as a arg
if len(sys.argv) == 2:
    if "prod" in sys.argv[1]:
        attrs = {}

# Start conection to dynamoDB
ddb = boto3.client('dynamodb', **attrs)

table_name = 'cruddur-messages'

# Creating table the 'cruddur-messages'
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

3. Create `list-tables` bash script to see if the table has been cretaed, it should be placed it in side of `backend-flask/bin/ddb/`.

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

4. Create `drop` bash script to make the table removal and place it in side of `backend-flask/bin/ddb/`.

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

5. Execution logs:
5.1. Executing `schema-load`:

<p align="center"><img src="assets/week5/dynamodb_loading_schema.png" alt="accessibility text"></p>

5.2. Executing `list-tables`:

<p align="center"><img src="assets/week5/dynamodb_show_tables.png" alt="accessibility text"></p>

5.3. Executing `drop`:

<p align="center"><img src="assets/week5/dynamodb_dropping_table.png" alt="accessibility text"></p>

<b>Link to files:</b>
- [schema-load](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/schema-load)
- [list-tables](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/list-tables)
- [drop](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/drop)

### Implement Seed Script
:white_check_mark: DONE. I didn't have any issue to follow Andre's instructions.

To implement the Seed script, we have to create `seed` python script and place it in `backend-flask/bin/ddb/`. This script has hardcoded a conversation which is parsed which it saves into local DynamoDB table by using the the `patterm C` (new conversation). 

<p align="center"><img src="assets/week5/db_model.png" alt="accessibility text"></p>

To carry on this work the script performs the following instructions:
1. Extract `handles` from postgres DB.
2. Create Message groups in `cruddur-messages` table by using the `pattern C` from DB model.
3. Prase the conversations.
4. Create the Mesasses and associate it to Message group in `cruddur-messages`.

Link to file: [seed](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/seed)

Execution log:

<p align="center"><img src="assets/week5/dynamodb_seed_table.png" alt="accessibility text"></p>

### Implement Scan Script
:white_check_mark: DONE. I didn't have any issue to follow Andre's instructions.

To implement the Scan script, we have to create `seed` python script and place it in `backend-flask/bin/ddb/`. This script connects to dynamoDB and gather all information from `cruddur-messages` table.

```python
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}
# unset endpoint url for use with production database
if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}
dynamodb = boto3.resource('dynamodb',**attrs)
table_name = 'cruddur-messages'

#Run the scan
table = dynamodb.Table(table_name)
response = table.scan()

# Print the scan
print("="*20)
print(response)
print("="*20)
items = response['Items']
for item in items:
    print(item)
```

Link to file: [scan](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/scan)

Execution log:

<p align="center"><img src="assets/week5/dynamodb_scan_table.png" alt="accessibility text"></p>

### Implement Pattern Scripts for Read and List Conversations
:white_check_mark: DONE. This part was hard to follow up, because I got lost in many parts of it. Although, I could make it :)

#### Implementing get-conversation script
To implement the Scan script, we have to create `get-conversation` python script and place it in `backend-flask/bin/ddb/patterns`. This script connects to dynamoDB, makes a query to get the info of some determinated message group ID within a determinated period of time and parses this information.

```python
#!/usr/bin/env python3

import boto3
import sys
import json
import datetime

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb',**attrs)
table_name = 'cruddur-messages'

message_group_uuid = "5ae290ed-55d1-47a0-bc6d-fe2bc2700399"

# define the query parameters
query_params = {
  'TableName': table_name,
#   'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',              # filter paramater
  'KeyConditionExpression': 'pk = :pk AND sk between :start_date AND :end_date', # filter paramater
  'ScanIndexForward': False,                                                     # send in desending direction
  'Limit': 20,                                                                   # Limt of items to be returned
  'ExpressionAttributeValues': {
    ':pk': {'S': f"MSG#{message_group_uuid}"},                                   # partition key == MSG#{message_group_uuid}
    ':start_date': {'S': "2023-03-01T00:00:00.000000+00:00"},
    ':end_date': {'S': "2023-03-30T23:38:15.735541+00:00"},
    # ':year': {'S': '2023'}
  },
  'ReturnConsumedCapacity': 'TOTAL'
}

# query the table
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))

# print the consumed capacity
print(json.dumps(response['ConsumedCapacity'], sort_keys=True, indent=2))

items = response['Items']
reversed_array = items[::-1]              # showing the messages in ascending order

for item in reversed_array:
  sender_handle = item['user_handle']['S']
  message       = item['message']['S']
  timestamp     = item['sk']['S']
  dt_object = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
  formatted_datetime = dt_object.strftime('%Y-%m-%d %I:%M %p')
  print(f'{sender_handle: <16}{formatted_datetime: <22}{message[:40]}...')
```

Link to file: [get-converstations](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/patterns/get-converstations)

Execution log:

<p align="center"><img src="assets/week5/dynamodb_get_conversation.png" alt="accessibility text" width="500"></p>

<p align="center"><img src="assets/week5/dynamodb_get_conversation2.png" alt="accessibility text" width="500"></p>

#### Implementing list-conversation script
To implement the Scan script, we have to create `list-conversation` python script and place it in `backend-flask/bin/ddb/patterns`. This script connects to dynamoDB, makes a query to get the info of some determinated group message ID within and consumed capacity.

```python
#!/usr/bin/env python3

import boto3
import sys
import json
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from lib.db import db

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb',**attrs)
table_name = 'cruddur-messages'

def get_my_user_uuid():
    #Query to get the user UUID from local postgres DB
    sql = """
    SELECT 
        users.uuid
    FROM users
    WHERE
        users.handle = %(handle)s
    """
    uuid = db.query_array_json(sql,{
    'handle':  'andrewbrown'
    })
    return uuid[0]['uuid']

my_user_uuid = get_my_user_uuid()
print(f"my-uuid: {my_user_uuid}\n")

# define the query parameters
query_params = {
  'TableName': table_name,
  'KeyConditionExpression': 'pk = :pk',
  'ExpressionAttributeValues': {
    ':pk': {'S': f"GRP#{my_user_uuid}"}
  },
  'ReturnConsumedCapacity': 'TOTAL' # to see the spending
}

# query the table
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))
```

Link to file: [list-converstations](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/ddb/patterns/list-converstations)

Execution log:

<p align="center"><img src="assets/week5/dynamodb_list_conversation.png" alt="accessibility text" width="500"></p>

<p align="center"><img src="assets/week5/dynamodb_list_conversation2.png" alt="accessibility text" width="500"></p>

### Implement Update Cognito ID Script for Postgres Database
:white_check_mark: DONE.
To implement the update cognito ID script for postgres DB,  the following files were added or modified:
- This is a new scritp that lists Cognito user pools: `backend-flask/bin/cognito/list-users`. It can be used to check Congnito user information. :point_right: [Link to File](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/cognito/list-users)
- The file `backend-flask/db/seed.sql` was modified to add current Cognito's users (picture below). :point_right: [link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/seed.sql)

<p align="center"><img src="assets/week5/update_seed_sql.png" alt="accessibility text" width="500"></p>

- This is new script that gathers the user's UUID from Cognito and set this information in pogress DB: `backend-flask/bin/db/update_cognito_user_id` :point_right: [link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db/update_cognito_user_id)
- This script `backend-flask/bin/db/setup` was adapted to add the script `update_cognito_user_id` in the execution list. :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/bin/db/setup)

<b>Execution:</b>
- `list-users`: In the picture below the handle and UUID is being displayed after the script execution:

<p align="center"><img src="assets/week5/update_cognito_id.png" alt="accessibility text" width="500"></p>

- `update_cognito_user_id`:

Before the script execution:

<p align="center"><img src="assets/week5/users_list_pre.png" alt="accessibility text" width="500"></p>

Once the script is executed:

<p align="center"><img src="assets/week5/update_db_execution.png" alt="accessibility text" width="500"></p>

After execution:

<p align="center"><img src="assets/week5/update_db_post_execution.png" alt="accessibility text" width="500"></p>

### Implement (Pattern A) Listing Messages in Message Group into Application
:white_check_mark: DONE.
The pattern A describes the needed paramteres to list messages within message group as it is shown in the picture below:

<p align="center"><img src="assets/week5/patter_a.png" alt="accessibility text" width="500"></p>

To implment the pattern A, the following changes were done in backend and frontend side:
- From backend side:
    - Make sure that local DynamoDB and Postgres are running with the `schema` and `seed` informationation already loaded
    -  `ddb.py` was adapted to list conversations from old to new and add mor conditions to return messages which were created this year. Also the function `list_message_groups` was adedd to extract and return the list of messages.
    -  `app.py` was adapted to receive the http request with user uuid and route it to `messages.py` service.
    -   `message_groups.py` and `messages.py` service was adapted to return the list of messages with: display name, created at and message information.
- From fronted side:
    - `frontend-react-js/src/App.js` the endpoint MessageGroupPage was modifed from `handle` to accept `message_group_uuid`
    - `MessageGroupItem.js`, `MessageGroupPage.js` were modifed to accept `message_group_uuid` and make the request.

Execution log:

<p align="center"><img src="assets/week5/list_conversation.png" alt="accessibility text" ></p>

<b>Link to files:</b>
- [ddb.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/lib/ddb.py)
- [app.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
- [messages.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/messages.py)
- [message_groups.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/message_groups.py)
- [App.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/App.js)
- [MessageGroupItem.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/components/MessageGroupItem.js)
- [MessageGroupPage.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/pages/MessageGroupPage.js)

### Implement (Pattern B) Listing Messages Group into Application
:white_check_mark: DONE.
The pattern B describes the required input and output paramaeters required to display the message groups from message tab.

<p align="center"><img src="assets/week5/patter_b.png" alt="accessibility text"></p>

To implment the pattern B, the following changes were done in backend and frontend side:
- From backend side:
    - Make sure that local DynamoDB and Postgres are running with the `schema` and `seed` informationation already loaded.
    - Save in gitpod and `docker-compose.yml` the local environment variable `AWS_ENDPOINT_URL` where Dynamo.
    -  `ddb.py` lib was created in `backend-flask/lib` directory with functions: `client` and `list_message_groups` which supports the connection with `boto3` to local `DynamoDB`.
    -  `app.py` was adapted to validate the autentication sent by frontend to backend and extract `cognito user id` and route it to`message_groups.py` service.
    -   `uuid_from_cognito_user_id.sql` this file was created to be used to extract `cognito user id` from postgres DB.
    -   `message_groups.py` service was adapted to return the list of messages groups with: display name, created at and message information.
- From fronted side:
    - `HomeFeedPage.js`, `MessageGroupsPage.js`, `MessageGroupPage.js`, `MessageForm.js` were adapted to make the `GET` request with the `access token` and display the information received from backend side.

Execution log:

<p align="center"><img src="assets/week5/group_message_list.png" alt="accessibility text" width="500"></p>

<b>Link to files:</b>
- [ddb.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/lib/ddb.py)
- [app.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
- [messages.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/messages.py)
- [message_groups.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/message_groups.py)
- [docker-compose.yml](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml)
- [MessageGroupItem.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/components/MessageGroupItem.js)
- [MessageGroupPage.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/pages/MessageGroupPage.js)
- [HomeFeedPage.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/pages/HomeFeedPage.js)
- [MessageGroupsPage.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/pages/MessageGroupsPage.js)

### Implement (Pattern C) Listing Messages Group into Application
:white_check_mark: DONE.

Pattern C is created to describe the needed paramaters to create new message groups.

<p align="center"><img src="assets/week5/patter_c.png" alt="accessibility text" width="500"></p>

Execution log:

<p align="center"><img src="assets/week5/new_chat.png" alt="accessibility text" width="500"></p>

### Implement (Pattern D) Listing Messages Group into Application
:white_check_mark: DONE.

Pattern D is created to describe the needed paramaters to create new message within message group.

<p align="center"><img src="assets/week5/patter_d.png" alt="accessibility text" width="500"></p>

To implment the pattern D, the following changes were done in backend and frontend side:
- From backend side:
    - Make sure that local DynamoDB and Postgres are running with the `schema` and `seed` informationation already loaded.
    - Save in gitpod and `docker-compose.yml` the local environment variable `AWS_ENDPOINT_URL` where Dynamo.
    -  `ddb.py` lib was adapted with function`create_message` which supports the connection with `boto3` to local `DynamoDB` to sabe the messages there.
    -  `app.py` was adapted to validate the autentication sent by frontend to backend and extract `cognito user id` and route it to`create_message.py` service.
    -   `create_message_users.sql` this file was created to be used to save messages from frontend into local DynamoDB.
    -   `create_message.py` service was adapted to save the message within local no-estructured DB (DynamoDB).
- From fronted side:
    - `MessageForm.js` were adapted to pass the message with `user_uuid`, `message_group_uuid`, `message` to backend side, once there it should be added into DynamoDB

Execution log:

<p align="center"><img src="assets/week5/add_message.png" alt="accessibility text" width="500"></p>

<b>Link to files:</b>
- [ddb.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/lib/ddb.py)
- [app.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
- [create_message.py](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/create_message.py)
- [create_message_users.sql](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/db/sql/users/create_message_users.sql)
- [MessageGroupItem.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/components/MessageGroupItem.js)
- [MessageForm.js](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/frontend-react-js/src/components/MessageForm.js)


### Implement (Pattern E) Listing Messages Group into Application
