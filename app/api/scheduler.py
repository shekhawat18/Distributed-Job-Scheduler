from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.worker import Worker
from app.scheduler.execution_service import complete_job
from app.db.database import get_db
from app.scheduler.scheduler_service import (
    assign_job,
    get_available_worker,
    get_next_job,
)

router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"],
)


@router.post("/run-once")
def run_scheduler_once(
    db: Session = Depends(get_db),
):
    job = get_next_job(db)

    if job is None:
        return {
            "message": "No queued jobs available"
        }

    worker = get_available_worker(db)

    if worker is None:
        return {
            "message": "No idle workers available"
        }

    assign_job(
        db,
        job,
        worker,
    )

    return {
        "message": "Job assigned successfully",
        "job_id": str(job.id),
        "worker_id": str(worker.id),
        "job_state": job.state,
        "worker_status": worker.status,
    }

@router.post("/complete/{job_id}")
def complete_running_job(
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

    log = complete_job(
        db,
        job,
        worker,
    )

    return {
        "message": "Job completed successfully",
        "job_id": str(job.id),
        "worker": worker.hostname,
        "execution_log": str(log.id),
    }