from discord.ext import commands
from discord import __version__ as discordV
from platform import python_version as python_version
import asyncio
import inspect
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
        message_content = message.content.strip()
        # escaping messages without invoke prefix
        if not message_content.startswith(self.getPrefix):
            return
        # splitting messages with with args to pass them later on
        command, *args = message_content.split()
        # cleaning command and lowering it
        command = command[len(self.getPrefix):].lower().strip()
        # [] produces ['']
        if args:
            args = ' '.join(args).lstrip(' ').split(' ')
        # get handler
        handler=getattr(self,"cmd_%s" %command,None)
        # escaping empty handlers for vain invokes.
        if not handler:
            return
        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()
        sent_message=response=None
        try:
            handler_kwargs={}
            if params.pop('message',None):
                handler_kwargs['message']=message
            if params.pop('channel',None):
                handler_kwargs['channel']=message.channel
            if params.pop('author', None):
                handler_kwargs['author'] = message.author
            if params.pop('guild', None):
                handler_kwargs['guild'] = message.guild
            if params.pop('user_mentions', None):
                handler_kwargs['user_mentions'] = list(map(message.guild.get_member, message.raw_mentions))
            if params.pop('channel_mentions', None):
                handler_kwargs['channel_mentions'] = list(map(message.guild.get_channel, message.raw_channel_mentions))
            if params.pop('voice_channel', None):
                handler_kwargs['voice_channel'] = message.guild.me.voice.channel if message.guild.me.voice else None
            if params.pop('leftover_args', None):
                handler_kwargs['leftover_args'] = args
            args_expected= []
            for key,param in list(params.items()):
                if param.kind == param.VAR_POSITIONAL:
                    handler_kwargs[key] =args
                    params.pop(key)
                    continue
            response = await handler(**handler_kwargs)
        except Exception:
            self.logger.error("Error in On_message handler")