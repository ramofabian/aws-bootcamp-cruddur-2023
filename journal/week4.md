# Week 4 — Postgres and RDS
## Mandatory tasks
### Watched Ashish's Week 4 - Security Considerations
:white_check_mark: DONE and the quiz as well.
### Create RDS Postgres Instance
:white_check_mark: DONE. I didn't have any issue to follow Andrew's instructions.

To create the DB via AWS CLI the following command was used:

```bash
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot \
  --master-user-password xxxxxxx \
  --allocated-storage 20 \
  --availability-zone eu-central-x \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

With the CLI command `aws rds describe-db-instances` can be seen the recently created instance:

<p align="center"><img src="assets/week4/db_instance_info.png" alt="accessibility text"></p>

Created DB from AWS we console:

<p align="center"><img src="assets/week4/db_created.png" alt="accessibility text"></p>

We leave the instance temporally stop to avoid any possible charge while it is not in use:

<p align="center"><img src="assets/week4/db_stoped.png" alt="accessibility text"></p>

### Bash scripting for common database actions
:white_check_mark: DONE. I didn't have any issue to follow Andrew's instructions.

The following scripts were created to help the tool and developer during DB creation:

<b>Note:</b> In this phase the the postgres DB must be running to make the proper tests.

1. Add environment variables to connect to DBs via URL string:

```bash
# For RDS
export PROD_CONNECTION_URL=postgresql://cruddurroot:<<password>>@cruddur-db-instance.XXXXX.eu-XXXX.rds.amazonaws.com:5432/cruddur
gp env PROD_CONNECTION_URL=postgresql://cruddurroot:<<password>>@cruddur-db-instance.XXXXX.eu-XXXX.rds.amazonaws.com:5432/cruddur

# For local db
export CONNECTION_URL=postgresql://postgres:password@localhost:5432/cruddur
gp env CONNECTION_URL=postgresql://postgres:password@localhost:5432/cruddur
```

Saved variable on Gitpod:

<p align="center"><img src="assets/week4/connection_url_db.png" alt="accessibility text" width="500"></p>

2. New folder `db` will be created within `aws-bootcamp-cruddur-2023/backend-flask/` to allocate db schemas. Once the dicrectory is creted the following files must be created with the information below:
- `schema.sql`: This file contains the code in `SQL` syntax to install `uuid-ossp` plugin, create tables: `users` and `activities` as `public and drop it if it those exists.

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text,
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

- `seed.sql`: This file contains the code in `SQL` syntax to load information in the tables: `public.users` and `public.activities.`

```sql
-- this file was manually created
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
```

3. The folder `bin` will be created within `aws-bootcamp-cruddur-2023/backend-flask/` to allocate db bash scripts to manage the DB. Once the dicrectory is creted the following files must be created with the information below:
- `db-connect`: Bash script used to login `cruddur` DB.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-connect"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

# Connect to cruddur DB
psql $CONNECTION_URL
```

- `db-create`: Bash script used to create `cruddur` DB.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-create"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

#Create DB cruddur
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "CREATE DATABASE cruddur;"
```

- `db-drop`: Bash script used to drop `cruddur` DB.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-drop"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP DATABASE cruddur;"
```

- `db-schema-load`: Bash script used to load the information in the file `schema.sql` in to `cruddur` DB.

<b>Note:</b> Investigating on internet I found this way `find -name schema.sql` to make the script capable of find the file `schema.sql` from any directory.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

schema_path=$(find -name schema.sql)
echo $schema_path

#Check if the conection URL is prod or dev
if [ "$1" = "prod" ]; then
    CON_URL=$PROD_CONNECTION_URL
    echo "This is production enviroment."
else
    CON_URL=$CONNECTION_URL
    echo "This is dev enviroment."
fi

psql $CON_URL cruddur < $schema_path
```

- `db-seed`: Bash script used to load the information in the file `seed.sql` in to `cruddur` DB.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path=$(find -name seed.sql)
echo $seed_path

#Check if the conection URL is prod or dev
if [ "$1" = "prod" ]; then
    CON_URL=$PROD_CONNECTION_URL
    echo "This is production enviroment."
