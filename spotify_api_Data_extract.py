import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    playlist_link = "https://open.spotify.com/playlist/3cEYpjA9oz9GiPac4AsH4n"
    playlist_URI = playlist_link.split("/")[-1] 

    spotify_data = sp.playlist_tracks(playlist_URI)

    client = boto3.client('s3')

    filename = 'spotify_raw_' + str(datetime.now()) + '.json'

    print('filenameis:',filename)

    client.put_object(Body=json.dumps(spotify_data), Bucket='spotify-etl-project-swethagopisetty', Key='raw_data/to_processed/' +filename)
