from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

issue_labels = Table(
    "issue_labels",
    Base.metadata,
    Column("issue_id", Integer, ForeignKey("issues.id")),
    Column("label_id", Integer, ForeignKey("labels.id")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="open")
    assignee_id = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)

    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime)

    comments = relationship("Comment", back_populates="issue", cascade="all,delete")
    labels = relationship("Label", secondary=issue_labels, back_populates="issues")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey("issues.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    issue = relationship("Issue", back_populates="comments")

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    issues = relationship("Issue", secondary=issue_labels, back_populates="labels")
