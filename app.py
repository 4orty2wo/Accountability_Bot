import os, logging, asyncio
import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandError
from pymongo import MongoClient
from dotenv import load_dotenv
import yaml
import datetime

load_dotenv()

# Use environment variables for sensitive data
BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

# Load the config file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

WELCOME_CHANNEL_ID = config['WELCOME_CHANNEL_ID']
AUDIT_CHANNEL_ID = config['AUDIT_CHANNEL_ID']

# Configure the logging level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)  # Set this to DEBUG to log all messages, or INFO for less verbosity


# Initialize Discord bot
intents = Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Initialize MongoDB client
# mongo_client = MongoClient(MONGO_CONNECTION_STRING)
# db = mongo_client.your_database_name


@bot.event
async def on_ready():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

    # Get the welcome channel
    welcome_channel = bot.get_channel(int(WELCOME_CHANNEL_ID))
    await welcome_channel.send(f"Bot started at {current_time}") # Note: This message will be sent to the welcome channel every time the bot starts


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


# Reload cogs without stopping the bot
@bot.command()
async def reload(ctx, cog: str):
    bot.reload_extension(f'cogs.{cog}')
    await ctx.send(f'{cog} reloaded')


@bot.command(name='ping')
async def ping(ctx):
    print('ping')
    await ctx.send("Pong!")


async def main():
    async with bot:
        await load()
        loaded_cogs = [cog for cog in bot.extensions]
        await bot.start(BOT_TOKEN)
        await bot.get_channel(int(AUDIT_CHANNEL_ID)).send(f"Bot started with cogs: {loaded_cogs}")


asyncio.run(main())