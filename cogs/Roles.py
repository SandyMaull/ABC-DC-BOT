from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from discord.utils import get
import discord
import os

load_dotenv()
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        regis = 1052679879675629638
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.message_id == regis:
            if payload.emoji.name == '👌':
                role = discord.utils.get(guild.roles, id=802066849314504725)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    await payload.member.send("Halo `{name}`, Anda mendapatkan roles `{rl}` di ABC Guild!".format(name = payload.member.name, rl = role.name))
                    return

            else:
                return

        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        regis = 1052679879675629638
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.message_id == regis:
            if payload.emoji.name == '👌':
                role = discord.utils.get(guild.roles, id=802066849314504725)
                if role in member.roles:
                    await member.remove_roles(role)
                    return

            else:
                return

        else:
            return

async def setup(bot):
    await bot.add_cog(
        Roles(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )