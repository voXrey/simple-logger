import typing
import discord
from discord.ext import commands
import core


def guild_settings(lang:str, guild_data:core.GuildData) -> discord.Embed:
    users_settings = core.get_json('data/users-settings.json')
    embed = discord.Embed(color=discord.Color.og_blurple())

    def en():
        embed.title = "Settings"
        for users_setting in users_settings.values():
            value = guild_data.get(users_setting["data-guild-name"])
            if value is None: value = users_setting["default"] 
            embed.add_field(name=users_setting["name"], value=f"`{value}`")
        return embed
    def fr():
        embed.title = "Settings"
        for users_setting in users_settings.values():
            value = guild_data.get(users_setting["data-guild-name"])
            if value is None: value = users_setting["default"] 
            embed.add_field(name=users_setting["name"], value=f"`{value}`")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def setting_set(lang:str, setting:dict, value) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.og_blurple())

    def en():
        embed.title = f"Setting '{setting['name']}' changed"
        embed.description = f"New value for this setting is `{value}`."
        return embed
    def fr():
        embed.title = f"Le setting '{setting['name']}' a changé"
        embed.description = f"La nouvelle valeur pour ce setting est `{value}`."
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

def setting_help(lang:str, setting:dict) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.og_blurple())

    def en():
        embed.title = f"Setting '{setting['name']}'"
        embed.description = setting["description"]["en"]
        embed.add_field(name="Default", value=f"`{setting['default']}`")
        if setting["restricted"]:
            embed.add_field(name="Values", value=f"{', '.join([f'`{v}`' for v in setting['values']])}")
        return embed
    def fr():
        embed.title = f"Setting '{setting['name']}'"
        embed.description = setting["description"]["fr"]
        embed.add_field(name="Défault", value=f"`{setting['default']}`")
        if setting["restricted"]:
            embed.add_field(name="Valeurs", value=f"{', '.join([f'`{v}`' for v in setting['values']])}")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()
