import discord
from discord.ext import commands

class SendMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_user_id = 213678267155087360  # Replace with your Discord user ID

    @commands.command(name='send_message')
    async def send_message(self, ctx, channel_id: int, *, message: str):
        # Check if the author is you and if the command is invoked in DM
        if ctx.author.id != self.my_user_id or not isinstance(ctx.channel, discord.DMChannel):
            return  # Silently ignore if not from you or not in DMs

        # Find the channel
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await ctx.send(f"Channel with ID {channel_id} not found.")
            return

        # Check if the bot can send messages to the channel
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("The specified ID does not belong to a text channel.")
            return

        # Try sending the message
        try:
            await channel.send(message)
            await ctx.send(f"Message sent to channel {channel.name}.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to send messages to this channel.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(SendMessageCog(bot))
