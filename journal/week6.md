# Week 6 — Deploying Containers
## Mandatory tasks
### Watched Ashish's Week 6 - Amazon ECS Security Best Practices
:white_check_mark: DONE.
### Watched ECS Fargate (Part 1)
:white_check_mark: DONE.
### Forecast cost of Fargate
:white_check_mark: DONE.
In we worst case if we have 2 containers running every day for the whole month the cost will be arround 20USD. This forecast has been done with AWS calculator and using the parameters below:

```
- Region: Europe (Frankfurt)
- OS: Linux
- CPU Architecture: x86
- Number of tasks: 2 per month
- Average duration: 730 hours (1 month)
- Amount of vCPU allocated: 0.25 vCPU
- Amount of memory allocated: 0.5 GB
- Amount of ephemeral storage allocated for Amazon ECS: 20 GB
```

Log output:

<p align="center"><img src="assets/week6/aws_fargate_forecast cost.png" alt="accessibility text"></p>

### Creating healthchecks
:white_check_mark: DONE.
#### Healthcheck RDS connection
Script to test the connection to AWS RDS DB, this script will be named as `test` and will be placed in `backend-flask/bin/db/`

```py
#!/usr/bin/env python3

import psycopg
import os
import sys

connection_url = os.getenv("CONNECTION_URL")

conn = None
try:
  print('attempting connection')
  conn = psycopg.connect(connection_url)
  print("Connection successful!")
except psycopg.Error as e:
  print("Unable to connect to the database:", e)
finally:
  conn.close()
```

Then fix the permissions:

```bash
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (main) $ chmod u+x bin/db/test 
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (main) $ ls -la bin/db/test 
-rwxr--r-- 1 gitpod gitpod 331 Apr  1 09:31 bin/db/test
```

Execute python `test` to test if RDS DB is alive and conection stablished, `./bin/db/test`:

<p align="center"><img src="assets/week6/RDS_test_connection.png" alt="accessibility text"></p>

#### Healthcheck endpoint for Flask
1. In `backend-flask\app.py` we need to add a new endpoint with the route `/api/health-check` and returns 200 message as success.

```py
# Flask healthcheck
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```

2. Then we need to create a python scritp at `bin/flask/health-check` with the code below:

```py
#!/usr/bin/env python3

import urllib.request

try:
  response = urllib.request.urlopen('http://localhost:4567/api/health-check')
  if response.getcode() == 200:
    print("[OK] Flask server is running")
    exit(0) #succed message
  else:
    print("[BAD] Flask server is not running")
    exit(1) #fail message
except Exception as e:
    print("[BAD] ", e)
    exit(1) #fail message
```

3. Fix the permissions `chmod u+x bin/flask/health-check` and run the script (first try not succeded becuase local postgres DB was not running):

<p align="center"><img src="assets/week6/flask_check.png" alt="accessibility text"></p>

4. Create new logs groups in AWS with the follwing commands:

```bash
aws logs create-log-group --log-group-name "cruddur-fargate-cluster"
aws logs put-retention-policy --log-group-name "cruddur-fargate-cluster" --retention-in-days 1
```

<b>Note:</b> The information will be retained 1 day only, then it will be removed by the system itself.

<p align="center"><img src="assets/week6/new_logs_cruddur.png" alt="accessibility text"></p>

### Provision ECS Cluster
:white_check_mark: DONE.
To create the ECS cluster from AWS CLI we have to run the following command:

```bash
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

In the picture below is shown the ECS cluster created from previous command (it is empty, so no services attached):

<p align="center"><img src="assets/week6/create_ecs_cluster.png" alt="accessibility text"></p>

### Create ECR repo and push image for backend-flask
:white_check_mark: DONE.
#### Storing ours containers on ECR
We are going to store ours containers as private and it will be done from Gitpod console.

There is going to be 3 repos:
- Base-image python.
- Flask.
- React.

##### 1. Create `cruddur-python` repo as mutable from Gitpod CLI:

```bash
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```

- Created repo seen from AWS console:

<p align="center"><img src="assets/week6/container_repo.png" alt="accessibility text"></p>

- Get logged in AWS ECR from gitpod CLI:

```bash
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

Execution log:

<p align="center"><img src="assets/week6/login_in_ECR_AWS.png" alt="accessibility text"></p>

- Set the repo URL with the command below and confirm that this information matched with the one in AWS console:

```bash
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```

Execution logs:

<p align="center"><img src="assets/week6/create_repo_url.png" alt="accessibility text"></p>

- Pull, tag and push docker image in our AWS repo:

```bash
docker pull python:3.10-slim-buster
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
docker push $ECR_PYTHON_URL:3.10-slim-buster
```
Logs from CLI:

<p align="center"><img src="assets/week6/pushed_image_in_ecr_repo.png" alt="accessibility text"></p>

Logs AWS console:

<p align="center"><img src="assets/week6/pushed_image_aws_repo.png" alt="accessibility text"></p>

After running the db and backend service, we see the flask healthcheck is workig:

<p align="center"><img src="assets/week6/test_flask_health_check.png" alt="accessibility text"></p>

##### 2. Create `bakend-flask` repo as mutable from Gitpod CLI:

```bash
#Create repo
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
  
#Create connection URL
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
```
Log from AWS console:

<p align="center"><img src="assets/week6/backend_repo.png" alt="accessibility text"></p>

Log from gitpod CLI:

<p align="center"><img src="assets/week6/flask_string_url.png" alt="accessibility text"></p>

- Build, tag and push docker image in our AWS repo:

```bash
cd /workspace/aws-bootcamp-cruddur-2023/backend-flask
docker build -t backend-flask .
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
docker push $ECR_BACKEND_FLASK_URL:latest
```
Logs from gitpod cli:

<p align="center"><img src="assets/week6/docker_push_backend.png" alt="accessibility text"></p>

Image seen from AWS repo:

<p align="center"><img src="assets/week6/image_from_repo.png" alt="accessibility text"></p>

### Deploy Backend Flask app as a service to Fargate
:white_check_mark: DONE.
To deploy backend flask app in Fargate, it is necessary to follow the next steps:
#### Implement parameters

#### Implement AWS service policy
AIM roles are needed for Fargate task definition, do we need to create a new `role` in AIM service called `CruddurServiceExecutionRole` with the json configuration in this file :point_right: [aws/policies/service-execution-policy.json]() --->FIX!!

The execution was done with AWS CLI with the command below:

```bash
aws iam create-role \
    --role-name CruddurServiceExecutionRole \
    --assume-role-policy-document file://aws/policies/service-execution-policy.json
```

From AWS console go to ECS service -> task definitions
<b>Note:</b> task definitions is `similar to docker-`compose file where we define how the containers will run. [LINK](https://docs.docker.com/cloud/ecs-integration/)

From AWS console go to ECS service -> cruddur cluster -> services.
<b>Note:</b> we will use service because at the end when the container is stoped, it will be killed if we implment it as a task. For that reason we will use it as a service. 
