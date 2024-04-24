from fastapi import APIRouter, Depends, HTTPException
from smtplib import SMTP_SSL

from typing import List, Optional

from ..internal.schemas import (
    Email,
    EmailEntry,
    EmailCreate
    )
from ..internal.common import logger
from ..internal.crud import (
    Session,
    crud_create_email,
    crud_get_emails
    )
from ..internal.databases import get_db
from ..internal.settings import settings


router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Email])
def read_emails(
    db: Session = Depends(get_db)
    ):
    return crud_get_emails(db=db)


def send_email(recipient, subject, body):
    if recipient[0] == "[" and recipient[-1] == "]":
        recipient = recipient[1:-1]
    recipient = recipient.replace(' ','').split(',')
    logger.info(f"recipient: {recipient}")

    # Prepare actual message
    message = f'From: {settings.gmail_user}\n' + \
        f'To: {", ".join(recipient)}\n' + \
            f'Subject: {subject}\n\n' + \
                f'{body}\n\n\n\nRegards\nReally Team'
    # logger.info(f"message: {message}")
    try:
        server = SMTP_SSL(settings.gmail_smtp_url, settings.gmail_smtp_port)
        server.ehlo()
        server.login(settings.gmail_user, settings.gmail_app_pwd)
        server.sendmail(settings.gmail_user, recipient, message)
        server.close()
        return True, None
    except Exception as e:
        logger.error(f"failed to send mail: {e}")
        return False, "failed to send mail"


@router.post("/send/", response_model=Optional[Email])
def create_and_send_email(
    email: EmailEntry,
    db: Session = Depends(get_db)
    ):
    # send email
    logger.info(f"email: {email.subject}")
    email_status = send_email(
        recipient=email.recipient,
        subject=email.subject,
        body=email.body
        )
    logger.info(f"Email sent: {email_status[0]}")
    if email_status[0]:
        email = EmailCreate(**(email.__dict__))
        email.status = "Sent"
        email.error = None
    else:
        logger.error(f'Send email error')
        email = EmailCreate(**(email.__dict__))
        email.status = "Not Sent"
        email.error = email_status[1]

    # create email entry in the DB
    try:
        logger.info(f"About to write the email record in DB: {email.subject}")
        return crud_create_email(db=db, email=email)
    except Exception as e:
        logger.error(f'Create email record error: {e}')
        raise HTTPException(
            status_code=404,
            detail="Issue with creating Email Record to DB"
            )

