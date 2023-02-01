from __main__ import bot
import env
import database
import resources

import discord

@bot.event
async def on_message(msg):
    if msg.author.bot: return
    if msg.guild is None: return

    #~ ~ ~/ If message is a command, let's just process it
    if msg.content.startswith(env.DISCORDBOT_PREFIX):
        await bot.process_commands(msg)
        return