else
    CON_URL=$CONNECTION_URL
    echo "This is dev enviroment."
fi

psql $CON_URL cruddur < $seed_path
```

- `db-sessions`: Bash script used to identify current active/idle session in `cruddur` DB.

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

#Check if there is any process running that might be blocking the DB removal
if [ "$1" = "prod" ]; then
    CON_URL=$PROD_CONNECTION_URL
    echo "This is production enviroment."
else
    CON_URL=$CONNECTION_URL
    echo "This is dev enviroment."
fi

NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$CON_URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

- `db-setup`: Bash script used to automate all previous scripts.

```bash
#! /usr/bin/bash
-e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

#find bind folder
bin_path=$(find /workspace/aws-bootcamp-cruddur-2023/backend-flask/ -type d -name bin)
echo $bin_path

#Execute the bash scripts
source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

- Fix bash scripts permitions from `/workspace/aws-bootcamp-cruddur-2023` directory:

``` bash
chmod u+x backend-flask/bin/db-connect
chmod u+x backend-flask/bin/db-create
chmod u+x backend-flask/bin/db-drop
chmod u+x backend-flask/bin/db-schema-load
chmod u+x backend-flask/bin/db-seed
chmod u+x backend-flask/bin/db-sessions
chmod u+x backend-flask/bin/db-setup
```

Executing `db-setup` script:

<p align="center"><img src="assets/week4/db-setup.png" alt="accessibility text"></p>

`cruddur` DB recently created:

<p align="center"><img src="assets/week4/db_created_docker.png" alt="accessibility text"></p>

Tables recently created:

<p align="center"><img src="assets/week4/created_tables.png" alt="accessibility text"></p>

Recently added information:

<p align="center"><img src="assets/week4/added_info.png" alt="accessibility text"></p>

### Install Postgres Driver in Backend Application
:white_check_mark: DONE. I didn't have any issue to follow Andrew's instructions.

To install Postgres Diver in the backed side, the following steps where followed:

1. Add `Psycopg` packets: `psycopg[binary]` and `psycopg[pool]` for postgres driver in  python `requirements.txt` file located in `backend-flask` folder.

2. In `backend-flask/lib/` directory create a new python file called `db.py` and add the following information:

This file will handle the 

```python
from psycopg_pool import ConnectionPool
import os

#Loading env variables
connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)

def query_wrap_object(template):
  sql = f'''
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  '''
  return sql

def query_wrap_array(template):
  sql = f'''
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  '''
  return sql
```

3. In `backend-flask/services/home_activities.py` endpoint we will add the folling code:

<b>Notes:</b>
* To run the code below the legacy `return` variable must be commented or removed.
* This new code will get logged in local posgres db, get the needed info and returns the outpur in json format.

```python
from datetime import datetime, timedelta, timezone
from opentelemetry import trace

# posgres driver psycopg --------------------------------
from lib.db import pool, query_wrap_array

tracer = trace.get_tracer(__name__)

class HomeActivities:
  #loggger turned off for spend reasons on Cloudwatch
  #def run(logger):
  def run(cognito_user_id=None):
    #loggger turned off for spend reasons on Cloudwatch
    #logger.info('Hello Cloudwatch! from  /api/activities/home')
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())  
      results = []
      # SQL query
      sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """)
      #initializing connection pool and cursor to fetch only the first element in activities table return the output in json format
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          results = cur.fetchone()
      return results[0]
```
4. In `docker-compose.yml` file add the environment variable `CONNECTION_URL` withing `backend-flask` service with the value of local DB URL string.

```yml
services:
  backend-flask:
    environment:
      CONNECTION_URL: "postgresql://postgres:password@db:5432/cruddur"
```

Information seen at frontend:

<p align="center"><img src="assets/week4/db_info_in_frontend.png" alt="accessibility text"></p>

Information seen at backend:

<p align="center"><img src="assets/week4/db_info_in_backend.png" alt="accessibility text"></p>

### Connect Gitpod to RDS Instance
:white_check_mark: DONE. I didn't any issue to follow Andrews instructions, it is the first time I did such work like this and I found it very interesting and applicable in projects at work.

