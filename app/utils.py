import asyncio
from asyncio.tasks import Task
from typing import Any, Callable, Coroutine

from app.exceptions import TaskError


class TaskManager:
    """Task manager and scheduler that manages tasks in the same event loop."""

    def __init__(self) -> None:
        self.tasks: dict[str, Task[Any]] = {}

    async def get_task(self, task_name: str) -> Task[Any]:
        """Fetch the task object for a specified task.
        Args:
            task_name (str): The name assigned to the task object to retrieve.
        Returns:
            Task[Any]: A coroutine wrapped in a Future.
        """
        return self.tasks[task_name]

    async def start_task(
        self,
        coro_fn: Callable[..., Coroutine[Any, Any, Any]],
        task_name: str,
        *coro_args: Any,
    ) -> tuple[str, Task[Any]]:
        """
        Schedule the execution of a coroutine.
        Args:
            coro_fn (Callable[..., Coroutine[Any, Any, Any]]): The coroutine to
                execute.
            task_name (str): The name of the task to execute.
            execute_in (float): The execution time delay.

        Raises:
            TaskError: Raised when a task with the same `task_name` is already
                scheduled to run.

        Returns:
            tuple[str, Task[Any]]: The task name and `asyncio.Task` object.
        """
        if task_name in self.tasks:
            raise TaskError(f"'{task_name}' is already scheduled to run")

        async def wrapped_coro():
            try:
                return await coro_fn(*coro_args)
            finally:
                if task_name in self.tasks:
                    del self.tasks[task_name]

        loop = asyncio.get_running_loop()
        task = loop.create_task(wrapped_coro(), name=task_name)
        self.tasks[task_name] = task
        return task_name, task

    async def stop_task(self, task_name: str) -> bool:
        """Stop a task running in the background.
        Args:
            task_name (str): The name of the task to stop.

        Returns:
            bool: True if tasked was successfully stopped, False otherwise.
        """
        try:
            task = self.tasks[task_name]
            task.cancel()
            del self.tasks[task_name]
        except KeyError:
            return False

        return True
