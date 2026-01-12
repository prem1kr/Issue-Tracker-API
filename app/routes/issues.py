from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Issue
from ..schemas import IssueCreate, IssueUpdate
from fastapi import UploadFile, File
from app.utils.csv_import import import_issues_from_csv

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/")
def create_issue(data: IssueCreate, db: Session = Depends(get_db)):
    issue = Issue(**data.dict())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue

@router.get("/")
def list_issues(db: Session = Depends(get_db)):
    return db.query(Issue).all()

@router.get("/{issue_id}")
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(404, "Issue not found")
    return issue

@router.patch("/{issue_id}")
def update_issue(issue_id: int, data: IssueUpdate, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    if issue.version != data.version:
        raise HTTPException(409, "Version conflict")

    for k, v in data.dict(exclude={"version"}).items():
        if v is not None:
            setattr(issue, k, v)

    issue.version += 1
    db.commit()
    return issue

@router.post("/import")
def import_issues(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files allowed")

    return import_issues_from_csv(db, file)
