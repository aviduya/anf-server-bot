from pydoc import describe
from discord import app_commands

def register_say(tree, guild, id, token):
    @tree.command(
        name="say",
        description="Broadcast a message to the Minecraft server chat",
        guild=guild
    )
    @app_commands.describe(message="Message to the server")
    async def say(interaction, message: str):
        user = interaction.user
