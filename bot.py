import discord
from discord import app_commands

from config import DISCORD_TOKEN, GUILD_ID
from commands import register_all

class SlashBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        register_all(self.tree, self.logger, guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self):
        self.logger.usage("Bot is ready and slash commands are live!")

if __name__ == "__main__":
    # bot = SlashBot()
    # bot.run(DISCORD_TOKEN)
