from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.worker import Worker


def register_worker(
    db: Session,
    hostname: str,
) -> Worker:

    worker = Worker(
        hostname=hostname,
        status="idle",
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker


def get_workers(
    db: Session,
):
    return (
        db.query(Worker)
        .order_by(Worker.created_at.desc())
        .all()
    )


def get_worker(
    db: Session,
    worker_id: UUID,
):
    return (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
    )


def update_worker_status(
    db: Session,
    worker: Worker,
    status: str,
):
    worker.status = status
    worker.heartbeat = datetime.utcnow()

    db.commit()
    db.refresh(worker)

    return worker


def heartbeat(
    db: Session,
    worker: Worker,
):
    worker.heartbeat = datetime.utcnow()

    db.commit()
    db.refresh(worker)

    return worker


def delete_worker(
    db: Session,
    worker: Worker,
):
    db.delete(worker)
    db.commit()