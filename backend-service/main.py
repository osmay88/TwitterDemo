from fastapi import FastAPI

from TwitterDemo.db import create_tables
from TwitterDemo.routes import router
from TwitterDemo.api_routes import router as api_router

app = FastAPI()
app.include_router(router)
app.include_router(api_router)


@app.on_event("startup")
async def initialize():
    await create_tables()
