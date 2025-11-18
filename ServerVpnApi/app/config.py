import json

import pytz

# from app.schemas import ServerConfig
from app.settings import ProjectDir


DEFAULT_TZ = pytz.timezone("Europe/Moscow")

with open(ProjectDir / "server_config.json", "r") as f:
    server_config = json.load(f)


server_config = {
    "server_config": {
        "ip": "5.129.233.56",
        "port": 443,
        "public_key": "jyXkfCiq0kR8Wt-vU-MBU0Mou6OH7I9hJXLVu-33eBs",
        "private_key": "oPp3Fnn5d_yHnCu2qoIl3VT5VdjPclQWIDR3QxcmXHA",
        "sni": "www.vk.ru",
        "server_names": ["vk.ru", "www.vk.ru"],
        "short_ids": ["12345678", "abcdef12"],
        "flow": "xtls-rprx-vision"
    }
}



