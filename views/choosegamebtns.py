from __main__ import bot
import env
import database

import discord

buttonStyle = discord.ButtonStyle.secondary

class ChooseGameButtons_view(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    async def handleGamingButtonsClick(self, interaction: discord.Interaction, button: discord.ui.Button, roleKey: str):
        role = interaction.guild.get_role(
            database.obtainConfiguration(interaction.guild.id, roleKey)
        )
        gamingRole = interaction.guild.get_role(
            database.obtainConfiguration(interaction.guild.id, 'gamingRole')
        )
        if not role or not gamingRole:
            if not role:
                try:
                    role = await interaction.guild.fetch_roles(
                        database.obtainConfiguration(interaction.guild.id, roleKey)
                    )
                except:
                    env.logger.error("Guild: %i // Failed to obtain %s role" % (interaction.guild.id, roleKey))
                    await interaction.response.send_message(
                        content="`❌`: Unable to fetch role.. Please contact an admin!",
                        ephemeral=True
                    )
                    return

            if not gamingRole:
                try:
                    gamingRole = await interaction.guild.fetch_roles(
                        database.obtainConfiguration(interaction.guild.id, 'gamingRole')
                    )
                except:
                    env.logger.warning("Guild: %i // Failed to obtain %s role" % (interaction.guild.id, 'gamingRole'))
                    #~ Non critical error, we can continue


        if role in interaction.user.roles:
            await interaction.user.remove_roles(
                role, reason="Choose role directly in #%s, but already has it" % interaction.channel.name
            )
            msg = "`✅`: Removed you the role %s" % role.mention
        else:
            await interaction.user.add_roles(
                gamingRole,
                role,
                reason="Choose role directly in #%s" % interaction.channel.name
            )
            msg = "`✅`: Added you the role %s" % role.mention

        await interaction.response.send_message(
            content=msg,
            ephemeral=True
        )


    @discord.ui.button(
        label="League Of Legends", emoji="<:leagueoflegends:1070129917255237632>",
        style=buttonStyle, custom_id="choose_game_btn_league_of_legends",
        row=0
    )
    async def callback_league_of_legends(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'lolGamingRole')

    @discord.ui.button(
        label="Rocket League", emoji="<:rocketleague:1070133041319653437>",
        style=buttonStyle, custom_id="choose_game_btn_rocket_league",
        row=0
    )
    async def callback_rocket_league(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'rlGamingRole')

    @discord.ui.button(
        label="Fall Guys", emoji="<:fallguys:1070134496860581978>",
        style=buttonStyle, custom_id="choose_game_btn_fall_guys",
        row=0
    )
    async def callback_fall_guys(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'fgGamingRole')


    @discord.ui.button(
        label="Call Of Duty", emoji="<:callofduty:1070134491567362069>",
        style=buttonStyle, custom_id="choose_game_btn_call_of_duty",
        row=1
    )
    async def callback_call_of_duty(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'codGamingRole')

    @discord.ui.button(
        label="CS:GO", emoji="<:csgo:1070134494763434014>",
        style=buttonStyle, custom_id="choose_game_btn_csgo",
        row=1
    )
    async def callback_csgo(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'csgoGamingRole')

    @discord.ui.button(
        label="Fortnite", emoji="<:fortnite:1070134485267533824>",
        style=buttonStyle, custom_id="choose_game_btn_fortnite",
        row=1
    )
    async def callback_fortnite(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'fortniteGamingRole')

    @discord.ui.button(
        label="Apex Legends", emoji="<:apex:1070139762041692190>",
        style=buttonStyle, custom_id="choose_game_btn_apex",
        row=1
    )
    async def callback_apex(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'apexGamingRole')

    @discord.ui.button(
        label="Rainbox 6 Siege", emoji="<:rainboxsixsiege:1070139758870806568>",
        style=buttonStyle, custom_id="choose_game_btn_rainbox_six_siege",
        row=1
    )
    async def callback_rainbow_six_siege(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'r6GamingRole')


    @discord.ui.button(
        label="World Of Warcraft", emoji="<:worldofwarcraft:1070134487721185290>",
        style=buttonStyle, custom_id="choose_game_btn_world_of_warcraft",
        row=2
    )
    async def callback_world_of_warcraft(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'wowGamingRole')

    @discord.ui.button(
        label="Valorant", emoji="<:valorant:1070134498047578163>",
        style=buttonStyle, custom_id="choose_game_btn_valorant",
        row=2
    )
    async def callback_valorant(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'valorantGamingRole')

    @discord.ui.button(
        label="Overwatch", emoji="<:overwatch:1070134489755422770>",
        style=buttonStyle, custom_id="choose_game_btn_overwatch",
        row=2
    )
    async def callback_overwatch(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'owGamingRole')


    @discord.ui.button(
        label="Minecraft", emoji="<:minecraft:1070139763346128987>",
        style=buttonStyle, custom_id="choose_game_btn_minecraft",
        row=3
    )
    async def callback_minecraft(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'mcGamingRole')

    @discord.ui.button(
        label="Among Us", emoji="<:among:1070139760854716487>",
        style=buttonStyle, custom_id="choose_game_btn_amongus",
        row=3
    )
    async def callback_amongus(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("Guild: %i // %s#%s (%i) clicked on %s" % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id, button.custom_id))
        return await self.handleGamingButtonsClick(interaction, button, 'amongusGamingRole')

