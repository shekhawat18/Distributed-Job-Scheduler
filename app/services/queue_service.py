from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.queue import Queue
from app.models.user import User
from app.schemas.queue import QueueCreate, QueueUpdate


def create_queue(
    db: Session,
    queue_data: QueueCreate,
    current_user: User,
) -> Queue:
    project = (
        db.query(Project)
        .filter(
            Project.id == queue_data.project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise ValueError("Project not found")

    queue = Queue(
        project_id=queue_data.project_id,
        name=queue_data.name,
        priority=queue_data.priority,
        concurrency_limit=queue_data.concurrency_limit,
    )

    db.add(queue)
    db.commit()
    db.refresh(queue)

    return queue


def get_queues(
    db: Session,
    current_user: User,
):
    return (
        db.query(Queue)
        .join(Project)
        .filter(Project.owner_id == current_user.id)
        .order_by(Queue.created_at.desc())
        .all()
    )


def get_queue_by_id(
    db: Session,
    queue_id: UUID,
    current_user: User,
):
    return (
        db.query(Queue)
        .join(Project)
        .filter(
            Queue.id == queue_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )


def update_queue(
    db: Session,
    queue: Queue,
    queue_data: QueueUpdate,
):
    if queue_data.name is not None:
        queue.name = queue_data.name

    if queue_data.priority is not None:
        queue.priority = queue_data.priority

    if queue_data.concurrency_limit is not None:
        queue.concurrency_limit = queue_data.concurrency_limit

    if queue_data.is_paused is not None:
        queue.is_paused = queue_data.is_paused

    db.commit()
    db.refresh(queue)

    return queue


def delete_queue(
    db: Session,
    queue: Queue,
):
    db.delete(queue)
    db.commit()


def pause_queue(
    db: Session,
    queue: Queue,
):
    queue.is_paused = True
    db.commit()
    db.refresh(queue)

    return queue


def resume_queue(
    db: Session,
    queue: Queue,
):
    queue.is_paused = False
    db.commit()
    db.refresh(queue)

    return queue