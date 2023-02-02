from __main__ import bot
import env
import apis
import database
import resources

import discord


class OAuthInApp_Input_modal(discord.ui.Modal, title="Connexion à 360Learning | Identifiants"):
    username = discord.ui.TextInput(        
        placeholder="prenom.nom",
        label="Votre identifiant 360Learning :",
        min_length=3,
        custom_id="in_app_oauth2_username_input"
    )
    password = discord.ui.TextInput(
        placeholder="(Votre mot de passe n'est pas sauvegardé !)",
        label="Votre mot de passe 360Learning :",
        min_length=10,
        custom_id="in_app_oauth2_password_input"
    )

    async def on_submit(self, interaction: discord.Interaction):
        env.logger.debug("%s#%s (%i) submited OAuthInApp form." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))

        await interaction.response.defer()

        for component in interaction.data['components']:
            for child in component['components']:
                if child['custom_id'] == "in_app_oauth2_username_input":
                    username = child['value']
                elif child['custom_id'] == "in_app_oauth2_password_input":
                    password = child['value']

        api = apis.WigorServices() #~ Might as well use ingenium API
        try:
            api.login(username, password)
        except api.UnableToLogin as e:
            env.logger.debug("%s#%s (%i) failed to login: %s" % (interaction.user.name, interaction.user.discriminator, interaction.user.id, e))
            await interaction.followup.send(
                content="`❌` %s. Veuillez réessayer." % e,
                ephemeral=True
            )
            return

        #~ ~ ~/ Login was successful
        env.logger.debug("%s#%s (%i) logged in successfully." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))
        
        #~ ~ ~/ Save the user's credentials
        database.saveCredentials(interaction.user.id, 'global', username, None)

        #~ ~ ~/ Rename user
        status, user = await apis.epsi.getUserDetails(username)
        if status != 200:
            await interaction.followup.send(
                content="`❌` Une erreur est survenue lors de la récupération de vos informations. Veuillez réessayer.",
                ephemeral=True
            )
            return

        firstname = user['prenom']
        lastname = user['nom'][0]
        classe = user['classe']
        if classe == 'B1':
            classe = 'SN1'
        elif classe == 'B2':
            classe = 'SN2'
        elif classe == 'PROFS':
            classe = 'Intervenant'
            lastname = user['nom']

        try:
            await interaction.user.edit(nick="%s %s. | %s" % (firstname, lastname, classe))
        except discord.errors.Forbidden:
            env.logger.warning("Guild: %i // Failed to rename user %s#%s (%i)." % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id))


        #~ ~ ~/ Give guild access permissions to the user
        guild = interaction.guild
        role = guild.get_role(database.obtainConfiguration(guild.id, "verifiedRole"))
        if not role:
            try:
                role = await guild.fetch_role(database.obtainConfiguration(guild.id, "verifiedRole"))
            except:
                env.logger.error("Guild: %i // Failed to obtain verifiedRole.", guild.id)

        if role:
            await interaction.user.add_roles(role)


        #~ ~ ~/ Send a success message
        await interaction.followup.send(
            embed=discord.Embed(
                title="Vérification effectuée avec succès !",
                description="Vous pouvez désormais accéder au serveur.",
                color=resources.Colors.COLOR_SUCCESS
            ).set_footer(text="Rappel: Votre mot de passe n'a pas été sauvegardé."),
            ephemeral=True
        )

        #~ ~ ~/ Edit original welcome message
        await interaction.message.edit(view=None)

class OAuthInApp_view(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Accéder au serveur", emoji="🤖", style=discord.ButtonStyle.primary, custom_id="in_app_oauth2_btn")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != interaction.message.mentions[0].id:
            await interaction.response.send_message(
                content="`❌` Ce bouton ne vous est pas alloué, veuillez utiliser le votre.",
                ephemeral=True
            )
            return

        env.logger.debug("%s#%s (%i) clicked on OAuthInApp button." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))
        await interaction.response.send_modal(OAuthInApp_Input_modal())
