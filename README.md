# q3-pickup-bot
A basic Discord bot for Quake 3 rounds.

## Requirements
    py -3 -m pip install -U discord.py
    
    py -3 -m pip install -U python-dotenv
    
    py -3 -m pip install -U pyq3serverlist

## .env
- AUTH_TOKEN     - Your Discord OAuth Token
- GAME_SERVER01  - FQDN of game server 
- GAME_SERVER02  - FQDN of game server
- GAME_SERVER03  - FQDN of game server
- GAME_SERVER04  - FQDN of game server
- GAME_SERVER05  - FQDN of game server
- THRESHOLD_DUEL - Minimum number of players needed for duel notification
- THRESHOLD_TEAM - Minimum number of players needed for team notification
