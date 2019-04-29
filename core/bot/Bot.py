from discord.ext import commands
from discord import __version__ as discordV
from platform import python_version as python_version
from core.bot.cache import Cache
import Logging

from config import token
from config import description
from config import pm_help
from config import prefix_dm
from config import prefix_server


import discord, arrow, OSError

class Bot(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.getPrefix)