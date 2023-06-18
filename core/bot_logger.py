import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import discord
from discord.ext import commands

class BotLogger:
    def __init__(self, client:commands.Bot):
        self.client = client

        # Create logger
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

        # Create a file handler
        date = discord.utils.utcnow()
        filename = f"./logs/{str(date.day).zfill(2)}-{str(date.month).zfill(2)}-{str(date.year)}.log"
        self.file_handler = TimedRotatingFileHandler(
            filename=filename,
            when="midnight",
            encoding="utf-8",
            utc=True
        )
        self.file_handler.setLevel(logging.DEBUG)
        ## set formatter
        self.file_handler.setFormatter(formatter)

        # Add file handler to logger
        self.logger.addHandler(self.file_handler)

    def create_log_command_msg(self, ctx:commands.Context, error):
        msg = f'Impossible to execute command "{ctx.message.content}"'
        if ctx.guild is not None:
            a:discord.Member = ctx.author
            msg += f' in a guild'
            msg += f', user permissions({ctx.channel.permissions_for(ctx.author).value}) bot({ctx.author.bot}) owner({ctx.author.id in self.client.owner_ids})'
            msg += f', bot permissions({ctx.channel.permissions_for(ctx.me).value})'
        else:
            msg += f' in a dm'
        msg += f': {error.__class__.__name__}'
        return msg

    def log_command_debug(self, ctx:commands.Context, error):
        try: self.logger.debug(self.create_log_command_msg(ctx, error))
        except Exception as e: print(e)
    
    def log_event_warn(self, event, args, kwargs):
        self.logger.warn(f'During event "{event}"')
    
    def log_event_error(self, event, args, kwargs):
        self.logger.error(f'During event "{event}"')