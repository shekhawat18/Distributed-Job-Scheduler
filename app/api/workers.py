from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.worker import (
    WorkerHeartbeat,
    WorkerRegister,
    WorkerResponse,
)
from app.services.worker_service import (
    delete_worker,
    get_worker,
    get_workers,
    heartbeat,
    register_worker,
    update_worker_status,
)

router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)


@router.post(
    "",
    response_model=WorkerResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_new_worker(
    request: WorkerRegister,
    db: Session = Depends(get_db),
):
    return register_worker(
        db,
        request.hostname,
    )


@router.get(
    "",
    response_model=list[WorkerResponse],
)
def list_workers(
    db: Session = Depends(get_db),
):
    return get_workers(db)


@router.get(
    "/{worker_id}",
    response_model=WorkerResponse,
)
def get_worker_by_id(
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    worker = get_worker(
        db,
        worker_id,
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    return worker


@router.post(
    "/{worker_id}/heartbeat",
    response_model=WorkerResponse,
)
def worker_heartbeat(
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    worker = get_worker(
        db,
        worker_id,
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    return heartbeat(
        db,
        worker,
    )


@router.put(
    "/{worker_id}/status",
    response_model=WorkerResponse,
)
def update_status(
    worker_id: UUID,
    request: WorkerHeartbeat,
    db: Session = Depends(get_db),
):
    worker = get_worker(
        db,
        worker_id,
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    return update_worker_status(
        db,
        worker,
        request.status,
    )


@router.delete(
    "/{worker_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_worker(
    worker_id: UUID,
    db: Session = Depends(get_db),
):
    worker = get_worker(
        db,
        worker_id,
    )

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found",
        )

    delete_worker(
        db,
        worker,
    )