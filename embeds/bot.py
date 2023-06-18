import typing

import discord
from discord.ext import commands

line_jump = '\n'

def invite(lang:str, bot_invite:str) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.og_blurple())

    def en() -> discord.Embed:
        embed.title = "Invite me"
        embed.description = f"You can invite me with this [link]({bot_invite})"
        return embed
    def fr() -> discord.Embed:
        embed.title = "Invite moi"
        embed.description = f"Tu peux m'inviter avec ce [lien]({bot_invite})"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def guilds_message(lang:str, text:str, owner:typing.Union[discord.User, discord.Member]) -> discord.Embed:
    embed = discord.Embed(description=text, colour=discord.Color.og_blurple())
    embed.set_author(name=owner.name, icon_url=owner.avatar)

    def en() -> discord.Embed:
        embed.title = "Message from bot's owner"
        return embed
    def fr() -> discord.Embed:
        embed.title = "Message du propriétaire du bot"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def guilds_message2(lang:str, counter:int, guilds_count:int, text:str) -> discord.Embed:
    embed = discord.Embed(description=text, colour=discord.Color.og_blurple())

    def en() -> discord.Embed:
        embed.title = f"Message sent to `{(counter)}/{guilds_count}` servers."
        return embed
    def fr() -> discord.Embed:
        embed.title = f"Message envoyé à `{(counter)}/{guilds_count}` serveurs."
        return embed
        
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def guilds(lang:str, guilds_count:int) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.og_blurple())

    def en() -> discord.Embed:
        embed.title = f"I'm in `{guilds_count}` servers."
        return embed
    def fr() -> discord.Embed:
        embed.title = f"Je suis dans `{guilds_count}` serveurs."
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def help(lang:str, commands_info:dict, channels:dict) -> dict[discord.Embed]:
    embed_model = discord.Embed(colour=discord.Color.og_blurple())
    embeds = {
        "help": embed_model.copy(),
        "logging": embed_model.copy(),
        "others": embed_model.copy(),
        "settings": embed_model.copy(),
        "info": embed_model.copy(),
    }
    
    def en() -> dict[discord.Embed]:
        # first embed
        embeds["help"].title = "Help page"
        embeds["help"].description = """With this selection menu, you can select the categories you need help for and I will send you all the information about it.
                                        You can use `help [command]` to see more details for a specific command."""
        
        # logging embed
        embeds["logging"].title = "Logging"
        embeds["logging"].description = "Logging has a command and channels, they allow you to log certain actions. Here is the list of commands as well as channels and logged actions."
        logging_commands = commands_info["categories"]["logging"]
        embeds["logging"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in logging_commands]), inline=False)

        for channel_name in channels.keys():
            value = "\n".join(f"*{log}*" for log in channels[channel_name]["logs"][lang])
            embeds["logging"].add_field(name=channel_name, value=value)
            
        # settings embed
        embeds["settings"].title = "Settings"
        embeds["settings"].description = "The settings are personalized for each server, you can modify them to adapt the bot to your preferences and to your server."
        settings_commands = commands_info["categories"]["settings"]
        embeds["settings"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in settings_commands]))
        
        # info embed
        embeds["info"].title = "Info"
        embeds["info"].description = "With these commands you can get different information about the use of the bot or about servers and users."
        info_commands = commands_info["categories"]["info"]
        embeds["info"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in info_commands]))
        
        # others embed
        embeds["others"].title = "Others"
        embeds["others"].description = "This group brings together the various isolated commands unrelated to the features of the bot."
        others_commands = commands_info["categories"]["others"]
        embeds["others"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in others_commands]))

        return embeds
        
    def fr() -> dict[discord.Embed]:
        # first embed
        embeds["help"].title = "Page help"
        embeds["help"].description = """Avec ce menu de sélection, vous pouvez sélectionner les catégories pour lesquelles vous avez besoin d'aide et je vous enverrai toutes les informations à ce sujet.
                                        Vous pouvez utiliser `help [commande]` pour voir plus de détails sur une commande spécifique."""
        
        # logging embed
        embeds["logging"].title = "Journalisation"
        embeds["logging"].description = "La journalisation a une commande et des salons, ils vous permettent de logger certaines actions. Voici la liste des commandes ainsi que les salons et les actions enregistrées per ces derniers."
        logging_commands = commands_info["categories"]["logging"]
        embeds["logging"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in logging_commands]), inline=False)

        for channel_name in channels.keys():
            value = "\n".join(f"*{log}*" for log in channels[channel_name]["logs"][lang])
            embeds["logging"].add_field(name=channel_name, value=value)
            
        # settings embed
        embeds["settings"].title = "Paramètres"
        embeds["settings"].description = "Les paramètres sont personnalisés pour chaque serveur, vous pouvez les modifier pour adapter le bot à vos préférences et à votre serveur."
        settings_commands = commands_info["categories"]["settings"]
        embeds["settings"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in settings_commands]))
        
        # info embed
        embeds["info"].title = "Informations"
        embeds["info"].description = "Avec ces commandes, vous pouvez obtenir différentes informations sur l'utilisation du bot ainsi que sur les serveurs et les utilisateurs."
        info_commands = commands_info["categories"]["info"]
        embeds["info"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in info_commands]))
        
        # others embed
        embeds["others"].title = "Autres"
        embeds["others"].description = "Ce groupe rassemble les différentes commandes isolées sans rapport avec les fonctionnalités du bot."
        others_commands = commands_info["categories"]["others"]
        embeds["others"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['commands'][cmd]['description'][lang]}" for cmd in others_commands]))

        return embeds

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def help_owner(lang:str, commands_info:dict, channels:dict) -> dict[discord.Embed]:
    embed_model = discord.Embed(colour=discord.Color.blurple())
    embeds = {
        "help": embed_model.copy(),
        "spy": embed_model.copy(),
        "cogs": embed_model.copy(),
        "bot": embed_model.copy(),
    }
    
    def en() -> dict[discord.Embed]:
        # first embed
        embeds["help"].title = "Help page for owner"
        embeds["help"].description = """With this selection menu, you can select the categories you need help for and I will send you all the information about it.
                                        You can use `help [command]` to see more details for a specific command."""
        
        # spy embed
        embeds["spy"].title = "Spy"
        embeds["spy"].description = "To spy on the activities of different servers."
        spy_commands = commands_info["owner-categories"]["spy"]
        embeds["spy"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in spy_commands]), inline=False)
        
        # cogs embed
        embeds["cogs"].title = "Cogs"
        embeds["cogs"].description = "These are the commands that manage the cogs."
        cogs_commands = commands_info["owner-categories"]["cogs"]
        embeds["cogs"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in cogs_commands]))
        
        # bot embed
        embeds["bot"].title = "bot"
        embeds["bot"].description = "These are the commands that get or post info about the bot."
        bot_commands = commands_info["owner-categories"]["bot"]
        embeds["bot"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in bot_commands]))

        return embeds
        
    def fr() -> dict[discord.Embed]:
        # first embed
        embeds["help"].title = "Page help pour le propriétaire"
        embeds["help"].description = """Avec ce menu de sélection, vous pouvez sélectionner les catégories pour lesquelles vous avez besoin d'aide et je vous enverrai toutes les informations à ce sujet.
                                        Vous pouvez utiliser `help [commande]` pour voir plus de détails sur une commande spécifique."""
        
        # spy embed
        embeds["spy"].title = "Spy"
        embeds["spy"].description = "Pour espionner les activités des différents serveurs."
        spy_commands = commands_info["owner-categories"]["spy"]
        embeds["spy"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in spy_commands]), inline=False)
        
        # cogs embed
        embeds["cogs"].title = "Cogs"
        embeds["cogs"].description = "Ce sont les commandes qui gèrent les cogs."
        cogs_commands = commands_info["owner-categories"]["cogs"]
        embeds["cogs"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in cogs_commands]))
        
        # bot embed
        embeds["bot"].title = "Bot"
        embeds["bot"].description = "Ce sont les commandes qui obtiennent ou publient des informations sur le bot."
        bot_commands = commands_info["owner-categories"]["bot"]
        embeds["bot"].add_field(name="Commands", value="\n".join([f"`{cmd}`: {commands_info['owner-commands'][cmd]['description'][lang]}" for cmd in bot_commands]))

        return embeds

        return embeds

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def aliases_to_text(aliases:list[str]) -> str:
    """Converts list of aliases to string"""
    if len(aliases) == 0: return
    return " ".join([f"`{aliase}`" for aliase in aliases])


