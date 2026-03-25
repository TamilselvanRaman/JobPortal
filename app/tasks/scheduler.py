from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.db.database import SessionLocal
from app import models

def check_jobs_status():
    """Check and update job status based on start_date and end_date"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        jobs = db.query(models.Job).all()
        
        for job in jobs:
            should_be_active = True
            
            if job.start_date and job.start_date > now:
                should_be_active = False
            elif job.end_date and job.end_date < now:
                should_be_active = False
            
            if job.is_active != should_be_active:
                job.is_active = should_be_active
        
        db.commit()
        print(f"Updated job statuses at {now}")
    except Exception as e:
        print(f"Error updating job statuses: {e}")
    finally:
        db.close()

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_jobs_status, 'interval', minutes=5)  # Check every 5 minutes