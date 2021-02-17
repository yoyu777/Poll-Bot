# usage: python launcher.py num_shards first_shard_id:last_shard_id
import discord
from bot import PollBot
import sys
import json

# Import the Secret Manager client library.
from google.cloud import secretmanager

# GCP project in which to store secrets in Secret Manager.
project_id = "discord-bot-demo-304514"

# ID of the secret to create.
secret_id = "discord-bot-token"

# Create the Secret Manager client.
secretmanager_client = secretmanager.SecretManagerServiceClient()

response=secretmanager_client.access_secret_version(
    name=f'projects/{project_id}/secrets/{secret_id}/versions/1'
)

# Print the secret payload.
#
# WARNING: Do not print the secret in a production environment - this
# snippet is showing how to access the secret material.
discord_bot_token = response.payload.data.decode("UTF-8")


with open('config.json') as config_file:
    config = json.load(config_file)
    config['discord_token']=discord_bot_token

bot = PollBot(config)
bot.run()