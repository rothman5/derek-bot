from plugins.cm import Database
from plugins.logger import Logger

EXP_TARGETS_LIST = [5*(lvl**2) + 50*lvl + 100 for lvl in range(200)]

class Player:
	def __init__(self, user_id):
		self.exp_targets = EXP_TARGETS_LIST
		self.uid = user_id
		self.exp = 0
		self.lvl = 0

	def add_to_db(self):
		with Database() as db:
			db.cursor.execute("""INSERT INTO players (uid, exp, lvl) VALUES (:uid, :exp, :lvl)""",
				{'uid': self.uid, 'exp': self.exp, 'lvl': self.lvl})
			Logger.log.info("%s added to database.", self.uid)
			print(f"[INFO] {self.uid} added to database.")
	
	def update(self, new_exp, new_lvl):
		with Database() as db:
			db.cursor.execute("""UPDATE players SET exp = :exp, lvl = :lvl WHERE uid = :uid""",
				{'uid': self.uid, 'exp': new_exp, 'lvl': new_lvl})
			Logger.log.info("%s's xp and level updated.", self.uid)

	def locate_uid(self):
		with Database() as db:
			db.cursor.execute("""SELECT uid FROM players WHERE uid = :uid""", {'uid': self.uid})
			return db.cursor.fetchone()
		
	def locate_exp(self):
		with Database() as db:
			db.cursor.execute("""SELECT exp FROM players WHERE uid = :uid""", {'uid': self.uid})
			return int(db.cursor.fetchone()[0])
		
	def locate_lvl(self):
		with Database() as db:
			db.cursor.execute("""SELECT lvl FROM players WHERE uid = :uid""", {'uid': self.uid})
			return int(db.cursor.fetchone()[0])

	def get_lvl(self):
		remaining = self.exp
		lvl = 0
		while remaining >= self.exp_targets[lvl]:
			remaining -= self.exp_targets[lvl]
			lvl += 1
		return lvl	
