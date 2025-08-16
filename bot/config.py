import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
TOKEN = os.getenv("SERVER_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
RCON_HOST = os.getenv("RCON_HOST")
RCON_PASSWORD = os.getenv("RCON_PASSWORD")
RCON_PORT = int(os.getenv("RCON_PORT"))
