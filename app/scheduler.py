from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone
import pytz
import logging
from app import jobs

log = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.start()
    log.warning("Scheduler started")

def stop_scheduler():
    scheduler.shutdown(wait=True)
    log.warning("Scheduler stopped")

def schedule_job(job_row):
    job_id = str(job_row.id)
    if job_row.schedule_type.value == "cron":
        trigger = CronTrigger.from_crontab(job_row.schedule_expr, timezone=pytz.timezone(job_row.timezone or "UTC"))
    else:
        # For simplicity assume schedule_expr like "seconds=60" — parse if needed
        parts = dict(x.split("=") for x in job_row.schedule_expr.split(","))
        trigger = IntervalTrigger(**{k:int(v) for k,v in parts.items()})
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        func=execute_job,
        trigger=trigger,
        id=job_id,
        args=[job_id],
        replace_existing=True,
        max_instances=1,
    )

def execute_job(job_id):
    log.info(f"Executing job {job_id} at {datetime.now(timezone.utc)}")
    job = jobs.get_job(job_id)
    now = datetime.now(timezone.utc)
    aps_job = scheduler.get_job(str(job_id))
    next_run = aps_job.next_run_time if aps_job else None
    jobs.update_last_next_run(job_id, last_run=now, next_run=next_run)
