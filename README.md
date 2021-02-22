A Discord bot that lets you create strawpolls and reaction polls

This repo is forked from https://github.com/stayingqold/Poll-Bot.
This fork allows you to host this bot on App Engine easily, and use Google Cloud Secret Manager to manage your Discord Tokens.

Video tutorials here:
- Creating a Discord Bot on App Engine: https://www.youtube.com/watch?v=aczvOQ6S6sA
- Using Secret Manager to Manage Tokens: https://www.youtube.com/watch?v=wb4RU5rpooQ
- Hosting a Poll Bot: https://www.youtube.com/watch?v=wUdZKMeLG4w

## 

## How to use Poll Bot
Create a strawpoll by typing '+strawpoll {title} [Option1] [Option2] [Option 3]', with up to 26 options.

Create a reaction poll by typing '+poll _____’. Poll Bot will automatically add the reactions 👍, 👎, and 🤷

Create a multi reaction poll type '+poll {title} [option 1] [option 2] [option 3]'

## Requirements

- Python 3.5.3+
- discord.py==1.6.0
- google-cloud-secret-manager==2.2.0

Usually `pip` will work for these
