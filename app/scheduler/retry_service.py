from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog
from app.models.job import Job
from app.models.worker import Worker
from app.scheduler.dlq_service import move_to_dead_letter_queue


def retry_or_fail_job(
    db: Session,
    job: Job,
    worker: Worker,
):
    """
    Retry a failed job or move it to the Dead Letter Queue
    when the maximum retry limit has been reached.
    """

    # Release worker
    worker.status = "idle"
    worker.heartbeat = datetime.utcnow()

    # Increment retry count
    job.attempts += 1

    # No retry policy attached
    if job.retry_policy is None:
        job.state = "failed"

        log = ExecutionLog(
            job_id=job.id,
            message="Job failed (no retry policy).",
        )

        db.add(log)
        db.commit()

        return {
            "status": "failed",
            "attempts": job.attempts,
        }

    max_attempts = job.retry_policy.max_attempts

    # Retry limit reached
    if job.attempts >= max_attempts:
        job.state = "failed"

        dead_job = move_to_dead_letter_queue(
            db=db,
            job=job,
            reason="Maximum retry attempts reached.",
        )

        log = ExecutionLog(
            job_id=job.id,
            message="Job moved to Dead Letter Queue.",
        )

        db.add(log)
        db.commit()

        return {
            "status": "dead_letter",
            "attempts": job.attempts,
            "dead_letter_id": str(dead_job.id),
        }

    # Retry with delay
    delay = job.retry_policy.initial_delay

    if job.retry_policy.strategy == "exponential":
        delay = delay * (2 ** (job.attempts - 1))

    job.state = "queued"
    job.run_after = datetime.utcnow() + timedelta(seconds=delay)

    log = ExecutionLog(
        job_id=job.id,
        message=f"Retry scheduled in {delay} seconds.",
    )

    db.add(log)
    db.commit()

    return {
        "status": "retrying",
        "attempts": job.attempts,
        "next_run": job.run_after,
    }