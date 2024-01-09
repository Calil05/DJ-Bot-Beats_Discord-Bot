from  discord.ext import commands,tasks
from discord.flags import Intents
from key import token
from comands import oi, process_messages
import discord
from discord import Color

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.event
async def on_ready():  
    try:
        print('Discord bot succesfully connected')
    except:
        print("[!] Couldn't connect, an Error occured")

bot.add_command(oi)

@bot.event
async def on_message(message):
    await process_messages(message)

bot.run(token)