The steps to connect Gtpod to RDS instance are below:

1. Start RDS db `cruddur-db-instance`

Started with warmings when the status is active
<p align="center"><img src="assets/week4/dd_rds_start_failed.png" alt="accessibility text"></p>

No errors seein the events report:
<p align="center"><img src="assets/week4/dd_rds_start_faileld2.png" alt="accessibility text"></p>

3. Get Gipod public IP

```bash
GITPOD_IP=$(curl ifconfig.me)
echo $GITPOD_IP
```

4. add new inbound rule withing DB security group

<p align="center"><img src="assets/week4/security_group_inbound.png" alt="accessibility text"></p>

<p align="center"><img src="assets/week4/rds_security_group.png" alt="accessibility text"></p>

5. from Gitpod CLI connect to RDS DB with the command `psql $PROD_CONNECTION_URL`

<p align="center"><img src="assets/week4/psql_prod_con.png" alt="accessibility text"></p>

6. Since Gitpod IP is changing each time we login and to avoid the manual acle modification, the following script will be used to automatically change the IP

```bash
export DB_SG_ID="sg-0ca4df3a54879ef92"
gp env DB_SG_ID="sg-0ca4df3a54879ef92"
export DB_SG_RULE_ID="sgr-01c87b74c88097a21"
gp env DB_SG_RULE_ID="sgr-01c87b74c88097a21"
```

Create the file `rds-update-sg-rule` with the following code which will change the IP and fix the permissions with the command `chmod u+x backend-flask/bin/rds-update-sg-rule`:

```bash
#! /usr/bin/bash

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="rds-update-sg-rule"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

# # Getting gitpod IP
# GITPOD_IP=$(curl ifconfig.me)
echo "Gitpod IP: $GITPOD_IP"

echo "Result:"

# command to update the the rule
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$GITPOD_IP/32}"
```

Execution logs:

<p align="center"><img src="assets/week4/rds_ip_auto.png" alt="accessibility text"></p>

7. In `docker-compose.yml` commend the dev connection URL line and add one more for production DB, as its shown below: 

```yml
version: "3.8"
services:
  backend-flask:
    environment:
      CONNECTION_URL: "${PROD_CONNECTION_URL}"
      # CONNECTION_URL: "postgresql://postgres:password@db:5432/cruddur" 
```

8. Make `docker-compose up -d` to start docker containers and execute the following scripts to test RDS DB connectivity and upload the schema:

```bash
#Upload schema
./backend-flask/bin/db-schema-load prod

#Checking tables are prsent
./backend-flask/bin/db-connect prod
\dt
\q
```

Logs of loaded schema:

<p align="center"><img src="assets/week4/rds_prod_connection_and_schema.png" alt="accessibility text"></p>

No erros should be seen from backend and frontend:

<p align="center"><img src="assets/week4/rds_backed_logs.png" alt="accessibility text"></p>

### Create Congito Trigger to insert user into database
:white_check_mark: DONE.

1. Create lambda function in AWS console called with the following parameters:

```
- Name: cruddur-post-confirmation-2
- RuntimeInfo: Python 3.8
- Architecture: x86_64
- Advanced settings:
  - Enable VPC
    - Select: VPC, subnets, security groups (This is going to save time and avoid any additional policy creation)
```

<p align="center"><img src="assets/week4/lambda_vpc.png" alt="accessibility text"></p>

Once the lambda function is created 

<p align="center"><img src="assets/week4/lambda_function_created.png" alt="accessibility text"></p>

2. Add pyhton script and click on deplopy

```python
# lambda function to save new users in RDS database
import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('Atributes')
    print(user)

    user_display_name    = user['name']
    user_email           = user['email']
    user_handle          = user['preferred_username']
    user_cognito_user_id = user['sub']
    try:
        print("Entering to try")
  
        sql = f"""
        INSERT INTO users (display_name, email, handle, cognito_user_id)
        VALUES(%(display_name)s, %(email)s, %(handle)s, %(cognito_user_id)s)
        """
        print('SQL Statement ---------')
        print(sql)

        conn = psycopg2.connect(os.getenv('PROD_CONNECTION_URL'))
        cur = conn.cursor()
        params = {'display_name':user_display_name, 'email':user_email, 'handle':user_handle, 'cognito_user_id': user_cognito_user_id}
        cur.execute(sql, params)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
```

