import os
import httpx
from fastapi import FastAPI, Header, HTTPException, Depends

SHARED_SECRET = os.getenv("BOT_SHARED_SECRET")
SERVER_URL = os.getenv("SERVER_URL")
TOKEN = os.getenv("SERVER_TOKEN")

app = FastAPI(title="anf_bot_backend")

def auth(x_shared_secret: str = Header(...)):
    if x_shared_secret != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/command")
async def command(payload: dict, _=Depends(auth)):
    cmd = payload.get("command")
    directive = payload.get("directive")

    if not cmd:
        raise HTTPException(status_code=400, detail="Missing Command")

    full_cmd = cmd if not directive else f"{cmd} {directive}"

    url = f"{SERVER_URL}/command"
    body = {"command": full_cmd}

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        result = await client.post(url, json=body, headers=headers)
        result.raise_for_status()
        return {"ok": True}
