from datetime import datetime

from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.models.job import Job
from app.models.worker import Worker


def complete_job(
    db: Session,
    job: Job,
    worker: Worker,
):
    """
    Simulate successful execution of a job.
    """

    job.state = "completed"

    worker.status = "idle"
    worker.heartbeat = datetime.utcnow()

    log = ExecutionLog(
        job_id=job.id,
        message=f"Job executed successfully by {worker.hostname}",
    )

    db.add(log)

    db.commit()

    db.refresh(job)
    db.refresh(worker)

    return log