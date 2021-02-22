# usage: python launcher.py num_shards first_shard_id:last_shard_id
import discord
from bot import PollBot
import sys
import json

from secret import get_discord_token 

with open('config.json') as config_file:
    config = json.load(config_file)
    config['discord_token']=get_discord_token(config['project_id'],config['secret_id'])

bot = PollBot(config)
bot.run()