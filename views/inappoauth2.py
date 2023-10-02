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
    if env.ASK_FOR_PASSWORD_ON_JOIN:
        password = discord.ui.TextInput(
            placeholder="(Votre mot de passe n'est pas sauvegardé !)",
            label="Votre mot de passe 360Learning :",
            min_length=10,
            custom_id="in_app_oauth2_password_input"
        )
    if not env.FETCH_USER_DETAILS:
        firstname = discord.ui.TextInput(
            placeholder="John",
            label="Prénom :",
            min_length=2,
            custom_id="in_app_oauth2_firstname_input"
        )
        lastname = discord.ui.TextInput(
            placeholder="Doe",
            label="Nom :",
            min_length=2,
            custom_id="in_app_oauth2_lastname_input"
        )

    async def on_submit(self, interaction: discord.Interaction):
        env.logger.debug("%s#%s (%i) submited OAuthInApp form." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))

        await interaction.response.defer()

        for component in interaction.data['components']:
            for child in component['components']:
                if child['custom_id'] == "in_app_oauth2_username_input":
                    username = child['value']

                if env.ASK_FOR_PASSWORD_ON_JOIN:
                    if child['custom_id'] == "in_app_oauth2_password_input":
                        password = child['value']

                if not env.FETCH_USER_DETAILS:
                    if child['custom_id'] == "in_app_oauth2_firstname_input":
                        firstname = child['value']

                    if child['custom_id'] == "in_app_oauth2_lastname_input":
                        lastname = child['value']


        if env.ASK_FOR_PASSWORD_ON_JOIN:
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
        env.logger.debug("%s#%s (%i) logged in successfully. w/ psw: %s" % (interaction.user.name, interaction.user.discriminator, interaction.user.id, env.ASK_FOR_PASSWORD_ON_JOIN))
        
        #~ ~ ~/ Save the user's credentials
        database.saveCredentials(interaction.user.id, 'global', username, None)

        #~ ~ ~/ Rename user
        if env.FETCH_USER_DETAILS:
            status, user = await apis.epsi.getUserDetails(username)
            if status != 200:
                await interaction.followup.send(
                    content="`❌` Une erreur est survenue lors de la récupération de vos informations. Veuillez réessayer.",
                    view=OAuthInAppFailed_view(),
                    ephemeral=True
                )
                return

            isApprenant = False

            firstname = user['prenom']
            lastname = user['nom']
            classe = user['classe']
            if classe == 'B1':
                classe = 'SN1'
                isApprenant = True
            elif classe == 'B2':
                classe = 'SN2'
                isApprenant = True
            elif classe == 'PROFS':
                classe = 'Intervenant'
                lastname = user['nom']

        else:
            #~ Let's fetch class
            wigor = apis.WigorServices()
            wigor.login(username, None)

            def fetchAndParse(date: str, toJson: bool):
                try:
                    edt = wigor.fetchAndParse(date, toJson=toJson)
                    
                    for day in edt.keys():
                        if not edt[day]:
                            continue

                        classGrade = edt[day][0]['classGrade']
                        classLevel = classGrade['level']
                        classGroup = classGrade['group']

                        isApprenant = True

                except apis.WigorServices.CurrentlyOnHoliday:
                    classLevel = '?'
                    classGroup = '?'
                    isApprenant = False

                return classGrade, classLevel, classGroup, isApprenant

            classGrade, classLevel, classGroup, isApprenant = fetchAndParse('10/02/2023', toJson=True)
            if classLevel == '?':
                classGrade, classLevel, classGroup, isApprenant = fetchAndParse('10/09/2023', toJson=True)
                if classLevel == '?':
                    classGrade, classLevel, classGroup, isApprenant = fetchAndParse('10/16/2023', toJson=True)
                    if classLevel == '?':
                        classGrade, classLevel, classGroup, isApprenant = fetchAndParse('10/23/2023', toJson=True)
                        if classLevel == '?':
                            classGrade, classLevel, classGroup, isApprenant = fetchAndParse('10/30/2023', toJson=True)


            classe = "%s %s" % (classLevel, classGroup)

            
        try:
            await interaction.user.edit(nick="%s %s. | %s" % (firstname, lastname[0], classe))
        except discord.errors.Forbidden:
            env.logger.warning("Guild: %i // Failed to rename user %s#%s (%i)." % (interaction.guild.id, interaction.user.name, interaction.user.discriminator, interaction.user.id))


        #~ ~ ~/ Save the user's infos	
        database.saveInfos(interaction.user.id, classe, firstname, lastname, None, None)


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


        #~ ~ ~/ Give apprenant access permissions to the user
        if isApprenant:
            role = guild.get_role(database.obtainConfiguration(guild.id, "studentsRole"))
            if not role:
                try:
                    role = await guild.fetch_role(database.obtainConfiguration(guild.id, "studentsRole"))
                except:
                    env.logger.error("Guild: %i // Failed to obtain studentsRole.", guild.id)

            if role:
                await interaction.user.add_roles(role)


        #~ ~ ~/ Send a success message
        await interaction.followup.send(
            embed=discord.Embed(
                title="Vérification effectuée avec succès !",
                description="Vous pouvez désormais accéder au serveur.",
                color=resources.Colors.SUCCESS
            ).set_footer(text="Rappel: Votre mot de passe n'a pas été sauvegardé."),
            ephemeral=True
        )

        #~ ~ ~/ Edit original welcome message
        await interaction.message.edit(view=None)

