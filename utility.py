'''
This is where the magic happens
'''
import discord
import random
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class message_handler:
    def __init__(self, client, channels):
        self.client = client
        self.channels = channels
        self.keywords = "Spongebob"

        # initialize selenium
        self.driver = driver = webdriver.Chrome('E:\pawel\coding(learning)\discord\chromedriver.exe')
        self.driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

        #first dummy search as the xpath is different afterwards
        box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
        box.send_keys(self.keywords)
        box.send_keys(Keys.ENTER)



    async def help(self):
        await self.write_to_all_channels("""Here is a list of available commands:
/help - displays all the available commands
/search <keywords> - will change the search to the keyword
/get - will get the image based on the current search
""")

    def update_channel_list(self, new_channels):
        self.channels = new_channels

    async def get_image(self):
        box = self.driver.find_element_by_xpath('//*[@id="REsRA"]')
        box.clear()
        box.send_keys(self.keywords)
        box.send_keys(Keys.ENTER)

        images = self.driver.find_elements_by_css_selector("img")
        srcs = []
        for image in images:
            srcs.append(image.get_property("src"))

        #select a random image
        img = srcs[random.randint(0, len(srcs) - 1)]
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
            await self.write_to_all_file(picture)              
        elif len(img) != 0:
            await self.write_to_all_channels(img)
        else:
            await self.get_image()

    async def handle_message(self, msg):
        #figure out whether its a valid command
        if msg.startswith("/search"):
            self.keywords = msg[8:]
        if msg.startswith("/get"):
           await self.get_image()
        if msg.startswith("/help"):
            await self.help()


    async def write_to_all_file(self, f):
        for channel in self.channels:
            await channel.send(file=f)   
    async def write_to_all_channels(self, msg):
        for channel in self.channels:
            await channel.send(msg)

    def close_db(self):
        self.conn.close()