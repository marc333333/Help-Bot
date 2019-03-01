from bot.command_handler import CommandHandler
from bot.command_list import CommandList

class Command:
    PREFIX = "$"
    DEBUG = True

    @staticmethod
    async def execute(client, query):
        q = Command.parse(query)
        if q is None:
            return

        command = q["command"]
        params = q["params"]

        Command.log_query(query)

        last_match = None
        for c in CommandList.commands:
            for a in c["aliases"]:
                if command == a:
                    last_match = c
                    if len(params) == c["params_count"]:
                        Command.log_command(command, params)
                        await c["handler"](client, query, params)
                        return

        if last_match is not None:
            Command.log_command("help", [last_match["aliases"][0]])
            await CommandHandler.help(client, query, last_match)
        
    @staticmethod
    def parse(query):
        content = query.content
        if query.content[0] != Command.PREFIX:
            return None
        content = content[1:]

        split = content.split(' ')
        return { "command": split[0], "params": split[1:] }

    @staticmethod
    def log_query(query):
        print("- [{0.author}] {0.content}".format(query))

    @staticmethod
    def log_command(command, params):
        if Command.DEBUG:
            print("[DEBUG] [EXECUTION] Command: {0} ; Params: {1}".format(command, ", ".join(str(p) for p in params)))
