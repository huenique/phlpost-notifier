from fastapi import FastAPI

from app import models, services

app = FastAPI()
task = services.TaskService()


@app.get("/")
async def read_root() -> dict[str, str]:
    # TODO: show table of users registerd waiting for an email notification
    return {"Hello": "World"}


@app.post("/track")
async def track(info: models.TrackingInfo) -> str:
    return await task.track_number(info.email_usr, info.tracking_number)


@app.delete("/track/")
async def untrack(untrack: int) -> bool:
    return await task.untrack_number(untrack)
