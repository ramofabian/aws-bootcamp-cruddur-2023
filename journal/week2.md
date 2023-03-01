# Week 2 — Distributed Tracing
## Required Homework/Tasks
### Watch Week 2 Live-Stream Video	
:white_check_mark: DONE.
### Watch Chirag Week 2 - Spending Considerations 
### Watched Ashish's Week 2 - Observability Security Considerations	
### Instrument Honeycomb with OTEL
:white_check_mark: DONE. It was hard for me because it's the first time I use tracing, I had issues during the implmentation but I could fix them up in the way.

1. From Honeycomb

- Creating new enviroment in Honey enviroment  called "bootcamp"

<p align="center"><img src="assets/week2/bootcamp_environment.png" alt="accessibility text"></p>

- Getting enviroment API key:

<p align="center"><img src="assets/week2/honey_api_key.png" alt="accessibility text"></p>

- These are the priviledges for `bootcamp` enviroment, it can be seen from this [link](https://honeycomb-whoami.glitch.me/trace) and adding the API key.

<p align="center"><img src="assets/week2/honey_env_priviledges.png" alt="accessibility text"></p>

2. Save Honeycomb variables on gitpod and docker-compose file

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

3. Adding addtional Hoenycomb python packets.

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

Note: This code can seen in this :point_right: [Link](https://github.com/ramofabian/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py?plain=1#L17-L45)

5. Run the `docker-compose.yml` file and if the information is being collected in honeycomb, the prompt should show the logs after any action from browser and from Honeycomb webseid we should see the data plotted.

- Logging from CLI, the traing messages are seen in json format:

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

7. From Honeycomb website queries can be run to analize the collected data, all of the can be perfomred form 'New query button':

<p align="center"><img src="assets/week2/honey_query.png" alt="accessibility text"></p>

<b>References:</b> [Honeycomb documentation](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/#sampling) and [Open Telemtry](https://opentelemetry.io/docs/)

### Instrument AWS X-Ray	
### Configure custom logger to send to CloudWatch Logs	
### Integrate Rollbar and capture and error
