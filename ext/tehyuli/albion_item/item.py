import asyncio
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from ext.db_module import fetch
from ext.tehyuli.albion_item.function import sort_item
from ext.tehyuli.albion_item.function import price
import json
import os
import requests

def checkdata():
    albion_db = fetch.one("config", 'name', 'ALBION')
    albion_data = json.loads(albion_db)
    if albion_data['value'] == 'TRUE':
        return True
    else:
        return False

def checkchannel():
    get_channel = fetch.many("allow_channel", 'name', 'Albion_Item')
    channel_data = json.loads(get_channel)
    list_channel_allow = []
    for i in range(len(channel_data)):
        looping = '{i}'.format(i = i)
        list_channel_allow.append(int(channel_data[looping]['channel_id']))
    return list_channel_allow


def search_components(joinarg, data):
    embedOne = discord.Embed(
        title = "{arg} #1".format(arg=joinarg),
        description = "{item1}\nKecocokan Penelusuran: *{matching1}*\n\n{item2}\nKecocokan Penelusuran: *{matching2}*\n\n{item3}\nKecocokan Penelusuran: *{matching3}*".format(item1 = data[0][0], matching1 = round(data[0][1], 2), item2 = data[1][0], matching2 = round(data[1][1], 2), item3 = data[2][0], matching3 = round(data[2][1], 2) )
    )
    embedTwo = discord.Embed(
        title = "{arg} #2".format(arg=joinarg),
        description = "{item4}\nKecocokan Penelusuran: *{matching4}*\n\n{item5}\nKecocokan Penelusuran: *{matching5}*\n\n{item6}\nKecocokan Penelusuran: *{matching6}*".format(item4 = data[3][0], matching4 = round(data[3][1], 2), item5 = data[4][0], matching5 = round(data[4][1], 2), item6 = data[5][0], matching6 = round(data[5][1], 2) )
    )
    embedThree = discord.Embed(
        title = "{arg} #3".format(arg=joinarg),
        description = "{item7}\nKecocokan Penelusuran: *{matching7}*\n\n{item8}\nKecocokan Penelusuran: *{matching8}*\n\n{item9}\nKecocokan Penelusuran: *{matching9}\n\n{item10}\nKecocokan Penelusuran: *{matching10}*".format(item7 = data[6][0], matching7 = round(data[6][1], 2), item8 = data[7][0], matching8 = round(data[7][1], 2), item9 = data[8][0], matching9 = round(data[8][1], 2), item10 = data[9][0], matching10 = round(data[9][1], 2) )
    )

    return [embedOne, embedTwo, embedThree]

def button_components(paginationList, current):
    return [
        [
            Button(
                label = "Prev",
                id = "back",
                style = ButtonStyle.red
            ),
            Button(
                label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                id = "cur",
                style = ButtonStyle.grey,
                disabled = True
            ),
            Button(
                label = "Next",
                id = "front",
                style = ButtonStyle.red
            )
        ]
    ]

def reply_item(return_var, quality):
    data_api = sort_item.getrawfromAPI(return_var)
    embed = discord.Embed(
        title = data_api['name'],
        description = data_api['desc'],
        colour = discord.Colour.red()
    )
    
    dataPrice = price.priceCheck(return_var, quality)
    embed.set_footer(text="Bot Created by `Anti Bang Cat Guild`")
    embed.set_image(url='https://render.albiononline.com/v1/item/{item}?quality={qual}'.format(item = return_var, qual = quality))
    embed.set_thumbnail(url='https://render.albiononline.com/v1/item/{item}?quality={qual}'.format(item = return_var, qual = quality))
    embed.set_author(name="Item Searcher & Price Checker",
    icon_url='https://cdn.discordapp.com/avatars/925155040245710919/74f019575f3ec92dd35c5d371c11da61.webp?size=80')
    for i in range(len(dataPrice)):
        details = ""
        if dataPrice[i]['sell']['min'] != 0:
            data = "**S**ell-Min: {sellmin}\n".format(sellmin = dataPrice[i]['sell']['min'])
            details += str(data)
        if dataPrice[i]['sell']['max'] != 0:
            data = "**S**ell-Max: {sellmax}\n".format(sellmax = dataPrice[i]['sell']['max'])
            details += str(data)
        if dataPrice[i]['buy']['min'] != 0:
            data = "**B**uy-Min: {buymin}\n".format(buymin = dataPrice[i]['buy']['min'])
            details += str(data)
        if dataPrice[i]['buy']['max'] != 0:
            data = "**B**uy-Max: {buymax}\n".format(buymax = dataPrice[i]['buy']['max'])
            details += str(data)
        embed.add_field(name="*{city}".format(city = dataPrice[i]['city']), value=details, inline=True)
    return embed

def remove_containdata(data, lists):
    res = [ele for ele in lists if(ele in data)]
    res = ''.join(res)
    res = "{}".format(res)
    return res

