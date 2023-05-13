import logging

from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse

from .base import ServiceExceptionBase

logger = logging.getLogger(__name__)


async def service_exception_handler(request: Request, exc: ServiceExceptionBase):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            dict(
                status_code=exc.status_code,
                status_message=exc.status_message,
                error_details=exc.error_message,
            )
        ),
    )
