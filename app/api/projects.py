from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import (
    create_project,
    delete_project,
    get_project_by_id,
    get_projects,
    update_project,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_project(
        db,
        project,
        current_user,
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_projects(
        db,
        current_user,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(
        db,
        project_id,
        current_user,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def edit_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(
        db,
        project_id,
        current_user,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return update_project(
        db,
        project,
        project_data,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(
        db,
        project_id,
        current_user,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    delete_project(
        db,
        project,
    )