import core
import embeds
import discord
from discord.ext import commands


class Logging(core.MyCog, name="logging"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.logging")

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def _setup(self, ctx: commands.Context, category: str = None):
        """Setup logs channels"""
        guild = ctx.guild

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        # channels permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True)
        }

        # create or use a category for logs channels
        if category is not None:
            categories = filter(lambda x: x.name.lower() ==
                                category, guild.categories)
            try:
                category = next(categories)
            except StopIteration:
                category = await guild.create_category(name=category, reason="Setup logs", overwrites=overwrites)

        if category is None:
            categories = filter(lambda x: x.name.lower() ==
                                'logs', guild.categories)
            try:
                category = next(categories)
            except StopIteration:
                category = None
            if category is None:
                category: discord.CategoryChannel = await guild.create_category(name="logs", reason="Setup logs")

        channels = self.client.special_channels
        channels_setted = []

        # create channels and send messages, embeds, and pins them
        for channel, channel_info in channels.items():
            channel = await category.create_text_channel(name=channel, reason="Setup logs", overwrites=overwrites)
            embed = embeds.channel_setted(
                lang, channel.name, channel_info, ctx.author)
            msg: discord.Message = await channel.send(embed=embed)
            await msg.pin(reason="Setup logs")
            channels_setted.append(channel)

        # send final embed
        embed = embeds.setup(lang, channels_setted, ctx.author)
        await ctx.send(embed=embed)

    def get_datetime(self, utc: bool = False):
        date = discord.utils.utcnow()
        if utc:
            date.replace(tzinfo=None)
        return date

    def check_member(self, member: discord.Member, log_channel: discord.TextChannel) -> bool:
        """Check if a member's can be logged"""
        if (log_channel.topic is None):
            return True
        elif (str(member.id) in log_channel.topic):
            return False
        for role in member.roles:
            if self.check_role(role, log_channel):
                return False
        return True

    def check_channel(self, channel: discord.abc.GuildChannel, log_channel: discord.TextChannel):
        """Check if a channel can be logged"""
        if (log_channel.topic is None):
            return True
        elif (channel.category is not None) and (str(channel.category.id) in log_channel.topic):
            return False
        elif (str(channel.id) in log_channel.topic):
            return False
        else:
            return True

    def check_message(self, message: discord.Message, log_channel: discord.TextChannel) -> bool:
        """Check if a message can be logged"""
        if (log_channel.topic is None):
            return True
        elif not self.check_channel(message.channel, log_channel):
            return False
        elif not self.check_member(message.author, log_channel):
            return False
        else:
            return True

    def check_role(self, role: discord.Role, log_channel: discord.TextChannel) -> bool:
        """Check if a role can be logger"""
        if (log_channel.topic is None):
            return True
        elif (str(role.id) in log_channel.topic):
            return False
        else:
            return True

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """Log edited messages"""
        if (not isinstance(before.channel, discord.TextChannel)) or (before.author.bot):
            return
        guild: discord.Guild = before.channel.guild
        channel = discord.utils.get(guild.text_channels, name="logs-messages")

        if channel is not None:
            if self.check_message(before, channel):
                # get guild's lang
                lang = core.get_guild_lang(guild.id)

                embed = embeds.on_message_edit(lang, before, after)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """Log deleted messages"""
        if (not isinstance(message.channel, discord.TextChannel)) or (message.author.bot):
            return
        guild = message.guild
        channel = discord.utils.get(guild.text_channels, name="logs-messages")

        if channel is not None:
            if not self.check_message(message, channel):
                return  # check if the message can be logged
            now = self.get_datetime()

            # get guild's lang
            lang = core.get_guild_lang(guild.id)

            embed = embeds.on_message_delete(lang, message, now)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Log members update"""
        guild = before.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs-members")
        if log_channel is not None:
            # get guild's lang
            lang = core.get_guild_lang(guild.id)

            # log member's roles changements
            if before.roles != after.roles:
                audit_logs = guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.member_role_update)
                log: discord.AuditLogEntry = await audit_logs.__anext__()
                user = log.user
                if not self.check_member(user, log_channel):
                    return

                if len(before.roles) > len(after.roles):
                    changement = "role-removed"
                    role = set(before.roles).difference(set(after.roles)).pop()
                else:
                    changement = "role-added"
                    role = set(after.roles).difference(set(before.roles)).pop()
                date = log.created_at

                embed = embeds.on_member_update(lang, before, after, changement, user, date, role)
                await log_channel.send(embed=embed)

            # log member's nickname changements
            elif before.display_name != after.display_name:
                changement = "nickname-changed"
                audit_logs = guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.member_update)
                log: discord.AuditLogEntry = await audit_logs.__anext__()
                user = log.user
                if not self.check_member(user, log_channel):
                    return

                if log.before.nick != log.after.nick:
                    date = log.created_at

                    embed = embeds.on_member_update(lang, before, after, changement, user, date)
                    await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Log new members"""
        past_invite_info = await self.client.invitations_handler.track_new_join(member.guild)
        await self.client.invitations_handler.get_guild_invites(member.guild)

        channel = discord.utils.get(
            member.guild.text_channels, name="logs-members")
        if channel is not None:
            if not self.check_member(member, channel):
                return
            
            # get guild's lang
            lang = core.get_guild_lang(member.guild.id)

            embed = embeds.on_member_join(lang, member, past_invite_info)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log members who left"""
        channel = discord.utils.get(
            member.guild.text_channels, name="logs-members")
        if channel is not None:
            if not self.check_member(member, channel):
                return
            
            # get guild's lang
            lang = core.get_guild_lang(member.guild.id)

            embed = embeds.on_member_remove(lang, member)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        """Log new channels"""
        log_channel = discord.utils.get(
            channel.guild.text_channels, name="logs-server")
        if log_channel is not None:
            guild: discord.Guild = channel.guild
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_create)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user
            if not self.check_member(user, log_channel):
                return

            # get guild's lang
            lang = core.get_guild_lang(channel.guild.id)

            embed = embeds.on_guild_channel_create(lang, channel, log)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        """Log deleted channels"""
        log_channel = discord.utils.get(
            channel.guild.text_channels, name="logs-server")
        if log_channel is not None:
            guild: discord.Guild = channel.guild
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_delete)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user
            if not self.check_member(user, log_channel):
                return
            if not self.check_channel(channel, log_channel):
                return

            # get guild's lang
            lang = core.get_guild_lang(channel.guild.id)

            embed = embeds.on_guild_channel_delete(lang, channel, log)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        """Log all channels updates"""
        if before.position != after.position: return
        log_channel = discord.utils.get(before.guild.text_channels, name="logs-server")
        if log_channel is None: return
        if not self.check_channel(before, log_channel): return
        guild: discord.Guild = before.guild
        line_jump = '\n'

        # if permissions changed
        if before.overwrites != after.overwrites:
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.overwrite_update)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user
            changes_before, changes_after = log.changes.before.__dict__, log.changes.after.__dict__

            if not self.check_member(user, log_channel):
                return

            # get guild's lang
            lang = core.get_guild_lang(guild.id)

            embed = embeds.on_guild_channel_update_permissions(lang, before, after, log, self.client.permissions_trads)
            return await log_channel.send(embed=embed)

        # if channels settings changed
        else:
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_update)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user

            # check if the channel's update can be logged
            if not self.check_member(user, log_channel):
                return

            # get guild's lang
            lang = core.get_guild_lang(guild.id)

            embed = embeds.on_guild_channel_update(lang, before, after, log)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        """Log new roles"""
        managed = role.managed
        guild: discord.Guild = role.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs-server")
        if log_channel is None: return

        log = None
        if not managed:
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_create)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user
            if not self.check_member(user, log_channel):
                return

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        embed = embeds.on_guild_role_create(lang, role, log)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """Log deleted roles"""
        log_channel = discord.utils.get(
            role.guild.text_channels, name="logs-server")
        if log_channel is None: return
        guild: discord.Guild = role.guild
        
        log = None
        if not role.managed:
            audit_logs = guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            if not self.check_member(log.user, log_channel): return

        if not self.check_role(role, log_channel): return

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        embed = embeds.on_guild_role_delete(lang, role, log)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        """Log updated roles"""
        managed = (before.tags is not None) and (before.tags.is_integration())
        
        guild: discord.Guild = before.guild
        log_channel = discord.utils.get(guild.text_channels, name="logs-server")
        if log_channel is None: return
        if not managed:
            audit_logs = guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_update)
            log: discord.AuditLogEntry = await audit_logs.__anext__()
            user = log.user
            if not self.check_member(user, log_channel): return

        if not self.check_role(before, log_channel): return

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        if before.permissions != after.permissions:
            embed = embeds.on_guild_role_update_permissions(lang, before, after, log, self.client.permissions_trads)
            await log_channel.send(embed=embed)

        changes = []
        if before.name != after.name: changes.append("name")
        if before.color != after.color: changes.append("color")
        if before.hoist != after.hoist: changes.append("hoist")
        if before.mentionable != after.mentionable: changes.append("mentionable")

        if len(changes) > 0:
            embed = embeds.on_guild_role_update(lang, before, after, log, changes)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        """Log new invitations"""
        self.client.invitations_handler.add_guild_invite(invite)

        log_channel = discord.utils.get(invite.guild.text_channels, name="logs-invitations")
        if log_channel is None: return

        guild: discord.Guild = invite.guild
        audit_logs = guild.audit_logs(
            limit=1, action=discord.AuditLogAction.invite_create)
        log: discord.AuditLogEntry = await audit_logs.__anext__()
        user = invite.inviter

        if not self.check_member(user, log_channel):
            return

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        embed = embeds.on_invite_create(lang, invite, log)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        """Log deleted invitations"""
        log_channel = discord.utils.get(
            invite.guild.text_channels, name="logs-invitations")
        if log_channel is None:
            return
        guild: discord.Guild = invite.guild

        # get guild's lang
        lang = core.get_guild_lang(guild.id)

        embed = embeds.on_invite_delete(lang, invite)
        await log_channel.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Logging(client))
