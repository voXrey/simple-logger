import sqlite3
import typing
import core


class GuildData(object):
    def __init__(self, guild_id:int, lang:typing.Optional[str], prefix:typing.Optional[str]):
        users_settings = core.get_json('data/users-settings.json')
        self.guild_id = guild_id
        self.lang = lang if lang is not None else users_settings["lang"]["default"]
        self.prefix = prefix if prefix is not None else users_settings["prefix"]["default"]

    def get(self, attr:str):
        return self.__getattribute__(attr)

class Database(object):
    DB_LOCATION = "./data/database.sqlite3"

    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect(Database.DB_LOCATION)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS guilds(
            guild_id INTEGER PRIMARY KEY,
            lang TEXT,
            prefix TEXT
        )""")

    def add_guilds(self, guilds_id:set[int]):
        self.cursor.executemany("INSERT INTO guilds(guild_id) VALUES(?)", [(guild_id,) for guild_id in guilds_id])

    def remove_guilds(self, guilds_id:set[int]):
        self.cursor.execute("DELETE FROM guilds WHERE guild_id in ({seq})".format(seq=','.join(['?']*len(guilds_id))), tuple(guilds_id))

    def get_all_guilds_id(self) -> set[int]:
        self.cursor.execute("SELECT guild_id FROM guilds")
        rows = self.cursor.fetchall()
        guilds_id = {row[0] for row in rows}
        return guilds_id

    def get_guild(self, guild_id:int) -> GuildData:
        self.cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
        row = self.cursor.fetchone()
        return GuildData(*row)

    def get_all_guilds(self) -> list[GuildData]:
        self.cursor.execute("SELECT * FROM guilds")
        guilds = []
        for row in self.cursor.fetchall():
            guilds.append(GuildData(*row))
        return guilds

    def edit_guild(self, guild_id:int, settings:dict):
        seq = ", ".join([f"{k}=?" for k in settings.keys()])
        args = [v for v in settings.values()]
        args.append(guild_id)
        self.cursor.execute(f"UPDATE guilds SET {seq}WHERE guild_id = ?", args)