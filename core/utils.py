import json

import core.database as database
from discord.ext import commands


def get_json(file_path) -> dict:
    with open(file_path, 'r', encoding='utf8') as json_file:
        return json.load(json_file)

def get_guild_lang(guild_id:int) -> str:
    with database.Database() as db:
        guild_data = db.get_guild(guild_id)
        return guild_data.lang

def get_guild_prefix(guild_id:int) -> str:
    with database.Database() as db:
        guild_data = db.get_guild(guild_id)
        return guild_data.prefix

def get_prefix(client, message) -> str:
    return get_guild_prefix(message.guild.id)