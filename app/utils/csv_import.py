import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.models import Issue


def import_issues_from_csv(db: Session, file):
    """
    CSV columns expected:
    title, description, status
    """

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))

    created = 0
    failed = []

    for index, row in enumerate(reader, start=1):
        title = row.get("title")
        description = row.get("description")
        status = row.get("status", "open")

        if not title:
            failed.append({
                "row": index,
                "error": "Title is required"
            })
            continue

        issue = Issue(
            title=title.strip(),
            description=description,
            status=status
        )

        db.add(issue)
        created += 1

    db.commit()

    return {
        "created": created,
        "failed": failed
    }
