from pytube import Search
from pytube import YouTube
import os
import shutil    

music_folder = 'D:\_Projetos Maiores\DJ Bot\DJ-Bot-Beats_Discord-Bot\music'

def get_link(name):
    search_music = Search(f"{name}")
    yt_id = search_music.results
    video_ids = [video.video_id for video in yt_id]

    video_id = video_ids[0]
    base_url = f"https://www.youtube.com/watch?v={video_id}"
    return base_url

def download_video(name):
    search_music = Search(f"{name}")
    yt_id = search_music.results
    video_ids = [video.video_id for video in yt_id]

    if (name.startswith("https://")):
        print("Processing URL:", name)
        yt = YouTube(name)
    else:
        print("Processing query:", name)
        video_id = video_ids[0]
        base_url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(base_url)

    output_path = 'music'
    os.makedirs(output_path, exist_ok=True)

    try:
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        if audio_stream:
            audio_stream.download(output_path=output_path)
            print(f"Downloaded: {yt.title}")
        else:
            print(f"No available audio streams for: {yt.title}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def find_music():
    return (os.listdir("music")[0])

def delete_audio():
    shutil.rmtree('music')

def remove_files():
    for filename in os.listdir(music_folder):
        file_path = os.path.join(music_folder, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as err:
            print('Erro ao deletar arquivos: ', err)

