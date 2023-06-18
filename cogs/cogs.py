import core
import discord
import embeds
from discord.ext import commands


class Cogs(core.MyCog, name="cogs"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.cogs")

    @commands.group(name='cogs', invoke_without_command=True)
    @commands.is_owner()
    @commands.guild_only()
    async def cogs(self, ctx:commands.Context):
        """Show cogs"""
        cogs_names = self.client.get_cogs()
        loaded_cogs = [loaded_cog[5:] for loaded_cog in self.client.extensions.keys()]
        not_loaded_cogs = [cog_name for cog_name in cogs_names if cog_name not in loaded_cogs]

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
            
        embed = embeds.cogs(lang, loaded_cogs, not_loaded_cogs)
        await ctx.send(embed=embed)

    @cogs.command(name='load', ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def cogs_load(self, ctx:commands.Context, cog_name:str):
        """Load a cog"""
        result = await self.client.load_cog(cog_name=cog_name)

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.cogs_load(lang, cog_name, result, self)
        await ctx.send(embed=embed)

    @cogs.command(name='reload', ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def cogs_reload(self, ctx:commands.Context, cog_name:str):
        """Reload a cog"""
        result = await self.client.reload_cog(cog_name=cog_name)
        
        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
        
        embed = embeds.cogs_reload(lang, cog_name, result, self)
        await ctx.send(embed=embed)

    @cogs.command(name='unload', ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def cogs_unload(self, ctx:commands.Context, cog_name:str):
        """Unload a cog"""
        result = await self.client.unload_cog(cog_name=cog_name)
        
        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
        
        embed = embeds.cogs_unload(lang, cog_name, result, self)
        await ctx.send(embed=embed)
    


async def setup(client:commands.Bot):
    await client.add_cog(Cogs(client))
