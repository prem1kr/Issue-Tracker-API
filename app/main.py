from fastapi import FastAPI
from app.db import engine, Base
from app.routes import issues, comments, labels, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Issue Tracker API")

app.include_router(issues.router)
app.include_router(comments.router)
app.include_router(labels.router)
app.include_router(reports.router)
