import json

import pytz

# from app.schemas import ServerConfig
from app.settings import ProjectDir


DEFAULT_TZ = pytz.timezone("Europe/Moscow")

with open(ProjectDir / "server_config.json", "r") as f:
    server_config = json.load(f)






