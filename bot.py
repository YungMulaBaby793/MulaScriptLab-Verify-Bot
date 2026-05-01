import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        member = interaction.user

        verified_role = discord.utils.get(guild.roles, name="Verified")
        member_role = discord.utils.get(guild.roles, name="Member")

        roles = []

        if verified_role:
            roles.append(verified_role)

        if member_role:
            roles.append(member_role)

        await member.add_roles(*roles)

        await interaction.response.send_message(
            "You are now verified. Welcome to MulaScriptLabs.",
            ephemeral=True
        )


@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"Logged in as {bot.user}")


@bot.command()
@commands.has_permissions(administrator=True)
async def rebuild(ctx):

    guild = ctx.guild

    await ctx.send("Rebuilding server layout...")

    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

    everyone = guild.default_role

    owner = await guild.create_role(name="Owner", permissions=discord.Permissions(administrator=True))
    admin = await guild.create_role(name="Admin")
    mod = await guild.create_role(name="Moderator")
    vip = await guild.create_role(name="VIP")
    member = await guild.create_role(name="Member")
    verified = await guild.create_role(name="Verified")

    verify_overwrite = {
        everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False),
        verified: discord.PermissionOverwrite(view_channel=False),
    }

    read_only = {
        everyone: discord.PermissionOverwrite(view_channel=False),
        verified: discord.PermissionOverwrite(view_channel=True, send_messages=False)
    }

    chat_permissions = {
        everyone: discord.PermissionOverwrite(view_channel=False),
        verified: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    vip_permissions = {
        everyone: discord.PermissionOverwrite(view_channel=False),
        vip: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    welcome = await guild.create_category("Welcome")
    text_channels = await guild.create_category("Text Channels")
    premium = await guild.create_category("Premium")
    support = await guild.create_category("Support")

    verify = await guild.create_text_channel("verify", category=welcome, overwrites=verify_overwrite)
    rules = await guild.create_text_channel("rules", category=welcome, overwrites=read_only)
    announcements = await guild.create_text_channel("announcements", category=welcome, overwrites=read_only)
    vip_purchase = await guild.create_text_channel("vip-purchase", category=welcome, overwrites=read_only)

    await guild.create_text_channel("general-chat", category=text_channels, overwrites=chat_permissions)

    vip_chat = await guild.create_text_channel("vip-chat", category=premium, overwrites=vip_permissions)

    await guild.create_text_channel("open-a-ticket", category=support)
    await guild.create_text_channel("general-questions", category=support)

    games = [
        "2k",
        "fortnite",
        "apex",
        "rust",
        "call-of-duty",
        "warzone",
        "rainbow-six-siege"
    ]

    for game in games:

        category = await guild.create_category(game.upper())

        await guild.create_text_channel(
            f"{game}-script-info",
            category=category,
            overwrites=read_only
        )

        await guild.create_text_channel(
            f"{game}-free-scripts",
            category=category,
            overwrites=read_only
        )

        await guild.create_text_channel(
            f"{game}-chat",
            category=category,
            overwrites=chat_permissions
        )

        await guild.create_text_channel(
            f"{game}-clips",
            category=category,
            overwrites=chat_permissions
        )

    embed = discord.Embed(
        title="MulaScriptLab Verification",
        description="Click the button below to verify and unlock the server.",
        color=discord.Color.green()
    )

    await verify.send(embed=embed, view=VerifyView())

    await rules.send(
        "**Rules**\n\n"
        "1. Use these scripts responsibly\n"
        "2. Be respectful, report any undesirable behavior\n"
        "3. No leaking paid scripts\n"
        "4. No scamming, spam, or harassment\n"
        "5. Use the correct game channels\n"
        "6. Open support tickets for purchase or setup help\n"
        "7. Staff decisions are final"
    )

    await announcements.send(
        "**MulaScriptLabs Announcements**\n\n"
        "All scripts cost $30.\n\n"
        "DM staff or open a ticket to purchase.\n\n"
        "Buying any script grants VIP access.\n"
        "VIP members receive a 40% discount on all other scripts."
    )

    await vip_purchase.send(
        "**VIP Access**\n\n"
        "Buying any script grants VIP access.\n\n"
        "VIP members receive:\n"
        "- VIP chat access\n"
        "- 40% discount on all other scripts\n"
        "- Priority updates"
    )

    await ctx.send("Server layout complete.")


bot.run(TOKEN)
