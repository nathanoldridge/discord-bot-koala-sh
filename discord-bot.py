__author__ = "Nathan Oldridge aka ChemistNate"
__version__ = 1.0
__license__ = "Uncopyright. Use and modify however you want."

import os
import discord
import requests
from dotenv import load_dotenv

''' These are ENVIRONMENT VARIABLES,
which are stored in a file
called .env in the same directory as this script.
You can hardcore these if you aren't familiar with 
environment variables. '''
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KOALA_API_KEY = os.getenv('KOALA_KEY')
ASK_CHANNEL_ID = os.getenv('CHANNEL_ID')

''' Your bot needs to have "Messages Intent" for the bot to read messages '''
client = discord.Client(intents=discord.Intents(messages=True, guilds=True, message_content=True))

''' This function runs when the Bot STARTS'''
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild: '
        f'{guild.name}(id: {guild.id})'
    )
    channelIds = client.get_guild(guild.id).text_channels
    print("LIST OF TEXT CHANNELS:")
    # These print statements go to the Terminal
    # so you can see what channels your bot has access to
    for items in channelIds:
        print(items)
    print("")

''' This function runs when a message gets sent in the server '''
@client.event
async def on_message(message):
    if message.author == client.user: # This prevents the bot from replying to itself
        print("message.author is client.user. No output sent to Discord")
        return
    if message.channel.id == int(ASK_CHANNEL_ID):
        ''' Remember: print() statements go to the Terminal, I included these for debugging '''
        resp = requests.get("https://koala.sh/api/gpt/?input=" + str(message.content) + "&key=" + KOALA_API_KEY)
        print("Response from Koala:", resp.text)
        await message.channel.send("**ChatGPT's response to your question:**\n"+ resp.text)

client.run(TOKEN)