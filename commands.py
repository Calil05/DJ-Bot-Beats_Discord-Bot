from discord.ext import commands
from discord.flags import Intents
import discord
from music import get_link, download_video, find_music, remove_files, delete_audio
from time import sleep
import asyncio
from discord import FFmpegPCMAudio
from key import path

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

# Comandos de musica

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause() 
        await ctx.send("Pausano audio")
    else:
        await ctx.send("Ocorreu um erro: Você deve estar em algum canal de voz para executar esse comando")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume() 
        await ctx.send("Voltando a tocar")
    else:
        await ctx.send("Ocorreu um erro: Você deve estar em algum canal de voz para executar esse comando") 

@bot.command()
async def leave(ctx): 
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Saindo do canal de voz")
        sleep(1)
        remove_files()

    else:
        await ctx.send("Ocorreu um erro: Você deve estar em algum canal de voz para executar esse comando")

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("No voice channel")

@bot.command(name="play")
async def play(ctx,*,title):
    download_video(title)
    voice_channel = ctx.author.voice.channel
   
    if not ctx.voice_client:
        voice_channel = await voice_channel.connect()

    try:
        async with ctx.typing():
            player = FFmpegPCMAudio(executable=path, source=f"music/{find_music()}") #executable part is where we downloaded ffmpeg. We are writing our find_mmusic name func because , we want to bot to play our desired song fro the folder
            ctx.voice_client.play(player, after=lambda e: print('Erro no Player: %s' % e) if e else None)
        await ctx.send('Reproduzindo a musica: {}'.format(find_music())) #sening confirmmation

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
            sleep(1)
        remove_files()

    except Exception as e:
        await ctx.send(f'Error: {e}')

# Comandos Basicos

@bot.command(name="oi")
async def oi(ctx):
    await ctx.send("Oi!")

saudacoes = ['oi', 'ola', 'iae', 'iai']
async def process_messages(message):
    
    if message.content.lower().startswith(tuple(f"!{keyword}" for keyword in saudacoes)) and not message.author.bot:
        await message.channel.send('Ola {}!'.format(message.author.name))