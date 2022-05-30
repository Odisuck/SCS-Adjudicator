import asyncio
from collections import *
from distutils.log import error
from discord.ext import commands
import discord, pickle, string
from discord_ui import UI, Components, Button, SelectMenu, SelectOption
import random, time, json, os, datetime

DISCORD_TOKEN = ('OTc0MTg4MTI2OTMzMjIxNDI3.Gdtz01.U9DBN77j2-HcXc3_mIzz7mgc71vAlrAg9RVLfE')

client = commands.Bot(command_prefix='#')

quo_list = ['Know thy self, know thy enemy. A thousand battles, a thousand victories.', 'Invincibility lies in the defence; the possibility of victory in the attack.', 'Pretend inferiority and encourage his arrogance.', 'Know your enemy and know yourself and you can fight a hundred battles without disaster.', 'He will win who knows how to handle both superior and inferior forces.', 'Everything has beauty, but not everyone sees it.', 'They must often change who would be constant in happiness or wisdom.', 'What the superior man seeks is in himself; what the small man seeks is in others.']

ui = UI(client)

neg_words = {''}
pos_words = {''}


def positive_serial():
    pass 

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    await client.change_presence(activity=discord.Game(name="#helpme command"))
    print('online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global file_name
    file_name = f'scs_stat/{message.author.id}.json'

    pos_count = 0
    neg_count = 0
            
    neg_suggest = {}
    pos_suggest = {}

    msg_trans = message.content.translate(str.maketrans('', '', string.punctuation))
    message_list = msg_trans.lower().split()

    global expo_count
    
    print(message_list)

    for i in message_list:
        if i in neg_words:
            neg_count += 1
        else:
            pass

    for i in message_list:
        if i in pos_words:
            pos_count += 1
        else:
            pass

    if neg_count > pos_count:
        count = neg_count - pos_count
        expo_count = round(float(1.9) * pow(count, 2))
        negative_serial()
        embed=discord.Embed(title=(f"总廷王 dissaproves of your -{expo_count} credit score"), description=str(random.choice(quo_list)), color=0xff6060)
        embed.set_footer(text=(f'your SCS: {current_scs()}'), icon_url=message.author.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await message.channel.send(embed=embed)

    elif neg_count == pos_count:
        pass

    else:
        count = int(pos_count - neg_count)
        expo_count = round(5 * count * float(1.25))
        positive_serial()
        embed=discord.Embed(title=(f"总廷王 approves of your +{expo_count} credit score"), description=str(random.choice(quo_list)), color=0x99ff93)
        embed.set_footer(text=(f'your SCS: +{current_scs()}'), icon_url=message.author.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await message.channel.send(embed=embed)

    #leaderboard 'command'
    if message.content.startswith('leaderboard'):

        user_list = os.listdir('scs_stat/')
        leader_list_raw = []
        leader_list = []

        position = 1

        for i in user_list:
            if i != '.DS_Store':
                json_file = open('scs_stat/'+i)
                dict = json.load(json_file)
                json_file.close()

                score = dict["score"]
                global file_user_name
                file_user_name = i.replace(".json", "")
                print(file_user_name)
                
                tuple = (await client.fetch_user(file_user_name), score)
                leader_list_raw.append(tuple)

        def sort_score(score):
            return score[1]

        leader_list_raw.sort(key=sort_score, reverse=True)

        for i in leader_list_raw:
            leader_list.append((str(position)+'.',)+i)
            position += 1

        leader_list='\n'.join([str(i) for i in leader_list])

        remove_char = "()[]'"

        for char in remove_char:
            leader_list = leader_list.replace(char, "")
            leader_list = leader_list.replace(',', " |")

        embed=discord.Embed(title=(f'{leader_list}'), color=0x6735fc)
        embed.set_footer(text='requested this', icon_url=message.author.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await message.channel.send(embed=embed)

    #suggest 'command'
    if message.content.startswith('gest'):

        msg_trans = message.content.translate(str.maketrans('', '', string.punctuation))
        message_list = msg_trans.lower().split()
        message_form = len(message_list)

        if message_form == 2:

            global s_word
            s_word = message_list[1]
            
            if s_word != 'gest':

                btn = await (
                await message.channel.send(f'My 同志, You would like to add `{s_word}` to the social dictionary?', components=[
                Button("Confirm", color="green", custom_id="confirm_posword", emoji="✅", disabled=False),
                Button("Cancel", color="grey",  custom_id="decline_posword", emoji="🚫", disabled=False, new_line=False)])
                ).wait_for("button", client, timeout=10)

                await btn.message.disable_components()
                await btn.respond()

                

                if btn.custom_id == "confirm_posword":
                    btn = await (
                    await message.channel.send(f'My 同志, `{s_word}` is a positive or negatively socially impactable word?', components=[
                    Button("(+)Positive", color="blurple", custom_id="pos", disabled=False),
                    Button("(-)Negative", color="blurple",  custom_id="neg", disabled=False, new_line=False)])
                    ).wait_for("button", client, timeout=10)

                    await btn.message.disable_components()
                    await btn.respond()

                    if btn.custom_id == "pos":
                        pos_words.add(s_word)
                        print(pos_words)

                    else:
                        neg_words.add(s_word)
                        print(neg_words)
                    
                else:
                    await message.channel.send('没事, you can suggest another time. But i do not like wasting 时间.')
                    lose_rand = random.randrange(50, 100)
                    embed=discord.Embed(title=(f"总廷王 dissaproves of your -{lose_rand} credit score"), description=str(random.choice(quo_list)), color=0xff6060)
                    await message.channel.send(embed=embed)
        
            else:
                await message.channel.send('不会 waste, my 时间.')
                lose_rand = random.randrange(50, 100)
                embed=discord.Embed(title=(f"总廷王 dissaproves of your -{lose_rand} credit score"), description=str(random.choice(quo_list)), color=0xff6060)
                await message.channel.send(embed=embed)

        else:

            await message.channel.send('input format is not valid, please do `gest <word>`')

    else:
        pass


    await client.process_commands(message)

def negative_serial():
    if os.path.isfile(file_name):
        print('found file')

        json_file = open(file_name)
        dict = json.load(json_file)
        json_file.close()

        pre_score = dict["score"]
        new_score = int(pre_score) - int(expo_count)

        def_dict = {'score': new_score}

        with open(file_name, "w", encoding='utf8') as f:
            json.dump(def_dict, f)

    else:
        def_dict = {'score': -abs(expo_count)}

        with open(file_name, "w", encoding='utf8') as f:
            json.dump(def_dict, f)
    
def positive_serial():
    if os.path.isfile(file_name):
        print('found file')

        json_file = open(file_name)
        dict = json.load(json_file)
        json_file.close()

        pre_score = dict["score"]
        new_score = int(pre_score) + int(expo_count)

        def_dict = {'score': new_score}

        with open(file_name, "w", encoding='utf8') as f:
            json.dump(def_dict, f)

    else:
        print('file not found')
        def_dict = {'score': expo_count}

        with open(file_name, "w", encoding='utf8') as f:
            json.dump(def_dict, f)

def current_scs():
    json_file = open(file_name)
    dict = json.load(json_file)
    json_file.close()

    score = dict["score"]
    return score

def leaderboard():
    user_list = os.listdir('scs_stat/')
    leader_list_raw = []
    leader_list = []

    position = 1

    for i in user_list:
        if i != '.DS_Store':
            json_file = open('scs_stat/'+i)
            dict = json.load(json_file)
            json_file.close()

            score = dict["score"]
            global file_user_name
            file_user_name = i.replace(".json", "")
            print(file_user_name)
            
            tuple = (file_user_name, score)
            leader_list_raw.append(tuple)

    def sort_score(score):
        return score[1]

    leader_list_raw.sort(key=sort_score, reverse=True)

    for i in leader_list_raw:
        leader_list.append((str(position)+'.',)+i)
        position += 1

    leader_list='\n'.join([str(i) for i in leader_list])

    remove_char = "()[]'"

    for char in remove_char:
        leader_list = leader_list.replace(char, "")
        leader_list = leader_list.replace(',', " |")

    return leader_list

def add_pos():
    pass


@client.listen('on_button')
async def on_button(btn):
    pass

client.run(DISCORD_TOKEN)
