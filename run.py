import discord
from discord.ext import commands
import logging
import config
import aiohttp

logging.basicConfig(level=logging.INFO)
prefixes = ["+", "poll:", "Poll:", "POLL:"]
bot = commands.AutoShardedBot(command_prefix=prefixes, status=discord.Status.online, activity=discord.Game(name='+help'))
bot.remove_command("help")

extensions = (
                'cogs.poll',
                'cogs.strawpoll',
                'cogs.meta',
                'cogs.stats',
                'cogs.owner',
                'cogs.utils.BackgroundTasks'
            )


@bot.event
async def on_ready():
    bot.http_session = aiohttp.ClientSession()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

@bot.event
async def on_message(message):
    if not message.author.bot:
        if not "Direct Message with" in str(message.channel):
            await bot.process_commands(message)
        else:
            print("Someone tried to do commands in a private message")

def main():
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(config.discordToken)
main()
