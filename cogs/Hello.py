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
        description = 'Say Hello to Teh Yuli'
    )
    async def introduce(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello `{name}`, my name is **Teh Yuli!**, and i am a witch.\nNice to have you in this server :)".format(name = interaction.user.name))

    @app_commands.command(
        name = 'about',
        description = 'About this Bot'
    )
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(title='YuliBot Github',
            url='https://github.com/SandyMaull/ABC-DC-BOT',
            description='Im a Bot created by my Master using Python Programming Language')
        embed.set_author(name="Kuronekosan", url="https://github.com/SandyMaull", icon_url="https://avatars.githubusercontent.com/u/14269978")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/925155040245710919/74f019575f3ec92dd35c5d371c11da61.png")
        embed.add_field(name="What are you doing here?", value="Im help human in any way, but my main role right now is to help register newcomer to this server", inline=False)
        await interaction.response.send_message("Here is the detail about me.\n i hope you dont hate it >.<\n", embed = embed)

async def setup(bot):
    await bot.add_cog(
        Hello(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )