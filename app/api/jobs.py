from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services.job_service import (
    create_job,
    delete_job,
    get_job_by_id,
    get_jobs,
    update_job,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_job(
            db,
            job,
            current_user,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_jobs(
        db,
        current_user,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_job_by_id(
        db,
        job_id,
        current_user,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def edit_job(
    job_id: UUID,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_job_by_id(
        db,
        job_id,
        current_user,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return update_job(
        db,
        job,
        job_data,
    )


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = get_job_by_id(
        db,
        job_id,
        current_user,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    delete_job(
        db,
        job,
    )