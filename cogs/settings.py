import core
import discord
import embeds
from discord.ext import commands


class Settings(core.MyCog, name="settings"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.settings")

    @commands.group(name='settings', invoke_without_command=True)
    @commands.guild_only()
    async def _settings(self, ctx:commands.Context):
        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
        
        embed = embeds.guild_settings(lang, guild_data)
        await ctx.send(embed=embed)

    @_settings.command(name='reset')
    @commands.guild_only()
    async def _settings_reset(self, ctx:commands.Context, setting:str=None):
        users_settings = core.get_json('data/users-settings.json')
        settings = {}
        if setting is None:
            for users_setting in users_settings.values():
                settings[users_setting["db-column"]] = None
        else:
            if setting not in users_settings.keys(): raise core.UnknowSetting(setting)
            settings[setting] = None
        
        with core.Database() as db:
            db.edit_guild(ctx.guild.id, settings)
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.guild_settings(lang, guild_data)
        await ctx.send(embed=embed)
    
    @_settings.command(name="set")
    @commands.guild_only()
    async def _settings_set(self, ctx:commands.Context, setting_name:str, *, new_value:str):
        users_settings = core.get_json('data/users-settings.json')
        if setting_name not in users_settings.keys(): raise core.UnknowSetting(setting_name)
        setting = users_settings[setting_name]
        if setting["restricted"] and new_value not in setting["values"]: raise core.BadSettingValue(setting_name, new_value)
        
        with core.Database() as db:
            db.edit_guild(ctx.guild.id, {setting_name:new_value})
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.setting_set(lang, setting, new_value)
        await ctx.send(embed=embed)


    @_settings.command(name="help")
    @commands.guild_only()
    async def _settings_help(self, ctx:commands.Context, setting_name:str):
        users_settings = core.get_json('data/users-settings.json')
        if setting_name not in users_settings.keys(): raise core.UnknowSetting(setting_name)
        setting = users_settings[setting_name]
        
        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.setting_help(lang, setting)
        await ctx.send(embed=embed)


async def setup(client:commands.Bot):
    await client.add_cog(Settings(client))
