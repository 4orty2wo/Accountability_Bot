import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime, timedelta
import asyncio
import yaml

class DailyCheckInCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()
        self.check_in_message_channel_id = self.config['SESSION_PLANNING_CHANNEL_ID']  # Read from config.yml
        self.timezone = pytz.timezone('America/New_York')
        self.check_in.start()

    def load_config(self):
        with open('config.yml', 'r') as f:
            return yaml.safe_load(f)

    async def read_file(self, filepath):
        with open(filepath, 'r') as file:
            return file.read()

    async def format_message_with_pings(self, message, user_ids):
        pings = ' '.join([f'<@{user_id}>' for user_id in user_ids.splitlines()])
        return f"{pings}\n\n{message}"

    @tasks.loop(hours=24)
    async def check_in(self):
        now = datetime.now(self.timezone)
        if now.weekday() < 6:  # Monday (0) to Saturday (5)
            try:
                message = await self.read_file('assets/check_in_message.md')
                user_ids = await self.read_file('assets/check_in_pings.txt')
                formatted_message = await self.format_message_with_pings(message, user_ids)
                channel = self.bot.get_channel(self.check_in_message_channel_id)
                if channel:
                    await channel.send(formatted_message)
            except Exception as e:
                print(f"Error in sending daily check-in: {e}")

    @check_in.before_loop
    async def before_check_in(self):
        now = datetime.now(self.timezone)
        next_run_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
        if now.time() > next_run_time.time():
            next_run_time += timedelta(days=1)
        await discord.utils.sleep_until(next_run_time.astimezone(pytz.utc))

    def cog_unload(self):
        self.check_in.cancel()

def setup(bot):
    bot.add_cog(DailyCheckInCog(bot))
