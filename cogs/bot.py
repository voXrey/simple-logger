import datetime

import ui
import core
import discord
import embeds
from discord.ext import commands


class Bot(core.MyCog, name="bot"):
    def __init__(self, client: commands.Bot):
        super().__init__(client, full_name="cogs.bot")

    @commands.command(name='invite', ignore_extra=True)
    @commands.guild_only()
    async def _invite(self, ctx:commands.Context):
        permissions = discord.Permissions(1642560089329)
        bot_invite = discord.utils.oauth_url(self.client.user.id, permissions=permissions)

        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang

        embed = embeds.invite(lang, bot_invite)
        await ctx.send(embed=embed)
    
    
    @commands.command(name='help', ignore_extra=True)
    @commands.guild_only()
    async def _help(self, ctx:commands.Context, *, command:str=None):
        """Command to help users"""
        # get guild's lang
        lang = core.get_guild_lang(ctx.guild.id)

        if command is None:
            embeds_dict = embeds.help(lang, self.client.commands_info, self.client.special_channels)
            view = ui.ViewHelp(lang, timeout=320)
            message = await ctx.send(embed=embeds_dict["help"], view=view)
            
            while True:
                timeout = await view.wait()
                if timeout: break
                value = view.value
                view = ui.ViewHelp(lang)
                await message.edit(embed=embeds_dict[value], view=view)


        if command is not None:
            if command in self.client.commands_info["commands"]:
                command_info = self.client.commands_info["commands"][command]
                embed=embeds.help_command(lang, command, command_info, self.client.permissions_trads)
                await ctx.send(embed=embed)
            else: raise core.CommandUnknow(command)
        

    @commands.command(name='help-owner', ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def _help_owner(self, ctx:commands.Context, *, command:str=None):
        """Command to help owner"""
        # get guild's lang
        lang = core.get_guild_lang(ctx.guild.id)

        if command is None:
            embeds_dict = embeds.help_owner(lang, self.client.commands_info, self.client.special_channels)
            view = ui.ViewHelpOwner(lang, timeout=320)
            message = await ctx.send(embed=embeds_dict["help"], view=view)
            
            while True:
                timeout = await view.wait()
                if timeout: break
                value = view.value
                view = ui.ViewHelpOwner(lang)
                await message.edit(embed=embeds_dict[value], view=view)


        if command is not None:
            if command in self.client.commands_info["owner-commands"]:
                command_info = self.client.commands_info["owner-commands"][command]
                embed=embeds.help_command(lang, command, command_info, self.client.permissions_trads)
                await ctx.send(embed=embed)
            else: raise core.CommandUnknow(command)


    @commands.command(name="guilds-message")
    @commands.is_owner()
    @commands.guild_only()
    async def _guilds_message(self, ctx:commands.Context, *, text:str):
        """Send message to all guilds"""
        with core.Database() as db:
            guilds = db.get_all_guilds()
        
        counter = 0
        for guild in self.client.guilds:
            try:
                channel = discord.utils.get(guild.text_channels, name="simple-logger")
                if channel is None: continue
                guild_data = discord.utils.get(guilds, guild_id=guild.id)
                lang = guild_data.lang
                embed = embeds.guilds_message(lang, text, ctx.author)
                await channel.send(embed=embed)
                counter += 1
            except: pass
            
        lang = discord.utils.get(guilds, guild_id=ctx.guild.id).lang
        guilds_count = len(self.client.guilds)
        embed = embeds.guilds_message2(lang, counter, guilds_count, text)
        await ctx.send(embed=embed)  
    
    
    @commands.command(name="guilds", ignore_extra=True)
    @commands.is_owner()
    @commands.guild_only()
    async def _guilds(self, ctx:commands.Context):
        """Send guilds counter"""
        with core.Database() as db:
            guild_data = db.get_guild(ctx.guild.id)
            lang = guild_data.lang
        embed = embeds.guilds(lang, len(self.client.guilds))
        await ctx.send(embed=embed)


    @commands.command(name="report")
    @commands.is_owner()
    @commands.guild_only()
    async def _report(self, ctx:commands.Context):
        # get guild's lang
        lang = core.utils.get_guild_lang(ctx.guild.id)

        # ask category
        report_view = ui.ViewReport(lang)
        embed = embeds.report_choose_category(lang)
        category_message = await ctx.send(embed=embed, view=report_view)

        r = await report_view.wait()
        if r: return # return if timeout
    
        # get values
        category = report_view.category_value
        title = report_view.title_value
        description = report_view.description_value

        await category_message.delete() # delete first message

        # ask a confirmation
        embed = embeds.report(lang, ctx, title, description)
        view_confirm = ui.ViewConfirmReport(lang)
        confirm_message = await ctx.send(embed=embed, view=view_confirm)
        r = await view_confirm.wait()
        if r: return # return if timeout
        
        if view_confirm.value:
            # send report
            report_channel:discord.TextChannel = self.client.channel_handler.channels[f"reports-{category}"]
            report_message = await report_channel.send(embed=embed)
            embed = embeds.report_confirm(lang, report_message.jump_url)
            await ctx.send(embed=embed)
        else:
            #cancel
            embed = embeds.report_cancel(lang)
            await ctx.send(embed=embed)

        # delete confirm question
        await confirm_message.delete()


    @commands.command(name="suggest")
    @commands.is_owner()
    @commands.guild_only()
    async def _suggest(self, ctx:commands.Context):
        # get guild's lang
        lang = core.utils.get_guild_lang(ctx.guild.id)

        # ask first confirmation
        suggest_view = ui.ViewFirstConfirmSuggest(lang)
        embed = embeds.suggest_first_confirm(lang)
        first_confirmation_message = await ctx.send(embed=embed, view=suggest_view)

        r = await suggest_view.wait()
        if r: return # return if timeout
        await first_confirmation_message.delete() # delete message
        
        if not suggest_view.value: return # return if button "no" is pressed
    
        # get values
        title = suggest_view.title_value
        description = suggest_view.description_value

        # ask a  last confirmation
        embed = embeds.suggest(lang, ctx, title, description)
        view_confirm = ui.ViewConfirmSuggest(lang)
        last_confirm_message = await ctx.send(embed=embed, view=view_confirm)
        r = await view_confirm.wait()
        if r: return # return if timeout
        
        if view_confirm.value:
            # send suggestion
            suggest_channel:discord.TextChannel = self.client.channel_handler.channels["suggestions"]
            suggest_message = await suggest_channel.send(embed=embed)
            embed = embeds.suggest_confirm(lang, suggest_message.jump_url)
            await ctx.send(embed=embed)
        else:
            # cancel
            embed = embeds.suggest_cancel(lang)
            await ctx.send(embed=embed)

        # delete confirm question
        await last_confirm_message.delete()



async def setup(client:commands.Bot):
    await client.add_cog(Bot(client))
