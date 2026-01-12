from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Issue, Label
from ..schemas import LabelUpdate

router = APIRouter(prefix="/issues", tags=["Labels"])

@router.put("/{issue_id}/labels")
def replace_labels(issue_id: int, data: LabelUpdate, db: Session = Depends(get_db)):
    issue = db.get(Issue, issue_id)
    labels = []

    for name in data.labels:
        label = db.query(Label).filter_by(name=name).first()
        if not label:
            label = Label(name=name)
            db.add(label)
        labels.append(label)

    issue.labels = labels
    db.commit()
    return {"labels": data.labels}
