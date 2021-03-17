import discord
from utility import message_handler

client = discord.Client()
text_channel_list = []
handler = message_handler(client, text_channel_list)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    for guild in client.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    
    handler.update_channel_list(text_channel_list)

    #await handler.write_to_all_channels('Bought to you by Jonny sins. An engineer, a doctor, a real life astrounaut and a father to us all. https://img.mensxp.com/media/content/2019/Sep/johnny-sins-trolls-former-pakistan-envoy-abdul-basit1200-1567585868_1200x900.jpg')

    #write a list of commands
    await handler.help()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await handler.handle_message(message.content)



client.run("ODIxNzIyMjM3ODYyMTUwMTc1.YFH2eA.sRkidvG8NT4LQ5Po2rqSXp5klmM")
