from fastapi import FastAPI

from app import models, services

app = FastAPI()
task = services.TaskService()


@app.get("/")
async def read_root():
    # TODO: show table of users registerd waiting for an email notification
    return {"Hello": "World"}


@app.post("/track")
async def track(info: models.TrackingInfo):
    await task.track_number(info.email_usr, info.number, 5.0)
    return info