3. Add connection URL as environment variable:

<p align="center"><img src="assets/week4/lambda_env_variables.png" alt="accessibility text"></p>

4. Add a layer with python library with `psycopg2`:

<p align="center"><img src="assets/week4/lambda_layer.png" alt="accessibility text"></p>

5. Go to user pools and add the lambda trigger to save the new users within RDS DB:

<p align="center"><img src="assets/week4/lambda_trigger.png" alt="accessibility text"></p>

6. Create a new user, check the cloudwatch logs and RDS DB:

- Logs seen from cloudwatch:

<p align="center"><img src="assets/week4/lambda_logs.png" alt="accessibility text"></p>

- Created user trigered by Cognito to lambda to be stored in RDS DB:

<p align="center"><img src="assets/week4/lambda_created_user.png" alt="accessibility text"></p>

- Cognito new user:
<p align="center"><img src="assets/week4/cognito_newuser.png" alt="accessibility text"></p>

### Create new activities with a database insert
:white_check_mark: DONE. This task was very complex to follow but I end up undertanding it.

1. We have to refactor the `db.py` library to have all functions associated to a class, the following code should be added to add new users to RDS DB, save new post in DB and get the info from there:

```python
from psycopg_pool import ConnectionPool
import os, sys
import re
from flask import current_app as app

class Db():
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def template(self, *args):
    pathing = list((app.root_path,'db', 'sql',) + args)
    pathing[-1] = pathing[-1] + ".sql"
    template_path = os.path.join(*pathing) 
    
    green = '\033[92m'
    no_color = '\033[0m'
    print("pathing:")
    print(f'{green}Load SQL Template: {template_path} {no_color}') 
    
    with open(template_path,'r') as f:
      template_content = f.read()
      return template_content
  
  def print_sql(self, title, sql):
    cyan = '\033[96m]'
    no_color = '\033[0m'
    print(f'{cyan}SQL STATEMENT [{title}]-----------{no_color}')
    print(sql+'\n')


  def query_commit_id(self, sql, params):
    #Function returns the last query
    self.print_sql('commit with returning', sql)
    #Be sure to check for RETURNING in uppercase
    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)
    try:
        print("SQL STATEMENT [list]-----------")
        with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(sql, params)
            if is_returning_id:
              print("Fund match!")
              returning_id = cur.fetchone()[0]
            conn.commit() 
            if is_returning_id:
              return returning_id
    except Exception as err:
      # pass exception to function
      self.print_psycopg2_exception(err)
      # rollback the previous transaction before starting another
      # conn.rollback()
     
  def query_array_json(self, sql, params={}):
    #Function to launch a query and return and array of json objects
    self.print_sql('list', sql)
    wrapped_sql = self.query_wrap_array(sql)    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        # this will return a tuple
        # the first field being the data
        results = cur.fetchone()
    return results[0]

  def query_object_json(self, sql, params={}):
    #Function to launch a query and return it in a json object
    self.print_sql('object', sql)
    wrapped_sql = self.query_wrap_object(sql)    
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        # this will return a tuple
        # the first field being the data
        results = cur.fetchone()
        return results[0]

  def query_wrap_object(self, template):
    #Function to wrap the SQL query to make the DB returns a json array
    sql = f'''
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    '''
    return sql

  def query_wrap_array(self, template):
    #Function to wrap the SQL query to make the DB returns a json array
    sql = f'''
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    '''
    return sql

  def print_psycopg2_exception(self, err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

#Initialize function
db = Db()
```

2. Create `create.sql`, `home.sql`, `object.sql` files into `/backend-flask/db/sql/activities` directory with the SQL queries below:

- `create.sql`:

```sql
INSERT INTO public.activities (
      user_uuid, 
      message, 
      expires_at
    )
    VALUES (
      (SELECT uuid FROM public.users WHERE users.handle = %(handle)s LIMIT 1),
      %(message)s,
      %(expires_at)s) RETURNING uuid;
```

- `home.sql`:

