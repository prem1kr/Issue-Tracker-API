from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models import Issue, User

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/top-assignees")
def top_assignees(db: Session = Depends(get_db)):
    return db.query(
        User.name,
        func.count(Issue.id)
    ).join(Issue).group_by(User.name).all()

@router.get("/latency")
def avg_resolution_time(db: Session = Depends(get_db)):
    return db.query(
        func.avg(Issue.resolved_at - Issue.created_at)
    ).scalar()
