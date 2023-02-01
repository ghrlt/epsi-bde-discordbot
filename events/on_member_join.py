from __main__ import bot
import env
import views
import database

import discord


@bot.event
async def on_member_join(member):
    env.logger.info("Guild: %i // Member joined: %s#%s (%i)", member.guild.id, member.name, member.discriminator, member.id)

    welcomeChannel = member.guild.get_channel(
        database.obtainConfiguration(member.guild.id, "welcomeChannel")
    )
    if not welcomeChannel:
        try:
            welcomeChannel = await member.guild.fetch_channel(
                database.obtainConfiguration(member.guild.id, "welcomeChannel")
            )
        except:
            env.logger.error("Guild: %i // Failed to obtain welcomeChannel.", member.guild.id)
            return

    view = views.inappoauth2.OAuthInApp_view()
    await welcomeChannel.send(
        content="Bienvenue parmis nous %s!" % (member.mention),
        view=view
    )

@bot.command()
async def hi(ctx):
    await on_member_join(ctx.author)
    await ctx.message.delete()