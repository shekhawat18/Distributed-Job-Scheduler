from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.dead_letter_queue import DeadLetterQueue

router = APIRouter(
    prefix="/dlq",
    tags=["Dead Letter Queue"],
)


@router.get("")
def list_dead_letters(
    db: Session = Depends(get_db),
):
    return (
        db.query(DeadLetterQueue)
        .order_by(DeadLetterQueue.failed_at.desc())
        .all()
    )