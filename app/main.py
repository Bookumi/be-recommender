from fastapi import FastAPI
from app.routers import book
from app import models
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="recommender-service")

app.include_router(book.router)

@app.get("/")
def root():
    return {"message": "FastAPI service is running"}
