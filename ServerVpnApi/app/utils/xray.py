import json
import logging
import os
import uuid
from datetime import datetime, timedelta

from app.config import server_config

logger = logging.getLogger("xray")


class XrayConfigManager:
    def __init__(self, config_path="/usr/local/etc/xray/config.json"):
        self.config_path = config_path

    async def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    async def save_config(self, config):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    async def add_client_to_config(self, telegram_id: int):
        config = await self.load_config()
        
        # Генерируем уникальный UUID для клиента
        client_uuid = str(uuid.uuid4())
        
        # Создаем email на основе telegram_id
        client_email = f"user_{telegram_id}@telegram.com"
        
        # Устанавливаем срок действия (например, +30 дней)
        expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        client_config = {
            "id": client_uuid,
            "flow": "xtls-rprx-vision",
            "email": client_email,
            "expiry": expiry_date
        }

        for inbound in config['inbounds']:
            if inbound['tag'] == 'reality-inbound':
                if 'clients' not in inbound['settings']:
                    inbound['settings']['clients'] = []
                inbound['settings']['clients'].append(client_config)
                break

        await self.save_config(config)
        # Перезагружаем Xray
        await self.reload_xray()
        return client_uuid

    async def remove_client_from_config(self, telegram_id: int):
        config = await self.load_config()
        
        client_email = f"user_{telegram_id}@telegram.com"

        for inbound in config['inbounds']:
            if inbound['tag'] == 'reality-inbound':
                inbound['settings']['clients'] = [
                    client for client in inbound['settings']['clients']
                    if client.get('email') != client_email
                ]
                break

        await self.save_config(config)
        # Перезагружаем Xray
        await self.reload_xray()
        return True

    async def reload_xray(self):
        """Перезагружаем Xray конфигурацию"""
        try:
            os.system("systemctl reload xray || systemctl restart xray")
            logger.info("Xray configuration reloaded")
        except Exception as e:
            logger.error(f"Failed to reload Xray: {e}")


class VlessConfigGenerator:
    def __init__(self, server_config: dict):
        self.server_config = server_config

    def generate_vless_url(self, client_uuid: str, telegram_id: int) -> str:
        """Генерация полного VLESS URL для Reality"""
        
        # Получаем параметры из конфига сервера
        server_ip = self.server_config.get('ip', '5.129.233.56')
        server_port = self.server_config.get('port', 443)
        public_key = self.server_config.get('public_key', 'jyXkfCiq0kR8Wt-vU-MBU0Mou6OH7I9hJXLVu-33eBs')
        sni = self.server_config.get('sni', 'www.vk.ru')
        short_id = self.server_config.get('short_ids', ['12345678'])[0]
        flow = self.server_config.get('flow', 'xtls-rprx-vision')

        # Формируем полный VLESS URL
        vless_params = {
            'type': 'tcp',
            'security': 'reality',
            'encryption': 'none',
            'flow': flow,
            'pbk': public_key,
            'headerType': 'none',
            'fp': 'chrome',
            'sni': sni,
            'sid': short_id,
            'spx': '/'
        }

        # Собираем параметры в строку
        params_str = '&'.join([f"{k}={v}" for k, v in vless_params.items()])
        
        # Полная ссылка с комментарием
        vless_url = f"vless://{client_uuid}@{server_ip}:{server_port}?{params_str}#🇺🇸 Telegram_{telegram_id}"

        return vless_url


xray_manager = XrayConfigManager()
vless_manager = VlessConfigGenerator(server_config["server_config"])