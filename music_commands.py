from discord.ext import commands
from discord.flags import Intents
import discord
from music import get_link, download_video, find_music, remove_files, delete_audio
from time import sleep
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing(): # if the music is already playing 
        ctx.voice_client.pause() #pausing the music 
        await ctx.send("Playback paused.") #sending confirmation on  channel
    else:
        await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand') #if you are not in vc

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused(): # If the music is already paused
        ctx.voice_client.resume() #resuming the music
        await ctx.send("Playback resumed.")#sending confirmation on  channel
    else:
        await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand') #if you are not in vc

@bot.command()
async def leave(ctx): 
    if ctx.voice_client: #if you are in vc 
        await ctx.guild.voice_client.disconnect() #disconnecting from the vc
        await ctx.send("Lefted the voice channel") #sending confirmation on channel
        sleep(1)
        remove_files("music") #deleting the all the files in the folder that  we downloaded to not waste space on your pc

    else:
        await ctx.send("[-] An Error occured: You have to be in a voice channel to run this command") #if you are not in vc

@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("No voice channel")

@bot.command(name="play")
async def play(ctx,*,title):
    download_video(title) # Downloading the mp4 of the desired vid
    voice_channel = ctx.author.voice.channel
   
    if not ctx.voice_client: #if you are not in  vc 
        voice_channel = await voice_channel.connect() #connecting to vc

    try:
        async with ctx.typing():
            player = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\ffmpeg.exe", source=f"music/{find_music()}") #executable part is where we downloaded ffmpeg. We are writing our find_mmusic name func because , we want to bot to play our desired song fro the folder
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f'Now playing: {find_music()}') #sening confirmmation

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        delete_audio(find_music()) # deleting the file after it played

    except Exception as e:
        await ctx.send(f'Error: {e}') #sending error 