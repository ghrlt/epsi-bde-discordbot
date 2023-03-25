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

slash.add_command(Admin(name="admin", description="All bot administration slash commands"))