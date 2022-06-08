import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
from better_profanity import profanity
import json
import re

load_dotenv()
profanity.load_censor_words_from_file("./ext/tehyuyun/badword.txt")

def ImageFilter(content):
    if os.getenv('I_FILTER') == 'PicPurify':
        dataObject = {"url_image":"{link}".format(link = content.url), "API_KEY":"{token}".format(token = os.getenv('I_PP_TOKEN')), "task":"porn_moderation,suggestive_nudity_moderation", "origin_id":"{id}".format(id = content.id), "reference_id":"{name}".format(name = content.filename)}
        result_url = requests.post(os.getenv('I_PP_URL'), data = dataObject)
        result_url = json.loads(result_url.content)
        if result_url["final_decision"] == 'KO':
            return True
    
    elif os.getenv('I_FILTER') == 'SightEngine':
        params = {
            'url': "{link}".format(link = content.url),
            'models': 'nudity',
            'api_user': '{se_user}'.format(se_user = os.getenv('I_SE_USER')),
            'api_secret': '{se_token}'.format(se_token = os.getenv('I_SE_TOKEN'))
        }
        r = requests.get(os.getenv('I_SE_URL'), params=params)
        output = json.loads(r.text)
        if output['nudity']['raw'] > 0.35 or output['nudity']['partial'] > 0.35:
            return True
    return False

def ScamFilter(*arg):
    arg_word = arg[0]
    keywords = ["GIFT", "GET", "GAME", "GAMES", "GIFTS", "NITRO", "CATCH", "FOR", "FREE", "BOOST", "@EVERYONE", "@HERE"]
    keywords_met = 0
    for word in arg_word:
        link_matches = [ele for ele in ["https://", "http://"] if(ele in word)]
        if link_matches:
            dataLink = requests.get('https://raw.githubusercontent.com/nikolaischunk/discord-phishing-links/main/domain-list.json')
            dataLinkResponse = dataLink.json()['domains']
            split_word = re.split(',|/|://', word)
            link_scam = [ele for ele in dataLinkResponse if(ele == split_word[1])]
            if link_scam:
                return len(arg_word)
            else:
                with open('ext/tehyuyun/custom_url.txt') as f:
                    contents = f.read()
                    if(split_word[1] in contents):
                        return len(arg_word)

        if word.upper() in keywords:
            keywords_met += 1

        # Ban Hollywiz from tag everyone 
        if word.upper() in ["@EVERYONE", "@HERE"] and arg[1] == 965897162175152188:
            return len(arg_word)

    halfTotal = (len(arg_word) / 2) if (len(arg_word) >= 3) else (len(arg_word) + 10)
    if keywords_met >= round(halfTotal):
        keywords_met += 1
    if keywords_met >= 4:
        return keywords_met

    return False

class rules(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            content = message.content.split()
            keywords_met = ScamFilter(content, int(message.author.id))
            if keywords_met:
                hit_score = (keywords_met / len(content)) * 100
                await message.delete()
                await message.channel.send("Hai {author},\nPesan anda telah dihapus...\nPesan yg anda kirimkan melanggar rules/norma setempat\n\npelanggaran: scam message\nhit score: {hitscore}%\ndetected by: Similarity scammer words.".format(author = message.author.mention, hitscore = round(hit_score)))
                return

            if message.attachments:
                for x in message.attachments:
                    if x.content_type.startswith("image"):
                        if ImageFilter(x):
                            await message.delete()
                            await message.channel.send("Hai {author},\nPesan anda telah dihapus...\nGambar yg anda kirimkan melanggar rules/norma setempat\npelanggaran: raw nudes/partially".format(author = message.author.mention))
                return

            if profanity.contains_profanity(message.content):
                contentfix = []
                for word in content:
                    link_matches = [ele for ele in ["https://", "http://"] if(ele in word)]
                    if link_matches:
                        contentfix.append(word)
                    else:
                        if profanity.contains_profanity(word):
                            censored_text = profanity.censor(word, '#')
                            contentfix.append(censored_text)
                        else:
                            contentfix.append(word)
                hook = await message.channel.create_webhook(name="profanity_hook")
                await message.delete()
                await hook.send(
                    ' '.join(contentfix),
                    username=message.author.display_name + " | (Profanity Filter)",
                    avatar_url=message.author.avatar_url,
                    wait=True,
                )
                await hook.delete()
                return


def setup(client):
    client.add_cog(rules(client))