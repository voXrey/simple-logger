import discord
from discord.ext import commands
from babel import dates

import core
import locale

line_jump = '\n'

def guild(lang:str, guild:discord.Guild) -> discord.Embed:
    embed = discord.Embed(title=f"{guild.name} ({guild.id})", color=discord.Color.purple())
    if guild.description is not None: embed.description = guild.description
    embed.set_image(url=guild.banner)
    embed.set_thumbnail(url=guild.icon)
    datetime = guild.created_at

    def en() -> discord.Embed:
        embed.add_field(name="Owner", value=f"{guild.owner}\n`{guild.owner_id}`")
        embed.add_field(name="Members", value=f"● Users: `{guild.member_count}`\n● Bots: `{len([member for member in guild.members if member.bot])}`")
        
        premium_level = [
            "No premium",
            "Level 1",
            "Level 2",
            "Level 3"
        ]
        embed.add_field(name="Premium", value=premium_level[guild.premium_tier])
        embed.add_field(name="Text channels", value=f"`{len(guild.text_channels)}` channels")
        embed.add_field(name="Voice channels", value=f"`{len(guild.voice_channels)}` channels")
        embed.add_field(name="Roles", value=f"`{len(guild.roles)}` roles")
        embed.add_field(name="Emojis", value=f"`{len(guild.emojis)}/{guild.emoji_limit}`\n{''.join([str(emoji) for emoji in guild.emojis])}", inline=False)
        embed.add_field(name="Created the", value="{0:%A} {0:%d} {0:%B} {0:%Y} at {0:%I:%M%p}".format(datetime), inline=False)
        return embed
    def fr() -> discord.Embed:
        embed.add_field(name="Propriétaire", value=f"{guild.owner}\n`{guild.owner_id}`")
        embed.add_field(name="Membres", value=f"● Utilisateurs: `{guild.member_count}`\n● Bots: `{len([member for member in guild.members if member.bot])}`")

        premium_level = [
            "Non premium",
            "Niveau 1",
            "Niveau 2",
            "Niveau 3"
        ]
        embed.add_field(name="Premium", value=premium_level[guild.premium_tier])
        embed.add_field(name="Salons textuels", value=f"`{len(guild.text_channels)}` salons")
        embed.add_field(name="Salons vocaux", value=f"`{len(guild.voice_channels)}` salons")
        embed.add_field(name="Rôles", value=f"`{len(guild.roles)}` rôles")
        embed.add_field(name="Emojis", value=f"`{len(guild.emojis)}/{guild.emoji_limit}`\n{''.join([str(emoji) for emoji in guild.emojis])}", inline=False)
        embed.add_field(name="Création le", value=dates.format_datetime(datetime, "EEEE d MMMM yyyy à hh:mm", locale='fr').capitalize(), inline=False)
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()