from sqlalchemy.orm import Session

from app.models.dead_letter_queue import DeadLetterQueue
from app.models.job import Job


def move_to_dead_letter_queue(
    db: Session,
    job: Job,
    reason: str,
):
    """
    Move a permanently failed job into the Dead Letter Queue.
    """

    dead_job = DeadLetterQueue(
        original_job_id=job.id,
        payload=job.payload,
        reason=reason,
    )

    db.add(dead_job)

    db.commit()

    db.refresh(dead_job)

    return dead_job