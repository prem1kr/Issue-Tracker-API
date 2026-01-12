from pydantic import BaseModel
from typing import List, Optional

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None

class IssueUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    version: int

class CommentCreate(BaseModel):
    author_id: int
    body: str

class LabelUpdate(BaseModel):
    labels: List[str]
