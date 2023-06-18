import core
import discord
import embeds
from discord.ext import commands


class Spy(core.MyCog, name="spy"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.spy")

    @commands.command(name="invites", ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def _invites(self, ctx, *, guild:discord.Guild):
        invites = await guild.invites()

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
        
        embed = embeds.invites(lang, guild, invites)
        await ctx.send(embed=embed)
    
    @commands.command(name="create-invite", ignore_extra=True)
    @commands.is_owner()
    async def _create_invite(self, ctx:commands.Context, guild:discord.Guild, infinity:bool=False):
        channels = guild.text_channels + guild.voice_channels

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        invite_url = None
        if len(channels) > 0:
            channel:discord.abc.GuildChannel = channels[0]
            uses = 0 if infinity else 1
            invite:discord.Invite = await channel.create_invite(max_uses=uses, unique=False)
            invite_url = invite.url
        
        embed = embeds.create_invite(lang, invite_url)
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if isinstance(message.channel, discord.DMChannel) and (not message.author.bot):
            if self.client.channel_handler.channels["resend_dm"] is None: return
            embed = discord.Embed(description=message.content, colour=discord.Color.purple())
            embed.set_author(name=message.author, icon_url=message.author.avatar)
            embed.timestamp = message.created_at
            await self.client.channel_handler.channels["resend_dm"].send(embed=embed, files=[await f.to_file() for f in message.attachments])

    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        with core.Database() as db:
            db.add_guilds({guild.id})
            if self.client.channel_handler.channels["guilds"] is None: return
            channel:discord.TextChannel = self.client.channel_handler.channels["guilds"]
            guild_data = db.get_guild(channel.guild.id)
            lang = guild_data.lang

        embed = embeds.on_guild_join(lang, guild, len(self.client.guilds))    
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        with core.Database() as db:
            db.remove_guilds({guild.id})
            if self.client.channel_handler.channels["guilds"] is None: return
            channel:discord.TextChannel = self.client.channel_handler.channels["guilds"]
            guild_data = db.get_guild(channel.guild.id)
            lang = guild_data.lang

        embed = embeds.on_guild_remove(lang, guild, len(self.client.guilds))
        await channel.send(embed=embed)


async def setup(client:commands.Bot):
    await client.add_cog(Spy(client))
