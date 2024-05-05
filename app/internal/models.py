from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from .databases import Base


class Emails(Base):
    __tablename__ = 'emails'

    __table_args__ = {'schema': 'common'}

    id  = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=True)
    purpose = Column(String, nullable=True)
    recipient = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    body = Column(String, nullable=True)
    status = Column(String, nullable=True)
    error = Column(String, nullable=True)
    createdDatetime = Column(DateTime(timezone=True), server_default=func.now())
    updatedDatetime = Column(DateTime(timezone=True), onupdate=func.now())


class Classifications(Base):
    __tablename__ = 'classification'

    __table_args__ = {'schema': 'common'}

    id  = Column(Integer, primary_key=True, index=True)
    serial = Column(String, nullable=True)
    className = Column(String, nullable=True)
    classId = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    batch = Column(String, nullable=True)
    createdDatetime = Column(DateTime(timezone=True), server_default=func.now())
    updatedDatetime = Column(DateTime(timezone=True), onupdate=func.now())


class Feedbacks(Base):
    __tablename__ = 'feedback'

    __table_args__ = {'schema': 'common'}
    id  = Column(Integer, primary_key=True, index=True)
    serial = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    details = Column(String, nullable=True)
    imgLink = Column(String, nullable=True)
    createdDatetime = Column(DateTime(timezone=True), server_default=func.now())
    updatedDatetime = Column(DateTime(timezone=True), onupdate=func.now())

