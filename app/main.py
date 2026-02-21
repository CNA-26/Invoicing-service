from fastapi import FastAPI
from app.routes import router
from app.database import Base, engine

app = FastAPI(
    title="Invoicing Service",
    version="Sprint 3"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}