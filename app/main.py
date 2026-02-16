from fastapi import FastAPI
from app.routes import router
from app.database import Base, engine
from app import db_models

app = FastAPI(
    title="Invoicing Service API",
    version="Sprint 2"
)

# Automatically create tables in Postgres
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}