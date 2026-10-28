# Practical 12 — Prometheus and Grafana Monitoring

This setup instruments the Student Result Prediction FastAPI service with Prometheus metrics, scrapes them with Prometheus, visualizes them in Grafana, and defines basic alert rules.

## Included files

- `api.py`: exposes `/metrics` and records request counts, response status, request duration, prediction outcomes, and model availability.
- `docker-compose.monitoring.yml`: starts the API, Prometheus, and Grafana.
- `monitoring/prometheus/prometheus.yml`: Prometheus scrape configuration.
- `monitoring/prometheus/alert_rules.yml`: service-down and repeated-client-error alert rules.
- `monitoring/grafana/provisioning/datasources/prometheus.yml`: provisions the Prometheus data source.
- `monitoring/grafana/dashboards/student-result-api.json`: preconfigured dashboard.
- `monitoring/grafana/provisioning/dashboards/dashboard.yml`: loads the dashboard automatically.

## Run locally (Docker Desktop)

Run these commands from the repository folder. Docker Desktop must be running.

```bash
docker compose -f docker-compose.monitoring.yml up --build -d
docker compose -f docker-compose.monitoring.yml ps
```

Open these pages:

- FastAPI Swagger: http://localhost:5000/docs
- API metrics: http://localhost:5000/metrics
- Prometheus: http://localhost:9090
- Prometheus targets: http://localhost:9090/targets
- Prometheus alerts: http://localhost:9090/alerts
- Grafana: http://localhost:3000

Grafana default local credentials for this compose file are username `admin` and password `admin123`. Change the password if you expose this service beyond your own computer. These credentials are intended only for local demonstration.

## Generate sample metrics

Run a valid prediction:

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"attendance":95,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
```

Generate a validation error (expected HTTP 422):

```bash
curl -i -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"attendance":150,"internal_marks":95,"assignment_marks":95,"previous_score":95}'
```

Refresh `/metrics`, Prometheus, and Grafana after generating traffic. Prometheus needs a few scrape intervals before the dashboard shows data.

## Useful PromQL queries

```promql
sum(rate(student_api_http_requests_total[5m]))
sum by (status_code) (student_api_http_requests_total)
histogram_quantile(0.95, sum by (le) (rate(student_api_http_request_duration_seconds_bucket[5m])))
sum by (result) (student_api_predictions_total)
up{job="student-result-api"}
student_api_model_available
```

## Alerts

Prometheus loads the rules from `monitoring/prometheus/alert_rules.yml`:

- `StudentResultAPIUnavailable`: target scrape remains down for one minute.
- `StudentResultAPIHighClientErrors`: 4xx response rate remains above the configured threshold for two minutes.

The alerts appear in Prometheus under **Alerts**. Notifications to email or messaging services require an Alertmanager/receiver configuration and are not configured in this local demonstration.

## Stop the stack

```bash
docker compose -f docker-compose.monitoring.yml down
```

To also delete stored Prometheus and Grafana data, use `docker compose -f docker-compose.monitoring.yml down -v`.

## Deployment note

The existing Render service deploys the API container image. Prometheus and Grafana are configured here as a local Docker Compose monitoring stack; they are not automatically hosted publicly by the Render API service.
