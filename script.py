import socket
import discord
import os
import json
import random
from discord.ext import commands
from discord.ext import tasks
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

PLAYER_COUNT = os.getenv('THRESHOLD')

QUOTES     = os.getenv('QUOTES_FILE')

SERVERS = SERVER01,SERVER02,SERVER03,SERVER04,SERVER05

QUEUE = []

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def clear_queue():
    global QUEUE
    while len(QUEUE)>0:
        QUEUE.pop(0)

@tasks.loop(minutes=120)
async def queue_task():
     clear_queue()
    
@bot.event
async def on_ready():
     queue_task.start()

@bot.event
async def on_message(message):

    global QUEUE
    channel = message.channel

    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Do not interact with DMs
    if isinstance(channel, discord.channel.DMChannel):
        await channel.send("I'm not built to handle DM's. Please interact with me inside a proper channel.")
        return

    # Command logic
    if message.content.lower().startswith("!help"):
            await channel.send("Verbs: \n" + "add, clearqueue, help, hello, list, ping, remove, servers, turd.\n" + "Use ! as a prefix.")
    elif message.content.lower().startswith("!hello"):
            await channel.send("Hey there, " + message.author.name + ".")
    elif message.content.lower().startswith("!list"):
        s = '\n'.join(str(x.name) for x in QUEUE)
        await channel.send("Currently queued players: \n" + s)
    elif message.content.lower().startswith("!add"):
        s = ' '.join(str(x.name) for x in QUEUE)
        this_message = ""
        if message.author.name not in s:
            this_message = this_message + "Adding " + message.author.name + " to queue.\n"
            QUEUE.append(message.author)
            if len(QUEUE) == int(PLAYER_COUNT):
                this_message = this_message + "Enough players, go play! Queue cleared....\n"
                for x in QUEUE:
                    this_message = this_message +  x.mention + "\n"
                clear_queue()
        await channel.send(this_message)
        this_message = ""
        if message.author.name in s:
            await channel.send("You are already in queue...")
    elif message.content.lower().startswith("!remove"):
        s = ' '.join(str(x.name) for x in QUEUE)
        if message.author.name not in s:
            await channel.send("You weren't queued...")
        if message.author.name in s:
            await channel.send("Removing " + message.author.name + " from queue.")
            QUEUE.remove(message.author)
    elif message.content.lower().startswith("!servers"):
            this_message = ""
            this_message = this_message + "**Servers**\n"
            for x in SERVERS:
                if(len(x) != 0):
                    ip = socket.gethostbyname(x)
                    this_message = this_message + "__" + x + " | " + ip + "__" + "\n"
                    this_message = this_message + "> **Player**" + " | " + "**Frags**" + "\n"
                    serverStatus = query_quake3_server(x)
                    for i in serverStatus["players"]:
                        name  = str(i['name'])
                        frags = str(i['frags'])
                        ping  = str(i['ping'])
                        if ping != '0':
                            this_message = this_message + "> " + name + " | " + "" + frags + "\n"
            await channel.send(this_message)
            this_message = ""
    elif message.content.lower().startswith("!clearqueue"):
        clear_queue()
        await channel.send("Queue is empty.")
    elif message.content.lower().startswith("!ping"):
        this_message = ""
        this_message = this_message + "Hey!"
        for x in QUEUE:
            this_message = this_message + " " + x.mention
        await channel.send(this_message)
        this_message = ""
    elif message.content.lower().startswith("!turd"):
        await channel.send((getQuote()))

# Function return is JSON data
def query_quake3_server(server):
    server = Server(server, 27960)
    try:
        info = server.get_status()
        return(info)
    except (PyQ3SLError, PyQ3SLTimeoutError) as e:
        print(e)

def getQuote():
    with open(str(QUOTES), 'r', encoding='utf-8') as f:
        data = json.load(f)
    i = random.randint(0,len(data['quotes'])-1)
    f.close()
    return(data['quotes'][i])

bot.run(TOKEN)