```sql
SELECT
    activities.uuid,
    users.display_name,
    users.handle,
    activities.message,
    activities.replies_count,
    activities.reposts_count,
    activities.likes_count,
    activities.reply_to_activity_uuid,
    activities.expires_at,
    activities.created_at
FROM public.activities
    LEFT JOIN public.users ON users.uuid = activities.user_uuid
    ORDER BY activities.created_at DESC
```

- `object.sql`:

```sql
SELECT 
    activities.uuid,
    users.display_name,
    users.handle, 
    activities.message,
    activities.created_at,
    activities.expires_at
FROM 
    public.activities 
    INNER JOIN  public.users ON users.uuid = activities.user_uuid
    WHERE activities.uuid = %(uuid)s
```

3. Adapting the code in `home_activities.py` file use the class `db` and functions:

```python

from datetime import datetime, timedelta, timezone
from opentelemetry import trace

# posgres driver psycopg --------------------------------
from lib.db import db

tracer = trace.get_tracer(__name__)

class HomeActivities:
  def run(cognito_user_id=None):
    with tracer.start_as_current_span("home-activities-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat()) 
      if cognito_user_id == None:
        results = {
        'uuid': '248959df-3079-4947-b847-9e0892d1baj9',
        'handle':  'Lore',
        'message': 'My dear brother, it the humas are the problem',
        'created_at': (now - timedelta(hours=1)).isoformat(),
        'expires_at': (now + timedelta(hours=12)).isoformat(),
        'likes': 0,
        'replies': []
        }
        return [results]
      else: 
        sql = db.template('activities','home')
        results = db.query_array_json(sql) 
        return results
```

4. Adapting the code in `create_activity.py` file use the class `db` and functions to save the new post and get this info to be returned to frontend:

```python
import uuid
from datetime import datetime, timedelta, timezone
from lib.db import db

class CreateActivity:
  def run(message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      expires_at = (now + ttl_offset)
      uuid =CreateActivity.create_activity(user_handle, message, expires_at)
      object_json = CreateActivity.query_object_activity(uuid)
      model['data'] = object_json
    return model
  
  def create_activity(handle, message, expires_at): 
    #Save the post message in DB
    sql = db.template('activities','create')
    uuid = db.query_commit_id(sql, {'handle': handle, 'message': message, 'expires_at': expires_at})
    return uuid

  def query_object_activity(uuid):
    #Get the post message from DB
    sql = db.template('activities', 'object')
    modelObject = db.query_object_json(sql, {'uuid': uuid})
    return modelObject
```

5. Adding `user_handler` in the front end to send the `POST` request to backacend when any user does the post of a message:
- Frontend:
  - In `HomeFeed Page.js` add `user_handle={user}` within `ActivityForm` compoment:
    
    ```html
    <ActivityForm
      user_handle={user}
      popped={popped}
      setPopped={setPopped}
      setActivities={setActivities}
    />
    ```
  - From `components/ActivityForm.js` inclue `user_handle: props.user_handle.handle,` within request body:

    ```js
    body: JSON.stringify({
          user_handle: props.user_handle.handle,
          message: message,
          ttl: ttl
        }),
    ```
- Backendend:
  - In `app.y` under `/api/activities` route add the line: `user_handle  = request.json['user_handle']`:

    ```py
    @app.route("/api/activities", methods=['POST','OPTIONS'])
    @cross_origin()
    def data_activities():
      # app.logger.debug(request.json)
      user_handle  = request.json['user_handle']
      message = request.json['message']
      ttl = request.json['ttl']
      model = CreateActivity.run(message, user_handle, ttl)
      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200
      return
    ```
6. Post a message:

generating the message:

<p align="center"><img src="assets/week4/creat_activities.png" alt="accessibility text"></p>

Message saved and displayed:

<p align="center"><img src="assets/week4/creat_activities2.png" alt="accessibility text"></p>

Usuarios seen from DB CLI:

<p align="center"><img src="assets/week4/created_users.png" alt="accessibility text"></p>

List of activities seen from DB:

<p align="center"><img src="assets/week4/cli_saved_activities.png" alt="accessibility text"></p>

<b>References:</b>