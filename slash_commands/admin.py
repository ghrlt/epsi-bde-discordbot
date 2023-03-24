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
