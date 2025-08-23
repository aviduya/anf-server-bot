import logging
from logging_config import setup_logging, log_usage
setup_logging()
import bot_commands as cmd
import discord
from discord import app_commands
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, GUILD_ID

log = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(seconds=360)
async def presence_loop():
    try:
        online = await cmd.fetch_player_count()
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=f"Minecraft: {online} online"
        )
        status = discord.Status.online if online > 0 else discord.Status.idle
        await bot.change_presence(status=status, activity=activity)
    except Exception:
        await discord.utils.sleep_until(discord.utils.utcnow().replace(microsecond=0))

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

@bot.tree.command(name="restart", description="Vote to restart the server if performance is slow")
@log_usage
async def restart(interaction: discord.Interaction):
    await cmd.restart_server(interaction=interaction)

@bot.event
async def on_ready():
    DEV_GUILD = discord.Object(id=GUILD_ID)
    bot.tree.clear_commands(guild=DEV_GUILD)
    await bot.tree.sync(guild=DEV_GUILD)

    if not presence_loop.is_running():
        presence_loop.start()

    log.info(f"Bot Ready as {bot.user}!")

bot.run(str(DISCORD_TOKEN))
