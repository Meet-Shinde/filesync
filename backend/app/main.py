from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models

app = FastAPI(title="Filesync Backend")

"""@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)"""
# on_event Deprecated, hence using Lifespan parameter

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Server shutdown...")

@app.get("/health")
def health_check():
    return {"status":"ok"}
