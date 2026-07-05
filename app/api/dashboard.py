from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.dashboard_service import (
    get_dashboard_overview,
    get_recent_jobs,
    get_recent_workers,
    get_recent_queues,
    get_recent_executions,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/overview")
def overview(
    db: Session = Depends(get_db),
):
    return get_dashboard_overview(db)


@router.get("/jobs")
def jobs(
    db: Session = Depends(get_db),
):
    return get_recent_jobs(db)


@router.get("/workers")
def workers(
    db: Session = Depends(get_db),
):
    return get_recent_workers(db)


@router.get("/queues")
def queues(
    db: Session = Depends(get_db),
):
    return get_recent_queues(db)


@router.get("/executions")
def executions(
    db: Session = Depends(get_db),
):
    return get_recent_executions(db)