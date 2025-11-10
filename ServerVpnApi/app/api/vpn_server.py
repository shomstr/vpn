import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.utils.token import validate_connection_token
from app.utils.xray import xray_manager, vless_manager

vpn_server = APIRouter(prefix="/server")

@vpn_server.post("/create")
async def add_client(
        telegram_id: int,
        token: str = Depends(validate_connection_token),
):
    # await xray_manager.add_client_to_config(telegram_id)
    # vless_config = vless_manager.generate_vless_url(telegram_id)
    vless_config = uuid.uuid4()

    return {
        "info": "Конфиг был создан",
        "vless_config": vless_config
    }


@vpn_server.delete("/delete")
async def delete_client(
        telegram_id: int,
        token: str = Depends(validate_connection_token),
):
    """Удаление клиента"""

    #await xray_manager.remove_client_from_config(telegram_id)

    return {
        "info": "Конфиг удален"
    }





