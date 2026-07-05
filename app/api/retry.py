from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.job import Job
from app.models.worker import Worker
from app.scheduler.retry_service import retry_or_fail_job

router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"],
)


@router.post("/fail/{job_id}")
def fail_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.state == "running",
        )
        .first()
    )

    if job is None:
        return {
            "message": "Running job not found"
        }

    worker = (
        db.query(Worker)
        .filter(Worker.status == "busy")
        .first()
    )

    if worker is None:
        return {
            "message": "No busy worker found"
        }

    result = retry_or_fail_job(
        db,
        job,
        worker,
    )

    return result