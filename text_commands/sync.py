from __main__ import bot
import env

import discord


@bot.command()
async def sync(ctx):
    # bot.tree.copy_global_to(guild=discord.Object(env.DISCORDBOT_DEV_GUILD_ID))
    synced = await bot.tree.sync()
    synced += await bot.tree.sync(guild=ctx.guild)

    msg = "No commands synced!"
    if len(synced) > 0:
        msg = "Successfully synced %i commands!" % len(synced)

    await ctx.reply(content=msg)
