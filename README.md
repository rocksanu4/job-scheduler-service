# Job Scheduler Microservice (Python + FastAPI + APScheduler)

A microservice for scheduling recurring jobs (cron or interval) with API endpoints for job management.  
Supports job persistence with Postgres, and exposes clean API docs via Swagger and ReDoc.


## Setup Instructions

### 1. Clone repo
```bash
git clone https://github.com/rocksanu4/job-scheduler-service.git
cd job-scheduler-service
```
with docker installed in terminal enter the below command
```bash
docker-compose up --build
```
Access api documentation at 
http://localhost:8000/redoc or http://localhost:8000/docs


## For production:

- Run multiple FastAPI workers (e.g. with Gunicorn/Uvicorn)

- Use a distributed APScheduler backend (e.g. Redis or DB job store) to avoid duplicate job executions

- Add monitoring (Prometheus, Grafana) for job health

- Deploy on Kubernetes with HPA for API scaling

