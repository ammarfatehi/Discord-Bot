# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        #print("   %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))
        print(track['artists'][0]['name'],track['name'])

username = 'ammarfatehi'
if __name__ == '__main__':
    if len(username) > 1:
        username = 'ammarfatehi'
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        sys.exit()
    #GO TO THIS LINK AND GET A NEW TOKEN: https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=7kjMZjI0zzQN1ZFfuEm34Z&market=&fields=&limit=&offset=
    token = 'BQDL1gtqSwFI_MR_9vvPcLPyL-IU-_RSHzWFdqqtjsCgwNur2TbmGs6nnPrU28VFp8Ui1JD8y6FWSKQ-GAoc6E_tHCrXh1NWBSn6fWf28k0dK2hnzyUryEzAWwW4c6nqLXcDIfNzMqrn'

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print ('  total tracks', playlist['tracks']['total'])
                results = sp.playlist(playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)