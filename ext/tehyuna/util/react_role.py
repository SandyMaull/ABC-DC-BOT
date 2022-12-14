import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv


class RRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(802955327142101032)
        register = 830755947223318528
        await channel.send(f'Selamat Datang di Anti Bang Cat {member.mention}!\nMohon register IGN untuk memperluas akses di <#{register}>')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        ava = 973681518029439027
        hcerole = 973681542704537610
        hcelevel = 973681575143305307
        meatshield = 973681604490821682
        caerleonflag = 1014537328833863721
        if payload.message_id == ava:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '⚔️':
                role = discord.utils.get(guild.roles, id=973644426729627719)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            else:
                return
        elif payload.message_id == hcerole:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🟡':
                role = discord.utils.get(guild.roles, id=895141110433845280)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            elif payload.emoji.name == '💚':
                role = discord.utils.get(guild.roles, id=895141421315682405)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            elif payload.emoji.name == '🟦':
                role = discord.utils.get(guild.roles, id=895141549095153695)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            elif payload.emoji.name == '🔴':
                role = discord.utils.get(guild.roles, id=895141631932641363)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            else:
                return
        elif payload.message_id == hcelevel:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🟢':
                role = discord.utils.get(guild.roles, id=895153511858315265)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            elif payload.emoji.name == '🟡':
                role = discord.utils.get(guild.roles, id=895153519122849823)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            elif payload.emoji.name == '🔴':
                role = discord.utils.get(guild.roles, id=895154329680478281)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            else:
                return
        elif payload.message_id == meatshield:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🍖':
                role = discord.utils.get(guild.roles, id=830652030108041236)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            else:
                return
        elif payload.message_id == caerleonflag:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            emoji = get(guild.emojis, name="caerleon_flag")
            if payload.emoji == emoji:
                role = discord.utils.get(guild.roles, id=1014366445091692554)
                if role not in member.roles:
                    await payload.member.add_roles(role)
                    return
            else:
                return
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        ava = 973681518029439027
        hcerole = 973681542704537610
        hcelevel = 973681575143305307
        meatshield = 973681604490821682
        caerleonflag = 1014537328833863721
        if payload.message_id == ava:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '⚔️':
                role = discord.utils.get(guild.roles, id=973644426729627719)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            else:
                return
        elif payload.message_id == hcerole:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🟡':
                role = discord.utils.get(guild.roles, id=895141110433845280)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            elif payload.emoji.name == '💚':
                role = discord.utils.get(guild.roles, id=895141421315682405)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            elif payload.emoji.name == '🟦':
                role = discord.utils.get(guild.roles, id=895141549095153695)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            elif payload.emoji.name == '🔴':
                role = discord.utils.get(guild.roles, id=895141631932641363)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            else:
                return
        elif payload.message_id == hcelevel:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🟢':
                role = discord.utils.get(guild.roles, id=895153511858315265)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            elif payload.emoji.name == '🟡':
                role = discord.utils.get(guild.roles, id=895153519122849823)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            elif payload.emoji.name == '🔴':
                role = discord.utils.get(guild.roles, id=895154329680478281)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            else:
                return
        elif payload.message_id == meatshield:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.emoji.name == '🍖':
                role = discord.utils.get(guild.roles, id=830652030108041236)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            else:
                return
        elif payload.message_id == caerleonflag:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            emoji = get(guild.emojis, name="caerleon_flag")
            if payload.emoji == emoji:
                role = discord.utils.get(guild.roles, id=1014366445091692554)
                if role in member.roles:
                    await member.remove_roles(role)
                    return
            else:
                return
        else:
            return


def setup(client):
    client.add_cog(RRole(client))