import sqlite3
from plugins.logger import Logger

class Database:
	def __init__(self):
		self.path = 'data/store.db'
	
	def __enter__(self):
		self.connection: sqlite3.Connection = sqlite3.connect(self.path)
		self.cursor: sqlite3.Cursor = self.connection.cursor()
		Logger.log.info("Database connected.")
		return self
		
	def __exit__(self, exc_type, exc_val, traceback):
		self.cursor.close()
		self.connection.commit()
		self.connection.close()
