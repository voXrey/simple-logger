import core
import discord
import embeds
from discord.ext import commands


class Errors(core.MyCog, name="errors"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.errors")

    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:Exception):
        if ctx.guild is None: return

        # modify error to be able to correctly manage her
        if isinstance(error, discord.errors.Forbidden):
            if error.code == 50013:
                error = core.ForbiddenMissingPermissions
            elif error.code == 50001:
                error = core.ForbiddenMissingAccess
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        # get embed
        r = embeds.error(lang, error, ctx, self.client.permissions_trads)
        if r is None: return
        embed, log = r
        if log: self.client.logger.log_command_debug(ctx, error)
        await ctx.send(embed=embed)

async def setup(client:commands.Bot):
    await client.add_cog(Errors(client))
