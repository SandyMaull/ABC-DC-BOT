from discord.ext import commands
from discord.app_commands import Choice
from discord import app_commands
import discord
import json
from utils.JsonHandler import DeserializationJson, SerializationJson
from dotenv import load_dotenv
import os

load_dotenv()
class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'vtest',
        description = 'Membuat Voting Polls mu'
    )
    async def vtest(self, interaction: discord.Interaction):
        print()
        # message = await interaction.channel.fetch_message(interaction.message.reference)
        # await interaction.response.send_message(message, ephemeral = True)

    @app_commands.command(
        name = 'vcreate',
        description = 'Membuat Voting Polls mu'
    )
    async def vcreate(self, interaction: discord.Interaction, nama: str, unique_name: str):
        dataJson = DeserializationJson(inName = '{id}/voting'.format(id = interaction.user.id))
        if len(dataJson) >= 1:
            for i in range(len(dataJson)):
                if dataJson[i]['unique_name'] == unique_name:
                    matchedname = dataJson[i]['unique_name']
                    await interaction.response.send_message(f"ERROR!\nVoting dengan unique name '{unique_name}' sudah ada.\nsilahkan pilih nama unique name yang lain.")
                    return
            data = {
                'id' : len(dataJson) + 1,
                'unique_name': unique_name,
                'name' : nama,
                'author' : interaction.user.id,
                'choice' : []
            }
            dataJson.append(data)
            SerializationJson(dataJson, inName = '{id}/voting'.format(id = interaction.user.id))
        else: 
            data = [{
                'id' : 1,
                'unique_name': unique_name,
                'name' : nama,
                'author' : interaction.user.id,
                'choice' : []
            }]
            SerializationJson(data, inName = '{id}/voting'.format(id = interaction.user.id))
        await interaction.response.send_message(f"Voting '{nama}' sudah berjalan, silahkan vote melalui '/vote' (Pastikan kamu memilih bot ini).\nuntuk menambah pilihan di voting bisa melalui /vchoice")
        return

    @app_commands.command(
        name = 'vlist',
        description = 'List Voting Polls milikmu'
    )
    async def vlist(self, interaction: discord.Interaction):
        dataRaw = DeserializationJson( inName = '{id}/voting'.format(id = interaction.user.id) )
        listData = "List Voting Polls mu:\n"
        if len(dataRaw) >= 1:
            for i in range(len(dataRaw)):
                listData += "Voting Name: {name}\nUnique Name: {uniq} \n\n".format(name = dataRaw[i]['name'], uniq = dataRaw[i]['unique_name'])
            await interaction.response.send_message("{split}\n{data}{split}".format(data = listData, split = '=' * 30) , ephemeral=True)


    @app_commands.command(
        name = 'vdelete',
        description = 'Delete Voting Polls milikmu')
    async def vcreate(self, interaction: discord.Interaction, unique_name: str):
        dataRaw = DeserializationJson( inName = '{id}/voting'.format(id = interaction.user.id) )


    @app_commands.command(
        name = 'vchoice',
        description = 'Manipulasi Pilihan pada Voting Polls')
    @app_commands.describe(
        unique_name = "Unique Name Voting Poll",
        action = "Pilih Aksi untuk Voting Poll")
    @app_commands.choices(
        action = [
            Choice(name = "Tambah Choice Baru", value = 1),
            Choice(name = "Update Choice", value = 2),
            Choice(name = "Hapus Choice", value = 3),
        ])
    async def vchoice(self, interaction: discord.Interaction, unique_name: str, action: int):
        dataRaw = DeserializationJson( inName = '{id}/voting'.format(id = interaction.user.id) )
        matchedname = None
        for i in range(len(dataRaw)):
            if dataRaw[i]['unique_name'] == unique_name:
                matchedname = dataRaw[i]['unique_name']

        if matchedname is not None:
            print(matchedname)
            print("Masuk Sini!")
        else:
            await interaction.response.send_message("Data Voting `{name}` tidak ditemukan.".format(name = unique_name), ephemeral=True)

async def setup(bot):
    await bot.add_cog(
        Voting(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )
