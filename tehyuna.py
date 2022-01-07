import os
import json
import traceback
import discord
from discord.ext import commands

DESCRIPTION = """
Teh Yuna Discord BOT Created By ABC Guild.
"""

class TehYuna(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=("!1", "-"),
            description=DESCRIPTION,
            heartbeat_timeout=150.0,
            intents=intents,
            help_command=None,
        )
        self._load_extensions()

    def _load_extensions(self) -> None:
        musicModule = os.listdir("ext/tehyuna/music")
        registerModule = os.listdir("ext/tehyuna/register")
        
        for filename in musicModule:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"ext.tehyuna.music.{cog}")
                except Exception as e:
                    traceback.print_exc()

        for filename in registerModule:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"ext.tehyuna.register.{cog}")
                except Exception as e:
                    traceback.print_exc()
