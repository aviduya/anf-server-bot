import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")
GUILD_ID=int(os.getenv("GUILD_ID"))
SERVER_TOKEN=os.getenv("SERVER_TOKEN")
SERVER_ID=os.getenv("SERVER_ID")
SERVER_URL=os.getenv("SERVER_URL")
