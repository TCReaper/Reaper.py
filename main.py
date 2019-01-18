
# POKEMON ON DISCORD

import os
import sys
import time
import discord
import urllib.request

from keep_alive import keep_alive
from update_acc import update_acc
from text_search import text_search
from goggle_search import goggle_search

creatorID = os.environ.get("CREATOR_ID")


# CREATES INSTANCE OF CLIENT VARIABLE
client = discord.Client()
                
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!bot'):
        await client.delete_message(message)
        msg = message.content.split(' ')
        msg = ' '.join(msg[1:])
        if message.author.id == creatorID:
            msg = (msg).format(message)
            await client.send_message(message.channel, msg)
            return
        return

    if message.content.startswith('vote:'):
        await client.add_reaction(message,"\u2705")
        await client.add_reaction(message,"\u274E")
        return
            
    if 'exp' == message.content.lower() or 'spam' == message.content.lower():
        await client.delete_message(message)
        return

    try:
        embed = message.embeds[0]
    except Exception:
        # EXCEPTION RAISED MEANS MESSAGE IS PLAINTEXT
        name = message.author.name
        name = name.split('#')[0]
        msg = message.content
        print(name+': '+msg)
    else:
        # MESSAGE IS AN EMBED
        try:
            desc = embed['description']
            print('Embed: '+desc)
        except KeyError:
            pass#print(embed)
        
        
        # START OF P!CATCH

        desc = embed['description']
        if desc.startswith('Guess the pokémon'):
            url = embed['image']['url']
            google = 'https://images.google.com/searchbyimage?image_url='+url

            text = goggle_search(google)

            name = text_search(text,'https://bulbapedia.bulbagarden.net/wiki/','_(Pok%C3%A9mon)',40)
            if name == None:
                name = text_search(text,'https://pokemondb.net/pokedex/','"',30)
            if name == None:
                name = 'i am a stupid bot who can\'t find anything'

            msg = (name).format(message)
            msg = await client.send_message(message.channel, msg)
            # await client.add_reaction(msg,"\u2705")
            # await client.add_reaction(msg,"\u274E")
            # x = client.get_all_members()
            # for person in x:
            #     if person.id == creatorID:
            #         author = person
            #         break
            # response = await client.wait_for_reaction(["\u2705","\u274E"],user=author,message=msg)
            # accuracy = update_acc(response.reaction.emoji)
            # await client.clear_reactions(msg)
            return

        # END OF P!CATCH
        # START OF P!INFO

        if embed['title'].startswith('Level'):
          
            await client.delete_message(message)
            
            poke_url = embed['image']['url']
            footer_text = embed['footer']['text'].split('- Use')[0]

            if 'thumbnail' in embed:
                owner_img = embed['thumbnail']['url']
            else:
                owner_img = 'https://cdn1.iconfinder.com/data/icons/smashicons-movies-yellow/57/63_-Pokemon-_Yellow-512.png'
                

            em = discord.Embed(title=embed['title'], description=embed['description'], colour=0xb949b5)
            em = em.set_thumbnail(url=poke_url)
            em = em.set_author(name='reapyr',icon_url=owner_img)
            em = em.set_footer(text=footer_text)

            await client.send_message(message.channel,embed=em)
            return

        # END OF P!INFO
        # START OF P!MARKET

        if embed['title'].startswith('Pokécord Market'):
            desc = embed['description']
            lines = desc.split('\n')
            okay = []
            lowkay = []
            for i in range(len(lines)):
                item = lines[i]
                price = int(item.split('Price: ')[1].split(' Credits')[0])
                poke_id = item.split('ID: ')[1].split(' |')[0]
                if price < 8:
                    okay.append(poke_id)
                else:
                    lowkay.append(poke_id)
                    
            msg1 = ' '.join(okay)
            msg2 = ' '.join(lowkay)
            msg = msg1+'\n\n'+msg2
            await client.send_message(message.channel, msg)
            return

        # END OF P!MARKET
        # START OF P!POKEMON --NAME

        if desc.startswith('**'):
            emolgas = []
            desc = desc.split('Number: ')
            for i in desc:
                i = i.split(' | IV')[0]
                emolgas.append(i)
            emolgas = emolgas[1:]
            msg = ('p`!`p add '+' '.join(emolgas)).format(message)
            if len(emolgas) > 0:
            	await client.send_message(message.channel, msg)
            return

        # END OF P!POKEMON --NAME         
    # START OF P!SEARCH

    if message.content.startswith('!pokemon') or message.content.startswith('p!search'):
        pokemon = message.content.split(' ')[1]
        url = 'https://www.google.com/search?q=pokedex+'+pokemon
        text = goggle_search(url)
        try:
            index = text.index('https://pokemondb.net/pokedex/')
            link = text[int(index):int(index)+50].split('"')[0]
        except ValueError:
            link = 'No pokemon found named '+pokemon
        msg = (link).format(message)
        await client.send_message(message.channel, msg)
        return

    # END OF P!SEARCH
    # START OF P!ACCURACY
 
    # ctrl shift / to comment blocks

    # if message.content.startswith('p!accuracy'):
    #     accuracy = update_acc()
    #     msg = ('current accuracy: '+str(accuracy)).format(message)
    #     await client.send_message(message.channel,msg)
    #     if 'detailed' in message.content:
    #         msg = ('right/wrong ratio: '+update_acc(details=True))
    #         await client.send_message(message.channel,msg)

    # END OF P!ACCURACY
    # START OF !DETAILS

    if message.content.lower() == '!details':
        em = discord.Embed(title='read my code!', url='https://github.com/TCReaper/Reaper.py/', colour=0xb949b5)
        em = em.set_author(name='TCReaper')
        await client.send_message(message.channel,embed=em)

    # END OF !DETAILS

    if message.content.lower() == 'mkt':
    	msg = 'p!market search --order price a --showiv --name '.format(message)
    	await client.send_message(message.channel,msg)

    if message.content.lower().startswith('test'):
        msg = 'received, {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        return
        
    if message.content.startswith('p!ca') or message.content.startswith('p!p'):
        await client.delete_message(message)

    if message.content.lower().startswith('!servers'):
        if message.author.id != creatorID:
            return
        msg = 'i am in these servers:'.format(message)
        await client.send_message(message.channel, msg)
        for i in client.servers:
            msg = i.name.format(message)
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="with Python 3.6.7"))

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
