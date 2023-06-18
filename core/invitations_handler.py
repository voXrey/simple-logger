import discord
from discord.ext import commands

class InvitationHandler:
    def __init__(self, client:commands.Bot):
        self.client = client
        self.guilds_invites = {}

    def add_guild_invite(self, invite:discord.Invite):
        guild = invite.guild
        if guild.id not in self.guilds_invites: self.guilds_invites[guild.id] = {}
        self.guilds_invites[guild.id][invite.code] = {
            "code": invite.code,
            "uses": invite.uses,
            "inviter": {
                "id": invite.inviter.id,
                "full-name": f"{invite.inviter.name}#{invite.inviter.discriminator}"
            }
        }

    def remove_guild_invite(self, invite:discord.Invite):
        guild = invite.guild
        if guild.id not in self.guilds_invites: return
        if invite.code in self.guilds_invites[guild.id]:
            del self.guilds_invites[guild.id][invite.code]

    async def get_guild_invites(self, guild:discord.Guild):
        for invite in await guild.invites():
            self.add_guild_invite(invite)
    
    async def get_guilds_invites(self):
        for guild in self.client.guilds:
            try: await self.get_guild_invites(guild)
            except: pass
        msg = f"Invitations getted"
        self.client.logger.logger.info(msg)
        print(msg)
    
    async def compare(self, guild:discord.Guild):
        last_invites = self.guilds_invites[guild.id]
        new_invites = await guild.invites()
        for last_invite_code,last_invite_info in last_invites.items():
            new_invite = None
            for inv in new_invites:
                if last_invite_code == inv.code: new_invite = inv
            if new_invite is None: continue
            if (last_invite_info["uses"] < new_invite.uses): return last_invite_info
            
    async def track_new_join(self, guild:discord.Guild) -> tuple[discord.Invite, dict]:
        return await self.compare(guild)