from discord.ext import commands
from key import token
from music_commands import join, pause, resume, leave, play
from commands.basic_commands import oi, process_messages
import discord
import sys

sys.path.insert(0, r'd:\_Projetos Maiores\DJ Bot\DJ-Bot-Beats_Discord-Bot')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.event
async def on_ready():
    try:
        print('Discord bot successfully connected')
    except Exception as e:
        print(f"[!] Couldn't connect, an error occurred: {e}")

# Adicionando comandos do arquivo music_commands.py
bot.add_command(join)
bot.add_command(pause)
bot.add_command(resume)
bot.add_command(leave)
bot.add_command(play)
bot.add_command(oi)

@bot.event
async def on_message(message):
    await process_messages(message)

bot.run(token)