import requests
import json
import pandas as pd

#Load your access token
from main import ACCESS_TOKEN



def recently_played_songs():
    headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'}

# Get recently played tracks
    response = requests.get(
    "https://api.spotify.com/v1/me/player/recently-played",
    headers=headers,
    params={'limit': 50}  # Max is 50
)

#Get the data in json format
    data=response.json()


# data=json.dumps(data,indent=3)
# print(data)

#Fetch meaningful data
    recently_played=[]

    for item in data["items"]:
        track = item["track"]
        album = track["album"]
        artist_ids = [artist["id"] for artist in track["artists"]]
        artist_names = [artist["name"] for artist in track["artists"]]
        recently_played.append({
        "track_id":track["id"],
        "track_name":track["name"],
        "played_at":item["played_at"],
        "album_id":album["id"],
        "album_name":album["name"],
        "album_type":album["album_type"],
        "album_release_date":album["release_date"],
        "artist_id":artist_ids,
        "artist_name":artist_names,
        "duration_mins":track["duration_ms"]/60000
        })

#Convert this data to a pandas dataframe for better readability and ease of ingestion
    df_recently_played = pd.DataFrame(recently_played)
    return df_recently_played










