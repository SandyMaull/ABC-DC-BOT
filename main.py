from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import asyncio

load_dotenv()
Owner = int(os.getenv('OWNER_ID'))
Server = int(os.getenv('SERVER_ID'))
Time = 0

class MomoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!1",
            intents=discord.Intents.all(),
        )

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                await self.load_extension(f"cogs.{fn[:-3]}")
                await self.tree.sync(guild = discord.Object(id = Server))
        await self.change_presence(activity=discord.Game("Testing BOT..."))

client = MomoBot()

@client.command()
async def list(ctx):
    if ctx.author.id != Owner:
        await ctx.reply("You're not my Master! :angry: ")
        return
    else:
        var_list = []
        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                var_list.append(fn[:-3])
        await ctx.reply("List Extension: {ext}".format(ext = var_list))

@client.command()
async def load(ctx, extension=None):
    if ctx.author.id != Owner:
        await ctx.reply("You're not my Master! :angry: ")
        return
    else:
        if extension is None:
            await ctx.reply("You're Not Input Any Extension, Master! :cry: ")
            return
        else:
            try:
                await client.load_extension('cogs.{ext}'.format(ext = extension))
                await client.tree.sync(guild = discord.Object(id = Server))
                await ctx.reply("Your load request is Accepted, Master!")
            except Exception as e:
                print(e)
                await ctx.reply("Your load request is Rejected, Master!\nDetails: {e}".format(e=e))

@client.command()
async def unload(ctx, extension=None):
    if ctx.author.id != Owner:
        await ctx.reply("You're not my Master! :angry: ")
        return
    else:
        if extension is None:
            await ctx.reply("You're Not Input Any Extension, Master! :cry: ")
            return
        else:
            try:
                await client.unload_extension('cogs.{ext}'.format(ext = extension))
                await client.tree.sync(guild = discord.Object(id = Server))
                await ctx.reply("Your unload request is Accepted, Master!")
            except Exception as e:
                print(e)
                await ctx.reply("Your unload request is Rejected, Master!\nDetails: {e}".format(e=e))

@client.command()
async def reload(ctx, extension=None):
    if ctx.author.id != Owner:
        await ctx.reply("You're not my Master! :angry: ")
        return
    else:
        if extension is None:
            await ctx.reply("You're Not Input Any Extension, Master! :cry: ")
            return
        else:
            try:
                await client.reload_extension('cogs.{ext}'.format(ext = extension))
                await client.tree.sync(guild = discord.Object(id = Server))
                await ctx.reply("Your reload request is Accepted, Master!")
            except Exception as e:
                print(e)
                await ctx.reply("Your reload request is Rejected, Master!\nDetails: {e}".format(e=e))

client.run(os.getenv('DISCORD_TOKEN'))