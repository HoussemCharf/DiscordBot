from discord.ext import commands
from discord import __version__ as discordV
from platform import python_version as python_version
import asyncio

from core.bot.cache import Cache
from core.bot import Logging

from config import token
from config import description
from config import pm_help
from config import prefix_dm
from config import prefix_server


import discord, arrow, os

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.getPrefix,description=description,pm_help=pm_help)
        self.logger = Logging.get_logger("bot")
        self.cache = Cache()
    async def track_start(self):
        """
            start tracking stats
        """
        await self.wait_until_ready()
        self.start_time = arrow.now()
        self.messages = Cache.get("messages") or 0
    async def load_all_extension(self):
        """
            Attemp tot load all .py files in /cogs as an a third party
        """
        await self.wait_until_ready()
        # extra check to make sure the wait until ready is done loading.
        await asyncio.sleep(1)
        cogs = [ x.stem for x in os.path.join(os.getcwd(),"cogs").glob('*.py')]
        for ext in cogs:
            try:
                self.load_cog(f'cogs.{ext}')
            except Exception as e:
                error = f'{ext}\n {type(e).__name__}:{e}'
                self.logger.error(f'Failed to load extension: {error}')
    # functions to load and unload a cog
    async def load_cog(self,name):
        self.load_extension(f'cogs.{name}')
        self.logger.info(f'Loaded {name}')
    async def unload_cog(self,name):
        self.unload_extension(f'cogs.{name}')
        self.logger.info(f'Unloaded {name}')
    # get prefix function
    async def on_ready(self):
        self.app_info = await self.application_info()
        print("\n\n-------------------------------------------------")
        print(f"Bot: {self.user.name} | ready to report!")
        print(f"Bot creator: BlackArrow aka Cheesus")
        print(f"Bot owner: {self.app_info.owner}")
        print(f"Running Discord {discordV} - Python {python_version()}")
        print(f"ID: {self.user.id}")
        print(f"------------------------------------------------\n")
    async def on_message(self,message):
        if message.author.id in Cache.get("blacklisted"): return
        if message.author.bot: return
        self.messages+= 1
        self.cache.save("messages", self.messages)
        self.process_command(message)
    async def getPrefix(self):
        return prefix_server
    async def process_command(self,message):
        pass