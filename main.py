import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


@bot.command()
@commands.has_role('.say')  # Restrict the command to users with the .say role
async def say(ctx, user: discord.User, *, message):
    # Delete the command message as soon as possible
    await ctx.message.delete()

    # Fetch the user's profile picture URL
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    # Create a webhook in the current channel
    webhook = await ctx.channel.create_webhook(name="Message Relay")

    try:
        # Use the webhook to send a message with the user's name and avatar
        await webhook.send(content=message,
                           username=user.display_name,
                           avatar_url=avatar_url)
    finally:
        # Delete the webhook after use
        await webhook.delete()


# Error handling for missing role
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the required role to use this command.",
                       delete_after=5)


# Run the bot with the token
bot.run(os.getenv("DISCORD_TOKEN"))
