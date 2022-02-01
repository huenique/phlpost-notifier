from starlette.requests import Request

from app.services.tasks import TaskService


def get_task_manager(request: Request) -> TaskService:
    return request.app.state.tasks
