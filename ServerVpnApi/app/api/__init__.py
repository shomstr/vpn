from fastapi import FastAPI, APIRouter, Depends

from app.config import server_config
from app.utils.token import validate_connection_token

from .vpn_server import vpn_server


root_router = APIRouter()

@root_router.get("/")
async def root(token: str = Depends(validate_connection_token)) -> dict:
    return {
        "location": server_config["info"]["location"],
        "ip": server_config["server_config"]["ip"],
        "port": server_config["server_config"]["ip"],
        "status": "running",

    }


routers: list[APIRouter] = [root_router, vpn_server]

def setup_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)