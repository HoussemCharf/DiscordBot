import logging,os

token = os.getenv('bot_token') or '<token>'
prefix_server = '!'
prefix_dm = ['$','']
description = 'Jiggly is a discord bot designed by Houssem Charfeddine for private purposes'
pm_help=True
# cache file path
cache_file = os.path.abspath(os.path.join(os.getcwd(),'cache/cache.json'))
# logging
log_file = os.path.abspath(os.path.join(os.getcwd(),'logs/logs.log'))
file_logging_level = logging.INFO
stream_logging_level = logging.INFO
discord_logging_level = logging.WARNING
logging_sdtout = True
logging_file = True
logging_format = "%(levelname)s:%(asctime)s - %(name)s:%(filename)s:%(message)s"