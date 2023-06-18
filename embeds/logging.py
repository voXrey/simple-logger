import datetime
import typing
import discord
from discord.ext import commands


def setup(lang:str, channels: list[discord.TextChannel], author: typing.Union[discord.User, discord.Member]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.og_blurple())
    embed.description = "\n".join(
        [f"● {channel.mention}" for channel in channels])

    def en():
        embed.title = f"Channel setted"
        embed.set_footer(
            text=f"Setted by {author} ({author.id})", icon_url=author.avatar)
        return embed

    def fr():
        embed.title = f"Salons créés"
        embed.set_footer(
            text=f"Paramétrés par {author} ({author.id})", icon_url=author.avatar)
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def channel_setted(lang:str, channel_name: str, channel_info: dict, author: typing.Union[discord.User, discord.Member]) -> discord.Embed:
    embed = discord.Embed(
        description=channel_info["description"][lang], colour=discord.Color.og_blurple())

    def en():
        embed.title = f"Channel '{channel_name}'"
        embed.set_footer(
            text=f"Setted by {author} ({author.id})", icon_url=author.avatar)
        if len(channel_info['logs'][lang]) > 0:
            embed.add_field(name="Logs", value="\n".join(
                [f"- {log}" for log in channel_info['logs'][lang]]))
        if len(channel_info['unlog'][lang]) > 0:
            embed.add_field(name="Do not log if in topic", value="\n".join(
                [f"- {log}" for log in channel_info['unlog'][lang]]))
        return embed

    def fr():
        embed.title = f"Salon '{channel_name}'"
        embed.set_footer(
            text=f"Paramétré par {author} ({author.id})", icon_url=author.avatar)
        if len(channel_info['logs'][lang]) > 0:
            embed.add_field(name="Logs", value="\n".join(
                [f"- {log}" for log in channel_info['logs'][lang]]))
        if len(channel_info['unlog'][lang]) > 0:
            embed.add_field(name="Ne pas logger si dans le topic", value="\n".join(
                [f"- {log}" for log in channel_info['unlog'][lang]]))
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_message_edit(lang:str, before: discord.Message, after: discord.Message) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.orange())
    embed.timestamp = after.edited_at

    def en():
        embed.description = f"Message edited in {before.channel.mention} `{before.channel.id}` ([link]({after.jump_url}))"
        embed.set_author(
            name=f"Author: {after.author} ({after.author.id})", icon_url=after.author.avatar)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"Message id: {before.id}")
        return embed

    def fr():
        embed.description = f"Message modifié dans {before.channel.mention} `{before.channel.id}` ([lien]({after.jump_url}))"
        embed.set_author(
            name=f"Auteur: {after.author} ({after.author.id})", icon_url=after.author.avatar)
        embed.add_field(name="Avant", value=before.content, inline=False)
        embed.add_field(name="Après", value=after.content, inline=False)
        embed.set_footer(text=f"Id du message : {before.id}")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_message_delete(lang:str, message: discord.Message, date: datetime.datetime) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.red())
    embed.timestamp = date

    def en():
        embed.description = f"Message deleted in {message.channel.mention} `{message.channel.id}` ([link]({message.jump_url}))"
        embed.set_author(
            name=f"Author: {message.author} ({message.author.id})", icon_url=message.author.avatar)
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Message id: {message.id}")
        return embed

    def fr():
        embed.description = f"Message supprimé dans {message.channel.mention} `{message.channel.id}` ([lien]({message.jump_url}))"
        embed.set_author(
            name=f"Auteur: {message.author} ({message.author.id})", icon_url=message.author.avatar)
        embed.add_field(name="Contenu", value=message.content, inline=False)
        embed.set_footer(text=f"Id du message : {message.id}")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_member_update(lang:str, before: discord.Member, after: discord.Member,
                     changement: str, user: typing.Union[discord.User, discord.Member],
                     date: datetime.datetime, extra: discord.Role = None) -> discord.Embed:
    embed = discord.Embed()
    embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar)
    embed.timestamp = date
    colors = {
        "role-added": discord.Color.green(),
        "role-removed": discord.Color.red(),
        "nickname-changed": discord.Color.orange()
    }
    embed.color = colors[changement]

    def en():
        if changement in ["role-added", "role-removed"]:
            embed.add_field(name="Role mention", value=extra.mention)
            embed.add_field(name="Role id", value=f"`{extra.id}`")

            if changement == "role-added":
                embed.title = f"Role added"
                embed.description = f"A role has been added to {before.mention} `{before.id}`"

            else:
                embed.title = f"Role removed"
                embed.description = f"A role has been removed from {before.mention} `{before.id}`"

        else:
            embed.title = "Member's nickname changed"
            embed.description = f"The nickname of {before.mention} `{before.id}` has changed from **{before.display_name}** to **{after.display_name}**"
        return embed

    def fr():
        if changement in ["role-added", "role-removed"]:
            embed.add_field(name="Mention du rôle", value=extra.mention)
            embed.add_field(name="Id du rôle", value=f"`{extra.id}`")

            if changement == "role-added":
                embed.title = f"Rôle ajouté"
                embed.description = f"Un rôle a été ajouté à {before.mention} `{before.id}`"

            else:
                embed.title = f"Rôle retiré"
                embed.description = f"Un rôle a été retiré à {before.mention} `{before.id}`"

        else:
            embed.title = "Un membre a été renommé"
            embed.description = f"Le surnom de {before.mention} `{before.id}` est passé de **{before.display_name}** à **{after.display_name}**"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_member_join(lang:str, member:discord.Member, past_invite_info:typing.Optional[dict]) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.green())

    def en():
        embed.description = f"{member.mention} `{member.id}` joined server."
        if past_invite_info is not None:
            embed.add_field(name="Invited by", value=f"{past_invite_info['inviter']['full-name']} `{past_invite_info['inviter']['id']}`")
            embed.add_field(name="Invite code", value=f"`{past_invite_info['code']}`")
        return embed

    def fr():
        embed.description = f"{member.mention} `{member.id}` a rejoint le serveur."
        if past_invite_info is not None:
            embed.add_field(name="Invité par", value=f"{past_invite_info['inviter']['full-name']} `{past_invite_info['inviter']['id']}`")
            embed.add_field(name="Code de l'invitation", value=f"`{past_invite_info['code']}`")
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_member_remove(lang:str, member:discord.Member) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())

    def en():
        embed.description = f"**{member}** `{member.id}` left server."
        return embed

    def fr():
        embed.description = f"**{member}** `{member.id}` a quitté le serveur."
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_channel_create(lang:str, channel:discord.abc.GuildChannel, log:discord.AuditLogEntry) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.green())
    embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at

    def en():
        if isinstance(channel, discord.CategoryChannel): embed.description = f"Category created **{channel.name}** `{channel.id}`"
        else:
            embed.description = f"Channel created {channel.mention} `{channel.id}`"
            if channel.category is not None: embed.description += f" in **{channel.category.name}**"
        if log.reason is not None: embed.description += f"\nReason: {log.reason}"
        return embed

    def fr():
        if isinstance(channel, discord.CategoryChannel): embed.description = f"Catégorie créée **{channel.name}** `{channel.id}`"
        else:
            embed.description = f"Salon créé {channel.mention} `{channel.id}"
            if channel.category is not None: embed.description += f" dans **{channel.category.name}**"
        if log.reason is not None: embed.description += f"\nRaison : {log.reason}"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_channel_delete(lang:str, channel:discord.abc.GuildChannel, log:discord.AuditLogEntry) -> discord.Embed:
    embed = discord.Embed(color=discord.Color.red())
    embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at

    def en():
        if isinstance(channel, discord.CategoryChannel): embed.description = f"Category deleted **{channel.name}** `{channel.id}`"
        else:
            embed.description = f"Channel deleted #{channel.name} `{channel.id}`"
            if channel.category is not None: embed.description += f" in **{channel.category.name}**"
        if log.reason is not None: embed.description += f"\nReason: {log.reason}"
        return embed

    def fr():
        if isinstance(channel, discord.CategoryChannel): embed.description = f"Catégorie supprimée **{channel.name}** `{channel.id}`"
        else:
            embed.description = f"Salon supprimé #{channel.name} `{channel.id}"
            if channel.category is not None: embed.description += f" dans **{channel.category.name}**"
        if log.reason is not None: embed.description += f"\Raison : {log.reason}"
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_channel_update(lang:str, before:discord.abc.GuildChannel, after:discord.abc.GuildChannel, log:discord.AuditLogEntry) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.orange())
    embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at

    changes_before, changes_after = log.changes.before.__dict__, log.changes.after.__dict__
    
    sentences = {
        "name": {
            "en": "Name",
            "fr": "Nom"
        },
        "bitrate": {
            "en": "Bitrate",
            "fr": "Débit binaire",
        },
        "topic": {
            "en": "Topic",
            "fr": "Sujet"
        },
        "default_auto_archive_duration": {
            "en": "Auto archive duration",
            "fr": "Archivage automatique"
        },
        "slowmode_delay": {
            "en": "Slow mode delay",
            "fr": "Mode lent"
        },
        "nsfw": {
            "en": "NSFW",
            "fr": "NSFW"
        },
        "video_quality_mode": {
            "en": "Video quality mode",
            "fr": "Qualité de la vidéo"
        },
        "user_limit": {
            "en":  "User limit",
            "fr": "Limite d'utilisateurs"
        },
        "rtc_region": {
            "en": "Region",
            "fr": "Région"
        }
    }
    changements_values:dict[typing.Any,str] = {
        "slowmode_delay": {
            0: {
                "en": "Disabled",
                "fr": "Désactivé"
            },
            5: {
                "en": "5 seconds",
                "fr": "5 secondes"
            },
            10: {
                "en": "10 seconds",
                "fr": "10 secondes"
            },
            15: {
                "en": "15 seconds",
                "fr": "15 secondes"
            },
            30: {
                "en": "30 seconds",
                "fr": "30 secondes"
            },
            60: {
                "en": "1 minute",
                "fr": "1 minute"
            },
            120: {
                "en": "2 minutes",
                "fr": "2 minutes"
            },
            300: {
                "en": "5 minutes",
                "fr": "5 minutes"
            },
            600: {
                "en": "10 minutes",
                "fr": "10 minutes"
            },
            900: {
                "en": "15 minutes",
                "fr": "15 minutes"
            },
            1800: {
                "en": "30 minutes",
                "fr": "30 minutes"
            },
            3600: {
                "en": "1 hour",
                "fr": "1 heure"
            },
            7200: {
                "en": "2 hours",
                "fr": "2 heures"
            },
            21600: {
                "en": "6 hours",
                "fr": "6 heures"
            },
        },
        "default_auto_archive_duration": {
            60: {
                "en": "1 hour",
                "fr": "1 heure"
            },
            1440: {
                "en": "24 hours",
                "fr": "24 heures"
            },
            4320: {
                "en": "3 days",
                "fr": "3 jours"
            },
            10080: {
                "en": "7 days",
                "fr": "7 jours"
            }
        },
        "nsfw": {
            True: {
                "en": "Enabled",
                "fr": "Activé"
            },
            False: {
                "en": "Disabled",
                "fr": "Désactivé"
            }
        },
        "video_quality_mode": {
            1: {
                "en": "Auto",
                "fr": "Automatique"
            },
            2: {
                "en": "Full",
                "fr": "Qualitée max"
            }
        },
        "bitrate": {
            "en": "{bitrate} KBps",
            "fr": "{bitrate} KBps"
        },
        "user_limit": {
            "en": "{users_count} users",
            'fr': "{users_count} utilisateurs"
        },
        "topic": {
            "en": "No topic",
            "fr": "Aucun sujet"
        }
    }
    changements_getter = {
        "slowmode_delay": lambda x: changements_values["slowmode_delay"][x][lang],
        "default_auto_archive_duration": lambda x: changements_values["default_auto_archive_duration"][x][lang],
        "nsfw": lambda x: changements_values["nsfw"][x][lang],
        "video_quality_mode": lambda x: changements_values["video_quality_mode"][x][lang],
        "birate": lambda x: changements_values["bitrate"][lang].format(bitrate={x//1000}),
        "user_limit": lambda x: changements_values["user_limit"][lang].format(users_count=x) if x > 0 else "ထ",
        "rtc_region": lambda x: x if x is not None else "Auto",
        "name": lambda x: x,
        "topic": lambda x: x if x is not None else changements_values["topic"][lang]
    }

    def changements_string() -> str:
        changements_names = []
        for key in changes_before.keys():
            if key in sentences: changements_names.append(sentences[key][lang])
        return "\n".join(f"● `{c}`" for c in changements_names)

    def changements_values_string(changements:dict) -> str:
        L = []
        for key, value in changements.items():
            to_add = value
            if key in changements_getter:
                to_add = changements_getter[key](value)
            L.append(f"● `{to_add}`")
        return '\n'.join(L)

    def en():
        if isinstance(after, discord.CategoryChannel): embed.description = f"The category **{after.name}** `{after.id}` has been modfied"
        else: embed.description = f"The channel {after.mention} `{after.id}` has been modfied"
        if log.reason is not None: embed.description += f"\nReason: {log.reason}"
        embed.add_field(name="Changements", value=changements_string())
        embed.add_field(name="Before", value=changements_values_string(changes_before))
        embed.add_field(name="After", value=changements_values_string(changes_after))
        return embed

    def fr():
        if isinstance(after, discord.CategoryChannel): embed.description = f"La catégorie **{after.name}** `{after.id}` a été modifié"
        else: embed.description = f"Le salon {after.mention} `{after.id}` a été modifié"
        if log.reason is not None: embed.description += f"\nRaison: {log.reason}"
        embed.add_field(name="Changements", value=changements_string())
        embed.add_field(name="Avant", value=changements_values_string(changes_before))
        embed.add_field(name="Après", value=changements_values_string(changes_after))
        return embed

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_channel_update_permissions(lang:str, before:discord.abc.GuildChannel, after:discord.abc.GuildChannel, log:discord.AuditLogEntry, permissions_trads:dict[str,dict[str,str]]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.orange())
    embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at

    guild = before.guild
    changes_before, changes_after = log.changes.before.__dict__, log.changes.after.__dict__
    line_jump = "\n"

    def get_permissions_from_changes(changes_dict:dict):
        L_deny: list = None
        if 'deny' in changes_dict.values():
            L_deny = [permissions_trads[perm][lang] for perm, value in changes_dict['deny'] if value]
        L_allow: list = None
        if 'allow' in changes_dict.values():
            L_allow = [permissions_trads[perm][lang] for perm, value in changes_dict['allow'] if value]
        return (L_deny, L_allow)

    def en():
        def get_permissions_embed_value(allow: list, deny: list) -> str:
            string = f"✅ **Allow**\n{line_jump.join([f'● `{a}`' for a in allow]) if len(allow) > 0 else 'No permission'}\n"
            string += f"❌ **Deny**\n{line_jump.join([f'● `{d}`' for d in deny]) if len(deny) > 0 else 'No permission'}"
            return string
        embed.description = f"The channel {after.mention} `{after.id}` has been modfied\nPermissions for {log.extra.mention if log.extra != guild.default_role else log.extra} `{log.extra.id}` modified"
        
        L_allow_before, L_deny_before = get_permissions_from_changes(changes_before)
        embed.add_field(name="Before", value=get_permissions_embed_value(L_allow_before, L_deny_before))

        L_allow_after, L_deny_after = get_permissions_from_changes(changes_after)
        embed.add_field(name="After", value=get_permissions_embed_value(L_allow_after, L_deny_after))

    def fr():
        def get_permissions_embed_value(allow: list, deny: list) -> str:
            string = f"✅ **Autorisée**\n{line_jump.join([f'● `{a}`' for a in allow]) if len(allow) > 0 else 'Aucune permission'}\n"
            string += f"❌ **Refusée**\n{line_jump.join([f'● `{d}`' for d in deny]) if len(deny) > 0 else 'Aucune permission'}"
            return string
        embed.description = f"Le salon {after.mention} `{after.id}` a été modifié\nPermissions de {log.extra.mention if log.extra != guild.default_role else log.extra} `{log.extra.id}` changées"
        
        L_allow_before, L_deny_before = get_permissions_from_changes(changes_before)
        embed.add_field(name="Avant", value=get_permissions_embed_value(L_allow_before, L_deny_before))

        L_allow_after, L_deny_after = get_permissions_from_changes(changes_after)
        embed.add_field(name="Après", value=get_permissions_embed_value(L_allow_after, L_deny_after))

    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_role_create(lang:str, role:discord.Role, log:typing.Optional[discord.AuditLogEntry]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.green())
    embed.timestamp = log.created_at if not role.managed else discord.utils.utcnow()

    def en():
        description = f"Role created {role.mention} `{role.id}`"
        if role.managed:
            by = None
            if role.tags.bot_id is not None:
                by = f"The bot {role.guild.get_member(role.tags.bot_id).mention} `{role.tags.bot_id}`"
            elif role.tags.integration_id is not None:
                by = f"The integration `{role.tags.integration_id}`"
            elif role.tags.is_premium_subscriber():
                by = "Discord (boost role)"
            else:
                by = "Impossible to know who manage the role"
            description += f"\n**Managed by: {by}"
        if (not role.managed) and (log.reason is not None):
            description += f"\n**Reason:** {log.reason}"
        embed.description = description
        if not role.managed:
            embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
        return embed

    def fr():
        description = f"Rôle créé {role.mention} `{role.id}`"
        if role.managed:
            by = None
            if role.tags.bot_id is not None:
                by = f"Le bot {role.guild.get_member(role.tags.bot_id).mention} `{role.tags.bot_id}`"
            elif role.tags.integration_id is not None:
                by = f"L'intégration `{role.tags.integration_id}`"
            elif role.tags.is_premium_subscriber():
                by = "Discord (rôle boost)"
            else:
                by = "Impossible de savoir qui gère ce rôle"
            description += f"\n**Gérer par: {by}"
        if (not role.managed) and (log.reason is not None):
            description += f"\n**Raison:** {log.reason}"
        embed.description = description
        if not role.managed:
            embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
        return embed
    
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_role_delete(lang:str, role:discord.Role, log:typing.Optional[discord.AuditLogEntry]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.red())
    if log is not None:
        embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
        embed.timestamp = log.created_at

    def en():
        description = f"Role deleted @{role.name} `{role.id}`"
        if log is not None and log.reason is not None:
            description += f"\nReason: {log.reason}"
        embed.description = description
        return embed

    def fr():
        description = f"Rôle supprimé @{role.name} `{role.id}`"
        if log is not None and log.reason is not None:
            description += f"\nRaison : {log.reason}"
        embed.description = description
        return embed
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_role_update_permissions(lang:str, before: discord.Role, after: discord.Role, log:typing.Optional[discord.AuditLogEntry], permissions_trads:dict[str,dict[str,str]]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.orange())

    line_jump = "\n"

    if log is not None:
        embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at if log is not None else discord.utils.utcnow()

    def en():
        description = f"Role updated {after.mention if not after.is_default() else after} `{after.id}`"
        if (log is not None) and (log.reason is not None):
            description += f"\nReason: {log.reason}"
        embed.description = description

        def get_permissions_embed_value(allow: list) -> str:
            return f"{line_jump.join([f'● `{permissions_trads[a][lang]}`' for a in allow]) if len(allow) > 0 else 'No permission'}{line_jump}"

        permissions_before: list = [perm for perm, value in before.permissions if value]
        embed.add_field(name="Before permissions", value=get_permissions_embed_value(permissions_before))

        permissions_after: list = [perm for perm,value in after.permissions if value]
        embed.add_field(name="After permissions", value=get_permissions_embed_value(permissions_after))
        return embed

    def fr():
        description = f"Rôle modifié {after.mention if not after.is_default() else after} `{after.id}`"
        if (log is not None) and (log.reason is not None):
            description += f"\nRaison : {log.reason}"
        embed.description = description

        def get_permissions_embed_value(allow: list) -> str:
            return f"{line_jump.join([f'● `{a}`' for a in allow]) if len(allow) > 0 else 'Aucune permission'}{line_jump}"

        permissions_before: list = [perm for perm, value in before.permissions if value]
        embed.add_field(name="Permissions avant", value=get_permissions_embed_value(permissions_before))

        permissions_after: list = [perm for perm,value in after.permissions if value]
        embed.add_field(name="Permissions après", value=get_permissions_embed_value(permissions_after))
        return embed
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_guild_role_update(lang:str, before: discord.Role, after: discord.Role, log:typing.Optional[discord.AuditLogEntry], changes_list:list[str]) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.orange())

    if log is not None:
        embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = log.created_at if log is not None else discord.utils.utcnow()
    
    values = {
        "hoist": {
            True: {
                "en": "Yes",
                "fr": "Oui"
            },
            False: {
                "en": "No",
                "fr": "Non"
            }
        },
        "mentionable": {
            True: {
                "en": "Yes",
                "fr": "Oui"
            },
            False: {
                "en": "No",
                "fr": "Non"
            }
        }
    }
    getters = {
        "name": lambda name: name,
        "color": lambda color: '#%02x%02x%02x' % (color.r, color.g, color.b),
        "hoist": lambda x: values["hoist"][x][lang],
        "mentionable": lambda x: values["mentionable"][x][lang],
    }
    sentences = {
        "name": {
            "en": "Name",
            "fr": "Nom"
        },
        "color": {
            "en": "Color",
            "fr": "Couleur"
        },
        "hoist": {
            "en": "Displayed separately",
            "fr": "Affiché séparément"
        },
        "mentionable": {
            "en": "Mentionable",
            "fr": "Mentionable"
        }
    }

    changes_name = []
    changes_before = []
    changes_after = []
    for change in changes_list:
        changes_name.append(sentences[change][lang])
        changes_before.append(getters[change](getattr(before, change)))
        changes_after.append(getters[change](getattr(after, change)))

    def changes_to_string(changes:list) -> str:
        return '\n'.join([f"● `{change}`" for change in changes])

    def en():
        description = f"Role updated {after.mention if not after.is_default() else after} `{after.id}`"
        if (log is not None) and (log.reason is not None):
            description += f"\nReason: {log.reason}"
        embed.add_field(name="Changements", value=changes_to_string(changes_name))
        embed.add_field(name="Before", value=changes_to_string(changes_before))
        embed.add_field(name="After", value=changes_to_string(changes_after))
        return embed

    def fr():
        description = f"Rôle modifié {after.mention if not after.is_default() else after} `{after.id}`"
        if (log is not None) and (log.reason is not None):
            description += f"\nRaison : {log.reason}"
        embed.add_field(name="Changements", value=changes_to_string(changes_name))
        embed.add_field(name="Avant", value=changes_to_string(changes_before))
        embed.add_field(name="Après", value=changes_to_string(changes_after))
        return embed
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_invite_create(lang:str, invite:discord.Invite, log:discord.AuditLogEntry) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.green())
    embed.set_author(name=f"{log.user} ({log.user.id})", icon_url=log.user.avatar)
    embed.timestamp = invite.created_at

    max_uses = invite.max_uses if invite.max_uses > 0 else "ထ"

    ages = {
        0: {
            "en": "ထ",
            "fr": "ထ"
        },
        1800: {
            "en": "30 minutes",
            "fr": "30 minutes"
        },
        3600: {
            "en": "1 hour",
            "fr": "1 heure"
        },
        21600: {
            "en": "6 hours",
            "fr": "6 heures"
        },
        43200: {
            "en": "12 hours",
            "fr": "12 heures"
        },
        86400: {
            "en": "24 hours",
            "fr": "24 heures"
        },
        604800: {
            "en": "7 days",
            "fr": "7 jours"
        },
    }

    def en():
        description = f"Invitation created `{invite.url}`"
        if log.reason is not None:
            description += f"\nReason: {log.reason}"
        embed.description = description
        embed.add_field(name="Max usages", value=f"`{max_uses}`")
        embed.add_field(name="Max age", value=f"`{ages[invite.max_age][lang]}`")
        return embed

    def fr():
        description = f"Invitation créée `{invite.url}`"
        if log.reason is not None:
            description += f"\nRaison: {log.reason}"
        embed.description = description
        embed.add_field(name="Utilisations max", value=f"`{max_uses}`")
        embed.add_field(name="Expire après", value=f"`{ages[invite.max_age][lang]}`")
        return embed
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()


def on_invite_delete(lang:str, invite:discord.Invite) -> discord.Embed:
    embed = discord.Embed(colour=discord.Color.red())
    embed.timestamp = discord.utils.utcnow()

    def en():
        embed.description = f"Invitation deleted `{invite.url}`"
        embed.set_footer(text="See the audit logs to know who deleted invitation")
        return embed

    def fr():
        embed.description = f"Invitation supprimée `{invite.url}`"
        embed.set_footer(text="Regardez les audit logs du serveur pour savoir qui a supprimé l'invitaiton")
        return embed
    
    langs = {
        "en": en,
        "fr": fr
    }
    return langs[lang]()

