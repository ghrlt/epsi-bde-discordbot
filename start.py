import discord
from discord.ext import commands

import env


#~ ~ ~/ Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=env.DISCORDBOT_PREFIX,
    description=env.APP_NAME,
    intents=intents
)
slash = bot.tree


#~ ~ ~/ Setup database and related helpers
import database
database.setup()


#~ ~ ~/ Import modules
import views
import events
import transformers
import text_commands
import slash_commands


#~ ~ ~/ 

bot.setup_hook = views.setup_hook


#~ ~ ~/ Run bot
bot.run(env.DISCORDBOT_TOKEN, log_handler=None)
