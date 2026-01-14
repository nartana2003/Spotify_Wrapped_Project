import requests
import pandas as pd
from datetime import datetime
from main import ACCESS_TOKEN


# Fetch top 50 artists for a given time range
def get_top_50_artists(time_range: str, time_window: str) -> pd.DataFrame:

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "time_range": time_range,
        "limit": 50
    }

    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists",
        headers=headers,
        params=params
    )

    response.raise_for_status()
    data = response.json()

    rows = []

    for rank, artist in enumerate(data["items"], start=1):
        rows.append({
            "artist_id": artist["id"],
            "artist_name": artist["name"],
            "genres": artist["genres"],
            "follower_count": artist["followers"]["total"],
            "popularity": artist["popularity"],
            "artist_image_url":artist["images"][0]["url"],
            "rank": rank,
            "time_window": time_window})

    return pd.DataFrame(rows)


# Combine all time windows into one table
def build_fact_top_artists() -> pd.DataFrame:

    df_6m = get_top_50_artists("medium_term", "6_months")
    df_1y = get_top_50_artists("long_term", "1_year")

    fact_top_artists = pd.concat(
        [ df_6m, df_1y],
        ignore_index=True
    )

    return fact_top_artists


