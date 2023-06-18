import discord
from discord.ext import commands

import core

line_jump = '\n'

def error(lang:str, error:Exception, ctx:commands.Context, permissions_trads:dict[str,dict[str,str]]) -> discord.Embed:
    # exceptions to respond
    dic = {
        "core.exceptions.ForbiddenMissingPermissions": {
            "en": lambda: f"I'm missing permissions.\nUse `.help {ctx.command.usage}` to see more details and permissions required for your command.",
            "fr": lambda: f"Il me manque des permissions.\nUtilisez `.help {ctx.command.usage}` pour voir plus de détails et les permissions requises pour cette commande."
        },
        "core.exceptions.ForbiddenMissingAccess": {
            "en": lambda: f"I'm missing access to your target (this may be a channel, a server, or another discord's element).",
            "fr": lambda: f"Il me manque un accès (cela peut être à un salon, serveur, ou un autre élément de discord)."
        },
        "core.exceptions.BadSettingValue": {
            "en": lambda: f"The value `{error.value}` can't be assigned to setting `{error.setting}`.\nUse `.settings help, {error.setting}` to see more.",
            "fr": lambda: f"La valeur `{error.value}` ne peut pas être assignée au setting `{error.setting}`.\nUtilisez `.settings help {error.setting}` pour en savoir plus sur ce setting."
        },
        "core.exceptions.UnknowSetting": {
            "en": lambda: f"Setting `{error.setting}` doesn't exist.",
            "fr": lambda: f"Le setting `{error.setting}` n'existe pas."
        },
        "core.exceptions.CommandUnknow": {
            "en": lambda: f"Command `{error.command_name}` doesn't exist.",
            "fr": lambda: f"La commande `{error.command_name}` n'existe pas."
        },
        "discord.ext.commands.errors.ConversionError": {
            "en": lambda: "Converter failed",
            "fr": lambda: "Un converteur a échoué"
        },
        "discord.ext.commands.errors.MissingRequiredArgument": {
            "en": lambda: f"Missing required argument: `{error.param.name}`.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il manque un argument requis : `{error.param.name}`.\nUtilisez `.help {ctx.command.usage}` pour en savoir plus sur les arguments de cette commande."
        },
        "discord.ext.commands.errors.TooManyArguments": {
            "en": lambda: f"Too many arguments provided.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Trop d'arguments ont été fournis.\nUtilisez `.help {ctx.command.usage}` pour en savoir plus sur les arguments de cette commande."
        },
        "discord.ext.commands.errors.MessageNotFound": {
            "en": lambda: "This message is not found.",
            "fr": lambda: "Message introuvable"
        },
        "discord.ext.commands.errors.MemberNotFound": {
            "en": lambda: "This member is not found.",
            "fr": lambda: "Membre introuvable"
        },
        "discord.ext.commands.errors.UserNotFound": {
            "en": lambda: "This user is not found.",
            "fr": lambda: "Utilisateur introuvable"
        },
        "discord.ext.commands.errors.ChannelNotFound": {
            "en": lambda: "This channel is not found.",
            "fr": lambda: "Salon introuvable"
        },
        "discord.ext.commands.errors.GuildNotFound": {
            "en": lambda: "This server is not found.",
            "fr": lambda: "Serveur introuvable"
        },
        "discord.ext.commands.errors.ChannelNotReadable": {
            "en": lambda: "This channel is not readable.",
            "fr": lambda: "Impossible de lire ce salon"
        },
        "discord.ext.commands.errors.BadColourArgument": {
            "en": lambda: "Bad colour provided.",
            "fr": lambda: "Cette couleur n'existe pas"
        },
        "discord.ext.commands.errors.RoleNotFound": {
            "en": lambda: "This role is not found.",
            "fr": lambda: "Rôle introuvable"
        },
        "discord.ext.commands.errors.BadInviteArgument": {
            "en": lambda: "Bad invite provided.",
            "fr": lambda: "Cette invitation n'existe pas"
        },
        "discord.ext.commands.errors.EmojiNotFound": {
            "en": lambda: "This emoji is not found.",
            "fr": lambda: "Emoji introuvable"
        },
        "discord.ext.commands.errors.PartialEmojiConversionFailure": {
            "en": lambda: "Bad emoji format",
            "fr": lambda: "Format de l'emoji incorrect"
        },
        "discord.ext.commands.errors.BadBoolArgument": {
            "en": lambda: "Bad boolean argument, try to use True/False, Yes/No, 1/0.",
            "fr": lambda: "Argument bouléen invalide, essayez d'utiliser True/False (vrai/faux), Yes/No (oui/non), 1/0."
        },
        "discord.ext.commands.errors.BadUnionArgument": {
            "en": lambda: "Converters failed.",
            "fr": lambda: "Un converteur a échoué."
        },
        "discord.ext.commands.errors.ArgumentParsingError": {
            "en": lambda: "Impossible to parse your input.",
            "fr": lambda: "Impossible d'analyser votre entrée."
        },
        "discord.ext.commands.errors.CheckAnyFailure": {
            "en": lambda: "The check failed.",
            "fr": lambda: "La vérification a échoué."
        },
        "discord.ext.commands.errors.PrivateMessageOnly": {
            "en": lambda: "This operation does not work outside of private message.",
            "fr": lambda: "Cette opération ne fonctionne qu'en message privé."
        },
        "discord.ext.commands.errors.NoPrivateMessage": {
            "en": lambda: "This operation does not work in private message.",
            "fr": lambda: "Cette opération ne fonctionne pas en message privé."
        },
        "discord.ext.commands.errors.NotOwner": {
            "en": lambda: "You are not the bot's owner.",
            "fr": lambda: "Vous n'êtes pas propriétaire du bot."
        },
        "discord.ext.commands.errors.MissingPermissions": {
            "en": lambda: f"You are missing permissions: {' '.join([f'`{permissions_trads[permission][lang]}`' for permission in error.missing_permissions])}.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il vous manque ces permissions : {' '.join([f'`{permissions_trads[permission][lang]}`' for permission in error.missing_permissions])}.\nUtilisez `.help {ctx.command.usage}` pour avoir plus de détails."
        },
        "discord.ext.commands.errors.BotMissingPermissions": {
            "en": lambda: f"I'm missing permissions: {' '.join([f'`{permissions_trads[permission][lang]}`' for permission in error.missing_permissions])}.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il me manque ces permissions : {' '.join([f'`{permissions_trads[permission][lang]}`' for permission in error.missing_permissions])}.\nUtilisez `.help {ctx.command.usage}` pour avoir plus de détails."
        },
        "discord.ext.commands.errors.MissingRole": {
            "en": lambda: f"You are missing role: {error.missing_role.mention}.\nUtilisez `.help {ctx.command.usage}` pour avoir plus de détails.",
            "fr": lambda: f"Il vous manque ce rôle : {error.missing_role.mention}.\nse `.help {ctx.command.usage}` to see more details."
        },
        "discord.ext.commands.errors.BotMissingRole": {
            "en": lambda: f"I'm missing role: {error.missing_role.mention}.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il me manque ce rôle: {error.missing_role.mention}.\ntilisez `.help {ctx.command.usage}` pour avoir plus détails."
        },
        "discord.ext.commands.errors.MissingAnyRole": {
            "en": lambda: f"You are missing one of these roles: {' '.join([role.mention for role in error.missing_roles])}.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il vous manque un de ces rôles : {' '.join([role.mention for role in error.missing_roles])}.\ntilisez `.help {ctx.command.usage}` pour en savoir plus."
        },
        "discord.ext.commands.errors.BotMissingAnyRole": {
            "en": lambda: f"I'm missing one of these roles: {' '.join([role.mention for role in error.missing_roles])}.\nUse `.help {ctx.command.usage}` to see more details.",
            "fr": lambda: f"Il me manque un de ces rôles : {' '.join([role.mention for role in error.missing_roles])}.\ntilisez `.help {ctx.command.usage}` pour en savoir plus."
        },
        "discord.ext.commands.errors.NSFWChannelRequired": {
            "en": lambda: f"This channel does not have the required NSFW setting: {error.channel.mention}.",
            "fr": lambda: f"Ce salon n'est pas configuré domme NSFW : {error.channel.mention}."
        },
        "discord.ext.commands.errors.DisabledCommand": {
            "en": lambda: "This command is disabled.",
            "fr": lambda: "Cette commande est désactivée."
        },
        "discord.ext.commands.errors.CommandOnCooldown": {
            "en": lambda: f"You're going too fast, wait a moment!\nCooldown: `{error.cooldown.rate}` executions each `{error.cooldown.per}` seconds.",
            "fr": lambda: f"Vous allez trop vite, attendez un moment!\nCooldown: `{error.cooldown.rate}` exécutions toutes les `{error.cooldown.per}` secondes."
        },
        "discord.ext.commands.errors.MaxConcurrencyReached": {
            "en": lambda: "Too many users are using the command at the same time, please try again.",
            "fr": lambda: "Trop d'utilisateurs utilisent cette commande en même temps, veuillez réessayer."
        }
    }
    # exceptions to ignore
    ignore = [
        "discord.ext.commands.errors.CommandNotFound"
    ]
    error_class_name = f"{error.__class__.__module__}.{error.__class__.__name__}"
    if error_class_name in ignore: return

    description = None
    if error_class_name in dic.keys():
        description = dic[error_class_name][lang]()
    embed = discord.Embed(description=description, colour=discord.Color.red())

    def en() -> discord.Embed:
        log = False
        embed.title = f"❌ Error"
        if description is None:
            embed.description = f"Unknown reason, please contact support and provide this error message:\n```[ERROR]: {error_class_name}\n{error}```"
            log = True
        return (embed, log)
    def fr() -> discord.Embed:
        log = False
        embed.title = f"❌ Erreur"
        if description is None:
            embed.description = f"Raison inconnue, veuillez contacter le support et fournir ce message d'erreur:\n```[ERROR]: {error_class_name}\n{error}```"
            log = True
        return (embed, log)

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()