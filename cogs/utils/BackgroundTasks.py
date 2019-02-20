import discord
from discord.ext import commands
import asyncio
from cogs.utils.Database import Database
from datetime import datetime, timedelta
from cogs.poll import Poll
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class BackgroundTasks:
	
	def __init__(self, bot):
		self.bot = bot
		self.poll = Poll(bot)
		self.database = Database("sample_db", "finn", "localhost")
		self._task = bot.loop.create_task(self.checkForCompletePolls())

	async def checkForCompletePolls(self):
		while not self.bot.is_closed():
			print("Doing the thing")
			currentTime = datetime.strptime(str(datetime.utcnow())[0:16], "%Y-%m-%d %H:%M")
			self.database.cursor.execute("SELECT * FROM polls")
			data = self.database.cursor.fetchall()
			for i in range(len(data)):
				if datetime.strptime(data[i][2], "%Y-%m-%d %H:%M") < currentTime:
					final_options = data[i][4]
					print("ending")
					await self.endDurationPoll(data[i][0], data[i][1], final_options[1:-1].split(","), data[i][5])
					self.database.removePoll(data[i][0])
			await asyncio.sleep(60)

	async def endDurationPoll(self, pollMessageID, channelMessageID, final_options, title):
		channel = self.bot.get_channel(int(channelMessageID))
		print(pollMessageID)
		pollMessage = await channel.get_message(int(pollMessageID))
		print("got past pollMessage")
		reactions = []
		for reaction in pollMessage.reactions:
		    async for user in reaction.users():
		        if user == self.bot.user:
		            reactions.append(reaction.count - 1)
		j = 0
		for i in range(len(reactions)):
		    j+=reactions[i]

		if not j==0: #if only the bot has reactions, nothing gets sent
			print("doing something")
			plt.subplots(figsize = (9,6))
			plt.bar(final_options, reactions, width = 0.8, bottom = 0)
			plt.title(title, fontsize=27)
			print("Should save")
			plt.savefig('results.png')
			print("saved")
			print(reactions)
			print(final_options)
			await channel.send('Results for a passed poll', file=discord.File('results.png'))

def setup(bot):
	bot.add_cog(BackgroundTasks(bot))