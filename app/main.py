from fastapi import FastAPI
from app.routers import book
from app import models
from app.database import engine, Base
from app.recommenders.faiss import load_index
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="recommender-service")

app.include_router(book.router)

@app.on_event("startup")
def startup_event():
    load_index(
        os.getenv("PATH_TO_FAISS_INDEX_EN"),
        os.getenv("PATH_TO_FAISS_ID_MAPPING_EN"),
        os.getenv("PATH_TO_FAISS_INDEX_IND"),
        os.getenv("PATH_TO_FAISS_ID_MAPPING_IND")
    )

@app.get("/")
def root():
    return {"message": "FastAPI service is running"}
