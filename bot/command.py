from bot.utils import Utils
from bot.command_handler import CommandHandler, CommandList

class Command:
    PREFIX = "$"
    DEBUG = True

    @staticmethod
    async def execute(client, query):
        q = Command.parse(query)
        if q is None:
            return

        Command.log_query(query)

        command = Utils.find_command(q["command"], len(q["params"]))
       
        if command is not None:
            Command.log_command(q["command"], q["params"])
            await command["handler"](client, query, command, q["params"])
        
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