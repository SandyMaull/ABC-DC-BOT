from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import discord
import os

load_dotenv()
class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'hello',
        description = 'Say Hello to Momo'
    )
    async def introduce(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello `{name}`, my name is **MOMO!**, and my age is 17.\nNice to have you in this server :)".format(name = interaction.user.name))

    @app_commands.command(
        name = 'about',
        description = 'About this Bot'
    )
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(title='MomoBot Github',
            url='https://github.com/SandyMaull/DiscordMinecraft',
            description='Im a Bot created by my Master using Python Programming Language')
        embed.set_author(name="Kuronekosan", url="https://github.com/SandyMaull", icon_url="https://avatars.githubusercontent.com/u/14269978")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/966637175993151498/c457c9c381a1b3e47c078d519bc77869.png")
        embed.add_field(name="What are you doing here?", value="Im help human in any way, but my main role right now is to help remote and control the minecraft server", inline=False)
        await interaction.response.send_message("Here is the detail about me.\n i hope you dont hate it >.<\n", embed = embed)

async def setup(bot):
    await bot.add_cog(
        Hello(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )