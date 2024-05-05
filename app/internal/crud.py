from sqlalchemy.orm import Session
import re

from . import models, schemas
from ..internal.common import logger


def crud_get_emails(db: Session, skip: int = 0, limit: int = 100, source: str = "Comparison"):
    return db.query(models.Emails).\
        filter(models.Emails.source == source).\
            offset(skip).\
                limit(limit).\
                    all()


def crud_create_email(db: Session, email: schemas.EmailCreate):
    # insert into emails table
    db_email = models.Emails(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


def crud_get_sn_from_enb(enb: str):
    search_object = re.search("\d{12}.{2}[A-Z]{1}\d{4}", enb)
    if search_object:
        return_object = schemas.SN(**{
            "serialNumber": search_object.group(0),
            "eNB": enb,
            "status": "success"
        })
    else:
        return_object = schemas.SN(**{
            "serialNumber": None,
            "eNB": enb,
            "status": "failure"
        })
    logger.info(return_object)
    return return_object


def crud_create_classification(db: Session, classification: schemas.ClassificationCreate):
    # insert into classification table
    db_classfication = models.Classifications(**classification.dict())
    db.add(db_classfication)
    db.commit()
    db.refresh(db_classfication)
    return db_classfication


def crud_create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    # insert into feedback table
    db_feedback = models.Feedbacks(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def crud_get_feedbacks(db: Session, skip: int = 0, limit: int = 100, serial: str = "00:00:00:00:00:00:00"):
    return db.query(models.Feedbacks).\
        filter(models.Feedbacks.serial == serial).\
            offset(skip).\
                limit(limit).\
                    all()