class item(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def se(self, ctx, *, arg):

        if checkdata() != True:
            await ctx.reply("Fitur albion pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel():
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#804656940436160512>\n\nTerima Kasih Atas Pengertiannya.", delete_after=7)
            return

        data = sort_item.SearchEngine(arg)
        paginationList = search_components(arg, data)
        current = 0
        mainMessage = await ctx.reply(
            "**Hasil Pencarian (10 Hasil dengan Kecocokan Tinggi)**",
            embed = paginationList[current],
            components = button_components(paginationList, current)
        )
        while True:
            try:
                interaction = await self.client.wait_for(
                    "button_click",
                    check = lambda i:i.component.id in ["back", "front"],
                    timeout = 60.0
                )
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                if current == len(paginationList):
                    current = 0
                elif current < 0:
                    current = len(paginationList) - 1

                await interaction.respond(
                    type = 7,
                    embed = paginationList[current],
                    components = button_components(paginationList, current)
                )
            except asyncio.TimeoutError:
                await mainMessage.edit(
                    components = button_components(paginationList, current)
                )
                break
            except:
                break

        
    @commands.command()
    async def search(self, ctx, *arg):

        if checkdata() != True:
            await ctx.reply("Fitur albion pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        if ctx.channel.id not in checkchannel():
            await ctx.reply("Untuk menghindari spam, Tolong pergunakan bot ini hanya di text channel <#804656940436160512>\n\nTerima Kasih Atas Pengertiannya.", delete_after=7)
            return

        if len(arg) >= 2:
            albion_db = fetch.one("alias", 'name', arg[1])
            if albion_db:
                print(albion_db)

            else:
                if arg[0] in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']:
                    item_unique_search = arg[0] + "_" + arg[1]
                    return_var = sort_item.SearchUniqueName(item_unique_search)
                    if return_var == False:
                        joinarg = ' '.join(arg)
                        data = sort_item.SearchEngine(joinarg)
                        paginationList = search_components(joinarg, data)
                        current = 0
                        mainMessage = await ctx.reply(
                            "Data tidak ditemukan, Berikut adalah data yang menyerupai dengan yg anda cari\n**Hasil Pencarian (10 Hasil dengan Kecocokan Tinggi)**",
                            embed = paginationList[current],
                            components = button_components(paginationList, current)
                        )
                        while True:
                            try:
                                interaction = await self.client.wait_for(
                                    "button_click",
                                    check = lambda i:i.component.id in ["back", "front"],
                                    timeout = 60.0
                                )
                                if interaction.component.id == "back":
                                    current -= 1
                                elif interaction.component.id == "front":
                                    current += 1
                                if current == len(paginationList):
                                    current = 0
                                elif current < 0:
                                    current = len(paginationList) - 1

                                await interaction.respond(
                                    type = 7,
                                    embed = paginationList[current],
                                    components = button_components(paginationList, current)
                                )
                            except asyncio.TimeoutError:
                                await mainMessage.edit(
                                    components = button_components(paginationList, current)
                                )
                                break
                            except:
                                break
                    else:
                        async def callbacknormal(interaction):
                            embed = reply_item(return_var, 1)
                            await interaction.respond(
                                type=7,
                                embed=embed
                            )
                        async def callbackgood(interaction):
                            embed = reply_item(return_var, 2)
                            await interaction.respond(
                                type=7,
                                embed=embed
                            )
                        async def callbackoutstanding(interaction):
                            embed = reply_item(return_var, 3)
                            await interaction.respond(
                                type=7,
                                embed=embed
                            )
                        async def callbackexcellent(interaction):
                            embed = reply_item(return_var, 4)
                            await interaction.respond(
                                type=7,
                                embed=embed
                            )
                        async def callbackmasterpiece(interaction):
                            embed = reply_item(return_var, 5)
                            await interaction.respond(
                                type=7,
                                embed=embed
                            )
                        # async def callbackallqual(interaction):
                        #     embed = reply_item(return_var)
                        #     await interaction.send(embed=embed)

                        components = [[
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="Normal", custom_id="normal"), callbacknormal
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="Good", custom_id="good"), callbackgood
                            )]
                            ,[
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.green, label="Outstanding", custom_id="outstanding"), callbackoutstanding
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.blue, label="Excellent", custom_id="excellent"), callbackexcellent
                            )],
                            [
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.red, label="Masterpiece", custom_id="masterpiece"), callbackmasterpiece
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="All Quality", custom_id="allqual"), callbackmasterpiece
                            )]
                        ]

                        await ctx.send(
                            "Pilih Kualitas:",
                            components=components,
                        )
                        
                else:
                    item_unique_search = arg[0] + "_" + arg[1]
                    return_var = sort_item.SearchUniqueName(item_unique_search)
                    if return_var == False:
                        joinarg = ' '.join(arg)
                        data = sort_item.SearchEngine(joinarg)
                        paginationList = search_components(joinarg, data)

                        current = 0
                        mainMessage = await ctx.reply(
                            "Data tidak ditemukan, Berikut adalah data yang menyerupai dengan yg anda cari\n**Hasil Pencarian (10 Hasil dengan Kecocokan Tinggi)**",
                            embed = paginationList[current],
                            components = button_components(paginationList, current)

                        )
                        while True:
                            try:
                                interaction = await self.client.wait_for(
                                    "button_click",
                                    check = lambda i:i.component.id in ["back", "front"],
                                    timeout = 60.0
                                )
                                if interaction.component.id == "back":
                                    current -= 1
                                elif interaction.component.id == "front":
                                    current += 1
                                if current == len(paginationList):
                                    current = 0
                                elif current < 0:
                                    current = len(paginationList) - 1

                                await interaction.respond(
                                    type = 7,
                                    embed = paginationList[current],
                                    components = button_components(paginationList, current)

                                )
                            except asyncio.TimeoutError:
                                await mainMessage.edit(
                                    components = button_components(paginationList, current)

                                )
                                break
                            except:
                                break

                    else:
                        async def callbacknormal(interaction):
                            embed = reply_item(return_var, 1)
                            await interaction.send(embed=embed)
                        async def callbackgood(interaction):
                            embed = reply_item(return_var, 2)
                            await interaction.send(embed=embed)
                        async def callbackoutstanding(interaction):
                            embed = reply_item(return_var, 3)
                            await interaction.send(embed=embed)
                        async def callbackexcellent(interaction):
                            embed = reply_item(return_var, 4)
                            await interaction.send(embed=embed)
                        async def callbackmasterpiece(interaction):
                            embed = reply_item(return_var, 5)
                            await interaction.send(embed=embed)
                        # async def callbackallqual(interaction):
                        #     embed = reply_item(return_var)
                        #     await interaction.send(embed=embed)

                        components = [[
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="Normal", custom_id="normal"), callbacknormal
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="Good", custom_id="good"), callbackgood
                            )]
                            ,[
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.green, label="Outstanding", custom_id="outstanding"), callbackoutstanding
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.blue, label="Excellent", custom_id="excellent"), callbackexcellent
                            )],
                            [
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.red, label="Masterpiece", custom_id="masterpiece"), callbackmasterpiece
                            ),
                            self.client.components_manager.add_callback(
                                Button(style=ButtonStyle.gray, label="All Quality", custom_id="allqual"), callbackmasterpiece
                            )]
                        ]

                        await ctx.send(
                            "Pilih Kualitas:",
                            components=components,
                        )

        elif len(arg) == 1:
            return_var = sort_item.SearchUniqueName(arg[0])
            if return_var == False:
                data = sort_item.SearchEngine(arg[0])
                paginationList = search_components(arg[0], data)
                current = 0
                mainMessage = await ctx.reply(
                    "Data tidak ditemukan, Berikut adalah data yang menyerupai dengan yg anda cari\n**Hasil Pencarian (10 Hasil dengan Kecocokan Tinggi)**",
                    embed = paginationList[current],
                    components = button_components(paginationList, current)
                )
                while True:
                    try:
                        interaction = await self.client.wait_for(
                            "button_click",
                            check = lambda i:i.component.id in ["back", "front"],
                            timeout = 60.0
                        )
                        if interaction.component.id == "back":
                            current -= 1
                        elif interaction.component.id == "front":
                            current += 1
                        if current == len(paginationList):
                            current = 0
                        elif current < 0:
                            current = len(paginationList) - 1

                        await interaction.respond(
                            type = 7,
                            embed = paginationList[current],
                            components = button_components(paginationList, current)
                        )
                    except asyncio.TimeoutError:
                        await mainMessage.edit(
                            components = button_components(paginationList, current)
                        )
                        break
                    except:
                        break
            else:
                async def callbacknormal(interaction):
                    embed = reply_item(return_var, 1)
                    await interaction.respond(
                        type=7,
                        embed=embed
                    )
                async def callbackgood(interaction):
                    embed = reply_item(return_var, 2)
                    await interaction.respond(
                        type=7,
                        embed=embed
                    )
                async def callbackoutstanding(interaction):
                    embed = reply_item(return_var, 3)
                    await interaction.respond(
                        type=7,
                        embed=embed
                    )
                async def callbackexcellent(interaction):
                    embed = reply_item(return_var, 4)
                    await interaction.respond(
                        type=7,
                        embed=embed
                    )
                async def callbackmasterpiece(interaction):
                    embed = reply_item(return_var, 5)
                    await interaction.respond(
                        type=7,
                        embed=embed
                    )
                # async def callbackallqual(interaction):
                #     embed = reply_item(return_var)
                #     await interaction.send(embed=embed)

                components = [[
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.gray, label="Normal", custom_id="normal"), callbacknormal
                    ),
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.gray, label="Good", custom_id="good"), callbackgood
                    )]
                    ,[
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.green, label="Outstanding", custom_id="outstanding"), callbackoutstanding
                    ),
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.blue, label="Excellent", custom_id="excellent"), callbackexcellent
                    )],
                    [
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.red, label="Masterpiece", custom_id="masterpiece"), callbackmasterpiece
                    ),
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.gray, label="All Quality", custom_id="allqual"), callbackmasterpiece
                    )]
                ]

                await ctx.send(
                    "Pilih Kualitas:",
                    components=components,
                )

        else:
            await ctx.reply("Parameter input salah, `?/albion_help` untuk check perintah dan parameternya")



def setup(client):
    client.add_cog(item(client))