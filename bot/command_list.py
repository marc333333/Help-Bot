from bot.command_handler import CommandHandler

class CommandList:
    commands = [
        { "aliases": ["help"], "params_count": 0, "handler": CommandHandler.help_all, "usage": "Usage: help" },
        { "aliases": ["help"], "params_count": 1, "handler": CommandHandler.help, "usage": "Usage: help <command>" },
        { "aliases": ["hello"], "params_count": 0, "handler": CommandHandler.hello, "usage": "Usage: hello" }
    ]
