from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.devices import router as device_router
from app.routers.sync_spaces import router as sync_space_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server startup...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Server shutdown...")

app = FastAPI(title="Filesync Backend",
            lifespan=lifespan)

"""@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)"""
# on_event Deprecated, hence using Lifespan parameter

app.include_router(device_router)
app.include_router(sync_space_router)

@app.get("/health", tags=["health check"])
def health_check():
    return {"status":"ok"}
