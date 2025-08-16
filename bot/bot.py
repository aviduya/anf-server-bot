import logging
from logging_config import setup_logging
setup_logging()

import httpx
import discord
import functools
from discord import app_commands
from discord.ext import commands
from config import DISCORD_TOKEN

import bot_utils as utils

log = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

def log_usage(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        interaction = kwargs.get("interaction") or (args[0] if args else None)
        user = getattr(getattr(interaction, "user", None), "name", None) or "unknown-user"
        log.usage(f"{user} invoked {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            log.usage(f"{func.__name__} completed for {user}")
            return result
        except Exception as e:
            log.error(f"{func.__name__} failed for {user}: {e}")
            raise
    return wrapper


@bot.tree.command(name="say", description="Send a server-wide chat message")
@log_usage
@app_commands.describe(message="Message to be sent")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    user = interaction.user
    payload = {"command": "say", "directive": f" {user}: {message}"}

    try:
        await utils.send_command(payload)
    except ValueError as e:
        await interaction.followup.send("Error: Tell Anfernee to look at logs and fix it.", ephemeral=True)
        log.error(f"Error: {e}")
        return
    except httpx.HTTPError as e:
        await interaction.followup.send("Error: Tell Anfernee to look at logs and fix it.", ephemeral=True)
        log.error(f"API error: {e}")
        return

    await interaction.followup.send(f"Sent to server: {message}", ephemeral=True)

@bot.tree.command(name="list", description="List current online players")
@log_usage
async def list(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    response = utils.rcon_command("list")
    striped = utils.strip_color_codes(response)
    await interaction.followup.send(f"{striped}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    log.info(f"Bot Ready as {bot.user}!")

bot.run(str(DISCORD_TOKEN))
