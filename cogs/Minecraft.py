from utils.ApiConnection import Start as ApiStart, Stop as ApiStop, CheckStatus as ApiCheck
from utils.RemoteConnection import start as RmtStart, stop as RmtStop, status as RmtStatus
from discord.app_commands import Choice
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import discord
import json
import time
import os

load_dotenv()
class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'kuromine',
        description = 'Firing API to Server KuroMine')
    @app_commands.describe(
        action = "Choose Your Action",
        players = "Optional Parameters for Start Server"
    )
    @app_commands.choices(
        action = [
            Choice(name = "Start Server", value = 1),
            Choice(name = "Stop Server", value = 2),
            Choice(name = "Restart Server", value = 3),
            Choice(name = "Backup Server", value = 4),
            Choice(name = "Check Server", value = 5),
        ])
    async def kuromine(self, interaction: discord.Interaction, action: int, players: int = None):

        if interaction.user.id not in [172496511542755328, 267884420533321729]: #Kuro and Avus ID
            await interaction.response.send_message("**(ERR)** You're not Authorized to use this feature. :cry:")
            return

        if players is not None and players > 8:
            await interaction.response.send_message("**(ERR)** Cant Execute, Max Players right now is 8, maybe will increase soon.")
            return

        if action == 1 and players is None:
            await interaction.response.send_message("**(ERR)** Please define how much player when starting the server.")
            return

        elif action == 1 and players is not None:
            await interaction.response.send_message("**(1/5)** Connecting to API, Please wait for a moment.")
            ApiConn = await ApiStart()
            ApiConn = json.loads(ApiConn)
            if ApiConn['status'] != 0:
                await interaction.channel.send("**(ERR)** Error Occurred on API Connection.\nDetails: {e}".format(e = ApiConn['res']))
                return

            await interaction.channel.send("**(2/5)** Sending Start Signal to Server...\nPlease wait for a minutes.")
            ApiConn = await ApiCheck()
            ApiConn = json.loads(ApiConn)
            if ApiConn['status'] == 0 and ApiConn['res'] == 'running':
                await interaction.channel.send("**(3/5)** Server is running, Connecting to Remote Service")
                time.sleep(18)
                RmtConn = RmtStart()
                RmtConn = json.loads(RmtConn)
                if RmtConn['status'] != 0:
                    await interaction.channel.send("**(ERR)** Error Occurred on Remote Connection.\nDetails: {e}".format(e = RmtConn['res']))
                    return
                
                await interaction.channel.send("**(4/5)** Remote Service Connected...\nStarting Kuromine1 Service...\nPlease wait for a minutes.")
                time.sleep(10)
                RmtConn = RmtStatus()
                if RmtConn['status'] == 0 and RmtConn['res'] == 'active':
                    await interaction.channel.send("**(5/5)** Service is running, Enjoy the Game!")
                    return
                
                else:
                    await interaction.channel.send("**(ERR)** Something doesnt execute right on Remote Connection, check the code.")
                    return

            else:
                await interaction.channel.send("**(ERR)** Something doesnt execute right on API, check the code.")
                return

        elif action == 2:
            await interaction.response.send_message("**(1/3)** Connecting to API, Please wait for a moment.")
            ApiConn = await ApiStop()
            ApiConn = json.loads(ApiConn)
            if ApiConn['status'] != 0:
                await interaction.channel.send("**(ERR)** Error Occurred\nDetails: {e}".format(e = ApiConn['res']))
                return

            await interaction.channel.send("**(2/3)** Sending Stop Signal to Server...\nPlease wait for a minutes.")
            ApiConn = await ApiCheck()
            ApiConn = json.loads(ApiConn)
            if ApiConn['status'] == 0 and ApiConn['res'] == 'stopped':
                await interaction.channel.send("**(3/3)** Server is stop.")
                return

            else:
                await interaction.channel.send("**(ERR)** Something doesnt execute right, check the code.")
                return

        elif action == 3:
            await interaction.response.send_message("**(ERR)** This feature is under development right now.")
            return
        
        elif action == 4:
            await interaction.response.send_message("**(ERR)** This feature is under development right now.")
            return
        
        elif action == 5:
            await interaction.response.send_message("**(ERR)** This feature is under development right now.")
            return

        else:
            print("Catch me if you can!")
            await interaction.response.send_message("436f6e67726174756c6174696f6e732128666c616729")
            return



async def setup(bot):
    await bot.add_cog(
        Minecraft(bot),
        guild = discord.Object(id = os.getenv('SERVER_ID'))
    )