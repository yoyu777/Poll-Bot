import psycopg2 as postgresql

class Database:
	def __init__(self, databaseName, user, host):
		self.connection = postgresql.connect("dbname = '" + databaseName + "' user = '"+ user + "' host = '" + host + "'")
		self.cursor = self.connection.cursor()

	def createPoll(self, pollMessageID, channelID, endTime, serverID, final_options, title):
		print("Adding poll to database")
		self.cursor.execute("INSERT INTO polls VALUES (%s, %s, %s, %s, %s, %s);", (pollMessageID, channelID, endTime, serverID, final_options, title))
		self.connection.commit()
		print("Poll added to database")

	def removePoll(self, pollMessageID):
		print(pollMessageID)
		self.cursor.execute("DELETE FROM polls WHERE id = '" + str(pollMessageID) + "';")
		self.connection.commit()

	# Creates a premium user with the number of servers they bought, but does not activate any servers
	# It might seem like this function should be combined with addPremiumServer(),
	# but this allows me to add a premium user before a user requests a server to be activated
	def addPremium(self, userID, numServersPurchased):
		# First, check if the user already exists and has purchased servers
		self.cursor.execute("SELECT * FROM premium WHERE customer = '" +  userID + "';")
		data = self.cursor.fetchall()

		# Check if the user has already bought premium before
		if data is not None:
			previouslyPurchased = int(data[0][2])
			purchased = previouslyPurchased + int(numServersPurchased)
			self.cursor.execute("UPDATE premium SET serverspurchased = %s WHERE customer = %s;", (purchased, userID))
			self.connection.commit()
			print("servers added")
		else:
			self.cursor.execute("INSERT INTO premium VALUES (%s, %s, %s);", (userID, "{}", numServersPurchased))
			self.connection.commit()
			print("User added to database, with %s premium servers purchased", numServersPurchased)
