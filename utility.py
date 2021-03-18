'''
This is where the magic happens
'''
import discord
import random
import base64

from youtube_dl import YoutubeDL
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class message_handler:
    def __init__(self, client, channels):
        self.client = client
        self.channels = channels
        self.keywords = "Spongebob"

        # initialize selenium
        self.driver = webdriver.Chrome('E:\pawel\coding(learning)\discord\chromedriver.exe')
        self.driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

        #first dummy search as the xpath is different afterwards
        box = self.driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
        box.send_keys(self.keywords)
        box.send_keys(Keys.ENTER)

        self.help_message = """Here is a list of available commands:
/help - displays all the available commands
/search <keywords> - will change the search to the keyword
/get - will get the image based on the current search
/clear amount - will delete the past messages with the amount specified
"""
        self.srcs = []

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
        img = self.srcs[random.randint(0, len(self.srcs) - 1)]
        if len(img) > 2000:
            img_data = img
            # delete the header
            base64_place = img_data.find('base64') + 7
            header = img_data[:base64_place]
            img_type = header[header.find('image/') + 6: header.find(';')]
            img_name = "tmp." + img_type

            img_data = img_data[base64_place:]
            with open(img_name, "wb") as file:
                img_data = img_data.encode('utf-8')
                img_data = base64.decodebytes(img_data)
                file.write(img_data)

            picture = discord.File(img_name)
            await channel.send(file=picture)              
        elif len(img) != 0:
            await channel.send(img)
        else:
            await self.get_image(channel)

    async def clear(self, amount, channel):
        #make sure that the amount is valid
        if amount < 1:
            amount = 5
        await channel.purge(limit=amount)

    async def search(self):
        box = self.driver.find_element_by_xpath('//*[@id="REsRA"]')
        box.clear()
        box.send_keys(self.keywords)
        box.send_keys(Keys.ENTER)

        images = self.driver.find_elements_by_css_selector(".rg_i")
        self.srcs = []
        for image in images:
            self.srcs.append(image.get_property("src"))

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
                info = ydl.extract_info(self.music_queue[0][0], download=False)
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
                info = ydl.extract_info(self.music_queue[0][0], download=False)
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
                self.music_queue.append([song['source'], voice_channel])
                if self.is_playing == False:
                    await self.play_music()

    async def write_to_all_file(self, f):
        for channel in self.channels:
            await channel.send(file=f)   
    async def write_to_all_channels(self, msg):
        for channel in self.channels:
            await channel.send(msg)

    def close_db(self):
        self.conn.close()