import asyncio

import aiohttp

from app import utils
from app.clients import emailer, tracker
from app.settings import EMAIL_DOMAIN, EMAIL_PASSW, EMAIL_USR, PHLPOST_URL


class TaskService:
    def __init__(self) -> None:
        self.loop = asyncio.get_running_loop()
        self.http = aiohttp.ClientSession()
        self.task = utils.TaskManager()
        self.mail = emailer.Emailer.start(EMAIL_DOMAIN, EMAIL_USR, EMAIL_PASSW)
        self.trac = tracker.Tracker.start(self.http, self.mail, PHLPOST_URL, self.loop)

    async def track_number(
        self,
        email_usr: str,
        tracking_number: int,
        execute_in: float = 86_400.0,
    ) -> str:
        task_nm, _ = await self.task.start_task(
            self.trac.check_status,
            str(tracking_number),
            EMAIL_USR,
            email_usr,
            tracking_number,
            execute_in,
        )
        return task_nm

    async def untrack_number(self, tracking_number: int) -> bool:
        return await self.task.stop_task(str(tracking_number))
        # remove number from database
