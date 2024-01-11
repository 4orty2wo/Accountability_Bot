import os, asyncio
from datetime import datetime, time, timedelta
from discord.ext import tasks, commands

class DailyCheckin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("SESSION_PLANNING_CHANNEL_ID"))
        self.last_sent_file = 'last_sent.txt'  # File to store the timestamp of the last sent message
        self.daily_message.start()


    def was_message_sent_today(self):
        try:
            with open(self.last_sent_file, 'r') as f:
                last_sent = datetime.fromisoformat(f.read().strip())
                return last_sent.date() == datetime.now().date()
        except (FileNotFoundError, ValueError):
            return False


    def mark_message_as_sent(self):
        with open(self.last_sent_file, 'w') as f:
            f.write(datetime.now().isoformat())


    @tasks.loop(hours=24)
    async def daily_message(self):
        if datetime.now().weekday() == 6:  # Sunday is 6
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
                dt = datetime.now().strftime("%A, %d %B %Y, %H:%M")

                # Combine message content and user mentions
                full_message = f"{dt}\n\nGood morning {user_mentions}!\n\n{message_content}"

                await channel.send(full_message)


    @daily_message.before_loop
    async def before_daily_message(self):
        await self.bot.wait_until_ready()

        while True:
            now = datetime.now()
            target_time = time(9, 0)  # 9 AM
            target_datetime = datetime.combine(now.date(), target_time)

            if now.weekday() != 6:  # Check if it's not Sunday
                if now < target_datetime or self.was_message_sent_today():
                    # Wait until the next day's 9 AM if it's before 9 AM or if today's message is already sent
                    sleep_duration = (target_datetime - now).total_seconds()
                    if sleep_duration < 0:
                        sleep_duration += 86400  # Add a day in seconds
                    await asyncio.sleep(sleep_duration)
                else:
                    # It's after 9 AM, and today's message hasn't been sent
                    await self.daily_message()
                    break
            else:
                # If it's Sunday, wait until Monday 9 AM
                sleep_duration = (target_datetime - now).total_seconds() + 86400  # Skip to next day
                await asyncio.sleep(sleep_duration)


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
