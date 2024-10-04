from __main__ import bot, slash
import env
import views
import database
import resources

import discord
from discord import app_commands
from discord.app_commands import Choice


@slash.command(name="install", description="Install pre-configured things")
@app_commands.guild_only()
@app_commands.choices(
    thing=[
        Choice(name="Choisis tes jeux - Buttons", value="chooseGamesButtons"),
        Choice(
            name="Mets à jour tes informations - Button", value="updateMemberDataButton"
        ),
    ]
)
async def _install(
    interaction: discord.Interaction, thing: Choice[str], channel: discord.TextChannel
):
    await interaction.response.defer(ephemeral=True)

    match thing.value:
        case "chooseGamesButtons":
            await channel.send(view=views.choosegamebtns.ChooseGameButtons_view())

        case "updateMemberDataButton":
            await channel.send(view=views.updatedata.UpdateMemberData_view())

        case _:
            await interaction.response.send_message(
                "Unknown thing to install", ephemeral=True
            )
            return

    await interaction.followup.send(content="Install was successful!", ephemeral=True)
