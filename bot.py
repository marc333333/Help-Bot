import discord
import requests

from bot.utils import Utils
from bot.command import Command

TOKEN = Utils.get_token()

client = discord.Client()

@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    await Command.execute(client, message)

    """if message.content.startswith("$hello"):
        msg = "Hello {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)
        
    elif message.content.startswith("$meaning"):
        params = message.content.split(' ')
        if (len(params) != 2):
            msg = "Error: Invalid format\n\nUsage: $meaning <word>"
            await client.send_message(message.channel, msg)
            return
        
        word = params[-1]
        definition = getDefinition(word)
        
        embed=discord.Embed(
            title = "Top definition of " + word,
            description = definition["definition"].replace('[', '').replace(']', ''),
            color = 0xff8000
        )
        embed.set_author(
            name = "Urban Dictionary",
            url = definition["permalink"]
        )
        
        await client.send_message(message.channel, embed=embed)"""

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------------")

client.run(TOKEN)
