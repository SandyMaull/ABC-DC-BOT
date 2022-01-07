import os
import json
import traceback
import discord
from discord.ext import commands

DESCRIPTION = """
Kang Pimpin Discord BOT Created By ABC Guild.
"""

class KangPimpin(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$4',
            description=DESCRIPTION,
            heartbeat_timeout=150.0,
            help_command=None,
        )
        self._load_extensions()

    def _load_extensions(self) -> None:
        albionModule = os.listdir("ext/kangpimpin")
        for filename in albionModule:
            if filename.endswith(".py"):
                cog = filename[:-3]
                try:
                    self.load_extension(f"ext.kangpimpin.{cog}")
                except Exception as e:
                    traceback.print_exc()
