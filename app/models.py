from pydantic import BaseModel, EmailStr


class TrackingInfo(BaseModel):
    email_usr: EmailStr
    number: int
