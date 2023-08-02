import socket
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from pyq3serverlist import Server
from pyq3serverlist.exceptions import PyQ3SLError, PyQ3SLTimeoutError

load_dotenv()

TOKEN        = os.getenv('AUTH_TOKEN')
SERVER01     = os.getenv('GAME_SERVER01')
SERVER02     = os.getenv('GAME_SERVER02')
SERVER03     = os.getenv('GAME_SERVER03')
SERVER04     = os.getenv('GAME_SERVER04')
SERVER05     = os.getenv('GAME_SERVER05')

PLAYER_COUNT_DUEL = os.getenv('THRESHOLD_DUEL')
PLAYER_COUNT_TEAM = os.getenv('THRESHOLD_TEAM')

SERVERS = SERVER01,SERVER02,SERVER03,SERVER04,SERVER05

QUEUE = []

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
        
        channel = message.channel
  
        # Ignore bot's own messages
        if message.author == bot.user:
            return

        # Do not interact with DMs
        if isinstance(channel, discord.channel.DMChannel):
            await channel.send("I'm not built to handle DM's. Please interact with me inside a proper channel.")
            return

        # Command logic
        if "!help" == message.content.lower():
             await channel.send("Verbs: " + "help, hello, list, add, remove, servers, clearqueue. Use ! as a prefix. ")
        elif "!hello" == message.content.lower():
             await channel.send("Fuck you " + message.author.mention + ".")
        elif "!list" == message.content.lower():
            s = ' '.join(str(x) for x in QUEUE)
            await channel.send("Currently queued players: " + s) 
        elif "!add" in message.content.lower():
            s = ' '.join(str(x) for x in QUEUE)
            if message.author.mention not in s:
                await channel.send("Adding " + message.author.mention + " to queue.") 
                QUEUE.append(message.author.mention)
                if len(QUEUE) == int(PLAYER_COUNT_DUEL):
                     await channel.send("Enough players for duels, go play!")
                     for x in QUEUE:
                        await channel.send(x)
                elif len(QUEUE) == int(PLAYER_COUNT_TEAM):
                    await channel.send("Enough players for team modes, go play!")
                    for x in QUEUE:
                        await channel.send(x)
            if message.author.mention in s:
                await channel.send("You are already in queue...")           
        elif "!remove" in message.content.lower():
            s = ' '.join(str(x) for x in QUEUE)
            if message.author.mention not in s:
                await channel.send("You weren't queued...")
            if message.author.mention in s:
                await channel.send("Removing " + message.author.mention + " from queue.")
                QUEUE.remove(message.author.mention) 
        elif "!servers" in message.content.lower():
                await channel.send("**Servers**")
                for x in SERVERS:
                    if(len(x) != 0):
                        ip = socket.gethostbyname(x)
                        await channel.send("*" + x + ": " + ip + "*")
                        serverStatus = query_quake3_server(x)                  
                        for i in serverStatus["players"]:
                            name  = str(i['name'])
                            frags = str(i['frags'])
                            ping  = str(i['ping'])
                            if ping != '0':
                                await channel.send("> *player* -> **" + name + "** *frags*-> **" + frags + "**")
        elif "!clearqueue" in message.content.lower():
            while len(QUEUE)>0:
                QUEUE.pop(0)
            await channel.send("Queue is empty.") 

# Function return is JSON data
def query_quake3_server(server):
    server = Server(server, 27960)
    try:
        info = server.get_status()
        return(info)
    except (PyQ3SLError, PyQ3SLTimeoutError) as e:
        print(e)

bot.run(TOKEN)