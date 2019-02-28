import discord
import requests

def getDefinition(word):
	r = requests.get(
		url="https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=" + word,
		headers = { "X-RapidAPI-Key": "f586b7f7e0mshc0b8dccb1fdd4ffp1a9b18jsn9ca3fedad99d" }		
	)
	definitions = r.json()["list"]
	return definitions[0]

TOKEN = "NTUwNDg1NjM4NjAwODUxNDYx.D1jK1A.P1S1sxhN6blz4YALgO145aSZyHk"

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
	if message.author == client.user:
		return

	if message.content.startswith("$hello"):
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
		
		await client.send_message(message.channel, embed=embed)

@client.event
async def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print("------")

client.run(TOKEN)