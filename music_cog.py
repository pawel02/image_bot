import discord
from discord.ext import commands

import youtube_dl
import requests

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containg [channel, url]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    @commands.command()
    async def play(self, ctx, *args):
        query = " ".join(args)
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
        
        return {'source': info['formats'][0]['url'], 'title': info['title']}