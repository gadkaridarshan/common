from fastapi import APIRouter, Depends, HTTPException

from typing import Optional

from ..internal.schemas import (
    Classification,
    ClassificationCreate
    )
from ..internal.crud import (
    crud_create_classification,
    Session
    )
from ..internal.common import logger
from ..internal.databases import get_db


router = APIRouter(
    prefix="/classification",
    tags=["classification"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create/", response_model=Optional[Classification])
def create_classification(
    classification: ClassificationCreate,
    db: Session = Depends(get_db)
    ):
    # send email
    logger.info(f"classification batch: {classification.batch}")

    # create classification entry in the DB
    try:
        logger.info(f"About to write the classification record in DB: {classification.className}")
        return crud_create_classification(db=db, classification=classification)
    except Exception as e:
        logger.error(f'Create classification record error: {e}')
        raise HTTPException(
            status_code=404,
            detail="Issue with creating Classification Record to DB"
            )


