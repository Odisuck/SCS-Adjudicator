import asyncio
from collections import *
from click import edit
from discord.ext import commands
import discord, pickle, string
from discord_ui import UI, Components, Button, SelectMenu, SelectOption
import random, time

DISCORD_TOKEN = ('OTc0MTg4MTI2OTMzMjIxNDI3.Gdtz01.U9DBN77j2-HcXc3_mIzz7mgc71vAlrAg9RVLfE')

client = commands.Bot(command_prefix='#')

quo_list = ['Know thy self, know thy enemy. A thousand battles, a thousand victories.', 'Invincibility lies in the defence; the possibility of victory in the attack.', 'Pretend inferiority and encourage his arrogance.', 'Know your enemy and know yourself and you can fight a hundred battles without disaster.', 'He will win who knows how to handle both superior and inferior forces.', 'Everything has beauty, but not everyone sees it.', 'They must often change who would be constant in happiness or wisdom.', 'What the superior man seeks is in himself; what the small man seeks is in others.']

ui = UI(client)

neg_words = {'trash', 'kys', 'tiananmen', '1989', '195394141524328448'}
pos_words = {'social', 'comrade', 'racism', 'mao', 'communism', 'love china'}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    await client.change_presence(activity=discord.Game(name="#helpme command"))
    print('online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global neg_words
    global pos_words

    pos_count = 0
    neg_count = 0
            
    neg_suggest = {}
    pos_suggest = {}

    msg_trans = message.content.translate(str.maketrans('', '', string.punctuation))
    message_list = msg_trans.lower().split()
    
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
        if neg_count == 1:
            count = neg_count - pos_count
            embed=discord.Embed(title="总廷王 dissaproves of your -5 credit score", description=str(random.choice(quo_list)), color=0xff6060)
            await message.channel.send(embed=embed)
        else:
            count = neg_count - pos_count
            expo_count = round(float(1.9) * pow(count, 2))
            embed=discord.Embed(title=(f"总廷王 dissaproves of your -{expo_count} credit score"), description=str(random.choice(quo_list)), color=0xff6060)
            await message.channel.send(embed=embed)
    elif neg_count == pos_count:
        pass
    else:
        if pos_count == 1:
            count = pos_count - neg_count
            embed=discord.Embed(title="总廷王 approves of your +5 credit score", description=str(random.choice(quo_list)), color=0x99ff93)
            await message.channel.send(embed=embed)
        else:
            count = int(pos_count - neg_count)
            expo_count = round(5 * count * float(1.25))
            embed=discord.Embed(title=(f"总廷王 approves of your +{expo_count} credit score"), description=str(random.choice(quo_list)), color=0x99ff93)
            await message.channel.send(embed=embed)

    #suggest 'command'
    if message.content.startswith('gest'):

        msg_trans = message.content.translate(str.maketrans('', '', string.punctuation))
        message_list = msg_trans.lower().split()
        message_form = len(message_list)

        if message_form == 2:

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

@client.listen('on_button')
async def on_button(btn):
    pass

client.run(DISCORD_TOKEN)