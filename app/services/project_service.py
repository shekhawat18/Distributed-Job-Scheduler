from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(
    db: Session,
    project_data: ProjectCreate,
    current_user: User,
) -> Project:
    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(
    db: Session,
    current_user: User,
):
    return (
        db.query(Project)
        .filter(Project.owner_id == current_user.id)
        .order_by(Project.created_at.desc())
        .all()
    )


def get_project_by_id(
    db: Session,
    project_id,
    current_user: User,
):
    return (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
):
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project


def delete_project(
    db: Session,
    project: Project,
):
    db.delete(project)
    db.commit()