from discord.ext import commands
from discord.flags import Intents
import discord
from music import get_link, download_video, find_music, remove_files, delete_audio
from time import sleep
import asyncio
from discord import FFmpegPCMAudio
from key import ffmpeg_path

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

music_playing = False
music_loop = False

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
        music_playing = False
        music_loop = False

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
async def play(ctx, *, title):

    remove_files()  

    global music_playing
    global music_loop

    download_video(title)
    voice_channel = ctx.author.voice.channel

    if not ctx.voice_client:
        voice_channel = await voice_channel.connect()

    try:
        async with ctx.typing():
            player = FFmpegPCMAudio(executable=r'D:\_Projetos Maiores\DJ Bot\ffmpeg\bin\ffmpeg.exe', source=f"music/{find_music()}")
            ctx.voice_client.play(player, after=lambda e: on_music_end(ctx, e))
        await ctx.send('Reproduzindo a música: {}'.format(find_music()))

        music_playing = True

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
            sleep(1)

        if music_loop:
            await play_in_loop(ctx)

        remove_files()

    except Exception as e:
        await ctx.send(f'Error: {e}')
        music_playing = False

@bot.command(name="loop")
async def loop(ctx):
    global music_loop

    if music_playing == True:
        music_loop = not music_loop
        if music_loop:
            await ctx.send('Reproduzindo em loop...')
        else:
            await ctx.send('Loop desativado')
            await asyncio.sleep(2)  
    else:
        await ctx.send('Não há nenhuma música reproduzindo no momento')
    
# Comandos Basicos

@bot.command(name="oi")
async def oi(ctx):
    await ctx.send("Oi!")

saudacoes = ['oi', 'ola', 'iae', 'iai']
async def process_messages(message):
    
    if message.content.lower().startswith(tuple(f"!{keyword}" for keyword in saudacoes)) and not message.author.bot:
        await message.channel.send('Ola {}!'.format(message.author.name))

# Funções de Loop
        
def verify_loop(loop):
    if loop == True:
        is_looping = True
        return is_looping
    else:
        is_looping = False
        return is_looping

def on_music_end(ctx, error):
    global music_playing
    music_playing = False

async def play_in_loop(ctx):
    global music_playing

    while music_loop and ctx.voice_client:
        await asyncio.sleep(1)
        if not ctx.voice_client.is_playing() and not music_playing:
            download_video(find_music())
            player = FFmpegPCMAudio(executable=r'D:\_Projetos Maiores\DJ Bot\ffmpeg\bin\ffmpeg.exe', source=f"music/{find_music()}")
            ctx.voice_client.play(player, after=lambda e: on_music_end(ctx, e))
            await ctx.send('Reproduzindo a música em loop: {}'.format(find_music()))
            music_playing = True