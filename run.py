from discord import __version__ as discordV
from core.bot import Bot
from core.bot import Logging
from config import token
from config import discord_logging_level
from config import logging_format
import errno, sys, os, re
import logging

logger = Logging.get_logger('discord')
discordV = tuple([int(vnum) for vnum in (re.sub('[^1234567890.]','',discordV)).split('.')])

discordmaj,discordmino,discordmicro = discordV

if not(discordmaj,discordmino) >= (1, 0):
    print('[ERROR] Wrong version, Use rewrite')
    print('[INFO] pip install discord-rewrite')
    exit(errno.EINVAL)
if __name__ == '__main__':
    os.system('pip install -r requirements.txt')
    bot = Bot()
    bot.run(token)