from __main__ import bot
import env
import apis
import database
import resources

import discord


class UpdateMemberData_modal(discord.ui.Modal, title="Synchronisation | Email requis"):
    email = discord.ui.TextInput(
        placeholder="prenom.nom<1>@ecoles-<epsi/wis>.net",
        label="Votre email campus :",
        min_length=10,
        custom_id="update_member_data_email_input",
    )

    async def on_submit(self, interaction: discord.Interaction):
        env.logger.debug(
            "%s#%s (%i) submited UpdateMemberData form."
            % (
                interaction.user.name,
                interaction.user.discriminator,
                interaction.user.id,
            )
        )

        await interaction.response.defer()

        for component in interaction.data["components"]:
            for child in component["components"]:
                if child["custom_id"] == "update_member_data_email_input":
                    email = child["value"]

        if not email:
            await interaction.followup.send(
                content="`❌` Veuillez renseigner votre email.",
                view=UpdateMemberData_modal(),
                ephemeral=True,
            )
            return

        mailing = apis.MailingList
        student = mailing.findStudentByEmail(email)
        if student:
            classDetail = student["classe"]["classe"].replace("MTP", "").strip()
            if classDetail != "":
                classDetail = " (%s)" % classDetail

            classe = "%s %s %s" % (
                student["classe"]["level"],
                student["classe"]["type"].replace("ALT", "").replace("INI", "").strip(),
                classDetail,
            )
            email = student["email"]
            isApprenant = True
        else:
            await interaction.followup.send(
                content="`❌` Une erreur est survenue lors de la récupération de vos informations. Veuillez réessayer.",
                ephemeral=True,
            )
            return

        try:
            pseudo = "%s %s. | %s" % (
                student["firstname"].title(),
                student["lastname"][0].upper(),
                classe,
            )
            await interaction.user.edit(nick=pseudo[:32])
        except discord.errors.Forbidden:
            env.logger.warning(
                "Guild: %i // Failed to rename user %s#%s (%i)."
                % (
                    interaction.guild.id,
                    interaction.user.name,
                    interaction.user.discriminator,
                    interaction.user.id,
                )
            )

        # ~ ~ ~/ Save the user's infos
        database.saveInfos(
            interaction.user.id,
            classe,
            student["firstname"],
            student["lastname"],
            email,
            None,
        )

        # ~ ~ ~/ Give guild access permissions to the user
        guild = interaction.guild
        role = guild.get_role(database.obtainConfiguration(guild.id, "verifiedRole"))
        if not role:
            try:
                role = await guild.fetch_role(
                    database.obtainConfiguration(guild.id, "verifiedRole")
                )
            except:
                env.logger.error(
                    "Guild: %i // Failed to obtain verifiedRole.", guild.id
                )

        if role:
            await interaction.user.add_roles(role)

        # ~ ~ ~/ Give apprenant access permissions to the user
        if isApprenant:
            role = guild.get_role(
                database.obtainConfiguration(guild.id, "studentsRole")
            )
            if not role:
                try:
                    role = await guild.fetch_role(
                        database.obtainConfiguration(guild.id, "studentsRole")
                    )
                except:
                    env.logger.error(
                        "Guild: %i // Failed to obtain studentsRole.", guild.id
                    )

            if role:
                await interaction.user.add_roles(role)

        # ~ ~ ~/ Send a success message
        await interaction.followup.send(
            embed=discord.Embed(
                title="Synchronisation effectuée avec succès !",
                description="Vos informations ont bien été mise à jour",
                color=resources.Colors.SUCCESS,
            ),
            ephemeral=True,
        )


class UpdateMemberData_view(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)

    async def handleClick(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # ~ Ask for email, in a form view
        await interaction.response.send_modal(UpdateMemberData_modal())

    @discord.ui.button(
        label="Mettre à jour mes informations",
        emoji="<:upvote:1070077946720686122>",
        style=discord.ButtonStyle.secondary,
        custom_id="update_member_data_btn",
    )
    async def callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        env.logger.debug(
            "Guild: %i // %s#%s (%i) clicked on %s"
            % (
                interaction.guild.id,
                interaction.user.name,
                interaction.user.discriminator,
                interaction.user.id,
                button.custom_id,
            )
        )

        await self.handleClick(interaction, button)
