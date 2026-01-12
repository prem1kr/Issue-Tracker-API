from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Comment, Issue
from ..schemas import CommentCreate

router = APIRouter(prefix="/issues", tags=["Comments"])

@router.post("/{issue_id}/comments")
def add_comment(issue_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    if not data.body.strip():
        raise HTTPException(400, "Empty comment")

    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(404, "Issue not found")

    comment = Comment(issue_id=issue_id, **data.dict())
    db.add(comment)
    db.commit()
    return comment
