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
		if data != []:
			print(data)
			previouslyPurchased = int(data[0][2])
			purchased = previouslyPurchased + int(numServersPurchased)
			self.cursor.execute("UPDATE premium SET serverspurchased = %s WHERE customer = %s;", (purchased, userID))
			self.connection.commit()
			return "Added " + str(numServersPurchased) + " to user " + str(userID)
		else:
			self.cursor.execute("INSERT INTO premium VALUES (%s, %s, %s);", (userID, "{}", numServersPurchased))
			self.connection.commit()
			return "User " + str(userID) + " added to database and " + str(numServersPurchased) + " servers added to user."
			print("User added to database, with %s premium servers purchased", numServersPurchased)

	# Registers a premium server for a user. Check if a user has any unregistered servers using checkPremium
	def addPremiumServer(self, userID, serverID):
		self.cursor.execute("SELECT * FROM premium WHERE customer = '" +  userID + "';")
		data = self.cursor.fetchall()
		if data != []:
			print(data)
			servers = data[0][1][1:-1].split(",")
			print(servers)
			if serverID in servers:
				return "Server was already registered as a premium server for that user."
			else:
				servers.append(str(serverID))
				servers.remove('')
				print(serverID)
				print(type(servers))
				print(servers)
				self.cursor.execute("UPDATE premium SET server_ids = %s WHERE customer = %s;", (servers, userID))
				self.connection.commit()
				return "Server ID added"
		else:
			servers = [serverID]
			self.cursor.execute("UPDATE premium SET server_ids = %s WHERE customer = %s;", (servers, userID))
			self.connection.commit()
			return "Server ID added"
	
	# Checks how many servers a user has purchased and how many servers a user has registered.
	def checkPremium(self, userID):
		self.cursor.execute("SELECT * FROM premium WHERE customer = '" +  userID + "';")
		data = self.cursor.fetchall()
		
		# If the user has already bought premium
		if data != []:
				print(data)
				print(type(data))
				servers = data[0][1][1:-1].split(",") 
				return str(userID) + " has purchased " + data[0][2] + " server(s) and has registered " + str(len(servers)-1) + " server(s)."
		else:
			return str(userID) + " has not purchased any premium servers."

	# Switches the ids of servers
	# This does not work yet
	def changePremium(self, userID, previousServerID, newServerID):
		self.cursor.execute("SELECT * FROM premium WHERE customer = '" +  userID + "';")
		data = self.cursor.fetchall()

		if data != []:
			servers = data[0][1][1:-1].split(",") 
			print(servers)
			switched = False
			for i in range(len(servers)):
				# TODO: This if statement is not returning true when it should.
				if servers[i] == str(previousServerID) and not switched:
					print(servers[i])
					print(newServerID)
					servers[i] = newServerID
					switched = True
					print(servers)
					self.cursor.execute("UPDATE premium SET server_ids = %s WHERE customer = %s;", (servers, userID))
					print("got to here")
					self.connection.commit()
					return "Successfully removed server " + previousServerID + " and added " + newServerID + " for user " + userID 
		else:
			return str(userID) + " has not purchased any premium servers"