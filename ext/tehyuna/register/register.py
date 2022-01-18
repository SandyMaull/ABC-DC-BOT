import asyncio
import discord
from discord.ext import commands
import traceback
import json
from ext.db_module import fetch, insert
import sys
import requests
import urllib

from random import shuffle
from youtube_dl import YoutubeDL

def checkdata(guild_id):
    regis_db = fetch.one(guild_id, "config", 'name', 'REGISTER')
    regis_data = json.loads(regis_db)
    if regis_data['value'] == 'TRUE':
        return True
    else:
        
        return False

def checkchannel(guild_id):
    get_channel = fetch.many(guild_id, "allow_channel", 'name', 'Register')
    channel_data = json.loads(get_channel)
    list_channel_allow = []
    for i in range(len(channel_data)):
        looping = '{i}'.format(i = i)
        list_channel_allow.append(int(channel_data[looping]['channel_id']))
    return list_channel_allow
    

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "-"

    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.reply("Something Error, Check BOT Permission.", delete_after=7)
            return
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.reply("Something Error, User Not Found.", delete_after=7)
            return
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    # @commands.command(
    #     name="dreg",
    #     help="*Register khusus untuk dev, contoh: -dreg [Mention yg ingin di register] [nickname]",
    #     aliases=["devregister"],
    # )
    # @commands.has_permissions(manage_nicknames=True)
    # async def dreg(self, ctx, m: discord.Member, *args):
        # if ctx.prefix != '-':
        #     return

        # if checkdata() != True:
        #     await ctx.reply("Fitur register pada bot ini sedang dimatikan oleh developer.", delete_after=7)
        #     return

        # if ctx.channel.id not in checkchannel() and "ticket" not in ctx.channel.name:
        #     await ctx.reply("Bot hanya bisa digunakan di channel `ticket-xxxx`\n\nTerima Kasih Atas Pengertiannya.", delete_after=7)
        #     return
        # print(insert.history("('Test', 'Test', 'Test')"))
        # guild_db = fetch.one("guild", 'guild_id', '787698443442323476')
        # guild_data = json.loads(guild_db)
        
        # if len(args) == 1:
        #     nickname = args[0]
        #     tguild = "-"
        #     rename = (f"[{tguild}] {nickname}")
        #     role = discord.utils.get(ctx.guild.roles, id=int(guild_data['visitorrole']))
        #     await ctx.channel.trigger_typing()
            
        # elif len(args) == 2:
        # else:
        #     await ctx.reply("Parameter Invalid, use `-rh` for help.", delete_after=7)
        #     return

        # await m.edit(nick=args)


    @commands.command(
        name="reg",
        help="*Register untuk mendapatkan roles\n*format: -reg [nickname - MAX 12 Characters] [In Game Name di Albion - jika ada, jika tidak dapat dikosongkan]\n*contoh: -reg Sandy Kuronekosannn",
        aliases=["register"],
    )
    async def reg(self, ctx, *args):

        if ctx.prefix != '-':
            return

        if checkdata(ctx.guild.id) != True:
            await ctx.reply("Fitur register pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id) and "ticket" not in ctx.channel.name:
            await ctx.reply("Bot hanya bisa digunakan di channel `ticket-xxxx`\n\nTerima Kasih Atas Pengertiannya.", delete_after=7)
            return

        guild_db = fetch.one(ctx.guild.id, "guild", 'guild_id', '787698443442323476')
        guild_data = json.loads(guild_db)
        if len(args) == 1:
            nickname = args[0]
            tguild = "-"
            rename = (f"[{tguild}] {nickname}")
            role = discord.utils.get(ctx.guild.roles, id=int(guild_data['visitorrole']))
            await ctx.channel.trigger_typing()
        elif len(args) == 2:
            nickname = args[0]
            ign = args[1]
            await ctx.channel.trigger_typing()
            await ctx.reply(f'Searching for Player {ign}\nMaybe take a while, please be patient.', delete_after=15)
            fullURL = (f"https://gameinfo.albiononline.com/api/gameinfo/search?q={ign}")
            print('Searching For Player',ign)
            data = urllib.request.urlopen(fullURL).read().decode()
            await ctx.channel.trigger_typing()
            output = json.loads(data)
            try:
                player = output["players"][0]
            except IndexError:
                player = 'null' 
            await ctx.channel.trigger_typing()
            if player == 'null':
                await ctx.reply(f'Player {ign} Not Found.\nIgnoring IGN, and continue the process.')
                tguild = "-"
                rename = (f"[{tguild}] {nickname}")
                role = discord.utils.get(ctx.guild.roles, id=int(guild_data['visitorrole']))
            else:
                ign_fix = player['Name']
                guild = player['GuildName']
                if guild == "":
                    tguild = '-'
                elif guild == guild_data['name']:
                    role = discord.utils.get(ctx.guild.roles, id=int(guild_data['memberrole']))
                    tguild = "ABC"
                else:
                    role = discord.utils.get(ctx.guild.roles, id=int(guild_data['visitorrole']))
                    alias_db = fetch.all(ctx.guild.id, "guild_alias")
                    alias_data = json.loads(alias_db)
                    alias_exist = False
                    for i in range(len(alias_data)):
                        looping = '{i}'.format(i = i)
                        if guild == alias_data[looping]['name']:
                            tguild = alias_data[looping]['alias']
                            alias_exist = True
                        else:
                            continue
                    if alias_exist == False:
                        if len(guild) >= 6:
                            tguild = guild[0:5]
                        else:
                            tguild = guild
                rename = (f"[{tguild}] {ign_fix} ({nickname})")

        else:
            await ctx.reply("Parameter Invalid, use `-rh` for help.", delete_after=7)
            return

        role_remove1 = discord.utils.get(ctx.guild.roles, id=int(guild_data['memberrole']))
        role_remove2 = discord.utils.get(ctx.guild.roles, id=int(guild_data['visitorrole']))
        if role_remove1 in ctx.author.roles and role_remove2 in ctx.author.roles:
            await ctx.author.remove_roles(role_remove1)
            await ctx.author.remove_roles(role_remove2)
        elif role_remove1 in ctx.author.roles:
            await ctx.author.remove_roles(role_remove1)
        elif role_remove2 in ctx.author.roles:
            await ctx.author.remove_roles(role_remove2)
        else:
            print(f"{ctx.author.name} has no role for removing")

        try:
            await ctx.author.edit(nick=rename)
            await ctx.author.add_roles(role)
            await ctx.reply(f'Registration Success\nYour Nickname Is `{nickname}` And You Are In Guild `[{tguild}]`\nYour Nickname Changed to {ctx.message.author.mention}\nAnd You Get `{role}` Role')
        except:
            helpers = discord.utils.get(ctx.guild.roles, name='Helpers')
            await ctx.reply(f"Something Error Happening :(\n\nplease check the role, make sure to clean up before register or re-register.\ncontact {helpers} if you need assistance.")
        



def setup(bot):
    bot.add_cog(Register(bot))
