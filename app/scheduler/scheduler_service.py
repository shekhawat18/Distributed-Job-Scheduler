from datetime import datetime

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.queue import Queue
from app.models.worker import Worker


def get_next_job(db: Session):
    """
    Returns the highest-priority job that is ready for execution.
    """

    return (
        db.query(Job)
        .join(Queue)
        .filter(
            Job.state == "queued",
            Queue.is_paused.is_(False),
            Job.run_after <= datetime.utcnow(),
        )
        .order_by(
            Queue.priority.desc(),
            Job.priority.desc(),
            Job.created_at.asc(),
        )
        .first()
    )


def get_available_worker(db: Session):
    """
    Returns the first idle worker.
    """

    return (
        db.query(Worker)
        .filter(Worker.status == "idle")
        .order_by(Worker.heartbeat.asc())
        .first()
    )


def assign_job(
    db: Session,
    job: Job,
    worker: Worker,
):
    """
    Assign a job to a worker.
    """

    job.state = "running"

    worker.status = "busy"

    db.commit()

    db.refresh(job)
    db.refresh(worker)

    return job, worker