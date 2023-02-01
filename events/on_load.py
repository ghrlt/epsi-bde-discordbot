from __main__ import bot, slash
import env

import discord

isItReconnection = False

@bot.event
async def on_ready():
    global isItReconnection
    if isItReconnection == True: return

    env.logger.info(
        "Logged in as %s#%s (%i) | Prefix: %s",
        bot.user.name, bot.user.discriminator, bot.user.id, env.DISCORDBOT_PREFIX
    )

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="BDE WHI-SKY, Dites whi !"
        )
    )


    isItReconnection = True
