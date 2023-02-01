import os
from dotenv import dotenv_values

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

config = {
    **os.environ,
    **dotenv_values('.env'),
    **dotenv_values('.env.local')
}
ENVMODE = config.get("ENV_MODE", "dev")

config = {
    **config,
    **dotenv_values(f".env.{ENVMODE}"),
    **dotenv_values(f".env.{ENVMODE}.local")
}

def areWeInProd():
    return ENVMODE == "prod"

def isItDevEnvironment():
    return not areWeInProd()


APP_NAME = config.get("APP_NAME", "unset")
LOG_LEVEL = config.get("LOG_LEVEL", "NOTSET").upper()

logger = logging.getLogger(config.get("APP_NAME", __name__))
if LOG_LEVEL == 'NOTSET':     logger.setLevel(logging.NOTSET)
elif LOG_LEVEL == 'DEBUG':    logger.setLevel(logging.DEBUG)
elif LOG_LEVEL == 'INFO':     logger.setLevel(logging.INFO)
elif LOG_LEVEL == 'WARNING':  logger.setLevel(logging.WARNING)
elif LOG_LEVEL == 'ERROR':    logger.setLevel(logging.ERROR)
elif LOG_LEVEL == 'CRITICAL': logger.setLevel(logging.CRITICAL)

DISCORDBOT_TOKEN = config.get("DISCORDBOT_TOKEN")
DISCORDBOT_PREFIX = config.get("DISCORDBOT_PREFIX")

DISCORDBOT_DEV_GUILD_ID = config.get("DISCORDBOT_DEV_GUILD_ID")

EPSIAPI_USERSURL = config.get("EPSIAPI_USERSURL")
if not EPSIAPI_USERSURL:
    raise ValueError("EPSIAPI_USERSURL is not set.")

logger.info("App: %s | Env: %s | Log: %s", APP_NAME, ENVMODE, LOG_LEVEL)

if not DISCORDBOT_TOKEN:
    raise ValueError("DISCORDBOT_TOKEN is not set.")

if not DISCORDBOT_PREFIX:
    logger.warning("DISCORDBOT_PREFIX is not set. Using default value (\"*/\").")

