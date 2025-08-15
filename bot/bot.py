import logging
from logging_config import setup_logging

setup_logging()

import os
from discord.ext.commands.core import command
import httpx
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("FASTAPI_URL")
SHARED = os.getenv("BOT_SHARED_SECRET")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)
log = logging.getLogger(__name__)

@bot.event
async def on_ready():
    await bot.tree.sync()
    log.info(f"Bot Ready!")

def auth_hdr():
    return {"x-shared-secret": SHARED}


@bot.tree.command(name="say", description="Send a server-wide chat message")
@app_commands.describe(message="Message to be sent")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    user = interaction.user
    log.usage(f"{user} invoked: /say")

    payload = {"command": "say", "directive": f" {user}: {message}"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(f"{API_URL}/command", json=payload, headers=auth_hdr())
            r.raise_for_status()
            log.usage(f"{user} used /say")
    except httpx.HTTPError as e:
        await interaction.followup.send(f"API error: {e}", ephemeral=True)
        return

    await interaction.followup.send(f"Sent to server: {message}", ephemeral=True)

bot.run(str(TOKEN))
