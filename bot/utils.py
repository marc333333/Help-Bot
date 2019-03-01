def get_token():
    with open("bot.token") as f:
        return f.readline().strip()

def find_command(command, param_count):
    last_match = None
    for c in CommandList.commands:
        for a in c["aliases"]:
            if command == a:
                last_match = c
                if param_count == c["param_count"] or param_count == -1:
                    return c
    if last_match is None:
        return None
    else:
        return { "handler": CommandHandler.help_error, "usage": last_match["usage"] }

def get_top_definition(word):
    r = requests.get(
        url="https://mashape-community-urban-dictionary.p.rapidapi.com/define?term=" + word,
        headers = { "X-RapidAPI-Key": "f586b7f7e0mshc0b8dccb1fdd4ffp1a9b18jsn9ca3fedad99d" }		
    )
    definitions = r.json()["list"]
    return definitions[0]