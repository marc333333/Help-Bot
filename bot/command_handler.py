from bot.utils import Utils

class CommandList:
    commands = [
        { "aliases": ["help"], "param_count": 0, "handler": CommandHandler.help_all, "usage": "Usage: help" },
        { "aliases": ["help"], "param_count": 1, "handler": CommandHandler.help, "usage": "Usage: help <command>" },
        { "aliases": ["hello"], "param_count": 0, "handler": CommandHandler.hello, "usage": "Usage: hello" }
    ]

class CommandHandler:
    @staticmethod
    async def help(client, query, command, params):
        c = Utils.find_command(params[0], -1)
        await client.send_message(query.channel, c["usage"])

    @staticmethod
    async def help_error(client, query, command, params):
        await client.send_message(query.channel, "Error: Invalid format\n\n{0}".format(command["usage"]))

    @staticmethod
    async def help_all(client, query, command, params):
        await client.send_message(query.channel, "help all")

    @staticmethod
    async def hello(client, query, command, params):
        msg = "Hello {0.author.mention}".format(query)
        await client.send_message(query.channel, msg)