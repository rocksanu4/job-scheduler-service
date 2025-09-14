from fastapi import FastAPI
from app import db, jobs, api
import logging
from app.scheduler import start_scheduler, stop_scheduler, schedule_job
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    start_scheduler()
    for job in jobs.list_jobs(limit=1000):
        if job.status.value == "enabled":
            schedule_job(job)
    yield
    stop_scheduler()

app = FastAPI(title="Job Scheduler Service", lifespan=lifespan, description="""
This microservice lets you schedule recurring jobs (cron or interval) and track their executions.  
Features:
- Create new jobs
- List all jobs
- Get job details
- Tracks last/next run times
- Scalable for thousands of jobs
""",)
app.include_router(api.router)

@app.get("/")
async def root_path():
    return {"message": "Hello world!"}
