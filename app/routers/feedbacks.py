from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import aiofiles

from os import listdir
from os.path import isfile, join

from typing import Optional, List

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


@router.get("/img", response_class=FileResponse)
async def read_img(
    serial: Optional[str] = "00:00:00:00:00:00:00",
    date_time_str: Optional[str] = "2024-05-23-18-00-34-328+100"
    ):
    path="/Users/darshangadkari/Documents/Homeopath/uploaddata/"
    onlyFiles = [f for f in listdir(path) if isfile(join(path, f))]
    logger.info(f"About to return img for the serial: {serial} and date time : {date_time_str}")
    logger.info(onlyFiles)
    return FileResponse(
        path=f"{path}{serial.replace(':','_')}__{date_time_str}.png",
        filename=f"{serial.replace(':','_')}__{date_time_str}.png",
        media_type="image/png"
        )


@router.post("/create/", response_model=Optional[Feedback])
async def create_feedback(
    serial: Optional[str] = "Example: 00:00:00:00:00:00:00",
    summary: Optional[str] = "Example: Less Itchy",
    details: Optional[str] = "Example: There is some improvement, the rash is less itchy now",
    img_link: Optional[str] = "Example: /storage.azure.com/sgsgsrg",
    # feedback: FeedbackCreate,
    feedback_file: UploadFile = File(None),
    db: Session = Depends(get_db)
    ):
    feedback = FeedbackCreate(**{
        "serial": serial,
        "summary": summary,
        "details": details,
        "imgLink": img_link
    })
    # create feedback entry
    logger.info(f"feedback serial: {feedback.serial}")
    if not feedback_file:
        logger.info("feedback file: No upload file sent")
    else:
        logger.info(f"feedback file name: {feedback_file.filename}")
        logger.info(f"feedback file size: {feedback_file.size}")
        # save file to disk
        try:
            content = await feedback_file.read()  # async read
            async with aiofiles.open(
                f"/Users/darshangadkari/Documents/Homeopath/uploaddata/{feedback_file.filename}",
                'wb'
                ) as out_file:
                await out_file.write(content)  # async write
        except Exception as e:
            logger.error(f'Open file to save error: {e}')
            raise HTTPException(
                status_code=404,
                detail="Issue with opening the file to save"
                )
        finally:
            await feedback_file.close()

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
async def read_feedbacks(
    serial: Optional[str] = "00:00:00:00:00:00:00",
    db: Session = Depends(get_db)
    ):
    logger.info(f"About to read the feedback records in DB for: {serial}")
    return crud_get_feedbacks(db=db, serial=serial)

