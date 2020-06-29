import discord
import spotipy
import os
import shutil
from discord.ext import commands
from discord.utils import get
import youtube_dl
import urllib.request
from bs4 import BeautifulSoup

songs = []
players = {}
links = []
queues = []
links = []


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        s = track['name'] + ' by ' + track['artists'][0]['name']
        songs.append(s)


def get_playlist(username):
    # GO TO THIS LINK AND GET A NEW TOKEN: https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=7kjMZjI0zzQN1ZFfuEm34Z&market=&fields=&limit=&offset=
    token = 'BQAm5mmq7H83BFT0pVP2E2ysMdjiUKC9UtKoG5TQ5uedV1OkS6xS-m686HnzalhvMzzmWbxRTOja-5e3uW7nAe4zPC5-PR-22YB3GQxomNohndxp8VWYrRbI-TksM0mG8EJoVMlD37B7'

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                results = sp.playlist(playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)


def convert_link(pos):  # converts one link only and takes a postion in the link array
    query = urllib.parse.quote(songs[pos])
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    try:
        vid = soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
        link = 'https://www.youtube.com' + vid
        links.append()
    except:
        print('unable to convert song to YouTube link' + songs[pos])


client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    print('welcome')


@client.event
async def on_member_remove(member):
    print(str(member) + ' bye')


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"the bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('music paused')
        voice.pause()
        await ctx.send('Music paused')
    else:
        print('music not playing, failed pause')
        await ctx.send('music not playing, failed pause')


@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print('Resumed music')
        voice.resume()
        await ctx.send('resumed music')
    else:
        print('music is not paused; failed resume')
        await ctx.send('music is not paused failed resume')


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()
    queue_infile = os.path.isdir('./Queue')
    if queue_infile is True:
        shutil.rmtree('./Queue')

    if voice and voice.is_connected():
        if voice and voice.is_playing():
            print('music paused')
            voice.stop()

        await voice.disconnect()
        print(f"bot has left {channel}")
        await ctx.send(f"left {channel}")
    else:
        print("bot was told to leave channel but was not in")
        await ctx.send("i am not in voice")


@client.command()
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print('playing next song')
        voice.stop()
        await ctx.send('Song Skipped')

    else:
        print('music not playing, failed skip')
        await ctx.send('music not playing, failed skip')


@client.command()
async def volume(ctx, volume: int):
    if ctx.voice_client is None:
        return await ctx.send('not connected to voice channel')
    print(volume / 100)

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f'volume set to: {volume}%')


@client.command()
async def play(ctx, url: str):
    await join(ctx)
    print(url)
    if url.startswith('https') is False:

        query = urllib.parse.quote(url)
        url = "https://www.youtube.com/results?search_query=" + query
        print(url)
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.find(attrs={'class':'yt-uix-tile-link'})['href'])

        try:
            vid = soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
            url = 'https://www.youtube.com' + soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
            print(url)
        except:
            print('skipped ' + url)
            await ctx.send('could not play song')
            return

    def check_queue():
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print('no more songs in queue')
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                print('song done. playing next song')
                print(f'songs still in queue: {still_q}')
                song_there = os.path.isfile('song.mp3')
                if song_there:
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('no songs were queueed before the ending of the last song')

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file but its being played")
        await ctx.send("ERROR Music playing")
        return

    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('removed old queue folder')
            shutil.rmtree(Queue_folder)
    except:
        print('no old queue folder')

    await ctx.send("Getting song ready now!")
    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('dowloading audio now')
        try:
            ydl.download([url])
        except:
            print("can't download song || try: youtube-dl --rm-cache-dir or pip install --upgrade youtube-dl")
            return
    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    # voice.source = 0.01
    try:
        nname = name.rsplit('-', 2)
        await ctx.send(f'playing: {nname[0]}')
    except:
        await ctx.send('playing song')
    print('playing')


@client.command()
async def queue(ctx, url: str):
    if url.startswith('https') is False:

        query = urllib.parse.quote(url)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib.request.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.find(attrs={'class':'yt-uix-tile-link'})['href'])

        try:
            vid = soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
            url = 'https://www.youtube.com' + soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
            print(url)
        except:
            print('skipped ' + url)
            await ctx.send('could not play song')
            return

    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath('Queue'))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues.append(q_num)

    queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('dowloading audio now')
        try:
            ydl.download([url])
        except:
            print(f'this throws an error and was skipped: {url}')

    await ctx.send('adding song ' + url + ' to the queue')
    print('song added to the queue')


@client.command()
async def spot(ctx, username='ammarfatehi'):
    await join(ctx)
    voice = get(client.voice_clients, guild=ctx.guild)
    songs.clear()

    print(f'getting songs from user: {username}')
    get_playlist(username)  # gets the songs in string form
    print(f'converting {len(songs)} songs')
    print(songs)
    print(f'playing song: {songs[0]}')
    await play(ctx, songs[0])
    for song in range(1,len(songs)):
        await queue(ctx, songs[song])
        print('yes')

    await ctx.send('done queueing up songs')


@client.command()
async def Help(ctx):
    await ctx.send(
        '.clear # clears # of lines in chat \n .join joins voice channel \n .play ["name of song"] plays the song '
        '\n .queue ["name of song"] queues up a song \n .pause pauses music \n .resume resumes music '
        '\n .stop stops all music and clears queue \n .leave leaves voice channel \n .skip skips current song '
        '\n .volume # input a number >1 to change volume \n .spot [spotify username] plays all public playlist for the username, still in work dont make it play more than 20 songs at once it will break plz')


client.run('')  # PUT YOUR DISCORD TOKEN IN THE ' '
