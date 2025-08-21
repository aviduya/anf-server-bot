import discord
from .cmd_utils import rcon_command, strip_color_codes

async def list_players(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    response = rcon_command("list")
    striped = strip_color_codes(response)
    await interaction.followup.send(f"{striped}")
