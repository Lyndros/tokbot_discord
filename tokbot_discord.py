#!/usr/bin/env python3
# Copyright (c) 2018 Lyndros <lyndros@hotmail.com>
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

###################################################################
# If you want o support this repository I accept donations        #
# even 1 TOK is always welcome :-)!                               #
# > ethereum address: 0x44F102616C8e19fF3FED10c0b05B3d23595211ce  #
# > tokugawa address: TjrQBaaCPoVW9mPAZHPfVx9JJCq7yZ7QnA          #
###################################################################
import discord
import requests
import coinmarketcap
import json
import yaml
import argparse

from urllib.request         import urlopen
from discord.ext.commands   import Bot
from discord.ext            import commands
from datetime               import datetime
from prettytable            import PrettyTable

def justify_text_fix (string, width=None):
    #Define default separation to 10 if width
    SepWidth = 10 if (width==None) else width
    SepChar  = ' '

    #Initialise returning string
    new_string = '\n'

    for line in string.splitlines():
        for word in line.split():
            new_string+=word.ljust(SepWidth,SepChar)

        new_string += '\n'

    #print("Justified fix(%s): %s" %(SepWidth, new_string))

    return new_string

def justify_text_dyn (string):
    #Define minimun separation between fields
    min_separation=2

    #Init the maximum word lenght
    max_word_width=0
    for word in string.split():
        if len(word) > max_word_width:
            max_word_width = len(word)

    #Define the separation
    total_separation = max_word_width+min_separation

    #Get the text justified with the proper separation
    new_string = justify_text_fix(string, width=total_separation)

    #print("Justified dyn(%s): %s" %(total_separation, new_string))

    return new_string

def get_coinmarketcap_id(coin_acronym):
    #Request coin listing to coinmarket cap
    request = requests.get('https://api.coinmarketcap.com/v2/listings/')
    results = request.json()

    #Search for the id
    for coin in results["data"]:
        if coin["symbol"].upper() == coin_acronym.upper():
            return int(coin["id"])

def get_coinmarketcap_stats(coin_acronym):
    # Retrieve coinmarketcap id (comment o avoid recurrent calls, done in config)
    # coin_id = get_coinmarketcap_id(CONFIG['COIN']['acronym'])

    # Get specific coin data
    request = requests.get('https://api.coinmarketcap.com/v2/ticker/' + str(CONFIG['COIN']['id']) + "/?convert=EUR")
    coin_data = request.json()

    return coin_data

def mostrar_ayuda():
    # Declare embed object
    embed       = discord.Embed()
    embed.color = CONFIG['STYLE']['FRAME']['default_color']
    embed.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/32x32/%s' %CONFIG['COIN']['id']  + '.png')

    embed.title = "**__LISTA DE COMANDOS__**"

    for comando in sorted(dict.keys(LISTA_COMANDOS)):
        embed.add_field(name="- "+comando.capitalize(), value="*"+LISTA_COMANDOS[comando]+"*", inline=False)

    return embed

def show_price():
    # Declare embed object
    embed       = discord.Embed()
    embed.color = CONFIG['STYLE']['FRAME']['default_color']
    embed.set_thumbnail(url='https://s2.coinmarketcap.com/static/img/coins/32x32/%s' %CONFIG['COIN']['id']  + '.png')
    embed.title = "**__PRECIO DE %s (%s)__**" %(CONFIG['COIN']['name'].upper(), CONFIG['COIN']['acronym'].upper())
    embed.url   = 'https://coinmarketcap.com/currencies/' + CONFIG['COIN']['name'] + '/'

    try:
        #Read coin stats from coinmarketcap
        coin_stats = get_coinmarketcap_stats(CONFIG['COIN']['acronym'])

        embed.description = "**Ranking:**        " + str('{:,.0f}'.format(coin_stats['data']['rank'])) + "\n" + \
                            "\n**Price EUR**:     " + str('{:,.8f}'.format(float(coin_stats['data']['quotes']['EUR']['price']))) + " €" + \
                            "\n**Price USD**:     " + str('{:,.8f}'.format(float(coin_stats['data']['quotes']['USD']['price']))) + " $" + \
                            "\n**MarketCap EUR**:  " + str('{:,.0f}'.format(float(coin_stats['data']['quotes']['EUR']['market_cap']))) + " €" + \
                            "\n**Volume24h EUR**:  " + str('{:,.0f}'.format(float(coin_stats['data']['quotes']['EUR']['volume_24h']))) + " €" + \
                            "\n**Total distributed**: " + str('{:,.0f}'.format(float(coin_stats['data']['total_supply']))) + " " + coin_stats['data']['symbol'] + "\n" + \
                            "\n**Change 01h**:     " + str(coin_stats['data']['quotes']['EUR']['percent_change_1h']) + "%" + \
                            "\n**Change 24h**:     " + str(coin_stats['data']['quotes']['EUR']['percent_change_24h']) + \
                            "\n**Change 07d**:     " + str(coin_stats['data']['quotes']['EUR']['percent_change_7d']) + "%"

        embed.set_footer(text="coinmarketcap @%s" %coin_stats['metadata']['timestamp'], icon_url="https://logo.clearbit.com/coinmarketcap.com")

    except:
        embed.color = CONFIG['STYLE']['FRAME']['error_color']
        embed.description = "Error retrieving data from coinmarketcap."

    return embed

def comando_bot(cmd):
    if   (cmd == "HELP"):
        embed_message = show_help()
    elif (cmd == "PRICE"):
        embed_message = show_price()
    else:
        # Declare embed object
        embed_message       = discord.Embed()
        embed_message.color = CONFIG['STYLE']['FRAME']['error_color']
        embed_message.title = "**__ERROR__**"
        embed_message.description = "Type '/bot help' to show a full list of the command available."

    return embed_message

#Define global var to store the list of supported commands
LISTA_COMANDOS = {
  "HELP":               "Shows this help",
  "PRICE":              "Shows the current coin price"
}

#Tested in iPhone 6S this is the maximum length per string
MAX_MOBILE_STRLEN = 43

#Parse program parameters
parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="The configuration file to be loaded.")
args = parser.parse_args()

#Parse configuration file
with open(args.config_file, 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)
    #Store the coin ID at the beginning to avoid recurrent calls to coinmarketcap
    CONFIG['COIN']['id'] = get_coinmarketcap_id(CONFIG['COIN']['acronym'])

#Start the discord client
Client = discord.Client()
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print(CONFIG['COIN']['name'] + " BOT funcionando")

@client.event
async def on_message(message):
    if (message.content.upper()[0:5]=="/BOT "):
        embed_message = comando_bot(message.content.upper()[5:])
        await client.send_message(message.channel, embed=embed_message)

client.run(CONFIG['DISCORD']['api_key'])
