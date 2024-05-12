import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from db import createTables, insertUser, insertChannel, insertMessage, getLastNMessages, getLastNMessagesChannel
from format_utils import formatMessages, formatChannelMessages

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
    # Creer les table dans la BD si elles n'existent pas
    await createTables()

    # Inserer les utilisateurs dans la BD
    for guild in bot.guilds:
        for member in guild.members:
            print(member.id)
            await insertUser(member.id, member.name)
    
    channels = bot.guilds[0].text_channels
    # Inserer les canaux dans la BD
    for channel in channels:
        await insertChannel(channel.id, channel.name)

    # Inserer les messages dans la BD
    for channel in channels:
        channel_info = bot.get_channel(channel.id)
        try:
            messages = [message async for message in channel_info.history()]
            for message in messages:
                await insertMessage(message.id, message.content, message.author.id, channel.id, message.created_at)
        except Exception as e:
            print(f"An error occurred: {e}")

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

@bot.command(name='show-message')
async def showMessage(ctx, n=None, username=None):
    if username is None:
        await ctx.send('Please enter a username')
        return
    
    if n is None:
        await ctx.send('Please enter n')
        return
    
    elif int(n) < 0 or int(n) > 5:
        await ctx.send('Please enter n between 0 and 5')
        return
        
    messages = await getLastNMessages(n, username)
    await ctx.reply(formatMessages(messages))

@bot.command(name='show-message-channel')
async def showMessageChannel(ctx, n=None, channel_id=None):
    if channel_id is None:
        await ctx.send('Please enter a channel_id')
        return
    
    if n is None:
        await ctx.send('Please enter n')
        return
    
    elif int(n) < 0 or int(n) > 5:
        await ctx.send('Please enter n between 0 and 5')
        return
        
    messages = await getLastNMessagesChannel(n, channel_id)
    await ctx.reply(formatChannelMessages(messages))

bot.run(TOKEN)
