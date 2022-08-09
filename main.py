# Authors: rothman & mike
import os
import discord
import sqlite3

from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
load_dotenv()

debug = True

# Create a client object from the discord.py module
bot = commands.Bot(command_prefix='$', intents=intents)

# This function listens for server join events
# and initializes the new user information into
# a database if the user hasn't joined before. 
@bot.event
async def on_member_join(user):    
    # Establish connection to database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Create the table if it doesn't already exist
    create_query = """CREATE TABLE IF NOT EXISTS users (id INTEGER, xp INTEGER)"""
    cursor.execute(create_query)

    # Select only the user ID column
    select_query = """SELECT id FROM users"""
    cursor.execute(select_query)

    ids = {data[0] for data in cursor.fetchall()}
    
    if not user.id in ids:
        cursor.execute("""INSERT INTO users (id, xp) VALUES (?, ?)""", (user.id, 0))
        if debug: print(f"[Debug] Added {user.id} to the database.")
    else:
        if debug: print(f"[Debug] {user.id} is already in the database.")
    
    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
    
    # Get the welcome channel ID and send a welcome message
    # channel = bot.get_channel(1006419916351611051)
    # await channel.send(f"{user.mention} has joined the server!")

# Listen for when the bot switches states
@bot.event
async def on_ready():
    server_count = 0

    for server in bot.guilds:
        server_count += 1

    print("[Info] Derek-Bot is online. (" + str(server_count) + ")")

# Listen for when a new message is sent
@bot.event
async def on_message(msg):
    # If the message is a command
    if msg.content == "$test":
        await msg.channel.send("confirmed")
    
# Run the bot
bot.run(os.getenv("TOKEN")) 
