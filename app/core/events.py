from typing import Any, Callable, Coroutine

from fastapi import FastAPI
from loguru import logger

from app.db.operations import Database
from app.services.tasks import TaskService
from app.settings import DATABASE_URL


def create_start_app_handler(app: FastAPI) -> Callable[..., Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        app.state.tasks = TaskService(await Database.start_connection(DATABASE_URL))

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable[..., Coroutine[Any, Any, None]]:
    @logger.catch
    async def stop_app() -> None:
        await app.state.tasks.close()

    return stop_app
