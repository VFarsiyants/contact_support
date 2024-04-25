import logging
import sys
import os
import asyncio

from src.bot.dispatcher import run_bot

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

logging.basicConfig(level=LOGLEVEL, stream=sys.stdout)
asyncio.run(run_bot())
