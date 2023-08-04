# q3-pickup-bot
A basic Discord bot for Quake 3 rounds. Port 27960 is assumed. 

## Requirements
    py -3 -m pip install -U discord.py
    
    py -3 -m pip install -U python-dotenv
    
    py -3 -m pip install -U pyq3serverlist

    py -3 -m pip install -U cysystemd

## .env File
- AUTH_TOKEN     - Your Discord OAuth Token
- GAME_SERVER01  - FQDN of game server 
- GAME_SERVER02  - FQDN of game server
- GAME_SERVER03  - FQDN of game server
- GAME_SERVER04  - FQDN of game server
- GAME_SERVER05  - FQDN of game server
- THRESHOLD      - Minimum number of players needed to notify & pop the queue
- QUOTES_FILE    - JSON formatted file with quotes