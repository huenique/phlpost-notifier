from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class PackageOwner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    tracking_number: int
