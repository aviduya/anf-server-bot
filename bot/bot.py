import logging
from logging_config import setup_logging, log_usage
setup_logging()
import bot_commands as cmd
import discord
from discord import app_commands
from discord.ext import commands
from config import DISCORD_TOKEN, GUILD_ID

log = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

@bot.tree.command(name="say", description="Send a server-wide chat message")
@log_usage
@app_commands.describe(message="Message to be sent")
async def say(interaction: discord.Interaction, message: str):
    await cmd.say_to_players(interaction=interaction, message=message)

@bot.tree.command(name="list", description="List current online players")
@log_usage
async def list(interaction: discord.Interaction):
    await cmd.list_players(interaction=interaction)

@bot.tree.command(name="joinserver", description="Join the minecraft server")
@log_usage
async def join(interaction: discord.Interaction):
    await cmd.join_server(interaction=interaction)

@bot.event
async def on_ready():
    DEV_GUILD = discord.Object(id=GUILD_ID)
    bot.tree.clear_commands(guild=DEV_GUILD)
    await bot.tree.sync(guild=DEV_GUILD)
    await bot.tree.sync()
    log.info(f"Bot Ready as {bot.user}!")

bot.run(str(DISCORD_TOKEN))
