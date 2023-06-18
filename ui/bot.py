import discord
from discord.ext import commands
import typing
import traceback


class SelectHelp(discord.ui.Select):
    trads = {
        "logging": {
            "label": {
                "en": "Logging",
                "fr": "Journalisation"
            },
            "description": {
                "en": "Commands and channels for logging",
                "fr": "Commandes et salons pour la journalisation"
            }
        },
        "settings": {
            "label": {
                "en": "Settings",
                "fr": "Paramètres"
            },
            "description": {
                "en": "Commands for settings",
                "fr": "Commandes pour les paramètres"
            }
        },
        "info": {
            "label": {
                "en": "Info",
                "fr": "Informations"
            },
            "description": {
                "en": "Commands for info",
                "fr": "Commandes informatives"
            }
        },
        "others": {
            "label": {
                "en": "Others",
                "fr": "Autres"
            },
            "description": {
                "en": "Others commands and info",
                "fr": "Autres commandes et informations"
            }
        }
    }
    def __init__(self, lang:str, *args, **kwargs) -> None:
        options = [
            discord.SelectOption(value="logging", label=self.trads["logging"]["label"][lang], emoji="📝", description=self.trads["logging"]["description"][lang]),
            discord.SelectOption(value="settings", label=self.trads["settings"]["label"][lang], emoji="⚙️", description=self.trads["settings"]["description"][lang]),
            discord.SelectOption(value="info", label=self.trads["info"]["label"][lang], emoji="💡", description=self.trads["info"]["description"][lang]),
            discord.SelectOption(value="others", label=self.trads["others"]["label"][lang], emoji="🧭", description=self.trads["others"]["description"][lang]),
        ]
        super().__init__(options=options, *args, **kwargs)

    async def callback(self, interaction:discord.Interaction):
        self.view.value = self.values[0]
        await interaction.response.defer()
        self.view.stop()

