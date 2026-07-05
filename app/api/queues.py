from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.queue import (
    QueueCreate,
    QueueResponse,
    QueueUpdate,
)
from app.services.queue_service import (
    create_queue,
    delete_queue,
    get_queue_by_id,
    get_queues,
    pause_queue,
    resume_queue,
    update_queue,
)

router = APIRouter(
    prefix="/queues",
    tags=["Queues"],
)


@router.post(
    "",
    response_model=QueueResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_queue(
    queue: QueueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_queue(
            db,
            queue,
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[QueueResponse],
)
def list_queues(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_queues(
        db,
        current_user,
    )


@router.get(
    "/{queue_id}",
    response_model=QueueResponse,
)
def get_queue(
    queue_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue = get_queue_by_id(
        db,
        queue_id,
        current_user,
    )

    if queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found",
        )

    return queue


@router.put(
    "/{queue_id}",
    response_model=QueueResponse,
)
def edit_queue(
    queue_id: UUID,
    queue_data: QueueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue = get_queue_by_id(
        db,
        queue_id,
        current_user,
    )

    if queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found",
        )

    return update_queue(
        db,
        queue,
        queue_data,
    )


@router.delete(
    "/{queue_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_queue(
    queue_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue = get_queue_by_id(
        db,
        queue_id,
        current_user,
    )

    if queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found",
        )

    delete_queue(
        db,
        queue,
    )


@router.post(
    "/{queue_id}/pause",
    response_model=QueueResponse,
)
def pause_selected_queue(
    queue_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue = get_queue_by_id(
        db,
        queue_id,
        current_user,
    )

    if queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found",
        )

    return pause_queue(
        db,
        queue,
    )


@router.post(
    "/{queue_id}/resume",
    response_model=QueueResponse,
)
def resume_selected_queue(
    queue_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    queue = get_queue_by_id(
        db,
        queue_id,
        current_user,
    )

    if queue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found",
        )

    return resume_queue(
        db,
        queue,
    )