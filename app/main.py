from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.api.errors import http_error_handler
from app.api.routes import router as api_router
from app.core.events import create_start_app_handler, create_stop_app_handler


def start_application() -> FastAPI:
    app = FastAPI(title="APP_NAME", debug=True, version="APP_VERSION")

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", create_start_app_handler(app))  # type: ignore
    app.add_event_handler("shutdown", create_stop_app_handler(app))  # type: ignore

    app.add_exception_handler(HTTPException, http_error_handler)  # type: ignore

    app.include_router(api_router)

    return app


app = start_application()
