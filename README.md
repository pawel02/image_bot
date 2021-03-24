# Simple discord bot
This bot has only 3 commands available

## General commands:
- /help - displays all the available commands
- /clear amount - will delete the past messages with the amount specified

## Image commands:
- /search <keywords> - will change the search to the keyword
- /get - will get the image based on the current search

## Music commands:
- /p <keywords> - finds the song on youtube and plays it in your current channel
- /q - displays the current music queue
- /skip - skips the current song being played

# install with docker
If you have docker then you can run the following command and it will automatically pull the image and then run it

PLEASE DONT FORGET TO CREATE THE TOKEN.TXT FILE TO STORE YOUR TOKEN

`
docker pull pabolo02345/discord_bot
`

create token.txt and store you discord token there

run 
`
docker run -d discord_bot
`


# bot.py
Responsible for handling all the discord API stuff

# need to install the following libraries
pip install discord.py[voice]
pip install youtube_dl

## to install google_images_download (download the feature branch with the fix)
git clone https://github.com/Joeclinton1/google-images-download.git
cd google-images-download && python setup.py install