import discord
from player import Player
from random import randint
from plugins.cm import Database
from plugins.logger import Logger

class Paul(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        print("[INFO] Bot online.")
    
    def create_table(self):
        with Database() as db:
            db.cursor.execute("""CREATE TABLE IF NOT EXISTS players (
                uid INT PRIMARY KEY,
                exp INT NOT NULL,
                lvl INT NOT NULL )""")
        Logger.log.info("Players table created.")
    
    async def on_ready(self):        
        self.create_table()
        for user in self.users:
            if not user.bot:
                player = Player(user.id)
                if not player.locate_uid():
                    player.add_to_db() 
                elif not user.bot:
                    Logger.log.info("%s already found.", player.uid)
        Logger.log.info("User data loaded.")
        print("[INFO] User data loaded.")
        
    async def on_member_join(self, member):
        if not member.bot:
            player = Player(member.id)
            if not player.locate_uid():
                player.add_to_db()
            else:
                Logger.log.info("%s already found.", player.uid)

    async def on_message(self, msg):
        if not msg.author.bot:
            player = Player(msg.author.id)
            gain = randint(*(15, 25))
            
            db_exp = player.locate_exp()
            db_lvl = player.locate_lvl()
            
            player.exp = gain + db_exp
            player.lvl = player.get_lvl()
            player.update(player.exp, player.lvl)
            
            Logger.log.info("lvl: %s xp: %s", db_lvl, db_exp)
            print(f"LVL: {db_lvl} XP: {db_exp}")              
            
            if msg.content == "$data":
                embed_var = discord.Embed(title="", description="", color=0x2b2b2b)
                embed_var.add_field(name="ID", value=str(player.uid), inline=True)
                embed_var.add_field(name="XP", value=str(player.locate_exp()), inline=True)
                embed_var.add_field(name="LVL", value=str(player.locate_lvl()), inline=True)
                await msg.channel.send(embed=embed_var)