class OAuthInApp_NotStudent_modal(discord.ui.Modal, title="Vérification"):
    prenom = discord.ui.TextInput(        
        placeholder="John",
        label="Prénom :",
        min_length=2,
        custom_id="in_app_oauth2_not_student_prenom_input"
    )
    nom = discord.ui.TextInput(
        placeholder="Doe",
        label="Nom :",
        min_length=2,
        custom_id="in_app_oauth2_not_student_nom_input"
    )
    email = discord.ui.TextInput(
        placeholder="prenom.nom@epsi.fr",
        label="Email :",
        min_length=3,
        custom_id="in_app_oauth2_not_student_email_input"
    )
    role = discord.ui.TextInput(
        placeholder="Administration, Intervenant, etc.",
        label="Votre poste à l'école :",
        min_length=1,
        custom_id="in_app_oauth2_not_student_role_input"
    )

    async def on_submit(self, interaction: discord.Interaction):
        env.logger.debug("%s#%s (%i) submited OAuthInApp NotStudent form." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))

        prenom = None
        nom = None
        email = None
        role = None

        for component in interaction.data['components']:
            for child in component['components']:
                if child['custom_id'] == "in_app_oauth2_not_student_prenom_input":
                    prenom = child['value']

                if child['custom_id'] == "in_app_oauth2_not_student_nom_input":
                    nom = child['value']

                if child['custom_id'] == "in_app_oauth2_not_student_email_input":
                    email = child['value']

                if child['custom_id'] == "in_app_oauth2_not_student_role_input":
                    role = child['value']

        if not prenom or not nom or not email or not role:
            await interaction.response.send_message(
                content="`❌` Veuillez remplir tous les champs.",
                ephemeral=True
            )
            return


        #~ ~ ~/ Save the user's infos
        database.saveInfos(interaction.user.id, role, prenom, nom, email, None)

        try:
            await interaction.user.edit(nick="%s %s. | %s" % (prenom, nom.title()[0], role))
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


        #~ ~ ~/ Edit to a success message
        await interaction.response.edit_message(
            embed=discord.Embed(
                title="Vérification effectuée avec succès !",
                description="Vous pouvez désormais accéder au serveur.",
                color=resources.Colors.SUCCESS
            ),
            view=None,
            content=None
        )

        #~ ~ ~/ Edit original welcome message, which the current one is a reply to
        msgId = interaction.message.reference.message_id
        if msgId:
            msg = await interaction.channel.fetch_message(msgId)
            if msg:
                await msg.edit(view=None)


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

class OAuthInAppFailed_view(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Pas un apprenant ?", emoji="🕵️", style=discord.ButtonStyle.primary, custom_id="in_app_oauth2_not_student_btn")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        env.logger.debug("%s#%s (%i) clicked on OAuthInApp_NotStudent button." % (interaction.user.name, interaction.user.discriminator, interaction.user.id))
        await interaction.response.send_modal(OAuthInApp_NotStudent_modal())