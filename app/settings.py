# type: ignore
from decouple import config

EMAIL_USR: str = config("SERVICE_EMAIL_USER", cast=str)

EMAIL_PASSW: str = config("SERIVCE_EMAIL_PASSWORD", cast=str)

PHLPOST_URL = "https://tracking.phlpost.gov.ph/HOME/GetSummary"

EMAIL_DOMAIN = "smtp.gmail.com"
