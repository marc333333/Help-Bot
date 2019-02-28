class CommandHandler:
    @staticmethod
    async def help(client, query, params):
        await client.send_message(query.channel, params["usage"])

    @staticmethod
    async def help_all(client, query, params):
        await client.send_message(query.channel, "help all")

    @staticmethod
    async def hello(client, query, params):
        msg = "Hello {0.author.mention}".format(query)
        await client.send_message(query.channel, msg)