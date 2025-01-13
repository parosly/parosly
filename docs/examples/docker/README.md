## Getting started with Docker Compose

First, clone the project, and then start up the services with Docker Compose.
```shell
$ git clone https://github.com/parosly/parosly.git
$ cd parosly/docs/examples/docker
$ docker compose up -d
```
After successfully starting up services, the Parosly server will be ready to accept requests.

### Crating example alerting rule via API
> POST /api/v1/rules
> 
**Request**
```shell
curl -i -XPOST 'http://localhost:5000/api/v1/rules' \
--header 'Content-Type: application/json' \
--data '{
  "data": {
    "groups": [
      {
        "name": "ServiceHealthAlerts",
        "rules": [
          {
            "alert": "HighCPUUsage",
            "expr": "sum(rate(cpu_usage{job=\"webserver\"}[5m])) > 0.8",
            "for": "5m",
            "labels": {
              "severity": "warning"
            },
            "annotations": {
              "summary": "High CPU Usage Detected",
              "description": "The CPU usage for the web server is {{ $value }}% for the last 5 minutes."
            }
          }
        ]
      }
    ]
  }
}'
```

**Response**
```
HTTP/1.1 201 Created
content-length: 99
content-type: application/json

{"status":"success","message":"The rule was created successfully","file":"453ee16d-6310-42e0-8d57-2857e27d250f.yml"}
```
Where the `453ee16d-6310-42e0-8d57-2857e27d250f.yml` is the randomly generated filename created by the Parosly server.

### Deleting alerting rule file via API
> DELETE /api/v1/rules/{file}

_Note that the filename in your example is different from the example below._

**Request**
```shell
curl -i -XDELETE 'http://localhost:5000/api/v1/rules/453ee16d-6310-42e0-8d57-2857e27d250f.yml'
```
**Response**
```
HTTP/1.1 204 No Content
content-type: application/json
```
You can find the complete API documentation [here](https://docs.parosly.io). Enjoy!