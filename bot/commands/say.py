from discord import app_commands
import httpx
import logging
from .command_util import command

log = logging.getLogger(__name__)

def register_say(tree, guild, url, token):
    @tree.command(
        name="say",
        description="Broadcast a message to the Minecraft server chat",
        guild=guild
    )
    @app_commands.describe(message="Message to the server")
    async def say(interaction, message: str):
        await command(interaction=interaction, command="say", directive=message)
