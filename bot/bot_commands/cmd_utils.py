import httpx
from player_model import ServerPlayerModel as ServerPlayerStatus
from dotenv import load_dotenv
from mcrcon import MCRcon
from config import TOKEN, SERVER_URL, RCON_PORT, RCON_HOST, RCON_PASSWORD
import re
load_dotenv()

headers = {"Authorization": f"Bearer {TOKEN}"}

async def send_command(payload: dict):
    cmd = payload.get("command")
    directive = payload.get("directive")

    if not cmd:
        raise ValueError("Command is missinng.")

    full_cmd = cmd if not directive else f"{cmd} {directive}"

    url = f"{SERVER_URL}/command"
    body = {"command": full_cmd}

    async with httpx.AsyncClient() as client:
        result = await client.post(url, json=body, headers=headers)
        result.raise_for_status()

async def fetch_server_player_info() -> ServerPlayerStatus:
    url = f"{SERVER_URL}/minecraft/players"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return ServerPlayerStatus(**response.json())

def rcon_command(cmd: str) -> str:
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        return mcr.command(cmd)

def strip_color_codes(text: str) -> str:
    r = re.compile(r"§[0-9a-fk-or]", flags=re.IGNORECASE)
    return r.sub("", text)
