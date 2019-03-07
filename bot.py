print("Starting...")

import discord
import asyncio

from random import randint
from googleapiclient.discovery import build

import utils

PREFIX = "$"
DEBUG = True
TOKEN = utils.get_token("bot")

client = discord.Client()
service = build("customsearch", "v1", developerKey = utils.get_token("google"))

commands = None

"""
   _____ ____  __  __ __  __          _   _ _____   _____ 
  / ____/ __ \|  \/  |  \/  |   /\   | \ | |  __ \ / ____|
 | |   | |  | | \  / | \  / |  /  \  |  \| | |  | | (___  
 | |   | |  | | |\/| | |\/| | / /\ \ | . ` | |  | |\___ \ 
 | |___| |__| | |  | | |  | |/ ____ \| |\  | |__| |____) |
  \_____\____/|_|  |_|_|  |_/_/    \_\_| \_|_____/|_____/ 

"""

# Help
async def help(query, command, params):
    c = find_command(params[0], -1)
    if c is None:
        await client.send_message(query.channel, "Error: Invalid command \"{0}\"\n\n{1}".format(params[0], command["usage"]))
    else:
        await client.send_message(query.channel, c["usage"])

# Help Error
async def help_error(query, command, params):
    await client.send_message(query.channel, "Error: Invalid format\n\n{0}".format(command["usage"]))

# Help All
async def help_all(query, command, params):
    cmds = list(set(str(c["aliases"][0]) for c in commands))
    cmds.sort()
    msg = "Available commands: {0}\n\nUse \"help <command>\" for commands usage".format(", ".join(cmds))
    await client.send_message(query.channel, msg)

# Hello
async def hello(query, command, params):
    msg = "Hello {0.author.mention}".format(query)
    await client.send_message(query.channel, msg)

# Alias
async def alias(query, command, params):
    c = find_command(params[0], -1)
    if c is None or len(c["aliases"]) < 2:
        await client.send_message(query.channel, "No alias found for {0}".format(params[0]))
    else:
        msg = "Aliases for {0}: {1}".format(c["aliases"][0], ", ".join(c["aliases"][1:]))
        await client.send_message(query.channel, msg)

# Meaning
async def meaning(query, command, params):
    if len(params) < 1:
        await help_error(query, command, params)
        return

    word = " ".join(params)

    try:
        definition = utils.get_top_definition(word)

        embed=discord.Embed(
            title = "Top definition of " + word,
            url = definition["permalink"],
            description = definition["definition"].replace('[', '').replace(']', ''),
            color = 0xff8000
        )
        embed.set_author(
            name = "Urban Dictionary",
        )
        
        await client.send_message(query.channel, embed=embed)
    except Exception as e:
        await client.send_message(query.channel, "No definition found for {0}".format(word))

# Image
async def image(query, command, params):
    if len(params) < 1:
        await help_error(query, command, params)
        return

    word = " ".join(params)

    split = word.split("|")
    if len(split) > 2:
        await help_error(query, command, params)
        return
    random = False
    if len(split) == 2:
        if split[1].strip() == "random":
            random = True
        else:
            await help_error(query, command, params)
            return

    res = service.cse().list(
        q = split[0].strip(),
        cx = "017064401556617570624:1l1erxhxwm0",
        safe = "active",
        searchType = "image"
    ).execute()

    try:
        if random:
            rnd = randint(0, len(res["items"]))
            await client.send_message(query.channel, res["items"][rnd]["link"])
        else:
            await client.send_message(query.channel, res["items"][0]["link"])

    except Exception as e:
        await client.send_message(query.channel, "No result found for {0}".format(word))
		
# Loli
async def loli(query, command, params):
    msg = "FBI open up!\nhttps://media1.tenor.com/images/93d11bc59526ce49f60766f0045d819b/tenor.gif"
    await client.send_message(query.channel, msg)
	
# Yiff
async def yiff(query, command, params):
    msg = "https://static1.fjcdn.com/thumbnails/comments/Cap+the+furries+yiff+war+now+_70a08678fdc5611ed8a31eefc551f2cc.gif"
    await client.send_message(query.channel, msg)

