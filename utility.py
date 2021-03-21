'''
This is where the magic happens
'''
import discord
import random
import base64

from youtube_dl import YoutubeDL
import requests
import os, shutil

from google_images_download import google_images_download

class message_handler:
    def __init__(self, client, channels):
        self.client = client
        self.channels = channels
        self.keywords = "Spongebob"

        self.response = google_images_download.googleimagesdownload()
        self.arguments = {
            "keywords": self.keywords, 
            "limit":20,
            "size":"medium"
            }

        self.image_names = []

        self.help_message = """Here is a list of available commands:
/help - displays all the available commands
/search <keywords> - will change the search to the keyword (REMOVED AS JOSH WAS BEING A DICK)
/get - will get the image based on the current search (REMOVED AS JOSH WAS BEING A DICK)
/clear amount - will delete the past messages with the amount specified
/play title - plays the video from youtube
/skip - skips the current played song
/q - shows all of the videos in queue
"""

        #all the music related stuff
        self.is_playing = False

        # 2d array containg [channel, url]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    async def help(self):
        await self.write_to_all_channels(self.help_message)

    def update_channel_list(self, new_channels):
        self.channels = new_channels

    async def get_image(self, channel):
        #select a random image
        img = self.image_names[random.randint(0, len(self.image_names) - 1)]
        await channel.send(file=img)              

    async def clear(self, amount, channel):
        #make sure that the amount is valid
        if amount < 1:
            amount = 5
        await channel.purge(limit=amount)

    def clear_folder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    async def search(self):
        #clear the current folder
        folder = 'downloads'
        self.clear_folder(folder)

        #fill the folder with new images
        self.arguments['keywords'] = self.keywords
        self.response.download(self.arguments)

        #store all the names to the files
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    self.image_names.append(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        print(self.image_names)

    #searching the item on youtube
    def search_yt(self, item):
        try: requests.get(item)
        except Exception: pass
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
            
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.music_queue[0][0]['source'], download=False)
            m_url = info['formats'][0]['url']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.music_queue[0][0]['source'], download=False)
            m_url = info['formats'][0]['url']

            try: self.vc = await self.music_queue[0][1].connect()
            except Exception: pass
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def handle_message(self, msg, channel, voice_channel):
        #figure out whether its a valid command
        if msg.startswith("/search"):
            self.keywords = msg[8:]
            await self.search()
        if msg.startswith("/get"):
           await self.get_image(channel)
        if msg.startswith("/help"):
            await channel.send(self.help_message)
        if msg.startswith("/clear"):
            try:
                amount = int(msg[6:])
                await self.clear(amount, channel)    
            except Exception:
                await self.clear(5, channel)

        #playing the music in the queue
        if msg.startswith("/play"):
            #make sure that the voice_channel exists
            if voice_channel is None:
                await channel.send("Connect to a voice channel!")
            else:
                await channel.send("Song added to the queue")
                song = self.search_yt(msg[6:])
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()

        if msg.startswith("/skip"):
            try:
                self.vc.stop()
                await self.play_music()
            except Exception: pass

        if msg.startswith("/q"):
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += self.music_queue[i][0]['title'] + "\n"

            if retval != "":
                await channel.send(retval)
            else:
                await channel.send("No music in queue")


    async def write_to_all_file(self, f):
        for channel in self.channels:
            await channel.send(file=f)   
    async def write_to_all_channels(self, msg):
        for channel in self.channels:
            await channel.send(msg)

    def close_db(self):
        self.conn.close()