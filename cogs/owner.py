import discord
from discord.ext import commands
from cogs.utils.Database import Database


class Owner:

	def __init__(self, bot):
		self.bot = bot
		self.database = Database("sample_db", "finn", "localhost")

	# thanks to evieepy on github for these cogs commands 
	# https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
	@commands.command(name = "load", hidden = True)
	@commands.is_owner()
	async def cog_load(self, ctx, *, cog: str):
		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send("**`ERROR:`**")
		else:
			await ctx.send("**`SUCCESS`**")

	@commands.command(name = "unload", hidden = True)
	@commands.is_owner()
	async def cog_unload(self, ctx, *, cog: str):
		print(cog)
		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send('**`ERROR:`**')
		else:
			await ctx.send('**`SUCCESS`**')

	@commands.command(name='reload', hidden=True)
	@commands.is_owner()
	async def cog_reload(self, ctx, *, cog: str):
		try:
			self.bot.unload_extension(cog)
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send('**`ERROR:`**')
		else:
			await ctx.send('**`SUCCESS`**')

	# Check how many unclaimed premium servers a user has and total # of premium servers they have purchased
	# Format: +checkpremium {userID}
	@commands.command(name="checkpremium")
	@commands.is_owner()
	async def checkpremium(self, ctx):
		message = ctx.message.content
		userID = message.split(" ")[1]
		self.database.checkPremium(userID)
		emb1 = discord.Embed(description=self.database.checkPremium(userID))
		await ctx.message.channel.send(embed=emb1)

	# Adds the number of premium servers a user bought to the database
	# Format: +addpremium {userID} {numServersPurchased}
	@commands.command(name="addpremium")
	@commands.is_owner()
	async def addpremium(self, ctx):
		print(ctx.message.content)
		message = ctx.message.content
		userID = message.split(" ")[1]
		numServersPurchased = message.split(" ")[2]
		emb1 = discord.Embed(description=self.database.addPremium(userID, numServersPurchased))
		await ctx.message.channel.send(embed=emb1)

	# Gives a server of a user's request premium if they have any unclaimed premium servers
	# Format: +addpremiumserver {userID} {serverIDToAdd}
	@commands.command(name="addpremiumserver")
	@commands.is_owner()
	async def addpremiumserver(self, ctx):
		message = ctx.message.content
		userID = message.split(" ")[1]
		serverIDToAdd = message.split(" ")[2]
		emb1 = discord.Embed(description=self.database.addPremiumServer(userID, serverIDToAdd))
		await ctx.message.channel.send(embed=emb1)

	# Changes one of the user's premium servers to another server
	# Format: +changepremium {userID} {previousServerID} {newServerID}
	# NOT IMPLEMENTED
	@commands.command(name="changepremium")
	@commands.is_owner()
	async def changepremium(self, ctx):
		message = ctx.message.content
		userID = message.split(" ")[1]
		previousServerID = message.split(" ")[2]
		newServerID = message.split(" ")[3]
		self.database.changePremium(userID, previousServerID, newServerID)
		emb1 = discord.Embed(description=self.database.changePremium(userID, previousServerID, newServerID))
		await ctx.message.channel.send(embed=emb1)

def setup(bot):
	bot.add_cog(Owner(bot))
