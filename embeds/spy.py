import typing
import discord
from discord.ext import commands


def invites(lang:str, guild:discord.Guild, invites:list[discord.Invite]) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.blurple())

    description = None
    if len(invites) > 0:
        description = '\n'.join([f"- [{invite.inviter}]({invite.url})" for invite in invites])

    def en(description):
        embed.title = f"Invites for '{guild.name}' ({guild.id})"
        if description is None:
            description = f"No invitation available on this server."
        embed.description = description
        return embed
    def fr(description):
        embed.title = f"Invitations pour '{guild.name}' ({guild.id})"
        if description is None:
            description = f"Aucune invitation disponible pour ce serveur."
        embed.description = description
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang](description)

def create_invite(lang:str, invite_url:typing.Optional[str]) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.blurple())

    def en():
        if invite_url is not None:
            embed.description = f"Invitation created: [link]({invite_url})"
        else:
            embed.description = "Impossible to create invite, server haven't channel."
        return embed
    def fr():
        if invite_url is not None:
            embed.description = f"Invitation créée : [lien]({invite_url})"
        else:
            embed.description = "Impossible de créer une invitation, le serveur n'a pas de salon."
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def on_guild_join(lang:str, guild:discord.Guild, guilds_count:int) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.green())
    embed.timestamp = guild.me.joined_at
    embed.set_author(name=f"{guild.name} ({guild.id})", icon_url=guild.icon)

    def en():
        embed.description = "Bot joined a new server!"
        embed.set_footer(text=f"Servers: {guilds_count}")
        return embed
    def fr():
        embed.description = "Le bot a rejoint un nouveau serveur !"
        embed.set_footer(text=f"Serveurs : {guilds_count}")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def on_guild_remove(lang:str, guild:discord.Guild, guilds_count:int) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.red())
    embed.timestamp = discord.utils.utcnow()
    embed.set_author(name=f"{guild.name} ({guild.id})", icon_url=guild.icon)

    def en():
        embed.description = "Bot left a server..."
        embed.set_footer(text=f"Servers: {guilds_count}")
        return embed
    def fr():
        embed.description = "Le bot a quitté un serveur..."
        embed.set_footer(text=f"Serveurs : {guilds_count}")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

