import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import setup_routers
from app.config import server_config
from app.middlewares import setup_middlewares
from app.settings import settings
from app.utils.log import init_logger
import uvicorn

init_logger()
logger = logging.getLogger(f"uvicorn.{__name__}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server API was started")
    cfg = server_config["server_config"]

    logger.info(f"Xray worked in ip: {cfg['ip']}, port: {cfg['port']}")

    yield
    logger.info("API was shutdown")


def main():
    app = FastAPI(
        title="VPN Manager API",
        description="API для управления коммерческим VPN сервисом",
        version="1.0.0",
        lifespan=lifespan
    )
    setup_middlewares(app)
    setup_routers(app)

    uvicorn.run(app, host="0.0.0.0", port=8082)

if __name__ == "__main__":
    main()