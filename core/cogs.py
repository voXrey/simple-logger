import discord
from discord.ext import commands


class MyCog(commands.Cog):
    def __init__(self, client:commands.Bot, full_name:str):
        super().__init__()
        self.client = client
        self.full_name = full_name
        msg = f"Cog '{self.qualified_name}' has been loaded (file: {self.full_name})"
        self.client.logger.logger.info(msg)
        print(msg)
        
    def cog_unload(self):
        msg = f"Cog '{self.qualified_name}' has been unloaded (file: {self.full_name})"
        self.client.logger.logger.info(msg)
        print(msg)
