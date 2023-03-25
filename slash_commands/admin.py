from __main__ import bot, slash
import env
import utils

import os
import sys
import discord
from discord import app_commands
from discord.app_commands import Choice, Transform

from transformers import *


@app_commands.guild_only()
class Admin(app_commands.Group):

    @app_commands.command(name="export_db", description="Export database")
    async def _exportDatabase(
        self, interaction: discord.Interaction
    ) -> None:
        
        dbPaths = [
            utils.getAbsolutePath("database.db")
        ]
        files = []
        for dbPath in dbPaths:
            files.append(discord.File(dbPath))

        await interaction.response.send_message(files=files, ephemeral=True)

    @app_commands.command(name="sync", description="Sync bot app commands")
    async def _sync(
        self, interaction: discord.Interaction
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        synced = await bot.tree.sync()
        synced += await bot.tree.sync(guild=interaction.guild)

        msg = "No commands synced!"
        if len(synced) > 0:
            msg = "Successfully synced %i commands!" % len(synced)

        await interaction.followup.send(content=msg,ephemeral=True)

    @app_commands.command(name="set_status", description="Set bot activity status")
    @app_commands.choices(
        status=[
            Choice(name="Online", value='online'),
            Choice(name="Idle", value='idle'),
            Choice(name="Do not disturb", value='dnd'),
            Choice(name="Invisible", value='invisible'),
            Choice(name="Offline", value='offline')
        ],
        activity_type=[
            Choice(name="Playing", value=0),
            Choice(name="Streaming", value=1),
            Choice(name="Listening", value=2),
            Choice(name="Watching", value=3),
            Choice(name="Custom", value=4),
            Choice(name="Competing", value=5)
        ]
    )
    async def _setStatus(
        self, interaction: discord.Interaction, status: Choice[str],
        activity_type: Choice[int]=None, activity: str=None, url: str=None
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        if activity_type is None and activity is None:
            currentActivity = interaction.guild.me.activity
            await bot.change_presence(status=status.value, activity=currentActivity)

            msg = "Successfully updated status!"

        else:
            if activity_type is None:
                activity_type = discord.ActivityType.playing
            
            if activity is None:
                msg = "Please provide an activity!"

            else:
                if activity_type.value == discord.ActivityType.streaming and url is None:
                    msg = "Please provide a stream URL!"

                else:
                    if activity_type.value == discord.ActivityType.streaming:
                        if not url.startswith("https://"):
                            url = "https://%s" % url
                        
                        activity = discord.Streaming(
                            name=activity,
                            url=url
                        )

                    else:
                        activity = discord.Activity(
                            name=activity,
                            type=activity_type.value,
                            url=url
                        )
            
                    await bot.change_presence(status=status.value, activity=activity)
                    msg = "Successfully updated status and activity!"

        await interaction.followup.send(content=msg, ephemeral=True)



slash.add_command(Admin(name="admin", description="All bot administration slash commands"))