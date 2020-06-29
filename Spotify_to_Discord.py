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


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        s = track['name']+' by '+track['artists'][0]['name']
        songs.append(s)


username = input('give me username: ')
if __name__ == '__main__':
    if len(username) < 1:
        username = 'ammarfatehi'
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        sys.exit()
    token = input('give me a token: ')
    if len(token) < 1:
        # GO TO THIS LINK AND GET A NEW TOKEN: https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=7kjMZjI0zzQN1ZFfuEm34Z&market=&fields=&limit=&offset=
        token = 'BQBTecf6kh1HV6vAqcBO81P5dx6ovBFoojjU0-v6Pr_tyqCeIuwLQe_r5Cguazq_cowABD8H7YlXqd_qvlRvVhjiCJ3XKZ5ta0ryXkE1Z9fATiZJ_HhFw_tURtw3tX2DIdcCuodGITW2'

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

#------------------------------------------------------------------------------------
#converting song titles to youtube links
print(songs)
links=[]
# for mus in songs:
#     query = urllib.parse.quote(mus)
#     url = "https://www.youtube.com/results?search_query=" + query
#     print(url)
#     response = urllib.request.urlopen(url)
#     html = response.read()
#     soup = BeautifulSoup(html, 'html.parser')
#
#     try:
#         vid = soup.find(attrs={'class':'yt-uix-tile-link'})['href']
#         print(vid)
#         link='https://www.youtube.com' + vid
#         print(link)
#         links.append(link)
#
#     except:
#         print('skipped '+mus)

# for l in links:
#     print(l)
lst =[]
for mus in songs:
    query = os.system(f'youtube-dl --get-url "ytsearch1: {mus}"')
    lst.append(query)
#print(lst)
