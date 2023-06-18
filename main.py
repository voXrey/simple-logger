import asyncio
import time
from pathlib import Path
from typing import Optional

import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import (ExtensionAlreadyLoaded,
                                         ExtensionError, ExtensionFailed,
                                         ExtensionNotFound, ExtensionNotLoaded)

import core

TOKEN_TO_USE = "DEV_TOKEN"
TEST_GUILD = discord.Object(1001431307651403867)

class MyBot(commands.Bot):
    """Represents the bot"""
    def init(self, logger:core.BotLogger):
        self.logger = logger
        self.logger.logger.info("Bot init begins")

        self.starting_time=time.time()

        self.commands_info = self.get_commands_info() # get commands info
        self.special_channels = self.get_special_channels() # get special channels info
        self.settings = self.get_settings() # get and set settings
        self.permissions_trads = core.get_json("./data/permissions.json") # get permissions trads
        
        with core.Database() as db: db.create_table() # create database's table

        self.channel_handler = core.ChannelHandler(self) # create the handler for channels
        self.invitations_handler = core.InvitationHandler(self) # create the handler for invitations
        
        self.logger.logger.info("Bot init complete")

    async def setup_hook(self):
        await self.load_cogs() # load cogs
        self.add_checks_permissions() # add check to verify bot and users permissions
        await self.tree.sync(guild=TEST_GUILD) # sync

    async def on_ready(self):
        """Executed during bot is connecting to discord"""
        await self.wait_until_ready_task()
        msg = f'Bot is ready! Loaded in {format(time.time()-self.starting_time, ".1f")} seconds'
        self.logger.logger.info(msg)
        print(msg)
    
    @tasks.loop(count=1)
    async def wait_until_ready_task(self):
        """Executed after bot is ready"""
        await self.wait_until_ready()
        self.logger.logger.info("Executing tasks after they are ready")
        
        # do
        await self.update_database_guilds() # update guilds in database
        await self.channel_handler.fetch_channels() # fetch channels in handler
        await self.invitations_handler.get_guilds_invites() # fetch guilds invitations


    async def on_error(self, event, *args, **kwargs):
        """Catchs errors in events"""

        events = [
            "on_message_delete",
            "on_message_edit",
            "on_member_join",
            "on_member_update",
            "on_member_remove",
            "on_guild_channel_create",
            "on_guild_channel_delete",
            "on_guild_channel_update",
            "on_guild_role_create",
            "on_guild_role_delete",
            "on_invite_create",
            "on_invite_delete",
            "on_guild_join",
            "on_guild_remove"
        ]
        if event not in events:
            self.logger.log_event_error(event, args=args, kwargs=kwargs)
            raise
        else:
            self.logger.log_event_warn(event, args=args, kwargs=kwargs)

    def get_config(self) -> dict:
        """Get bot's config"""
        self.logger.logger.info("Config getted")
        return core.get_json("./data/config.json")

    def get_settings(self) -> dict:
        "Get bot's settings"
        self.logger.logger.info("Settings getted")
        return core.get_json("./data/settings.json")
    
    def get_commands_info(self) -> dict:
        """Get bot's commands info"""
        self.logger.logger.info("Commands getted")
        return core.get_json("./data/commands.json")
    
    def get_special_channels(self) -> dict:
        """Get logs channels info"""
        self.logger.logger.info("Channels getted")
        return core.get_json("./data/channels.json")

    def get_cogs(self) -> list[str]:
        """
        Get all cogs names

        Returns:
            list[str]: list of names
        """
        self.logger.logger.info("Cogs paths getted")
        return [f.name[:-3] for f in list(Path("./cogs").rglob("*.py"))]

    def extension_error_to_string(self, error:ExtensionError) -> str:
        """Get string corresponding to an extension error"""
        if isinstance(error, ExtensionAlreadyLoaded):
            return "cog already loaded"
        elif isinstance(error, ExtensionNotLoaded):
            return "cog not loaded"
        elif isinstance(error, ExtensionNotFound):
            return "cog not found"
        else:
            return f"cog failed (impossible to setup cog: {error})"

    async def load_cogs(self):
        """
        Load all bot's cogs
        """
        files = self.get_cogs()
        for file in files:
            if file == "__init__": continue

            try:
                await self.load_extension(f"cogs.{file}")
            except ExtensionError as e:
                msg = f"Cog '{file}' couldn't be loaded: {self.extension_error_to_string(e)}"
                self.logger.logger.error(msg)
                print(msg)
                return e
    
    async def load_cog(self, cog_name:str) -> Optional[ExtensionError]:
        """
        Load a bot's cog

        Args:
            cog_name (str): name of the cog to load

        Returns:
            bool: loading's success
        """
        try:
            await self.load_extension("cogs."+cog_name)
        except ExtensionError as e:
            self.logger.logger.error(f"Cog '{cog_name}' couldn't be loaded: {self.extension_error_to_string(e)}")
            return e

    async def reload_cog(self, cog_name:str) -> Optional[ExtensionError]:
        """
        Reload a bot's cog

        Args:
            cog_name (str): name of cog to reload

        Returns:
            bool: reloading's success
        """
        try:
            await self.reload_extension("cogs."+cog_name)
        except ExtensionError as e:
            self.logger.logger.error(f"Cog '{cog_name}' couldn't be loaded: {self.extension_error_to_string(e)}")
            return e

    async def unload_cog(self, cog_name:str) -> Optional[ExtensionError]:
        """
        Unload a bot's cog

        Args:
            cog_name (str): name of the cog to unload

        Returns:
            bool: unloading's success
        """
        try:
            await self.unload_extension("cogs."+cog_name)
        except ExtensionError as e:
            self.logger.logger.error(f"Cog '{cog_name}' couldn't be loaded: {self.extension_error_to_string(e)}")
            return e

    async def check_permissions(self, ctx:commands.Context):
        """Check if user and bot have permissions to execute command"""
        if ctx.guild is not None:
            command_name = ctx.command.qualified_name
            if command_name in self.commands_info["commands"]: command_info = self.commands_info["commands"][command_name]
            elif command_name in self.commands_info["owner-commands"]: command_info = self.commands_info["owner-commands"][command_name]
            else: raise core.CommandNotReferenced(command_name)

            def predicate(bot:bool, member_permissions, perms:dict):
                missing = [perm for perm, value in perms.items() if getattr(member_permissions, perm) != value]
                if not missing: return

                if bot: raise commands.errors.BotMissingPermissions(missing)
                raise commands.errors.MissingPermissions(missing)
            
            user_required_permissions = {}
            for user_required_permission in command_info["user-permissions"]: user_required_permissions[user_required_permission] = True
            guild_user_permissions = ctx.author.guild_permissions
            predicate(False, guild_user_permissions, user_required_permissions)

            bot_required_permissions = {}
            for bot_required_permission in command_info["bot-permissions"]: bot_required_permissions[bot_required_permission] = True
            guild_bot_permissions = ctx.guild.me.guild_permissions
            predicate(True, guild_bot_permissions, bot_required_permissions)

        return True
    
    def get_subcommands(self, command:commands.Command) -> list:
        subcommands = []
        if isinstance(command, commands.Group):
            for subcommand in command.walk_commands():
                subcommands.append(subcommand)
                subcommands.extend(self.get_subcommands(subcommand))
        return subcommands

    def add_checks_permissions(self):
        """Add checks permissions to all commands"""
        def _add_check(command:commands.Command):
            try:
                command.add_check(self.check_permissions)
                self.logger.logger.info(f'Check permissions add to command [{command.qualified_name}]')
            except Exception as e:
                self.logger.logger.error(f'Impossible to add check permissions to command [{command.qualified_name}]: {e}')
        for command in self.commands:
            _add_check(command)
            for subcommand in self.get_subcommands(command):
                _add_check(subcommand)
            
    async def update_database_guilds(self):
        self.logger.logger.info("Database updating started")
        guilds_id = set()
        async for guild in self.fetch_guilds(limit=None):
            guilds_id.add(guild.id)

        with core.Database() as db:
            # know which guilds must to be added or removed to database
            database_guilds_id = db.get_all_guilds_id()
            missing_guilds_id = guilds_id.difference(database_guilds_id)
            guilds_id_surplus = database_guilds_id.difference(guilds_id)

            # modify database
            db.add_guilds(missing_guilds_id)
            db.remove_guilds(guilds_id_surplus)
        
        self.logger.logger.info("Database updating finished")

if __name__ == '__main__':
    # create client
    client = MyBot(
        command_prefix=core.get_prefix,
        help_command=None,
        intents=discord.Intents.all(),
        owner_id=625441412716167178,
        activity=discord.Game(name=".help")
    )
    # create logger
    logger = core.BotLogger(client)

    # init client
    try:
        client.init(logger)
    except Exception as e:
        msg = f"Impossible to init client: {e.__class__.__name__}"
        logger.logger.critical(msg)
        print(msg)

    # async
    async def main():

        # run client
        try:
            async with client:
                await client.start(client.get_config()[TOKEN_TO_USE])
        except Exception as e:
            msg = f"Impossible to connect bot to discord: {e.__class__.__name__}"
            client.logger.logger.critical(msg)
            print(msg)
        finally:
            client.logger.logger.info("Program finished")
    
    asyncio.run(main())
