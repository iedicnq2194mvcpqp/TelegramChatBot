import os
from dotenv import load_dotenv, dotenv_values

import googleapiclient.discovery
import googleapiclient.errors

load_dotenv()

yt_api_key = dotenv_values()['YT_KEY']
channel_id = 'UC7Elc-kLydl-NAV4g204pDQ'

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=yt_api_key)


def get_channel_playlist_ids():
    request = youtube.channels().list(
        id=channel_id,
        part='snippet,contentDetails,statistics'
    )
    response = request.execute()

    data = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return data


def get_channel_video_stats():
    playlist_id = get_channel_playlist_ids()

    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id
    )

    response = request.execute()
    return str(response['items'][1]['contentDetails']['videoId'])


def get_latest_video_statistics():
    video_id = get_channel_video_stats()

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )

    response = request.execute()
    return [response['items'][0]['snippet']['title'], response['items'][0]['statistics']]
