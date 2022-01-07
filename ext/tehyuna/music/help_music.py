import discord
from discord.ext import commands
import sys
import traceback
import json
from ext.db_module import fetch

def checkdata():
    music_db = fetch.one("config", 'name', 'MUSIC')
    music_data = json.loads(music_db)
    if music_data['value'] == 'TRUE':
        return True
    else:
        return False

def checkchannel():
    get_channel = fetch.many("allow_channel", 'name', 'Music')
    channel_data = json.loads(get_channel)
    list_channel_allow = []
    for i in range(len(channel_data)):
        looping = '{i}'.format(i = i)
        list_channel_allow.append(int(channel_data[looping]['channel_id']))
    return list_channel_allow

class Help_Music(commands.Cog):
    """Cog for the help command."""

    def __init__(self, bot):
        self.bot = bot
        self.prefix = "!1"
        self.bot_cogs = self.bot.cogs

    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @commands.command(name="musichelp", aliases=["mh"])
    async def help(self, ctx):

        if ctx.prefix != '!1':
            return
            
        if checkdata() != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel():
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#796774901285388288>\n\nTerima Kasih Atas Pengertiannya.", delete_after=7)
            return

        try:
            cog = self.bot_cogs["Music"]
        except KeyError:
            query_error_embed = discord.Embed(
                title="Query Error. Perhaps you mean:",
                description=f"{', '.join(self.bot_cogs.keys())}.",
                color=discord.Color.red(),
            )
            return await ctx.send(embed=query_error_embed)

        cog_help_embed = discord.Embed(
            title=f"Bot Commands",
            color=discord.Color.blue(),
        )

        for command in cog.get_commands():

            command_aliases = (
                f"{', '.join(command.aliases)}" if len(command.aliases) > 0 else "None"
            )
            cog_help_embed.add_field(
                name=(f"!1{command.name} , {command_aliases}")
                if (command_aliases != "None")
                else (f"!1{command.name}"),
                value=f"`{command.help}`",
                inline=False,
            )

        cog_help_embed.add_field(
            name="Developer:", value="Anti Bang Cat Guild", inline=False
        )
        await ctx.send(embed=cog_help_embed)


def setup(bot):
    bot.add_cog(Help_Music(bot))
