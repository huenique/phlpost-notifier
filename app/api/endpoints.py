from fastapi import APIRouter, Depends

from app import models
from app.api.dependencies import get_task_manager
from app.services.tasks import TaskService

router = APIRouter()


@router.get("/")
async def read_root() -> dict[str, str]:
    # TODO: show table of users registerd waiting for an email notification
    return {"Hello": "World"}


@router.post("/track")
async def track(
    info: models.TrackingInfo, task: TaskService = Depends(get_task_manager)
) -> str:
    return await task.track_number(info.email_usr, info.tracking_number)


@router.delete("/track/")
async def untrack(untrack: int, task: TaskService = Depends(get_task_manager)) -> bool:
    return await task.untrack_number(untrack)
