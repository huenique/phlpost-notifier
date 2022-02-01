import asyncio
import json
from http.client import HTTPException
from typing import Any

from loguru import logger
from pydantic import EmailStr

from app.db.operations import Database
from app.services import models


class Tracker:
    def __init__(
        self, http: Any, mail: Any, request_url: str, loop: asyncio.AbstractEventLoop
    ) -> None:
        self.loop = loop
        self.http = http
        self.mail = mail
        self.request_url = request_url

    async def _parse_response(self, data: str | bytes) -> bool:
        data_ = json.loads(data)

        if (
            data_["InqOV"][0]["Total"] != 0
            and "not found" not in data_["InqItems"][0]["Status"].lower()
        ):
            return True

        return False

    async def _check_response(self, resp: Any) -> bool:
        if resp.status == 200:
            if await self._parse_response(await resp.text()):
                return True
            else:
                return False
        else:
            raise HTTPException(f"server return a {resp.status} response")

    async def notify_user(
        self, from_email: str, email_usr: str, tracking_num: int
    ) -> None:
        message = "Subject: {}\n\n{}".format(
            "PHLPost",
            f"Your item is out for delivery.\nTracking number: {tracking_num}",
        )
        self.loop.run_in_executor(
            None,
            self.mail.sendmail,
            from_email,
            email_usr,
            message,
        )

    @logger.catch(asyncio.exceptions.CancelledError, level=1, message=f"task cancelled")
    async def check_status(
        self,
        from_email: str,
        email_usr: str,
        tracking_num: int,
        exec_in: float,
        db_conn: Database,
    ) -> None:
        await db_conn.add_row(
            models.PackageOwner(email=EmailStr(email_usr), tracking_number=tracking_num)
        )

        while True:
            await asyncio.sleep(exec_in)

            # Loop through the tracking numbers table and asynchronously query phlpost
            # for each row
            tracking_nums = await db_conn.get_all_row(models.PackageOwner)

            for num in tracking_nums:
                resp = await self.http.post(
                    self.request_url, json={"TrackingNos": [f"{num}"]}
                )

                # If package with tracking number is out for deliver, notify user and
                # delete associated row
                if await self._check_response(resp):
                    await self.notify_user(from_email, email_usr, tracking_num)
                    self.mail.disconnect()

    @classmethod
    def start(
        cls, http: Any, mail: Any, request_url: str, loop: asyncio.AbstractEventLoop
    ) -> "Tracker":
        return cls(http, mail, request_url, loop)
