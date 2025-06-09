# backend/api/main.py
from fastapi import FastAPI

app = FastAPI(title="CTI Dashboard API")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "CTI Dashboard API is up!"}
