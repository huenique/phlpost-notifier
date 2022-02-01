from smtplib import SMTP_SSL
from typing import Sequence


class Emailer:
    def __init__(self, domain: str) -> None:
        self.domain = domain

    def connect(self) -> "Emailer":
        self.conn = SMTP_SSL(self.domain)
        return self

    def disconnect(self) -> None:
        self.conn.__exit__(None, None, None)

    def identify(self) -> None:
        self.conn.ehlo_or_helo_if_needed()

    def login(self, user: str, passw: str) -> "Emailer":
        self.conn.login(user, passw)
        return self

    def sendmail(
        self,
        from_addr: str,
        to_addrs: str | Sequence[str],
        msg: bytes | str,
    ) -> None:
        self.conn.sendmail(from_addr, to_addrs, msg)

    @classmethod
    def start(cls, domain: str, email_usr: str, email_passw: str) -> "Emailer":
        return cls(domain).connect().login(email_usr, email_passw)
