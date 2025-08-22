import asyncio
from .cmd_utils import rcon_command, fetch_player_count, send_command

async def restart_server(interaction):
    current_users_count = await fetch_player_count()

    # if current_users_count == 0:
    #     return await interaction.followup.send(
    #         "No players are online, cannot restart server"
    #     )

    # needed = max(1, current_users_count // 2)
    needed = 2
    vote_text = (
            f"🗳️ **Vote to restart the server!**\n"
            f"React with 👍 to approve, 👎 to decline.\n"
            f"Needs at least {needed} yes votes."
    )

    await interaction.response.send_message(vote_text)
    msg = await interaction.original_response()

    for emoji in ("👍", "👎"):
        await msg.add_reaction(emoji)

    await asyncio.sleep(60)
    updated = await interaction.channel.fetch_message(msg.id)

    yes_votes = next(
        (r.count - 1 for r in updated.reactions if r.emoji == "👍"),
        0
    )

    if yes_votes >= needed:
        await interaction.followup.send(
            f"✅ Restart approved with {yes_votes} yes votes (required: {needed}). Restarting Server..."
        )
        payload = {"command": "restart"}
        await send_command(payload=payload)
    else:
        await interaction.followup.send(
            f"❌ Restart vote failed with only {yes_votes} yes votes (required: {needed})."
        )
