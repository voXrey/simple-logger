import core
import embeds
import discord
from discord.ext import commands


class Info(core.MyCog, name="info"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.info")

    @commands.command(name="guild")
    @commands.guild_only()
    async def _guild(self, ctx:commands.Context, *, guild:discord.Guild=None):
        """See guild's info"""
        if guild is None:
            if ctx.guild is None: await ctx.send(embed=discord.Embed(description=f"❌ Your are not in a guild"))
            else: guild = ctx.guild

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.guild(lang, guild)
        await ctx.send(embed=embed)

async def setup(client:commands.Bot):
    await client.add_cog(Info(client))
