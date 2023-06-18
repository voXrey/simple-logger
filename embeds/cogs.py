import discord
from discord.ext import commands

import core

line_jump = '\n'

def cogs(lang:str, loaded_cogs, not_loaded_cogs) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.og_blurple())
    def en() -> discord.Embed:
        embed.add_field(name="✅ Loaded", value=f"{line_jump.join([f'● `{c}`' for c in loaded_cogs])}", inline=False)
        if len(not_loaded_cogs) > 0:
            embed.add_field(name="❌ Not Loaded", value=f"{line_jump.join([f'● `{cog_name}`' for cog_name in not_loaded_cogs])}", inline=False)
        return embed
    def fr() -> discord.Embed:
        embed.add_field(name="✅ Chargés", value=f"{line_jump.join([f'● `{c}`' for c in loaded_cogs])}", inline=False)
        if len(not_loaded_cogs) > 0:
            embed.add_field(name="❌ Non Chargés", value=f"{line_jump.join([f'● `{cog_name}`' for cog_name in not_loaded_cogs])}", inline=False)
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def cogs_load(lang:str, cog_name:str, result, cog_cogs:core.MyCog) -> discord.Embed:
    def en() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Cog `{cog_name}` has been loaded", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Cog `{cog_name}` couldn't be loaded: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed
    def fr() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Le Cog `{cog_name}` a été chargé", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Le Cog `{cog_name}` n'a pas pu être chargé: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def cogs_unload(lang:str, cog_name:str, result, cog_cogs:core.MyCog) -> discord.Embed:
    def en() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Cog `{cog_name}` has been unloaded", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Cog `{cog_name}` couldn't be unloaded: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed
    def fr() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Le Cog `{cog_name}` a été déchargé", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Le Cog `{cog_name}` n'a pas pu être déchargé: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def cogs_reload(lang:str, cog_name:str, result, cog_cogs:core.MyCog) -> discord.Embed:
    def en() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Cog `{cog_name}` has been reloaded", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Cog `{cog_name}` couldn't be reloaded: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed
    def fr() -> discord.Embed:
        if result is None:
            embed = discord.Embed(description=f"✅ Le Cog `{cog_name}` a été rechargé", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"❌ Le Cog `{cog_name}` n'a pas pu être rechargé: {cog_cogs.client.extension_error_to_string(result)}", color=discord.Color.red())
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()
