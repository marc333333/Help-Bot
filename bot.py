print("Starting...")

import discord

import utils

PREFIX = "$" # 1 character only
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
    word = params[0]
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

commands = [
    { "aliases": ["help"], "param_count": 0, "handler": help_all, "usage": "Usage: help" },
    { "aliases": ["help"], "param_count": 1, "handler": help, "usage": "Usage: help <command>" },
    { "aliases": ["hello"], "param_count": 0, "handler": hello, "usage": "Usage: hello" },
    { "aliases": ["alias", "aliases"], "param_count": 1, "handler": alias, "usage": "Usage: alias <command>" },
    { "aliases": ["meaning", "define", "definition"], "param_count": 1, "handler": meaning, "usage": "Usage: meaning <word>" },
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