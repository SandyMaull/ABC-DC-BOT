import os
from dotenv import load_dotenv
import discord
import asyncio
from tehyuna import TehYuna
from tehyuli import TehYuli
from kangpimpin import KangPimpin
from discord_components import DiscordComponents

load_dotenv()


def main():
    tehyuna = TehYuna()
    tehyuli = TehYuli()
    kangpimpin = KangPimpin()

    @kangpimpin.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(kangpimpin))
        await kangpimpin.change_presence(activity=discord.Game("Guild Management"))
        DiscordComponents(kangpimpin)

    @tehyuna.event
    async def on_ready():
        print("We have logged in as {0.user}".format(tehyuna))
        await tehyuna.change_presence(activity=discord.Game("Receptionist"))

    # @tehyuna.event
    # async def on_member_join(member):
    #     channel = alfred.get_channel(790274325533378682)
    #     embed=discord.Embed(title="Welcome!",description=f"{member.mention} Just Joined")
    #     await channel.send(embed=embed)

    @tehyuli.event
    async def on_ready():
        print("We have logged in as {0.user}".format(tehyuli))
        await tehyuli.change_presence(activity=discord.Game("Price Checker"))
        DiscordComponents(tehyuli)

    @tehyuli.event
    async def on_message(message):
        if message.author == tehyuli.user:
            return
        msg = message.content
        await tehyuli.process_commands(message)

    loop = asyncio.get_event_loop()
    loop.create_task(kangpimpin.start(os.getenv("KP_TOKEN")))
    loop.create_task(tehyuna.start(os.getenv("TYA_TOKEN")))
    loop.create_task(tehyuli.start(os.getenv("TYI_TOKEN")))
    loop.run_forever()


if __name__ == "__main__":
    main()
