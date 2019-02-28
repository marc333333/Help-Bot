from bot.command_handler import CommandHandler

class Command:
    prefix = "$"

    commands = [
        { "aliases": ["help"], "params_count": 0, "handler": CommandHandler.help_all, "usage": "Usage: help" },
        { "aliases": ["help"], "params_count": 1, "handler": CommandHandler.help, "usage": "Usage: help <command>" },
        { "aliases": ["hello"], "params_count": 0, "handler": CommandHandler.hello, "usage": "Usage: hello" }
    ]

    @staticmethod
    async def execute(client, query):
        q = Command.parse(query)
        if q is None:
            return

        command = q["command"]
        params = q["params"]

        last_match = None
        for c in Command.commands:
            for a in c["aliases"]:
                if command == a:
                    last_match = c
                    if len(params) == c["params_count"]:
                        await c["handler"](client, query, params)
                        return

        if last_match is not None:
            await CommandHandler.help(client, query, last_match)
        
    @staticmethod
    def parse(query):
        content = query.content
        if query.content[0] != Command.prefix:
            return None
        content = content[1:]

        split = content.split(' ')
        return { "command": split[0], "params": split[1:] }