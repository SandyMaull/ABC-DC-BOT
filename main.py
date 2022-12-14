import os
from dotenv import load_dotenv
import discord
import asyncio
from tehyuna import TehYuna
# from tehyuli import TehYuli
from tehyuyun import TehYuyun
from kangpimpin import KangPimpin
from discord_components import DiscordComponents
from discord.utils import get

load_dotenv()


def main():
    kangpimpin = KangPimpin()
    tehyuna = TehYuna()
    # tehyuli = TehYuli()
    tehyuyun = TehYuyun()

    @kangpimpin.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(kangpimpin))
        await kangpimpin.change_presence(activity=discord.Game("Guild Management"))
        DiscordComponents(kangpimpin)

    @tehyuna.event
    async def on_ready():
        print("We have logged in as {0.user}".format(tehyuna))
        await tehyuna.change_presence(activity=discord.Game("Receptionist"))


        # channel = tehyuna.get_channel(924643614406090804)

        # -------- INITIAL SETUP FOR ROLES-REACT MESSAGE --------


        # embedava = discord.Embed(
		# 	title='AVA-RAID',
		# 	description='React emote :caerleon_flag: di bawah ini untuk mendapatkan role Ava-Raid.',
		# 	colour=discord.Colour.dark_red()
        # )
        # avaraid = await channel.send(embed=embedava)
        # await avaraid.add_reaction('⚔️')
        # await asyncio.sleep(5)

        # embedhce = discord.Embed(
		# 	title='HCE-ROLE',
		# 	description='React emote di bawah ini untuk mendapatkan role HCE.\n:yellow_circle: : @Tank\n:green_heart: : @Healer\n:blue_square: : @Support\n:red_circle: : @Dps',
		# 	colour=discord.Colour.dark_blue()
        # )
        # hcerole = await channel.send(embed = embedhce)
        # emojis1 = ['🟡', '💚', '🟦', '🔴']
        # for emoji in emojis1:
        #     await hcerole.add_reaction(emoji)
        # await asyncio.sleep(5)

        # embedhcelevel = discord.Embed(
		# 	title='HCE-LEVEL',
		# 	description='React emote di bawah ini untuk mendapatkan akses channel cari party HCE.\n:green_circle: : HCE under 10\n:yellow_circle: : HCE 11-14\n:red_circle: : HCE 15-18',
		# 	colour=discord.Colour.orange()
        # )
        # hcelevelrole = await channel.send(embed = embedhcelevel)
        # emojis2 = ['🟢', '🟡', '🔴']
        # for emoji in emojis2:
        #     await hcelevelrole.add_reaction(emoji)
        # await asyncio.sleep(5)

        # embedmeat = discord.Embed(
		# 	title='MEAT-SHIELD',
		# 	description='React emote 🍖 dibawah ini apabila kamu termasuk orang-orang yang siap ditumbalkan ataupun siap menghadapi fck up moment ketika sedang konten apapun.',
		# 	colour=discord.Colour.dark_grey()
        # )
        # meatshield = await channel.send(embed=embedmeat)
        # await meatshield.add_reaction('🍖')

        # emoji = get(channel.guild.emojis, name="caerleon_flag")
        # embed_caerleon_flag = discord.Embed(
		# 	title='CAERLEON-RIFFRAFF',
		# 	description=f'React emote {emoji} dibawah ini agar bisa di notif ketika kami akan capping flag caerleon.',
		# 	colour=discord.Colour.dark_red()
        # )
        # # for Editing message Embed
        # msg = 1014508626012020838
        # caerleon_flag = await channel.send(embed = embed_caerleon_flag)
        # emojis1 = [emoji]
        # for emoji in emojis1:
        #     await caerleon_flag.add_reaction(emoji)
        # await asyncio.sleep(5)


        # ---------------------------------------------------

    # @tehyuna.event
    # async def on_member_join(member):
    #     channel = alfred.get_channel(790274325533378682)
    #     embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    #     await channel.send(embed=embed)

    # @tehyuli.event
    # async def on_ready():
    #     print("We have logged in as {0.user}".format(tehyuli))
    #     await tehyuli.change_presence(activity=discord.Game("Price Checker"))
    #     DiscordComponents(tehyuli)

    @tehyuyun.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(tehyuyun))
        await tehyuyun.change_presence(activity=discord.Game("Watching Rules"))
        DiscordComponents(tehyuyun)

    loop = asyncio.get_event_loop()
    loop.create_task(kangpimpin.start(os.getenv("KP_TOKEN")))
    loop.create_task(tehyuna.start(os.getenv("TYA_TOKEN")))
    # loop.create_task(tehyuli.start(os.getenv("TYI_TOKEN")))
    loop.create_task(tehyuyun.start(os.getenv("TYY_TOKEN")))
    loop.run_forever()


if __name__ == "__main__":
    main()
