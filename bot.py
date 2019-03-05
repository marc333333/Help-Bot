import discord
import requests

import utils

PREFIX = "$"
DEBUG = True

commands = None

TOKEN = utils.get_token()
client = discord.Client()

"""
   _____ ____  __  __ __  __          _   _ _____   _____ 
  / ____/ __ \|  \/  |  \/  |   /\   | \ | |  __ \ / ____|
 | |   | |  | | \  / | \  / |  /  \  |  \| | |  | | (___  
 | |   | |  | | |\/| | |\/| | / /\ \ | . ` | |  | |\___ \ 
 | |___| |__| | |  | | |  | |/ ____ \| |\  | |__| |____) |
  \_____\____/|_|  |_|_|  |_/_/    \_\_| \_|_____/|_____/ 

"""

async def help(query, command, params):
    c = find_command(params[0], -1)
    if c is None:
        await client.send_message(query.channel, "Error: Invalid command \"{0}\"\n\n{1}".format(params[0], command["usage"]))
    else:
        await client.send_message(query.channel, c["usage"])

async def help_error(query, command, params):
    await client.send_message(query.channel, "Error: Invalid format\n\n{0}".format(command["usage"]))

async def help_all(query, command, params):
    cmds = list(set(str(c["aliases"][0]) for c in commands))
    msg = "Available commands: {0}\n\nUse \"help <command>\" for commands usage".format(", ".join(cmds))
    await client.send_message(query.channel, msg)

async def hello(query, command, params):
    msg = "Hello {0.author.mention}".format(query)
    await client.send_message(query.channel, msg)

commands = [
    { "aliases": ["help"], "param_count": 0, "handler": help_all, "usage": "Usage: help" },
    { "aliases": ["help"], "param_count": 1, "handler": help, "usage": "Usage: help <command>" },
    { "aliases": ["hello"], "param_count": 0, "handler": hello, "usage": "Usage: hello" }
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
    content = query.content
    if query.content[0] != PREFIX:
        return None
    content = content[1:]

    split = content.split(' ')
    return { "command": split[0], "params": split[1:] }

def find_command(command, param_count):
    last_match = None
    for c in commands:
        for a in c["aliases"]:
            if command == a:
                last_match = c
                if param_count == c["param_count"] or param_count == -1:
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