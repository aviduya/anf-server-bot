import logging
import os
import httpx
import discord
from discord import app_commands
from discord.ext import commands
from logging_config import setup_logging

setup_logging()
log = logging.getLogger(__name__)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = os.getenv("SERVER_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
SHARED = os.getenv("BOT_SHARED_SECRET")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

async def send_command(payload: dict):
    cmd = payload.get("command")
    directive = payload.get("directive")

    if not cmd:
        raise ValueError("Command is missinng.")

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
        log.usage(f"/{cmd} {directive} was sent to the server.")


@bot.event
async def on_ready():
    await bot.tree.sync()
    log.info(f"Bot Ready!")


@bot.tree.command(name="say", description="Send a server-wide chat message")
@app_commands.describe(message="Message to be sent")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    user = interaction.user
    log.usage(f"{user} invoked: /say")

    payload = {"command": "say", "directive": f" {user}: {message}"}

    try:
        await send_command(payload)
    except ValueError as e:
        await interaction.followup.send(f"Error: Tell Anfernee to look at logs and fix it.", ephemeral=True)
        log.error(f"Error: {e}")
        return
    except httpx.HTTPError as e:
        await interaction.followup.send(f"Error: Tell Anfernee to look at logs and fix it.", ephemeral=True)
        log.error(f"API error: {e}")
        return

    await interaction.followup.send(f"Sent to server: {message}", ephemeral=True)

bot.run(str(DISCORD_TOKEN))
