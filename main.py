from fastapi import FastAPI

from TwitterDemo.db import create_tables
from TwitterDemo.routes import router

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def initialize():
    await create_tables()
