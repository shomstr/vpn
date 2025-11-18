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
    # Добавляем клиента в конфиг и получаем его UUID
    client_uuid = await xray_manager.add_client_to_config(telegram_id)
    
    # Генерируем полный VLESS конфиг
    vless_config = vless_manager.generate_vless_url(client_uuid, telegram_id)

    return {
        "info": "Конфиг был создан",
        "telegram_id": telegram_id,
        "client_uuid": client_uuid,
        "vless_config": vless_config
    }


@vpn_server.delete("/delete")
async def delete_client(
        telegram_id: int,
        token: str = Depends(validate_connection_token),
):
    """Удаление клиента"""

    await xray_manager.remove_client_from_config(telegram_id)

    return {
        "info": f"Конфиг для Telegram ID {telegram_id} удален"
    }