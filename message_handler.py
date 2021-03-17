'''
This is currently not used as this was just me playing around with the api XD
'''

import discord
import random
import sqlite3

class message_handler:
    def __init__(self, client, channels):
        self.client = client
        self.channels = channels

        self.last_update_time = 0

        self.pictures = [
            "https://media.gettyimages.com/photos/adult-film-actress-kissa-sins-and-adult-film-actor-johnny-sins-attend-picture-id506573722?s=594x594",
            "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/1200px-SpongeBob_SquarePants_character.svg.png",
            "https://i.pinimg.com/originals/62/80/56/6280566a11e6cb4c46dd8843e6ecfd40.jpg",
            "https://s.abcnews.com/images/International/gy_putin_dc_011718_2x3_992.jpg"
        ]

        self.conn = sqlite3.connect("csgo.db")
        self.c = self.conn.cursor()

        #create the table csgo if it does not exist already
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS csgo (
            Name TEXT,
            Kills INTEGER,
            Assists INTEGER,
            Teamkills INTEGER,
            Deaths INTEGER
        );
        """)

        self.conn.commit()
    
    async def help(self):
        await self.write_to_all_channels("""Here is a list of available commands:
!help - lists all of the available commands
!add_name <name>
!add_teamkill <name>

!remove_teamkill <name>
!remove_name <name>

!clear - clears all the stats
!display - displays the current table
!nudes - will send a random nude from the internet
!purge - deletes the above
!DONOTTYPE - self explanatory DO NOT TYPE""")

    def update_channel_list(self, new_channels):
        self.channels = new_channels

    def find_name(self, name):
        self.c.execute("""
                SELECT * FROM csgo WHERE Name=?
                """, (name,))
        return self.c.fetchall()

    async def command_success(self):
        await self.write_to_all_channels("Command was successful")

    async def name_not_found(self):
        await self.write_to_all_channels("name not found")

    async def add_name(self, name):
        # get the name
        result = self.find_name(name)
        if not result:
            self.c.execute("""
            INSERT INTO csgo VALUES (?, ?, ?, ?, ?)
            """, (name, 0, 0, 0, 0))

            await self.command_success()
        else:
            await self.write_to_all_channels("name already exists")

    async def remove_name(self, name):
        self.c.execute("""
            DELETE FROM csgo WHERE Name=?
            """, (name,))
        await self.command_success()

    async def update_kill(self, name, amount):
        result = self.find_name(name)
        if result:
            kills = result[0][1] + amount
            self.c.execute("""
            UPDATE csgo SET Kills=? WHERE Name=?
            """, (kills, name))
            await self.command_success()
        else:
            await  self.name_not_found()

    async def update_assist(self, name, amount):
        result = self.find_name(name)
        if result:
            assists = result[0][2] + amount
            self.c.execute("""
            UPDATE csgo SET Assists=? WHERE Name=?
            """, (assists, name))
            await self.command_success()
        else:
            await self.name_not_found()

    async def update_teamkill(self, name, amount):
        result = self.find_name(name)
        if result:
            teamkills = result[0][3] + amount
            self.c.execute("""
            UPDATE csgo SET Teamkills=? WHERE Name=?
            """, (teamkills, name))
            await self.command_success()
        else:
            await self.name_not_found()

    async def update_death(self, name, amount):
        result = self.find_name(name)
        if result:
            deaths = result[0][4] + amount
            self.c.execute("""
            UPDATE csgo SET Deaths=? WHERE Name=?
            """, (deaths, name))
            await self.command_success()
        else:
            await self.name_not_found()

    def chunkstring(self, string, length):
        return [string[0+i:length+i] for i in range(0, len(string), length)]
    
    async def display(self):
        self.c.execute("""
            SELECT * FROM csgo
        """)
        result = self.c.fetchall()
        string = ""
        for r in result:
            string += ("NAME: " + r[0]) + "\n" + ("KILLS: " + str(r[1])) + "\n" + ("ASSISTS: " + str(r[2])) + "\n" + ("TEAMKILLS: " + str(r[3])) + "\n" + ("DEATHS: " + str(r[4]) + "\n\n")
        
        #split the string into max sizes
        string = self.chunkstring(string, 1500)
        for s in string:
            await self.write_to_all_channels(s)

    async def clear(self):
        self.c.execute("""
            SELECT * FROM csgo
        """)
        result = self.c.fetchall()
        for r in result:
            self.c.execute("""
            UPDATE csgo SET Kills=? , Assists=? , Teamkills=? , Deaths=? WHERE Name=? 
            """, (0,0,0,0, r[0]))


    async def handle_message(self, msg):
        #figure out whether its a valid command
        if msg.startswith("!DONOTTYPE"):
            await self.write_to_all_channels("http://gph.is/2eaV7lJ")
        if msg.startswith("!purge"):
            await self.write_to_all_channels("sorry the command is currently not working")
        if msg.startswith("!nudes"):
            await self.write_to_all_channels(self.pictures[random.randint(0,len(self.pictures) - 1)])
        if msg.startswith("!help"):
            await self.help()

        # handle adding to database
        if msg.startswith("!add_name"):
            name = msg[10:]
            await self.add_name(name)

        if msg.startswith("!add_kill"):
            name = msg[10:]
            await self.update_kill(name, 1)

        if msg.startswith("!add_assist"):
            name = msg[12:]
            await self.update_assist(name, 1)

        if msg.startswith("!add_teamkill"):
            name = msg[14:]
            await self.update_teamkill(name, 1)

        if msg.startswith("!add_death"):
            name = msg[11:]
            await self.update_death(name, 1)    

        #remove commands
        if msg.startswith("!remove_name"):
            name = msg[13:]
            await self.remove_name(name)

        if msg.startswith("!remove_kill"):
            name = msg[13:]
            await self.update_kill(name, -1)

        if msg.startswith("!remove_assist"):
            name = msg[15:]
            await self.update_assist(name, -1)

        if msg.startswith("!remove_teamkill"):
            name = msg[17:]
            await self.update_teamkill(name, -1)

        if msg.startswith("!remove_death"):
            name = msg[14:]
            await self.update_death(name, -1)

        if msg.startswith("!clear"):
            await self.clear()

        if msg.startswith("!display"):
            await self.display()

        #make sure that the result is saved to the database
        self.conn.commit()

    async def write_to_all_channels(self, msg):
        for channel in self.channels:
            await channel.send(msg)

    def close_db(self):
        self.conn.close()
