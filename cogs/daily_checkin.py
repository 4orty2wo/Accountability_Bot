import os, asyncio
from datetime import datetime, time, timedelta
from discord.ext import tasks, commands
import yaml
import pytz


class DailyCheckin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = self.load_channel_id()
        self.last_sent_file = 'last_sent.txt'  # File to store the timestamp of the last sent message
        self.daily_message.start()

    def load_channel_id(self):
        with open('config.prod.yml', 'r') as f:
            config = yaml.safe_load(f)
            return int(config['SESSION_PLANNING_CHANNEL_ID'])

    def was_message_sent_today(self):
        try:
            with open(self.last_sent_file, 'r') as f:
                last_sent = datetime.fromisoformat(f.read().strip())
                return last_sent.date() == datetime.now(pytz.timezone('EST')).date()
        except (FileNotFoundError, ValueError):
            return False

    def mark_message_as_sent(self):
        with open(self.last_sent_file, 'w') as f:
            f.write(datetime.now().isoformat())

    @tasks.loop(hours=24)
    async def daily_message(self):
        if datetime.now(pytz.timezone('EST')).weekday() == 6:  # Sunday is 6
            return

        if not self.was_message_sent_today():
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                # Read the message content
                with open('checkin_message.txt', 'r') as file:
                    message_content = file.read()

                # Read user IDs and format them for mentions
                with open('users.txt', 'r') as file:
                    user_mentions = ' '.join([f'<@{line.strip()}>' for line in file if line.strip()])

                # Get the current date and time
                dt = datetime.now(pytz.timezone('EST')).strftime("%A, %d %B %Y, %H:%M")

                # Combine message content and user mentions
                full_message = f"{dt}\n\nGood morning {user_mentions}!\n\n{message_content}"

                await channel.send(full_message)

    @daily_message.before_loop
    async def before_daily_message(self):
        await self.bot.wait_until_ready()

        now = datetime.now(pytz.timezone('EST'))
        target_time = time(9, 0)  # 9 AM
        target_datetime = datetime.combine(now.date(), target_time)

        if now.weekday() != 6:  # Check if it's not Sunday
            if now < target_datetime:
                sleep_duration = (target_datetime - now).total_seconds()
                await asyncio.sleep(sleep_duration)
            elif not self.was_message_sent_today():
                await self.daily_message()

    @daily_message.after_loop
    async def after_daily_message(self):
        # Handle any error or interruption here
        pass

    # Run daily_message when the cog is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        await self.before_daily_message()

async def setup(bot):
    await bot.add_cog(DailyCheckin(bot))
