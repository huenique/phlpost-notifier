from asyncio import Task
from typing import Any

from fastapi import FastAPI

from app import models, services

app = FastAPI()
task = services.TaskService()


@app.get("/")
async def read_root():
    # TODO: show table of users registerd waiting for an email notification
    return {"Hello": "World"}


@app.post("/track")
async def track(info: models.TrackingInfo) -> tuple[str, Task[Any]]:
    return await task.track_number(info.email_usr, info.tracking_number)


@app.post("/untrack")
async def untrack(tracking_number: int):
    return await task.untrack_number(tracking_number)
