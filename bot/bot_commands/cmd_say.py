import discord as dc
from .cmd_utils import rcon_command

async def say_to_players(interaction: dc.Interaction, message: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    user = interaction.user
    rcon_command(f"say Discord: {user}:{message}")
    await interaction.followup.send(f"Sent to server: {message}", ephemeral=True)
