import json
import logging
import os

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

    async def add_client_to_config(self, client_id: int):
        config = await self.load_config()
        client_config = {
            "id": client_id,
            "flow": "xtls-rprx-vision",
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
        return True

    async def remove_client_from_config(self, telegram_id: int):
        config = await self.load_config()

        for inbound in config['inbounds']:
            if inbound['tag'] == 'reality-inbound':
                inbound['settings']['clients'] = [
                    client for client in inbound['settings']['clients']
                    if client.get('telegram_id') != telegram_id
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

    def generate_vless_url(self, client_id: str) -> str:
        """Генерация VLESS URL для Reality"""
        short_id = self.server_config['short_ids'][0]

        vless_url = f"vless://{client_id}@{self.server_config['ip']}:{self.server_config['port']}?type=tcp&security=reality&flow={self.server_config['flow']}&pbk={self.server_config['public_key']}&sni={self.server_config['sni']}&fp=chrome&sid={short_id}"

        return vless_url


xray_manager = XrayConfigManager()
vless_manager = VlessConfigGenerator(server_config["server_config"])