from fastapi import FastAPI
from app.routers import book, auth, users, genre
from app import models
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.recommenders.faiss import load_index
from app.recommenders.cf_svd import load_svd_and_user_items_dict
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="recommender-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(genre.router)

@app.on_event("startup")
def startup_event():
    load_index(
        os.getenv("PATH_TO_FAISS_INDEX_EN"),
        os.getenv("PATH_TO_FAISS_ID_MAPPING_EN"),
        os.getenv("PATH_TO_FAISS_INDEX_IND"),
        os.getenv("PATH_TO_FAISS_ID_MAPPING_IND")
    )

    load_svd_and_user_items_dict(
        os.getenv("PATH_TO_SVD_MODEL"),
    )

@app.get("/")
def root():
    return {"message": "FastAPI service is running"}
