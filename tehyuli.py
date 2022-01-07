import os
import json
import traceback
import discord
from discord.ext import commands

DESCRIPTION = """
Teh Yuli Discord BOT Created By ABC Guild.
"""

class TehYuli(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix='?/',
            description=DESCRIPTION,
            heartbeat_timeout=150.0,
            intents=intents,
            help_command=None,
        )
        self._load_extensions()

    def _load_extensions(self) -> None:
        albionModule = os.listdir("ext/tehyuli/albion_item")
        for filename in albionModule:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"ext.tehyuli.albion_item.{cog}")
                except Exception as e:
                    traceback.print_exc()
