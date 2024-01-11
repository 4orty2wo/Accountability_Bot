import os, logging, asyncio
import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandError
from pymongo import MongoClient
from dotenv import load_dotenv


# Use environment variables for sensitive data
# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')


# Configure the logging level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)  # Set this to DEBUG to log all messages, or INFO for less verbosity


# Initialize Discord bot
intents = Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize MongoDB client
# mongo_client = MongoClient(MONGO_CONNECTION_STRING)
# db = mongo_client.your_database_name


@bot.event
async def on_ready():

    print(f'We have logged in as {bot.user}')
      
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

	# LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("Accountability Bot is in " + str(guild_count) + " guilds.")


# Additional commands and error handling here



@bot.event
async def on_message(message):
    # Your custom on_message logic
    if message.author == bot.user:
        return


@bot.command(name='ping')
async def ping(ctx):
    print('ping')
    await ctx.send("Pong!")


async def run_bot():
    await bot.start(BOT_TOKEN)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_bot())