def arguments_to_text(arguments:list[dict], lang:str) -> str:
    """Constructs arguments part for help command"""
    if len(arguments) == 0: return
    required = {
        "en": "Required:",
        "fr": "Requis :"
    }
    yes = {
        "en": "Yes",
        "fr": "Oui"
    }
    no = {
        "en": "No",
        "fr": "Non"
    }
    return "\n".join([f"**{arg['name']}**\n{arg['description'][lang]}\n*{required[lang]} {yes[lang] if arg['required'] else no[lang]}*" for arg in arguments])


def permissions_to_text(lang:str, permissions:list[str], permissions_trads:dict[str,dict[str,str]]) -> str:
    """Constructs permissions part for help command"""

    if len(permissions) == 0: return
    permissions_translated = [permissions_trads[perm][lang] for perm in permissions]
    return "\n".join(permissions_translated)


def create_command_entry(command_info:dict) -> str:
    """Constructs command example"""
    list_ = [command_info["usage"]]
    for arg in command_info['arguments']:
        list_.append(f"<{arg['name']}>" if arg['required'] else f"[{arg['name']}]")
    return f"`{' '.join(list_)}`"


def help_command(lang:str, command:str, command_info:dict, permissions_trads:dict[str,dict[str,str]]) -> discord.Embed:
    embed = discord.Embed(description=command_info["description"][lang], color=discord.Color.og_blurple())

    def en() -> discord.Embed:
        embed.title = f'Command {command}'
        embed.add_field(name="Usage", value=f"`{command_info['usage']}`")
        
        aliases = aliases_to_text(command_info["aliases"])
        embed.add_field(name="Aliases", value=aliases if aliases is not None else "No aliases")
        embed.add_field(name="Command entry", value=create_command_entry(command_info), inline=False)
        
        users_permissions = permissions_to_text(lang, command_info["user-permissions"], permissions_trads)
        embed.add_field(name="User's permissions", value=users_permissions if users_permissions is not None else "No permissions required")
        
        bots_permissions = permissions_to_text(lang, command_info["bot-permissions"], permissions_trads)
        embed.add_field(name="Bot's permissions", value=bots_permissions if bots_permissions is not None else "No permissions required")
        
        arguments = arguments_to_text(command_info["arguments"], lang)
        embed.add_field(name="Arguments", value=arguments if arguments is not None else "No arguments", inline=False)
        embed.set_footer(text="Arguments can be required <> or optional []")
        return embed
        
    def fr() -> discord.Embed:
        embed.title = f'Commande {command}'
        embed.add_field(name="Utilisation", value=f"`{command_info['usage']}`")
        
        aliases = aliases_to_text(command_info["aliases"])
        embed.add_field(name="Aliases", value=aliases if aliases is not None else "Pas d'alias")
        embed.add_field(name="Entrée de commande", value=create_command_entry(command_info), inline=False)
        
        users_permissions = permissions_to_text(lang, command_info["user-permissions"], permissions_trads)
        embed.add_field(name="Permisions de l'utilisateur", value=users_permissions if users_permissions is not None else "Aucune permission requise")
        
        bots_permissions = permissions_to_text(lang, command_info["bot-permissions"], permissions_trads)
        embed.add_field(name="Permissions du bot", value=bots_permissions if bots_permissions is not None else "Aucune permission requise")
        
        arguments = arguments_to_text(command_info["arguments"], lang)
        embed.add_field(name="Arguments", value=arguments if arguments is not None else "Pas d'argument", inline=False)
        embed.set_footer(text="Les arguments peuvent être requis <> ou optionnels []")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def report(lang:str, ctx:commands.Context, title:str, description:str) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar)
    embed.timestamp = discord.utils.utcnow()

    member = ctx.guild.get_member(ctx.author.id)

    def en() -> discord.Embed:
        embed.add_field(name="Server", value=f"`{ctx.guild.id}`")
        in_guild_text = "Yes" if member is not None else "No"
        embed.add_field(name="In support server", value=in_guild_text)
        return embed
        
    def fr() -> discord.Embed:
        embed.add_field(name="Serveur", value=f"`{ctx.guild.id}`")
        in_guild_text = "Oui" if member is not None else "Non"
        embed.add_field(name="Sur le serveur de support", value=in_guild_text)
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def report_choose_category(lang:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())

    def en() -> discord.Embed:
        embed.title = "Choose a category"
        return embed
        
    def fr() -> discord.Embed:
        embed.title = "Choisissez une catégorie"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def report_confirm(lang:str, message_link:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.green())

    def en() -> discord.Embed:
        embed.description = f"Your report has been sent to support serveur\n[Message link]({message_link})"
        return embed
        
    def fr() -> discord.Embed:
        embed.description = f"Votre rapport a été envoyé au serveur d'assistance\n[Lien du message]({message_link})"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def report_cancel(lang:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())

    def en() -> discord.Embed:
        embed.description = "Your report has not been sent"
        return embed
        
    def fr() -> discord.Embed:
        embed.description = "Votre rapport n'a pas été envoyé"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def suggest_first_confirm(lang:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.yellow())

    def en() -> discord.Embed:
        embed.description = "**Would you like to send us a suggestion? It will be visible to all members of the support server!**"
        return embed
        
    def fr() -> discord.Embed:
        embed.description = "**Vous souhaitez nous faire part d'une suggestion ? Elle sera visible par tous les membres du serveur de support !**"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def suggest(lang:str, ctx:commands.Context, title:str, description:str) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=discord.Color.yellow())
    embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar)
    embed.timestamp = discord.utils.utcnow()


    def en() -> discord.Embed:
        return embed
    def fr() -> discord.Embed:
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def suggest_confirm(lang:str, message_link:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.green())

    def en() -> discord.Embed:
        embed.description = f"Your suggestion has been sent to support serveur\n[Message link]({message_link})"
        return embed
        
    def fr() -> discord.Embed:
        embed.description = f"Votre suggestion a été envoyée au serveur d'assistance\n[Lien du message]({message_link})"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def suggest_cancel(lang:str) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())

    def en() -> discord.Embed:
        embed.description = "Your suggestion has not been sent"
        return embed
        
    def fr() -> discord.Embed:
        embed.description = "Votre suggestion n'a pas été envoyée"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()
