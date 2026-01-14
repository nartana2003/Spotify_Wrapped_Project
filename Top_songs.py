# Imports
import requests
import pandas as pd
from datetime import datetime
from main import ACCESS_TOKEN


# Reusable function
def get_top_50_tracks(time_range: str, time_window: str) -> pd.DataFrame:

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "time_range": time_range,   # short_term / medium_term / long_term
        "limit": 50
    }

    response = requests.get(
        "https://api.spotify.com/v1/me/top/tracks",
        headers=headers,
        params=params
    )

    response.raise_for_status()
    data = response.json()

    rows = []

    for rank, track in enumerate(data["items"], start=1):
        album = track["album"]

        rows.append({
            "track_id": track["id"],
            "track_name": track["name"],

            "album_id": album["id"],
            "album_name": album["name"],
            "album_type": album["album_type"],
            "album_release_date": album["release_date"],

            "artist_ids": [artist["id"] for artist in track["artists"]],
            "artist_names": [artist["name"] for artist in track["artists"]],
            "track_image_url":album["images"][0]["url"],

            "rank": rank,
            "time_window": time_window,
        })

    top_tracks=pd.DataFrame(rows)
    return top_tracks

# Build ONE fact table
def build_fact_top_tracks() -> pd.DataFrame:

    df_1m = get_top_50_tracks("short_term", "1_month")
    df_6m = get_top_50_tracks("medium_term", "6_months")
    df_1y = get_top_50_tracks("long_term", "1_year")

    fact_top_tracks = pd.concat(
        [df_1m, df_6m, df_1y],
        ignore_index=True
    )

    return fact_top_tracks

