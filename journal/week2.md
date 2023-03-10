# Week 2 — Distributed Tracing
## Required Homework/Tasks
### Watch Week 2 Live-Stream Video	
:white_check_mark: DONE.
### Watch Chirag Week 2 - Spending Considerations 
### Watched Ashish's Week 2 - Observability Security Considerations	
:white_check_mark: DONE.
### Instrument Honeycomb with OTEL
:white_check_mark: DONE. It was hard for me because it's the first time I use tracing, I had issues during the implementation but I could fix them up in the way.

1. From Honeycomb

- Creating new environment in Honey environment  called "bootcamp"

<p align="center"><img src="assets/week2/bootcamp_environment.png" alt="accessibility text"></p>

- Getting environment API key:

<p align="center"><img src="assets/week2/honey_api_key.png" alt="accessibility text"></p>

- These are the privileges for `bootcamp` environment, it can be seen from this [link](https://honeycomb-whoami.glitch.me/trace) and adding the API key.

<p align="center"><img src="assets/week2/honey_env_priviledges.png" alt="accessibility text"></p>

2. Save Honeycomb variables on Gitpod and docker-compose file

- CLI variables:

<p align="center"><img src="assets/week2/cli_env_variables.png" alt="accessibility text"></p>

- Saved Gitpod variables:

<p align="center"><img src="assets/week2/saved_variables.png" alt="accessibility text"></p>

- Adding the `OTEL` variables in `docker-compose.yml` for backend service:

```yml
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      OTEL_SERVICE_NAME: "backend-flask"
      OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
      OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
```

3. Adding additional Hoenycomb python packets.

The following commands should be added under backend `requirements.txt` file, like is present in this :point_right: [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/requirements.txt?plain=1#L4-L8):

```bash
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-exporter-otlp-proto-http
pip install opentelemetry-instrumentation-flask
pip install opentelemetry-instrumentation-requests

```

The file `requirements.txt` is used by backend dockerfile to build the image and be able to use `Hoenycomb` api.

4. Initialize the tracer and flask instrumentation to send data to Honeycomb and enable console logging within flask app. To do it, we need to add code below in `app.py` file within backend folder:

```python
# Honeycomb libs -----------------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# Honeycomb libs -----------------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Show this in the logs within the backend-flask app (STDOUT)
#this is used for troubleshooting and shouldn't run in production env
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__) 

# Honeycomb libs -----------------
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

<b>Note:</b> This code can seen in the following links
  - Imported libraries :point_right: [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py?plain=1#L17-L25)
  - Initialize tracing and an exporter :point_right: [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py?plain=1#L45-L58)
  - Initialize automatic instrumentation :point_right: [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py?plain=1#L65-L68)

5. Run the `docker-compose.yml` file and if the information is being collected in honeycomb, the prompt should show the logs after any action from browser and from Honeycomb website we should see the data plotted.

- Logging from CLI, the tracing messages are seen in json format:

<p align="center"><img src="assets/week2/tracing_cli.png" alt="accessibility text"></p>

- Logging from Honeycomb website, the information is plotted in the charts:

<p align="center"><img src="assets/week2/honey_website_logs.png" alt="accessibility text"></p>

6. To create the spam for some specific service, the following code should be added inside of service `.py` file:

- In this case the code was added at `/backend-flask/services/home_activities.py`, it can be seen in this :point_right: [link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/home_activities.py)

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class HomeActivities:
  def run():
    with tracer.start_as_current_span("home-activities-mock-data"): #here the span is named
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat()) # here the info is added and named as "app.now" and the value is the date.
      span.set_attribute("app.result_length", len(results)) # Second attribute 
```

- After this change, the span information can be seen from the website:

<p align="center"><img src="assets/week2/honey_website_span.png" alt="accessibility text"></p>

7. From Honeycomb website queries can be run to analyze the collected data, all of the can be performed form 'New query button':

<p align="center"><img src="assets/week2/honey_query.png" alt="accessibility text"></p>

<b>References:</b> [Honeycomb documentation](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/#sampling) and [Open Telemtry](https://opentelemetry.io/docs/)

### Instrument AWS X-Ray	
:white_check_mark: DONE. It was very hard to understand and make it works, the documentation is very extensive and tricky!!. Although, with Andrew's videos it was far way easy.

<table>
  
  <b>Definitions:</b>
  * <b>AWS X-Ray:</b> It's an Amazon service which gathers data based on requests made to its application (API), it also has tools to query, filter and get information regarding collected information. The gathered information is useful to identify problems and identify optimization opportunites.
  
  * Services send data to X-Ray as <b>segments</b>, it groups them according to common information in `traces`.
  
  * The `segments` can contains constrained information about subtasks as <b>subsegments</b>. It provides more detailed information about the service subprocess.
  
  * The <b>traces</b> tracks the path of some specific request and collects all segments and subsegments by a single request.

</table>

To instrument AWS X-Ray in backend side, the following steps were performed:

1. The python packet `aws-xray-sdk` is added to `requirements.txt` file. :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/requirements.txt?plain=1#L10).

2. Add the following code in `app.py`. 

```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```

- Add this line `@xray_recorder.capture('activities_home')` in `/api/activities/home` endpoint as it's shown below to create the segment 'activities_home'. 

```python
@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('activities_home')
def data_home():
  data = HomeActivities.run()
  return data, 200
```

- Add this line `@xray_recorder.capture('activities_users')` in `/api/activities/home` endpoint as it's shown below to create the segment 'activities_users'.

```python
@app.route("/api/activities/@<string:handle>", methods=['GET'])
@xray_recorder.capture('activities_users')
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
```

3. Add the following code in `backend-flask/services/user_activities.py` to create a subsegment called 'mock-data'.

```python
# X-Ray -----------------
from aws_xray_sdk.core import xray_recorder

# X-Ray -----------------
    # Start a subsegment
    subsegment = xray_recorder.begin_subsegment('mock-data')
    dict = {
      "now": now.isoformat(),
      "results-size": len(model['data'])
    }
    subsegment.put_metadata('key', dict, 'namespace')
    xray_recorder.end_subsegment()
```

4. Setup AWS X-Ray Resources by adding the file `xray.json` in this directory `aws/json/`. This file should contains the following below. 
```json
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "Cruddur",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```

5. Create the group by running the command below:

```bash
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"Backend-flask\")"
```
- Command launched from Gitpod bash CLI:

<p align="center"><img src="assets/week2/x-ray_group.png" alt="accessibility text"></p>

- Group created seen from AWS website:

<p align="center"><img src="assets/week2/group_log.png" alt="accessibility text"></p>

6. Run the command below to create a rule for the group `Cruddur` created in step 4.
 
```bash
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

- Command executed from CLI:

<p align="center"><img src="assets/week2/x_ray_rule.png" alt="accessibility text"></p>

- Rule seen from AWS website:

<p align="center"><img src="assets/week2/x_ray_rule_web.png" alt="accessibility text"></p>

7. Add the following lines in `docker-compose.yml` file:

- Adding `aws-xray-deamon` service. :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml?plain=1#L47-L56).

```yml
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "eu-central-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```

- Adding `aws-xray-deamon` environment variables in backend service. 

```yml
AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```

8. Run `docker-compose.yml` file, open `xray-daemon` console, open the frontend URL on browser and interact between home page and Andrew's profile many times to trigger traces from backend to AWS X-Ray. 

- The logs below should be seen from CLI:

<p align="center"><img src="assets/week2/x-ray_docker_logs.png" alt="accessibility text"></p>

- The information should be seen from AWS X-Ray traces:

<p align="center"><img src="assets/week2/x_ray_trace.png" alt="accessibility text"></p>

- Making click on one of the traces the `segment` and `subsegment` previously created and its metadata:

Subsegment overview info:

<p align="center"><img src="assets/week2/x-ray_trace_1.png" alt="accessibility text"></p>

Subsegment metadata:

<p align="center"><img src="assets/week2/x-ray_trace_2.png" alt="accessibility text"></p>

<b>Link to files:</b>
  * `docker-compose.yml` :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml).
  * `xray.json` :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/aws/json/xray.json).
  * `app.py` :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py).
  * `user_activities.py` :point_right: [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/services/user_activities.py).

