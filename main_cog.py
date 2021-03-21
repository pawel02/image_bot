import discord
from discord.commands import commands


class main_bot(commands.Cog):
    def __init__(self, bot):

        self.help_message = """
```
General commands:
/help - displays all the available commands
/clear amount - will delete the past messages with the amount specified

Image commands:
/search <keywords> - will change the search to the keyword
/get - will get the image based on the current search
```
"""
        self.text_channel_list = []

    #some debug info so that we know the bot has started    
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        await self.send_to_all(self.help_message)        

    @commands.command()
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.command()
    async def clear(self, ctx, arg):
        #extract the amount to clear
        amount = 5
        try:
            amount = int(arg)
        except Exception: pass

        await ctx.channel.purge(limit=amount)
