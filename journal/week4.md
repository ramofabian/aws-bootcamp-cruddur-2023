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

1. New folder `db` will be created within `aws-bootcamp-cruddur-2023/backend-flask/` to allocate db schemas. Once the dicrectory is creted the following files must be created with the information below:
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

2. The folder `bin` will be created within `aws-bootcamp-cruddur-2023/backend-flask/` to allocate db bash scripts to manage the DB. Once the dicrectory is creted the following files must be created with the information below:
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

Executing `db-setup` script:

<p align="center"><img src="assets/week4/db-setup.png" alt="accessibility text"></p>

`cruddur` DB recently created:

<p align="center"><img src="assets/week4/db_created_docker.png" alt="accessibility text"></p>

Tables recently created:

<p align="center"><img src="assets/week4/created_tables.png" alt="accessibility text"></p>

Recently added information:

<p align="center"><img src="assets/week4/added_info.png" alt="accessibility text"></p>

### Install Postgres Driver in Backend Application
### Connect Gitpod to RDS Instance
### Create Congito Trigger to insert user into database
### Create new activities with a database insert