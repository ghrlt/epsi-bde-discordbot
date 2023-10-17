from __main__ import bot, slash
import views
import database

import discord
from discord import app_commands




@app_commands.guild_only()
class Users(app_commands.Group):

    @app_commands.command(name="set_username", description="Set user usernames")
    async def _setUsername(
        self, interaction: discord.Interaction,
        user: discord.Member, username: str, app: str = 'global'
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        database.saveCredentials(user.id, app, username)

        await interaction.followup.send(
            content="Successfully updated %s username for %s!" % (user.mention, app),
            ephemeral=True
        )

    @app_commands.command(name="set_infos", description="Set user infos")
    async def _setInfos(
        self, interaction: discord.Interaction,
        user: discord.Member, firstName: str|None, lastName: str|None,
        email: str|None, phoneNumber: str|None,
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        database.saveInfos(user.id, firstName, lastName, email, phoneNumber)

        await interaction.followup.send(
            content="Successfully updated %s infos!" % (user.mention),
            ephemeral=True
        )


slash.add_command(Users(name="users", description="Manage users"))