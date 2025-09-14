from sqlalchemy import select, insert, update
from app.models import Job
from app.db import SessionLocal

def create_job(payload: dict):
    with SessionLocal() as session:
        job = Job(**payload)
        session.add(job)
        session.commit()
        session.refresh(job)   # refresh to load DB-generated fields
        return job

def list_jobs(limit=100, offset=0):
    with SessionLocal() as session:
        return session.query(Job).offset(offset).limit(limit).all()

def get_job(job_id):
    with SessionLocal() as session:
        return session.query(Job).filter(Job.id == job_id).first()

# def update_job(job_id, update_dict: dict):
#     values = {}
#     for key, value in update_dict:
#         values[key] = value
#     with SessionLocal() as session:
#         query = update(jobs).where(jobs.c.id == job_id).values(**values)
#         session.execute(query)
#         session.commit()

def update_last_next_run(job_id, last_run=None, next_run=None):
    with SessionLocal() as session:
        job = session.query(Job).filter(Job.id == job_id).first()
        if job:
            if last_run:
                job.last_run_at = last_run
            if next_run:
                job.next_run_at = next_run
            session.commit()
