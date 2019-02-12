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

	def checkForCompletePolls(self, time):
		completedPolls = []
		print("Checking for completed polls")
		return completedPolls