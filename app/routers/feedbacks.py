from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from typing import Optional, List, Union, Annotated

from ..internal.schemas import (
    Feedback,
    FeedbackCreate
    )
from ..internal.crud import (
    crud_create_feedback,
    crud_get_feedbacks,
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
    db: Session = Depends(get_db),
    feedback_file: UploadFile = File(None)
    ):
    # create feedback entry
    logger.info(f"feedback serial: {feedback.serial}")
    if not feedback_file:
        logger.info("feedback file: No upload file sent")
    else:
        logger.info(f"feedback file name: {feedback_file.filename}")
        logger.info(f"feedback file size: {feedback_file.size}")

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


@router.get("/", response_model=List[Feedback])
def read_feedbacks(
    serial: Optional[str] = "00:00:00:00:00:00:00",
    db: Session = Depends(get_db)
    ):
    logger.info(f"About to read the feedback records in DB for: {serial}")
    return crud_get_feedbacks(db=db, serial=serial)

