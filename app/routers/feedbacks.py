from fastapi import APIRouter, Depends, HTTPException

from typing import Optional

from ..internal.schemas import (
    Feedback,
    FeedbackCreate
    )
from ..internal.crud import (
    crud_create_feedback,
    Session
    )
from ..internal.common import logger
from ..internal.databases import get_db


router = APIRouter(
    prefix="/feedback",
    tags=["feedback"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create/", response_model=Optional[Feedback])
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
    ):
    # create feedback entry
    logger.info(f"feedback serial: {feedback.serial}")

    # create feedback entry in the DB
    try:
        logger.info(f"About to write the feedback record in DB: {feedback.summary}")
        return crud_create_feedback(db=db, feedback=feedback)
    except Exception as e:
        logger.error(f'Create feedback record error: {e}')
        raise HTTPException(
            status_code=404,
            detail="Issue with creating Feedback Record to DB"
            )