async def random(query, command, params):
    try:
        min = int(params[0])
        max = int(params[1])

        result = randint(min, max)

        msg = await client.send_message(query.channel, ":spades: :hearts: :diamonds: :clubs:")
        await asyncio.sleep(0.5)
        await client.edit_message(msg, ":diamonds: :clubs: :hearts: :spades:")
        await asyncio.sleep(0.5)
        await client.edit_message(msg, ":clubs: :diamonds: :spades: :hearts:")
        await asyncio.sleep(0.5)
        await client.edit_message(msg, ":hearts: :spades: :clubs: :diamonds:")
        await asyncio.sleep(0.5)
        await client.delete_message(msg)

        await client.send_message(query.channel, result)
    except Exception as e:
        await help_error(query, command, params)

commands = [
    { "aliases": ["help"], "param_count": 0, "handler": help_all, "usage": "Usage: help" },
    { "aliases": ["help"], "param_count": 1, "handler": help, "usage": "Usage: help <command>" },
    { "aliases": ["hello", "hi"], "param_count": 0, "handler": hello, "usage": "Usage: hello" },
    { "aliases": ["alias", "aliases"], "param_count": 1, "handler": alias, "usage": "Usage: alias <command>" },
    { "aliases": ["meaning", "define", "definition"], "param_count": -1, "handler": meaning, "usage": "Usage: meaning <word>" },
    { "aliases": ["image", "picture"], "param_count": -1, "handler": image, "usage": "Usage: image <word> [| random]" },
    { "aliases": ["loli"], "param_count": 0, "handler": loli, "usage": "Usage: loli" },
    { "aliases": ["yiff"], "param_count": 0, "handler": yiff, "usage": "Usage: yiff" },
    { "aliases": ["random"], "param_count": 2, "handler": random, "usage": "Usage: random <min> <max>" }
]

"""
  ____   ____ _______    _____ _______ _    _ ______ ______ 
 |  _ \ / __ \__   __|  / ____|__   __| |  | |  ____|  ____|
 | |_) | |  | | | |    | (___    | |  | |  | | |__  | |__   
 |  _ <| |  | | | |     \___ \   | |  | |  | |  __| |  __|  
 | |_) | |__| | | |     ____) |  | |  | |__| | |    | |     
 |____/ \____/  |_|    |_____/   |_|   \____/|_|    |_|     
                                                                                            
"""

def parse(query):
    log_message(query)

    content = query.content
    if not content.startswith(PREFIX):
        return None
    content = content[len(PREFIX):]

    split = content.split(' ')
    return { "command": split[0], "params": split[1:] }

def find_command(command, param_count):
    last_match = None
    for c in commands:
        for a in c["aliases"]:
            if command == a:
                last_match = c
                if param_count == c["param_count"] or param_count == -1 or c["param_count"] == -1:
                    return c
    if last_match is None:
        return None
    else:
        return { "handler": help_error, "usage": last_match["usage"] }

def log_query(query):
    print("- [{0.author}] {0.content}".format(query))

def log_command(command, params):
    if DEBUG:
        print("[DEBUG] [EXECUTION] Command: {0} ; Params: {1}".format(command, ", ".join(str(p) for p in params)))
		
def log_message(query):
	if DEBUG:
		print("[DEBUG] [MESSAGE] Author: {0.author} ; Content: {0.content}".format(query))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    query = parse(message)
    if query is None:
        return

    log_query(message)

    command = find_command(query["command"], len(query["params"]))
    
    if command is not None:
        log_command(query["command"], query["params"])
        await command["handler"](message, command, query["params"])
        
@client.event
async def on_ready():
    print("""
  _    _ ______ _      _____    ____   ____ _______ 
 | |  | |  ____| |    |  __ \  |  _ \ / __ \__   __|
 | |__| | |__  | |    | |__) | | |_) | |  | | | |   
 |  __  |  __| | |    |  ___/  |  _ <| |  | | | |   
 | |  | | |____| |____| |      | |_) | |__| | | |   
 |_|  |_|______|______|_|      |____/ \____/  |_|   
                                                                         
    """)
    
    print("Ready")
    print("----------------------------------------------------")

client.run(TOKEN)