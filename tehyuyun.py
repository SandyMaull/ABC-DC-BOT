import os
import json
import traceback
import discord
from discord.ext import commands

DESCRIPTION = """
Teh Yuyun Discord BOT Created By ABC Guild.
"""

class TehYuyun(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='+=',
            description=DESCRIPTION,
            heartbeat_timeout=150.0,
            help_command=None,
        )
        self._load_extensions()

    def _load_extensions(self) -> None:
        rulesModule = os.listdir("ext/tehyuyun")
        for filename in rulesModule:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"ext.tehyuyun.{cog}")
                except Exception as e:
                    traceback.print_exc()