class ViewHelp(discord.ui.View):
    value = None
    def __init__(self, lang:str, timeout: typing.Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.add_item(SelectHelp(lang))


class SelectHelpOwner(discord.ui.Select):
    trads = {
        "spy": {
            "label": {
                "en": "Spy",
                "fr": "Espionnage"
            },
            "description": {
                "en": "Spy commands",
                "fr": "Commandes d'espionnage"
            }
        },
        "cogs": {
            "label": {
                "en": "Cogs",
                "fr": "Cogs"
            },
            "description": {
                "en": "Commands to manage cogs",
                "fr": "Commandes pour gérer les cogs"
            }
        },
        "bot": {
            "label": {
                "en": "Bot",
                "fr": "Bot"
            },
            "description": {
                "en": "Get or post info about the bot",
                "fr": "Récupère ou poste des informations à propos du bot"
            }
        }
    }
    def __init__(self, lang:str, *args, **kwargs) -> None:
        options = [
            discord.SelectOption(value="spy", label=self.trads["spy"]["label"][lang], emoji="👓", description=self.trads["spy"]["description"][lang]),
            discord.SelectOption(value="cogs", label=self.trads["cogs"]["label"][lang], emoji="⚙️", description=self.trads["cogs"]["description"][lang]),
            discord.SelectOption(value="bot", label=self.trads["bot"]["label"][lang], emoji="🤖", description=self.trads["bot"]["description"][lang]),
        ]
        super().__init__(options=options, *args, **kwargs)

    async def callback(self, interaction:discord.Interaction):
        self.view.value = self.values[0]
        await interaction.response.defer()
        self.view.stop()

class ViewHelpOwner(discord.ui.View):
    value = None
    def __init__(self, lang:str, timeout: typing.Optional[float] = 180):
        super().__init__(timeout=timeout)
        self.add_item(SelectHelpOwner(lang))


class ModalReport(discord.ui.Modal):
    title_value:str = None
    description_value:str = None
    trads = {
        "modal-title": {
            "en": "Report",
            "fr": "Rapport"
        },
        "title": {
            "en": "Report title",
            "fr": "Titre du rapport"
        },
        "description": {
            "en": "Report description",
            "fr": "Description du rapport"
        }
    }
    def __init__(self, lang:str):
        super().__init__(title=self.trads["modal-title"][lang], timeout=600)
        self.lang = lang

        self.input_title = discord.ui.TextInput(
            label="title",
            style=discord.TextStyle.short,
            placeholder=self.trads["title"][lang],
            required=True,
            min_length=8,
            max_length=256,
        )
        self.add_item(self.input_title)

        self.input_description = discord.ui.TextInput(
            label="description",
            style=discord.TextStyle.paragraph,
            placeholder=self.trads["description"][lang],
            required=True,
            min_length=64,
            max_length=4000,
        )
        self.add_item(self.input_description)

    async def on_submit(self, interaction: discord.Interaction):
        self.title_value, self.description_value = self.input_title.value, self.input_description.value
        await interaction.response.defer()

class SelectReport(discord.ui.Select):
    trads = {
        "error": {
            "label": {
                "en": "Error",
                "fr": "Erreur"
            },
            "description": {
                "en": "An unknow error is occured",
                "fr": "Une erreur inconnue s'est produite"
            }
        },
        "dont-working": {
            "label": {
                "en": "Dont working",
                "fr": "Ne fonctionne pas"
            },
            "description": {
                "en": "A feature or a command doesn't work",
                "fr": "Une fonctionnalité ou une commande ne fonctionne pas"
            }
        },
        "lang": {
            "label": {
                "en": "Langage",
                "fr": "Langage"
            },
            "description": {
                "en": "A translation error or a mistake in a text",
                "fr": "Une erreur de traduction ou une faute dans un texte"
            }
        },
        "other": {
            "label": {
                "en": "Other",
                "fr": "Autre"
            },
            "description": {
                "en": "The problem does not fit into any category",
                "fr": "Le problème n'entre dans aucune catégorie"
            }
        }
    }
    def __init__(self, lang:str, *args, **kwargs) -> None:
        self.lang = lang
        options = [
            discord.SelectOption(value="error", label=self.trads["error"]["label"][lang], emoji="❌", description=self.trads["error"]["description"][lang]),
            discord.SelectOption(value="dont-working", label=self.trads["dont-working"]["label"][lang], emoji="🤕", description=self.trads["dont-working"]["description"][lang]),
            discord.SelectOption(value="langage", label=self.trads["lang"]["label"][lang], emoji="💬", description=self.trads["lang"]["description"][lang]),
            discord.SelectOption(value="other", label=self.trads["other"]["label"][lang], emoji="⚙️", description=self.trads["other"]["description"][lang]),
        ]
        super().__init__(options=options, *args, **kwargs)
    
    async def callback(self, interaction:discord.Interaction):
        self.view.category_value = self.values[0]
        modal = ModalReport(self.lang)
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.view.title_value, self.view.description_value = modal.title_value, modal.description_value
        self.view.stop()

class ViewReport(discord.ui.View):
    category_value:str = None
    title_value:str = None
    description_value:str = None
    def __init__(self, lang:str):
        super().__init__(timeout=300)
        self.add_item(SelectReport(lang))

class ButtonSubmitConfirmReport(discord.ui.Button):
    trads = {
        "en": "Submit",
        "fr": "Envoyer"
    }
    def __init__(self, lang:str):
        super().__init__(
            style=discord.ButtonStyle.green,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.value = True
        self.view.stop()

class ButtonCancelConfirmReport(discord.ui.Button):
    trads = {
        "en": "Cancel",
        "fr": "Annuler"
    }
    def __init__(self, lang:str):
        super().__init__(
            style=discord.ButtonStyle.red,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.stop()

class ViewConfirmReport(discord.ui.View):
    value:bool = False
    def __init__(self, lang:str):
        super().__init__(timeout=300)
        self.lang = lang
        self.add_item(ButtonSubmitConfirmReport(lang))
        self.add_item(ButtonCancelConfirmReport(lang))


class ModalSuggest(discord.ui.Modal):
    title_value:str = None
    description_value:str = None
    trads = {
        "modal-title": {
            "en": "Suggestion",
            "fr": "Suggestion"
        },
        "title": {
            "en": "Suggestion title",
            "fr": "Titre de la suggestion"
        },
        "description": {
            "en": "Suggestion description",
            "fr": "Description de la suggestion"
        }
    }
    def __init__(self, lang:str):
        super().__init__(title=self.trads["modal-title"][lang], timeout=600)
        self.lang = lang

        self.input_title = discord.ui.TextInput(
            label="title",
            style=discord.TextStyle.short,
            placeholder=self.trads["title"][lang],
            required=True,
            min_length=8,
            max_length=256,
        )
        self.add_item(self.input_title)

        self.input_description = discord.ui.TextInput(
            label="description",
            style=discord.TextStyle.paragraph,
            placeholder=self.trads["description"][lang],
            required=True,
            min_length=64,
            max_length=4000,
        )
        self.add_item(self.input_description)

    async def on_submit(self, interaction: discord.Interaction):
        self.title_value, self.description_value = self.input_title.value, self.input_description.value
        await interaction.response.defer()

class ButtonSubmitFirstConfirmSuggest(discord.ui.Button):
    trads = {
        "en": "Yes",
        "fr": "Oui"
    }
    def __init__(self, lang:str):
        self.lang = lang
        super().__init__(
            style=discord.ButtonStyle.green,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.value = True
        modal = ModalReport(self.lang)
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.view.title_value, self.view.description_value = modal.title_value, modal.description_value
        self.view.stop()

class ButtonCancelFirstConfirmSuggest(discord.ui.Button):
    trads = {
        "en": "No",
        "fr": "Non"
    }
    def __init__(self, lang:str):
        super().__init__(
            style=discord.ButtonStyle.red,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.stop()

class ViewFirstConfirmSuggest(discord.ui.View):
    value:bool = False
    def __init__(self, lang:str):
        super().__init__(timeout=300)
        self.lang = lang
        self.add_item(ButtonSubmitFirstConfirmSuggest(lang))
        self.add_item(ButtonCancelFirstConfirmSuggest(lang))

class ButtonSubmitConfirmSuggest(discord.ui.Button):
    trads = {
        "en": "Submit",
        "fr": "Envoyer"
    }
    def __init__(self, lang:str):
        super().__init__(
            style=discord.ButtonStyle.green,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.value = True
        self.view.stop()

class ButtonCancelConfirmSuggest(discord.ui.Button):
    trads = {
        "en": "Cancel",
        "fr": "Annuler"
    }
    def __init__(self, lang:str):
        super().__init__(
            style=discord.ButtonStyle.red,
            label=self.trads[lang]
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.stop()

class ViewConfirmSuggest(discord.ui.View):
    value:bool = False
    def __init__(self, lang:str):
        super().__init__(timeout=300)
        self.lang = lang
        self.add_item(ButtonSubmitConfirmSuggest(lang))
        self.add_item(ButtonCancelConfirmSuggest(lang))

