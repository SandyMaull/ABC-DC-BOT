from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'register',
        description = 'Register untuk memperkenalkan diri lo di Guild ini')
    @app_commands.describe(
        option = "Pilih Opsi",
        nickname = "Masukan nama yang cocok buat kita manggil lo",
        ign_albion = "Optional, hanya jika memiliki akun Albion"
    )
    @app_commands.choices(
        option = [
            Choice(name = "Punya Akun Albion.", value = 1),
            Choice(name = "Ga tau bang apa itu.", value = 2),
        ])
    async def register(self, interaction: discord.Interaction, option: int, nickname: str, ign_albion: str = None):
        if option == 2 and len(nickname) > 32:
            await interaction.response.send_message("**(ERR)** Nickname yang lo masukin kepanjangan cuy, pendekin lagi.")
            return

        if option == 1 and ign_albion == None:
            await interaction.response.send_message("**(ERR)** Mohon isi IGN Albion jika lo memilih opsi `Punya Akun Albion.`")
            return

        elif option == 1:
            await interaction.response.send_message("**(ERR)** This feature is still under development.")
            return

        elif option == 2:
            await interaction.user.edit( nick="[-] {nick}".format(nick = nickname) )
            await interaction.response.send_message( "**(DONE)** Halo `{name}`, Terimakasih sudah register.\nKita bakal membiasakan diri untuk manggil lo `{nick}`".format(name = interaction.user.name, nick = nickname) )
            return


async def setup(bot):
    await bot.add_cog(
        Register(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )