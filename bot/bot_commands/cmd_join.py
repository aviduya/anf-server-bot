import discord
import re
from .cmd_utils import rcon_command, strip_color_codes
import asyncio

def strip_name_from(list) -> list:
    stripped_names = [name.strip() for name in list.split(":", 1)[1].split(",")]
    return stripped_names

def parse_user_count(msg: str) -> int:
    match = re.search(r"There are (\d+) out of maximum (\d+)", msg)
    if match:
        return int(match.group(1))
    raise ValueError(f"Message not in expected format: {msg}")

async def join_server(interaction: discord.Interaction):
    countdown = 60

    await interaction.response.defer(thinking=True, ephemeral=True)
    await interaction.edit_original_response(
        content=f"Whitelist **disabled**. You have {countdown}s to join..."
    )
    rcon_command("whitelist off")

    for remaining in range(countdown - 1, -1, -1):
        await asyncio.sleep(1)
        await interaction.edit_original_response(
            content=f"Whitelist **disabled**. You have {remaining}s to join..."
        )

    rcon_command("whitelist on")

    connected_users = strip_color_codes(rcon_command("list"))
    if parse_user_count(connected_users) == 0:
        await interaction.edit_original_response(
            content="No one joined. Run the command again and join during the window."
        )
        return

    stripped_connected = strip_name_from(connected_users)
    whitelisted_users = strip_name_from(rcon_command("whitelist list"))

    newly_added = []
    for user in stripped_connected:
        if user not in whitelisted_users:
            rcon_command(f"whitelist add {user}")
            newly_added.append(user)

    if newly_added:
        await interaction.edit_original_response(
            content=f"Whitelisted: {', '.join(newly_added)}"
        )
    else:
        await interaction.edit_original_response(
            content="All current players were already whitelisted."
        )
