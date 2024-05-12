import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command(name='hey')
async def hey(ctx):
    await ctx.send('Hey  ❤️')

@bot.command(name='who-am-i')
async def whoami(ctx):
    message = f'You are: {ctx.author.name}\nYour id is: {ctx.author.id}\nYour avatar is: {ctx.author.avatar.key}\nThis server id is: {ctx.author.guild.id}'
    await ctx.send(message)

bot.run(TOKEN)
