from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.project import Project
from app.models.queue import Queue
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate


def create_job(
    db: Session,
    job_data: JobCreate,
    current_user: User,
) -> Job:
    queue = (
        db.query(Queue)
        .join(Project)
        .filter(
            Queue.id == job_data.queue_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if queue is None:
        raise ValueError("Queue not found")

    job = Job(
        queue_id=job_data.queue_id,
        retry_policy_id=job_data.retry_policy_id,
        type=job_data.type,
        payload=job_data.payload,
        priority=job_data.priority,
        run_after=job_data.run_after or datetime.utcnow(),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_jobs(
    db: Session,
    current_user: User,
):
    return (
        db.query(Job)
        .join(Queue)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
        .order_by(Job.created_at.desc())
        .all()
    )


def get_job_by_id(
    db: Session,
    job_id: UUID,
    current_user: User,
):
    return (
        db.query(Job)
        .join(Queue)
        .join(Project)
        .filter(
            Job.id == job_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )


def update_job(
    db: Session,
    job: Job,
    job_data: JobUpdate,
):
    if job_data.type is not None:
        job.type = job_data.type

    if job_data.payload is not None:
        job.payload = job_data.payload

    if job_data.priority is not None:
        job.priority = job_data.priority

    if job_data.state is not None:
        job.state = job_data.state

    if job_data.run_after is not None:
        job.run_after = job_data.run_after

    db.commit()
    db.refresh(job)

    return job


def delete_job(
    db: Session,
    job: Job,
):
    db.delete(job)
    db.commit()