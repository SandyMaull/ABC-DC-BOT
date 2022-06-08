import asyncio
import discord
from discord.ext import commands
import traceback
import json
from ext.db_module import fetch
import sys

from random import shuffle
from youtube_dl import YoutubeDL

def checkdata(guild_id, guild_dev_id):
    music_db = fetch.one(guild_id, "config", 'name', 'MUSIC')
    music_data = json.loads(music_db)
    dev_db = fetch.all(guild_id, 'developer')
    dev_data = json.loads(dev_db)
    dev_id = []
    for i in range(len(dev_data)):
        dev_id.append(int(dev_data["{i}".format(i = i)]["dev_id"]))

    if music_data['value'] == 'TRUE':
        return True
    else:
        # if guild_dev_id in dev_id :
        #     return True
        return False

def checkchannel(guild_id):
    get_channel = fetch.many(guild_id, "allow_channel", 'name', 'Music')
    channel_data = json.loads(get_channel)
    list_channel_allow = []
    for i in range(len(channel_data)):
        looping = '{i}'.format(i = i)
        list_channel_allow.append(int(channel_data[looping]['channel_id']))
    return list_channel_allow

def defaultchannel(guild_id):
    music_db = fetch.one(guild_id, "allow_channel", 'name', 'Default-Music')
    music_data = json.loads(music_db)
    return music_data['channel_id']

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = "!1"
        self.isTimed = False
        self.is_playing = False
        self.current_song = None
        self.music_queue = []
        self.skip_votes = set()

        self.YDL_OPTIONS = {
            "format": "bestaudio/best", 
            "yesplaylist": "True",
            'force-ipv4': True,
            'cachedir': False,
            'restrictfilenames': True,
            'nocheckcertificate': True,
            'quiet': True,
            'skip_download': True,
            # 'extract_flat': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            }
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        self.vc = ""

    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if not member.id == self.bot.user.id:
            return

        else:
            time = 0
            while True:
                await asyncio.sleep(1)
                if self.is_playing:
                    time = 0
                else:
                    time = time + 1
                    if time == 60:
                        self.current_song = None
                        self.music_queue = []
                        try:
                            if self.vc.is_connected():
                                await self.vc.disconnect()
                                self.vc = ""
                                break
                        except AttributeError:
                            self.vc = ""
                            break
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            ydl.cache.remove()
            link_matches = [ele for ele in ["https://", "http://"] if(ele in item)]
            if link_matches:
                try:
                    info = ydl.extract_info(u"{dataLink}".format(dataLink = item), download=False)
                    return {
                        "source": info["formats"][0]["url"],
                        "title": info["title"],
                        "song_length": info["duration"],
                    }
                except Exception:
                    return False
            else:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)["entries"][0]
        return {
            "source": info["formats"][0]["url"],
            "title": info["title"],
            "song_length": info["duration"],
        }

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            self.current_song = self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )
        else:
            self.is_playing = False
            self.current_song = None

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            await ctx.reply(
                f""":arrow_forward: Playing **{self.music_queue[0][0]['title']}** -- requested by {self.music_queue[0][2]}""", mention_author=False
            )

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(),
            )
            self.current_song = self.music_queue.pop(0)

        else:
            self.is_playing = False
            self.current_song = None

    @commands.command(
        name="p",
        help="Plays a selected song from youtube.",
        aliases=["play"],
    )
    async def p(self, ctx, *args):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        query = " ".join(args)
        try:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await ctx.reply("You're not in same voice with bot, not executing...", mention_author=False)
                    return
            if not ctx.voice_client and self.is_playing == True:
                self.is_playing = False
                self.current_song = None
                self.music_queue = []
                self.vc = ""
                await ctx.reply(
                    "Please re-enter the command, the bot is still on prepare to singing u a nice music :)", mention_author=False
                )
                return

            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.reply(
                    "Could not download the song. Incorrect format try another keyword. (Playlist not Supported Yet.)", mention_author=False
                )
            else:
                await ctx.reply(
                    f""":headphones: **{song["title"]}** has been added to the queue by {ctx.author.mention}""", mention_author=False
                )
                self.music_queue.append([song, voice_channel, ctx.author.mention])
                if self.is_playing == False:
                    await self.play_music(ctx)
        except AttributeError:
            await ctx.reply("Connect to a voice channel!", mention_author=False)

    @commands.command(
        name="cp",
        help="Shows the currently playing song.",
        aliases=["playing"],
    )
    async def cp(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        msg = (
            "No music playing"
            if self.current_song is None
            else f"""Currently Playing: **{self.current_song[0]['title']}** -- added by {self.current_song[2]}\n"""
        )
        await ctx.reply(msg, delete_after=5, mention_author=False)

    @commands.command(
        name="q",
        help="Shows the music added in list/queue.",
        aliases=["queue"],
    )
    async def q(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        retval = ""
        for (i, m) in enumerate(self.music_queue):
            retval += f"""{i+1}. **{m[0]['title']}** -- added by {m[int(2)]}\n"""

        if retval != "":
            await ctx.reply(retval, mention_author=False)
        else:
            await ctx.reply("No music in queue", mention_author=False)

    @commands.command(name="cq", help="Clears the queue.", aliases=["clear"])
    async def cq(self, ctx):
        
        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        self.music_queue = []
        await ctx.reply("""***Queue cleared !***""", delete_after=5, mention_author=False)

    @commands.command(name="shuffle", help="Shuffles the queue.")
    async def shuffle(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        shuffle(self.music_queue)
        await ctx.reply("""***Queue shuffled !***""", delete_after=5, mention_author=False)

    @commands.command(
        name="s", help="Skips the current song being played.", aliases=["skip"]
    )
    async def skip(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        if self.vc != "" and self.vc:
            await ctx.reply("""***Skipped current song !***""", delete_after=5, mention_author=False)
            self.skip_votes = set()
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(
        name="voteskip",
        help="Vote to skip the current song being played.",
        aliases=["vs"],
    )
    async def voteskip(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        if ctx.voice_client is None:
            return
        num_members = len(ctx.voice_client.channel.members) - 1
        self.skip_votes.add(ctx.author.id)
        votes = len(self.skip_votes)
        if votes >= num_members / 2:
            await ctx.reply(f"Vote passed by majority ({votes}/{num_members}).", delete_after=5, mention_author=False)
            await self.skip(ctx)

    @commands.command(
        name="l",
        help="Commands the bot to leave the voice channel.",
        aliases=["leave"],
    )
    async def leave(self, ctx, *args):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        if self.vc.is_connected():
            if self.vc != "" and self.vc:
                self.vc.stop()
            await ctx.reply("""**Bye Bye **:slight_smile:""", mention_author=False)
            self.is_playing = False
            self.current_song = None
            self.music_queue = []
            await self.vc.disconnect(force=True)
            self.vc = ""

    @commands.command(
        name="pn", help="Moves the song to the top of the queue."
    )
    async def playnext(self, ctx, *args):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.reply("Connect to a voice channel", delete_after=5, mention_author=False)
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.reply(
                    "Could not download the song. Incorrect format try another keyword.", delete_after=5, mention_author=False
                )
            else:
                vote_message = await ctx.reply(
                    f":headphones: **{song['title']}** will be added to the top of the queue by {ctx.author.mention}\n"
                    "You have 30 seconds to vote by reacting :+1: on this message.\n"
                    "If more than 50% of the people in your channel agree, the request will be up next!", delete_after=5, mention_author=False
                )
                await vote_message.add_reaction("\U0001F44D")
                await asyncio.sleep(30)
                voters = len(voice_channel.members)
                voters = voters - 1 if self.vc else voters
                result_vote_msg = await ctx.fetch_message(vote_message.id)
                votes = (
                    next(
                        react
                        for react in result_vote_msg.reactions
                        if str(react.emoji) == "\U0001F44D"
                    ).count
                    - 1
                )
                if votes >= voters / 2:
                    self.music_queue.insert(
                        0, [song, voice_channel, ctx.author.mention]
                    )
                    await ctx.reply(
                        f":headphones: **{song['title']}** will be added played next!", delete_after=5, mention_author=False
                    )
                else:
                    self.music_queue.append([song, voice_channel, ctx.author.mention])
                    await ctx.reply(
                        f":headphones: **{song['title']}** will be played add the end of the queue!", delete_after=5, mention_author=False
                    )

                if self.is_playing == False or (
                    self.vc == "" or not self.vc.is_connected() or self.vc == None
                ):
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pause the currently playing song.")
    async def pause(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.reply("I am currently playing nothing!", delete_after=5, mention_author=False)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.reply(f":pause_button:  {ctx.author.mention} Paused the song!", delete_after=5, mention_author=False)

    @commands.command(name="resume", help="Resume the currently playing song.")
    async def resume(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        vc = ctx.voice_client

        if not vc or vc.is_playing():
            return await ctx.reply("I am already playing a song!", delete_after=5, mention_author=False)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.reply(f":play_pause:  {ctx.author.mention} Resumed the song!", delete_after=5, mention_author=False)

    @commands.command(
        name="r",
        help="removes song from queue at index given.",
        aliases=["remove"],
    )
    async def remove(self, ctx, *args):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        if len(args) == 0:
            await ctx.reply("Wrong Parameters. See `!1help`.", delete_after=5, mention_author=False)
            return

        query = "".join(*args)
        index = 0
        negative = True if (query[0] == "-") else False
        if not negative:
            for i in range(len(query)):
                convert = (int)(query[i])
                index = index * 10 + convert
        index -= 1

        if negative:
            await ctx.reply("Index cannot be less than one", delete_after=5, mention_author=False)
        elif index >= len(self.music_queue):
            await ctx.reply("Wrong index. Indexed music not present in the queue", delete_after=5, mention_author=False)
        else:
            await ctx.reply(
                f""":x: Music at index {query} removed by {ctx.author.mention}""", delete_after=5, mention_author=False
            )
            self.music_queue.pop(index)

    @commands.command(
        name="rep",
        help="Restarts the current song.",
        aliases=["restart"],
    )
    async def restart(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        song = []
        if self.current_song != None:
            song = self.current_song[0]
            voice_channel = ctx.author.voice.channel
            self.music_queue.insert(0, [song, voice_channel, ctx.author.mention])
            self.vc.stop()
            if len(self.music_queue) > 0:
                self.is_playing = True

                m_url = self.music_queue[0][0]["source"]

                if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                    self.vc = await self.music_queue[0][1].connect()
                    await ctx.reply("No music added", delete_after=5, mention_author=False)
                else:
                    await self.vc.move_to(self.music_queue[0][1])

                    await ctx.reply(
                        f""":repeat: Replaying **{self.music_queue[0][0]['title']}** -- requested by {self.music_queue[0][2]}""", delete_after=5, mention_author=False
                    )

                    self.vc.play(
                        discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                        after=lambda e: self.play_next(),
                    )
                    self.current_song = self.music_queue.pop(0)

        else:
            self.is_playing = False
            self.current_song = None
            await ctx.reply(f""":x: No music playing""", delete_after=5, mention_author=False)

    @commands.command(
        name="qt",
        help="Calculates and outputs the total length of the songs in the queue.",
        aliases=["queuetime"],
    )
    async def qt(self, ctx):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        remaining_time = 0
        for song in self.music_queue:
            remaining_time += song[0]["song_length"]

        remaining_time_minutes = str(remaining_time // 60)
        remaining_time = str(remaining_time % 60)
        remaining_time = f"{remaining_time_minutes}:{remaining_time}"

        await ctx.reply(f"""The queue has a total of {remaining_time} remaining!""", delete_after=5, mention_author=False)

    @commands.command(
        name="sleep", help="Sets the bot to sleep.", aliases=["timer"]
    )
    async def sleep(self, ctx, *args):

        if ctx.prefix != '!1':
            return

        if checkdata(ctx.guild.id, ctx.author.id) != True:
            await ctx.reply("Fitur music pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel(ctx.guild.id):
            dc = int(defaultchannel(ctx.guild.id))
            print(dc)
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#{dc}>\n\nTerima Kasih Atas Pengertiannya.".format(dc = dc), delete_after=7)
            return

        second = int(0)
        query = list(args)
        if self.is_playing == False:
            return await ctx.reply(f"No music playing", delete_after=5, mention_author=False)

        if len(query) == 0 and self.isTimed:
            self.isTimed = False
            return
        elif len(query) == 2 and not self.isTimed:
            try:
                if query[0] == "m":
                    second = int(query[1]) * 60
                elif query[0] == "h":
                    second = int(query[1]) * 3600
                elif query[0] == "s":
                    second = int(query[1])
                else:
                    await ctx.reply("Invalid time format.", delete_after=5, mention_author=False)
                    return
            except:
                await ctx.reply("Invalid time specified", delete_after=5, mention_author=False)
                return
        elif len(query) == 2 and self.isTimed:
            await ctx.reply("Timer already set. Unset to reset.", delete_after=5, mention_author=False)
            return
        else:
            await ctx.reply("Invalid time format.", delete_after=5, mention_author=False)
            return
        seconds = f"{second}"
        if second < 0:
            await ctx.reply("Time cannot be negative", delete_after=5, mention_author=False)
        else:
            self.isTimed = True
            message = await ctx.reply("Timer set for : " + seconds + " seconds.", delete_after=5, mention_author=False)
            while True and self.isTimed:
                second = second - 1
                if second == 0:
                    await message.edit(new_content=("Ended!"))
                    break
                await message.edit(new_content=("Timer: {0}".format(second)))
                await asyncio.sleep(1)

            if self.isTimed == False:
                await ctx.reply("Timer disabled.", delete_after=5, mention_author=False)
            else:
                await ctx.reply(
                    f""" **{ctx.message.author.mention} Sleep time exceeded! Bye-Bye!** :slight_smile: """, delete_after=5, mention_author=False
                )
                self.isTimed = False
                await self.vc.disconnect(force=True)


def setup(bot):
    bot.add_cog(Music(bot))
