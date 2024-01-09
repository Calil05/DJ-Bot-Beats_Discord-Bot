from discord.ext import commands
from discord.flags import Intents
import discord
from music import get_link, download_video, find_music ,remove_files
from time import sleep

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@commands.command(name="oi")
async def oi(ctx):
    await ctx.send("Oi!")

saudacoes = ['oi', 'ola', 'iae', 'iai']
async def process_messages(message):
    
    if message.content.lower().startswith(tuple(f"!{keyword}" for keyword in saudacoes)) and not message.author.bot:
        await message.channel.send('Ola {}!'.format(message.author.name))