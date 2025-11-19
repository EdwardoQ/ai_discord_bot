import discord
from discord.ext import commands
from ai import scavenger_hunt
import os
import asyncio  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def scavenger(ctx):
    await ctx.send("Please upload your picture containing the item within the next 60 seconds.")
    # define a check so we only listen to this user's next message
    def check(message):
        return message.author == ctx.author and len(message.attachments) > 0

    try:
        # wait for user to send a file within 60 seconds
        message = await bot.wait_for('message', check=check, timeout=60.0)

        # get first attachment
        attachment = message.attachments[0]
        file_path = f"./downloads/{attachment.filename}"

        # save file to local folder
        await attachment.save(file_path)
        await ctx.send(f"✅ File `{attachment.filename}` has been inputted!")
        result = scavenger_hunt(attachment.filename)
        await ctx.send(f"{result}")

    except asyncio.TimeoutError:  
        await ctx.send("⏰ You took too long to upload a file.")

bot.run("token")