<b>References:</b> [AWS documentation for x-ray](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html) and [Git repo for x-ray sdk](https://github.com/aws/aws-xray-sdk-python)

### Configure custom logger to send to CloudWatch Logs	
:white_check_mark: DONE. This task was quite easy to follow up, I didn't have any issue to follow Andrew's video.

To configure custom logger in backend and send this data to AWS CloudWatch, the steps below were performed:

1. Add the python packet `watchtower` within `requrements.txt`, this file is located in `aws-bootcamp-cruddur-2023/backend-flask/`. [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/requirements.txt?plain=1#L11).

2. In the file `app.py` located in `aws-bootcamp-cruddur-2023/backend-flask/` and add the following code:

- Import libraries

```python
# CloudWatch logs -----------------
import watchtower
import logging
from time import strftime
```

- Configure the logger to send the information to log group called `cruddur`, it was created in x-ray procedure:

```python
# Configuring Logger to Use CloudWatch ---
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("Start logging")
```

- Adding new endpoint to log the answer after any request

```python
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```

3. Implementing logs within an endpoint
- Adding logs in the endpoint `/activities/home`:

From `app.py` add the parameter `logger=LOGGER` to send the object inside of `HomeActivities.run()` function:

```python
@app.route("/api/activities/home", methods=['GET'])
xray_recorder.capture('activities_home')
def data_home():
  data = HomeActivities.run(logger=LOGGER)
  return data, 200
```

In `aws-bootcamp-cruddur-2023/backend-flask/services/home_activities.py` modify the `run()` function as is shown below:

```python 
class HomeActivities:
  def run(logger): #add the 'logger' input parameter
    logger.info('Hello Cloudwatch! from  /api/activities/home') # Add this line
```

4. Add the enviroment variables in `docker-compose.yml` within backend service: 

```yml
AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

5. Run `docker-compose.yml` to deploy the docker containers and see the logs from AWS ClouldWatch:

- Deploy the containers
 
```bash
docker-compose up -d
```
- Open the backend and frontend URL and interact with them from web browser to generate logs:

  * Group log `cruddur` seen from CloudWatch console:

<p align="center"><img src="assets/week2/cloudwatch_log_group.png" alt="accessibility text"></p>

  * Received logs from application seen from CloudWatch console:

<p align="center"><img src="assets/week2/cloudwatch_log_list.png" alt="accessibility text"></p>

  * Log entry information:
  
<p align="center"><img src="assets/week2/cloudwatch_log_entry.png" alt="accessibility text"></p>

<b>Notes:</b> 
* Due to spending consideration on AWS CloudWatch and X-Ray services, I have disabled the functions to avoid any possible charge from AWS. Although, it can be activated any time!!
* Please find below files:
  * `app.py` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py) 
  * `home_activities.py` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
  * `docker-compose.yml` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml)

<b>References:</b> [Watchtower official documentation](https://kislyuk.github.io/watchtower/), [Watchtower python reference](https://pypi.org/project/watchtower/)

### Integrate Rollbar and capture and error
:white_check_mark: DONE. This task was quite easy to follow up, I didn't have any issue to follow Andrew's video.

<b>Rollbar</b> is a cloud-based bug tracking and monitoring solution that caters to organizations of all sizes. Rollbar supports multiple programming languages and frameworks like JavaScript, Python, .NET, Drupal, Wordpress and Pyramid. The solution can also be deployed on premises at the user end. <b>Source: </b>[softwareadvice](https://www.softwareadvice.com/continuous-integration/rollbar-profile/)
  
To integrate Rollbar and capture an error, I followed the next steps:

1. Add the following python packets to `requirements.txt` file. 👉 [Link to file](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/requirements.txt?plain=1#L13-L14)

```txt
blinker
rollbar
```

2. Set Rollbar access token in Gitpod environment variable.

```bash
export ROLLBAR_ACCESS_TOKEN=""
gp env ROLLBAR_ACCESS_TOKEN=""
```

Variable seen from gitpod:

<p align="center"><img src="assets/week2/rollbar_env_gitpod.png" alt="accessibility text"></p>

3. Add the environment variable created in previous step into `backend-flask` service for `docker-compose.yml`

```yml
ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
```

4. Import for Rollbar into backend-flask application:

- Import libraries in `backend-flask/app.py`:

```python
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
```

- In `backend-flask/app.py` initialize Rollbar module (this fragment should be allocated before line `app = Flask(__name__)`).

```python
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
 ```

- Add a new endpoint in  `backend-flask/app.py` to test Rollbar connection.

```python
@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"
```

5. Execute the file `docker-compose.yml` to deploy the applications.

```bash
docker-compose up -d
docker-compose ps -a
```

<p align="center"><img src="assets/week2/rollbar_contianers.png" alt="accessibility text"></p>

6. Open the backend URL in the browser and add at the end the route `/rollbar/test` and see if the warning messages has arrived in Rollbar `FirstProject`.

- From we browser:

<p align="center"><img src="assets/week2/rollbar_first_test.png" alt="accessibility text"></p>

- From Rollbar website `Items` tab:

 <p align="center"><img src="assets/week2/rollbar_first_test1.png" alt="accessibility text"></p>
 
 - By clicking on the warning recently arrived the information below was seen:
 
 <p align="center"><img src="assets/week2/rollbar_first_test2.png" alt="accessibility text"></p>

7. Generating a real error from backend and displaying it on Rollbar.

- From `backend-flask/services/home_activities.py` remove the `return` and keep the variable `results`.
- Open the backend URL and add at the end the route `/api/activities/home`, the error below is seen:

 <p align="center"><img src="assets/week2/rollbar_second_test.png" alt="accessibility text"></p>
 
 - From Rollbar/itmes the same error should be visible:
 
<p align="center"><img src="assets/week2/rollbar_second_test1.png" alt="accessibility text"></p>

- More details seen from Rollbar:

<p align="center"><img src="assets/week2/rollbar_second_test2.png" alt="accessibility text"></p>

- More information:

<p align="center"><img src="assets/week2/rollbar_second_test3.png" alt="accessibility text" width="400"></p>

<b>Notes:</b> 
* Please find below files:
  * `app.py` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py) 
  * `home_activities.py` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
  * `docker-compose.yml` 👉 [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/docker-compose.yml)

<b>References:</b> [pyrollbar github](https://github.com/rollbar/pyrollbar), [pyrollbar documentation](https://docs.rollbar.com/docs/python)

## Homework challenges
### Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span
:white_check_mark: DONE. 

I have added custom instrumentation for notifications activities endpoint located in this directory: `/backend-flask/services/notificattions_activities.py`. There the following work has been performed:

1. 4 span levels have been created, each of them has its own attributes
2. In the last span called `Result_content` the user_ID has been added.
3. The record of executions has been implemented in the span `Result_content` to show how to change the span status and create the event with the message.

```python
class NotificattionsActivities:
  def run():
    with tracer.start_as_current_span("Notificattions_Activities") as outer_span: # --> Second span
      with tracer.start_as_current_span("Result") as inner_span: # --> Third span
        now = datetime.now(timezone.utc).astimezone()
        outer_span.set_attribute("now", now.isoformat()) # --> Second span attribute set
        results = [{
          'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'Benji',
          'message': 'I\'m a dog',
          'created_at': (now - timedelta(days=2)).isoformat(),
          'expires_at': (now + timedelta(days=5)).isoformat(),
          'likes_count': 5,
          'replies_count': 1,
          'reposts_count': 0,
          'replies': [{
            'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
            'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
            'handle':  'Worf',
            'message': 'This post has no honor!',
            'likes_count': 0,
            'replies_count': 0,
            'reposts_count': 0,
            'created_at': (now - timedelta(days=2)).isoformat()
          }],
        },
        {
          'uuid': '66e12864-8c26-4c3a-9658-95a10f8fea67',
          'handle':  'Worf',
          'message': 'I am out of prune juice',
          'created_at': (now - timedelta(days=7)).isoformat(),
          'expires_at': (now + timedelta(days=9)).isoformat(),
          'likes': 0,
          'replies': []
        },
        {
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Garek',
          'message': 'My dear doctor, I am just simple tailor',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 0,
          'replies': []
        }
        ]
        inner_span.set_attribute("Result_lent", len(results)) # --> Third span attribute set
        #adding custom span
        with tracer.start_as_current_span("Result_content") as inner_inner_span: # --> Forth span set
          inner_inner_span.set_attribute("user_id", results[0]['uuid']) # --> Forth span attribute set as UUID for user
          inner_inner_span.set_attribute("user_handle", results[0]['handle']) # --> Forth span attribute set as handle for user
          #Custom span for catching errors
          try:   # --> Forth span attribute set to catch an error, sent the event and change the status to error
            print(error)
          except Exception as ex:
            inner_inner_span.set_status(Status(StatusCode.ERROR))
            inner_inner_span.record_exception(ex) 
        return results
  ```

- Trace information collected with the `user_id` sent and `user_handle` as well:

<p align="center"><img src="assets/week2/honeycom_custom_span_1.png" alt="accessibility text"></p>

- Collected trace information with the event generated:

<p align="center"><img src="assets/week2/honeycom_custom_span_2.png" alt="accessibility text"></p>

<b>References:</b> [Honeycomb open telemetry](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/), [open telemetry documentation](https://opentelemetry.io/docs/instrumentation/python/manual/)

### Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces
:white_check_mark: DONE. 

Based on the span previously created I have created this query to see the heatmap of user ID interactions and span status code: [Link to template](https://ui.honeycomb.io/ramillos/environments/bootcamp/datasets/backend-flask?query=%7B%22time_range%22%3A7200%2C%22granularity%22%3A0%2C%22breakdowns%22%3A%5B%5D%2C%22calculations%22%3A%5B%7B%22op%22%3A%22HEATMAP%22%2C%22column%22%3A%22app.result_uuid%22%7D%2C%7B%22op%22%3A%22HEATMAP%22%2C%22column%22%3A%22status_code%22%7D%5D%2C%22orders%22%3A%5B%5D%2C%22havings%22%3A%5B%5D%2C%22limit%22%3A1000%7D)

Please find below the picture of the gathered results:

<p align="center"><img src="assets/week2/honey_query_custom.png" alt="accessibility text" ></p>
