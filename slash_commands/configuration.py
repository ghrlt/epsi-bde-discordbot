from __main__ import bot, slash
import env
import database
import resources

import discord
from discord import app_commands
from discord.app_commands import Choice, Transform

from transformers import *


@app_commands.guild_only()
class Configuration(app_commands.Group):

    @app_commands.command(name="setchannel", description="Define channel for given key.")
    @app_commands.choices(
        key=[
            Choice(name="Channel where to welcome new members",  value="welcomeChannel"),
            Choice(name="Channel where to report any issue",     value="reportChannel"),
            Choice(name="Channel where to suggest new features", value="suggestionChannel"),
            Choice(name="Channel where to send log messages",    value="logChannel")
        ]
    )
    async def _setChannel(
        self, interaction: discord.Interaction,
        key: Choice[str], channel: discord.TextChannel|discord.VoiceChannel|discord.ForumChannel
    ) -> None:
        database.setConfiguration(interaction.guild.id, key.value, channel.id)

        reply = discord.Embed(
            description="Successfully assigned channel %s for `%s`." % (channel.mention, key.value),
            color=resources.Colors.SUCCESS
        )
        reply.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=reply, ephemeral=True)

    @app_commands.command(name="setrole", description="Define role for given key.")
    @app_commands.choices(
        key=[
            Choice(name="Membres vérifiés",             value="verifiedRole"),
            Choice(name="Membres réduits en sourdine",  value="mutedRole"),
            Choice(name="Apprenants",                   value="studentsRole"),
            Choice(name="Adhérents",                    value="adherentsRole"),
            Choice(name="Professeurs",                  value="teachersRole"),
            Choice(name="Staff EPSI",                   value="schoolstaffRole"),

            Choice(name="VideoGames players",                          value="gamingRole"),
            Choice(name="League Of Legends players",                   value="lolGamingRole"),
            Choice(name="Rocket League players",                       value="rlGamingRole"),
            Choice(name="Fall Guys players",                           value="fgGamingRole"),
            Choice(name="Call of Duty players",                        value="codGamingRole"),
            Choice(name="Counter-Strike: Global Offensive players",    value="csgoGamingRole"),
            Choice(name="Fortnite players",                            value="fortniteGamingRole"),
            Choice(name="World Of Warcraft players",                   value="wowGamingRole"),
            Choice(name="Valorant players",                            value="valorantGamingRole"),
            Choice(name="Overwatch players",                           value="owGamingRole"),
            Choice(name="Minecraft players",                           value="mcGamingRole"),
            Choice(name="Apex Legends players",                        value="apexGamingRole"),
            Choice(name="Rainbow Six Siege players",                   value="r6GamingRole"),
            Choice(name="Among Us players",                            value="amongusGamingRole"),

        ]
    )
    async def _setRole(
        self, interaction: discord.Interaction,
        key: Choice[str], role: discord.Role
    ) -> None:
        database.setConfiguration(interaction.guild.id, key.value, role.id)

        reply = discord.Embed(
            description="Successfully assigned role %s for `%s`." % (role.mention, key.value),
            color=resources.Colors.SUCCESS
        )
        reply.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=reply, ephemeral=True)

    @app_commands.command(name="setemote", description="Define emote for given key.")
    @app_commands.choices(
        key=[
            Choice(name="Upvote",           value="upvoteEmoji"),
            Choice(name="Downvote",         value="downvoteEmoji"),
            Choice(name="Invalid / Error",  value="errorEmoji"),
            Choice(name="Valid / Success",  value="validEmoji")
        ]
    )
    async def _setEmote(
        self, interaction: discord.Interaction,
        key: Choice[str], emote: str
    ) -> None:
        database.setConfiguration(interaction.guild.id, key.value, emote)

        reply = discord.Embed(
            description="Successfully assigned emote %s for `%s`." % (emote, key.value),
            color=resources.Colors.SUCCESS
        )
        reply.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=reply, ephemeral=True)

    @app_commands.command(name="get", description="Get configuration for given key.")
    async def _get(
        self, interaction: discord.Interaction,
        key: str
    ) -> None:
        value = database.obtainConfiguration(interaction.guild.id, key, ignoreError=True)
        if not value:
            desc = "Setting `%s` is not configured." % key
        else:
            desc = "`%s` is set to %s" % (key, value)

        reply = discord.Embed(
            description=desc,
            color=resources.Colors.SUCCESS
        )
        reply.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=reply)

    @app_commands.command(name="reset", description="Reset guild configuration")
    async def _reset(
        self, interaction: discord.Interaction
    ) -> None:
        database.deleteConfiguration(interaction.guild.id)

        reply = discord.Embed(
            description="Successfully deleted any custom configuration for current guild.",
            color=resources.Colors.SUCCESS
        )
        reply.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=reply)


slash.add_command(Configuration(name="config", description="Configure the bot for your guild."))