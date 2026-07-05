from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.models.job import Job
from app.models.project import Project
from app.models.queue import Queue
from app.models.worker import Worker


def get_dashboard_overview(db: Session):
    return {
        "projects": db.query(func.count(Project.id)).scalar(),
        "queues": db.query(func.count(Queue.id)).scalar(),
        "jobs": db.query(func.count(Job.id)).scalar(),
        "workers": db.query(func.count(Worker.id)).scalar(),
        "queued_jobs": db.query(Job).filter(Job.state == "queued").count(),
        "running_jobs": db.query(Job).filter(Job.state == "running").count(),
        "completed_jobs": db.query(Job).filter(Job.state == "completed").count(),
        "failed_jobs": db.query(Job).filter(Job.state == "failed").count(),
        "idle_workers": db.query(Worker).filter(Worker.status == "idle").count(),
        "busy_workers": db.query(Worker).filter(Worker.status == "busy").count(),
        "execution_logs": db.query(func.count(ExecutionLog.id)).scalar(),
    }


def get_recent_jobs(db: Session):
    return (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .limit(10)
        .all()
    )


def get_recent_workers(db: Session):
    return (
        db.query(Worker)
        .order_by(Worker.created_at.desc())
        .all()
    )


def get_recent_queues(db: Session):
    return (
        db.query(Queue)
        .order_by(Queue.created_at.desc())
        .all()
    )


def get_recent_executions(db: Session):
    return (
        db.query(ExecutionLog)
        .order_by(ExecutionLog.created_at.desc())
        .limit(20)
        .all()
    )