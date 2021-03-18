import discord
from utility import message_handler
from discord.utils import get

from youtube_dl import YoutubeDL

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
    
    await handler.search()

    await handler.write_to_all_channels('Bought to you by Jonny sins. An engineer, a doctor, a real life astrounaut and a father to us all. https://img.mensxp.com/media/content/2019/Sep/johnny-sins-trolls-former-pakistan-envoy-abdul-basit1200-1567585868_1200x900.jpg')

    #write a list of commands
    await handler.help()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await handler.handle_message(message.content, message.channel, message.author.voice.channel)

@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=ZiJYyPAzkQM&ab_channel=MrWolf", download=False)
    m_url = info['formats'][0]['url']
    
    voice = get(client.voice_clients, guild=before.channel.guild)
    if voice:
        await voice.move_to(before.channel)
    else:
        voice = await before.channel.connect()

    if voice.is_playing():
        voice.stop()
    voice.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after = lambda e: handler.play_music())
    
token = ""
with open("token.txt") as file:
    token = file.read()
client.run(token)

