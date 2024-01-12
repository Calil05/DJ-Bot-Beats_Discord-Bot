from discord.ext import commands
from key import token
from commands import join, pause, resume, leave, play, loop, oi, process_messages
import discord
import sys

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.event
async def on_ready():
    try:
        print('Bot foi conectado com sucesso')
    except Exception as err:
        print("Não foi possivel conectar devido ao erro: {}".format(err))

# Comandos de Musica
        
bot.add_command(join)
bot.add_command(pause)
bot.add_command(resume)
bot.add_command(leave)
bot.add_command(play)
bot.add_command(loop)

# Comandos Basicos

bot.add_command(oi)

# @bot.event
# async def on_message(message):
#     await process_messages(message)

bot.run(token)