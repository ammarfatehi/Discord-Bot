import urllib.request
from bs4 import BeautifulSoup
import sys
import spotipy
import spotipy.util as util

songs = []
players = {}


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        song_name = item['track']['name']
        artist = item['track']['artists'][0]['name']
        songs.append(f'{song_name} by {artist}')
    print(songs)


username = input('give me username: ')
if __name__ == '__main__':
    if len(username) < 1:
        username = 'ammarfatehi'

    token = input('give me a token: ')
    if len(token) < 1:
        # GO TO THIS LINK AND GET A NEW TOKEN: https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=7kjMZjI0zzQN1ZFfuEm34Z&market=&fields=&limit=&offset=
        token = 'BQCYWM1_T-wpyr6las2f1S6m0enGw9jx51Zn8MiPKNeGQRd3fCfjAcZ38AjRxD4HxGksJofgWC6-MA4HE_RIjMCRr7YDthZTFd4Djx-AwXV-3FEe24GecyI5EypAu6QuTtklT7OJOvNv'

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



links=[]
for mus in songs:
    query = urllib.parse.quote(mus)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.find(attrs={'class':'yt-uix-tile-link'})['href'])

    try:
        vid = soup.find(attrs={'class':'yt-uix-tile-link'})['href']
        links.append('https://www.youtube.com' + soup.find(attrs={'class':'yt-uix-tile-link'})['href'])
    except:
        print('skipped '+mus)

#for l in links:
 #   print(l)
