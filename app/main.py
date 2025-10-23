from fastapi import FastAPI

app = FastAPI(title="recommender-service")

@app.get("/")
def root():
  return {"message": "FastAPI service is running"}