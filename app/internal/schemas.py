from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class EmailEntry(BaseModel):
    source: Optional[str] = "Example: Comparison"
    purpose: Optional[str] = "Example: Validation Error Email"
    recipient: Optional[str] = "Example (multiple emails separated by commas): dgadkari@gmail.com"
    subject: Optional[str] = "Example: Plan Name Validation"
    body: Optional[str] = "Example: Body of the email...."


class EmailBase(EmailEntry):
    status: Optional[str] = ""
    error: Optional[str] = ""


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: Optional[int]
    createdDatetime: Optional[datetime]
    updatedDatetime: Optional[datetime]

    class Config:
        orm_mode = True


class ClassificationBase(BaseModel):
    serial: Optional[str] = "Example: 00000000"
    className: Optional[str] = "Example: Eczema"
    classId: Optional[int] = "Example: 8"
    score: Optional[float] = "Example: 0.1"
    batch: Optional[str] = "Example: 2024:04:22:16:14:25:234345"


class ClassificationCreate(ClassificationBase):
    pass


class Classification(ClassificationBase):
    id: Optional[int]
    createdDatetime: Optional[datetime]
    updatedDatetime: Optional[datetime]

    class Config:
        orm_mode = True

