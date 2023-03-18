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
:white_check_mark: DONE.

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

### Create Congito Trigger to insert user into database
### Create new activities with a database insert