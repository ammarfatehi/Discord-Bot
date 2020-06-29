# this file is for ammars use only as it.
# the user is required to manual re-enter a new token every time the current token expires.
import asyncio
import discord
import youtube_dl
import sys
import spotipy
import spotipy.util as util
import os
import shutil
import urllib.request
from bs4 import BeautifulSoup

songs = []
players = {}
links = []


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        s = track['name'] + ' by ' + track['artists'][0]['name']
        songs.append(s)
    print(songs)


def get_playlist(username):
    if len(username) < 1:
        username = 'ammarfatehi'

    # GO TO THIS LINK AND GET A NEW TOKEN: https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=7kjMZjI0zzQN1ZFfuEm34Z&market=&fields=&limit=&offset=
    token = 'BQDbjoM7bRbYOrbanKpP2UJ8_nyRFueiUB2pfu7f8gZysB7vE6mvKpYEFYOrYqrxlwd0pCKTk2wFSz1op0BCB-Vk_1SORZUGmxJH4EFsn71L51wa2ua4iJZN__bela1BvkUdbXmPU8Q4'

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:

                results = sp.playlist(playlist['id'],
                                      fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)


played_first_song = False


def convert_link(pos):  # converts one link only and takes a postion in the link array
    query = urllib.parse.quote(songs[pos])
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.find(attrs={'class':'yt-uix-tile-link'})['href'])
    try:
        vid = soup.find(attrs={'class': 'yt-uix-tile-link'})['href']
        links.append('https://www.youtube.com' + soup.find(attrs={'class': 'yt-uix-tile-link'})['href'])
    except:
        print('FUCK THIS LINE ' + songs[pos])


# ------------------------------------------------------------

# discord part of things


from discord.ext import commands
from discord.utils import get
import youtube_dl

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
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"bot has left {channel}")
        await ctx.send(f"left {channel}")
    else:
        print("bot was told to leave channel but was not in")
        await ctx.send("i am not in voice")


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


queues = []


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
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()
    queue_infile = os.path.isdir('./Queue')
    if queue_infile is True:
        shutil.rmtree('./Queue')

    if voice and voice.is_playing():
        print('music paused')
        voice.stop()
        await ctx.send('Music stopped')
    else:
        print('music not playing, failed stopped')
        await ctx.send('music not playing, failed stopped')


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
async def Help(ctx):
    await ctx.send(
        '.clear # clears # of lines in chat \n .join joins voice channel \n .play ["name of song"] plays the song '
        '\n .queue ["name of song"] queues up a song \n .pause pauses music \n .resume resumes music '
        '\n .stop stops all music and clears queue \n .leave leaves voice channel \n .skip skips current song '
        '\n .volume # input a number >1 to change volume \n .spot [spotify username] plays all public playlist for the username, still in work dont make it play more than 20 songs at once it will break plz')


def que_size():
    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is True:
        DIR = os.path.abspath(os.path.realpath('Queue'))
        length = len(os.listdir(DIR))
        still_q = length - 1
        return still_q


@client.command()
async def spot(ctx, username: str):
    voice = get(client.voice_clients, guild=ctx.guild)
    await join(ctx)
    songs.clear()
    print(f'getting songs from user: {username}')
    get_playlist(username)  # gets the songs in string form
    print(f'converting {len(songs)} songs to youtube links')
    print(f'playing first song: {songs[0]}')
    await play(ctx, songs[0])
    print('queueing up next song in the playlist')
    await queue(ctx, songs[1])
    i = 2
    while i < len(songs):
        if que_size() < 2:
            print(f'queueing up next song in the playlist: {songs[i]}')
            await queue(ctx, songs[i])
            i = i + 1

    print('finished queueing up songs')


client.run('Njk1ODk0MDM5MzMyOTEzMjI0.XojrVQ.Wi2l3KZdwD4qmpr8hCu9B5gyH7w')
