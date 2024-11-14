import asyncio
import logging
import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.config import settings
from api import api_router
from core.logging_config import setup_logging
from rabbitmq import start_broker, app_rb

setup_logging()

logger = logging.getLogger(__name__)


async def lifespan(app: FastAPI):
    await start_broker()
    broker_task = asyncio.create_task(app_rb.run())

    yield
    # await stop_broker()
    try:
        await broker_task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": [
                {
                    "msg": error["msg"],
                    "type": error["type"],
                }
                for error in exc.errors()
            ]
        },
    )


app.include_router(api_router, prefix=settings.api_prefix.prefix)