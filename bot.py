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
    
    #handler.update_channel_list(text_channel_list)
    
    #await handler.search()

    #await handler.write_to_all_channels('Bought to you by Jonny sins. An engineer, a doctor, a real life astrounaut and a father to us all. https://img.mensxp.com/media/content/2019/Sep/johnny-sins-trolls-former-pakistan-envoy-abdul-basit1200-1567585868_1200x900.jpg')

    #write a list of commands
    #await handler.help()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await handler.handle_message(message.content, message.channel, message.author.voice.channel)

token = ""
with open("token.txt") as file:
    token = file.read()
client.run(token)













# song_queue = []
# FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
# YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

# #Search videos from key-words or links
# def search(arg):
#     try: requests.get("".join(arg))
#     except Exception: arg = " ".join(arg)
#     else: arg = "".join(arg)
#     with YoutubeDL(YDL_OPTIONS ) as ydl:
#         info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        
#     return {'source': info['formats'][0]['url'], 'title': info['title']}

# #Plays the next song in the queue
# def play_next(ctx):
#     voice = get(bot.voice_clients, guild=ctx.guild)
#     if len(song_queue) > 1:
#         del song_queue[0]
#         voice.play(discord.FFmpegPCMAudio(song_queue[0][source], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
#         voice.is_playing()

# @bot.command()
# async def play(ctx, *arg):
#     print("hi")
#     channel = ctx.message.author.voice.channel

#     if channel:
#         voice = get(bot.voice_clients, guild=ctx.guild)
#         song = search(arg)
#         song_queue.append(song)

#         if voice and voice.is_connected():
#             await voice.move_to(channel)
#         else: 
#             voice = await channel.connect()

#         if not voice.is_playing():
#             voice.play(discord.FFmpegPCMAudio(song_queue[0][source], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
#             voice.is_playing()
#         else:
#             await ctx.send("Added to queue")
#     else:
#         await ctx.send("You're not connected to any channel!")
