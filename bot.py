import logging
from logging_config import setup_logging

setup_logging()

import discord
from discord import app_commands
from config import DISCORD_TOKEN, GUILD_ID, SERVER_TOKEN, SERVER_URL
from commands import register_all

log = logging.getLogger(__name__)

class SlashBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.token = SERVER_TOKEN
        self.server_url = SERVER_URL

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        register_all(self.tree, guild, self.server_url, self.token)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        log.info("Bot Online")

if __name__ == "__main__":
    bot = SlashBot()
    bot.run(DISCORD_TOKEN)
