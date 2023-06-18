import discord
from discord.ext import commands


class ChannelHandler:
    def __init__(self, client:commands.Bot):
        self.client = client
        self.channels = {}

    async def fetch_channels(self):
        """Fetchs some importants channels for the bot"""
        for key,channel_id in self.client.settings['channels'].items():
            try:
                self.channels[key] = await self.client.fetch_channel(channel_id)
                msg = f"Channel '{key}' ({channel_id}) fetched"
                self.client.logger.logger.info(msg)
                print(msg)
            except Exception as e:
                self.channels[key] = None
                msg = f"Impossible to fetch channel '{key}' ({channel_id}): {e.__class__.__name__}"
                self.client.logger.logger.warn(msg)
                print(msg)