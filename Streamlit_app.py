

# Imports
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Get the snowflake credentials from the .env file 
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT = os.getenv("ACCOUNT")
WAREHOUSE = os.getenv("WAREHOUSE")
DATABASE = os.getenv("DATABASE")
SCHEMA = os.getenv("SCHEMA")

# Snowflake connection & engine
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)

engine = create_engine(
    f"snowflake://{USER}:{PASSWORD}@{ACCOUNT}/{DATABASE}/{SCHEMA}?warehouse={WAREHOUSE}"
)

def run_query(sql):
    return pd.read_sql(sql, engine)

# Page config
st.set_page_config(page_title="Spotify Wrapped 2025", layout="wide")

# Title
st.title("🎧 Spotify Wrapped 2025")

# Main layout: 2 columns
# Left: Top Artists + Top Songs
# Right: Top Genres + Metrics
left_col, right_col = st.columns([2, 1])

# LEFT COLUMN: Top Artists + Top Songs
with left_col:
    # Top Artists
    st.subheader("🎤 Top 10 Artists")
    sql_top_artists = """
    SELECT artist_name, artist_image_url
    FROM "Top_Artists"
    WHERE time_window = '1_year' AND rank <= 10
    ORDER BY rank ASC
    """
    df_top_artists = run_query(sql_top_artists)

    artist_cols = st.columns(5)
    for i, row in enumerate(df_top_artists.itertuples(), start=1):
        col = artist_cols[(i-1) % 5]
        with col:
            st.image(row.artist_image_url, width=60)
            st.caption(f"{i}. {row.artist_name}")

    # Top Songs
    st.subheader("🎵 Top 10 Songs")
    sql_top_songs = """
    SELECT track_name, track_image_url
    FROM "Top_Tracks"
    WHERE time_window = '1_year' AND rank <= 10
    ORDER BY rank ASC
    """
    df_top_songs = run_query(sql_top_songs)

    song_cols = st.columns(5)
    for i, row in enumerate(df_top_songs.itertuples(), start=1):
        col = song_cols[(i-1) % 5]
        with col:
            st.image(row.track_image_url, width=60)
            st.caption(f"{i}. {row.track_name}")

# RIGHT COLUMN: Top Genres + Metrics
with right_col:
    # Top Genres
    st.subheader("🎼 Top Genres")
    sql_top_genres = """
    SELECT TRIM(value) AS genre
    FROM "Top_Artists",
         TABLE(FLATTEN(INPUT => SPLIT(genres, ',')))
    WHERE time_window = '1_year' 
      AND rank <= 10
      AND value IS NOT NULL
      AND TRIM(value) <> ''
    """
    df_top_genres = run_query(sql_top_genres)
    top_genres = df_top_genres["genre"].dropna().unique().tolist()
    for i, genre in enumerate(top_genres, start=1):
        st.write(f"{i}. {genre}")

    # Metrics
    st.subheader("📊 Metrics")

    # Most Active Day
    sql_most_active_day = """
    SELECT TO_DATE(played_at) AS played_date,
           COUNT(*) AS plays
    FROM "Recently_Played"
    GROUP BY played_date
    ORDER BY plays DESC
    LIMIT 1
    """
    df_active_day = run_query(sql_most_active_day)

    # Longest Listening Streak
    sql_longest_streak = """
    WITH play_dates AS (
        SELECT DISTINCT TO_DATE(played_at) AS played_date
        FROM "Recently_Played"
    ),
    numbered_dates AS (
        SELECT
            played_date,
            ROW_NUMBER() OVER (ORDER BY played_date) AS rn
        FROM play_dates
    ),
    streak_groups AS (
        SELECT
            played_date,
            rn - DATEDIFF(day, '1970-01-01', played_date) AS grp
        FROM numbered_dates
    )
    SELECT COUNT(*) AS longest_streak
    FROM streak_groups
    GROUP BY grp
    ORDER BY longest_streak DESC
    LIMIT 1;
    """
    df_longest_streak = run_query(sql_longest_streak)

    # Top Listening Year
    sql_top_year = """
    SELECT release_year FROM (
        SELECT YEAR(TO_DATE(album_release_date, 'YYYY-MM-DD')) AS release_year,
               COUNT(*) AS counter
        FROM "Top_Tracks"
        GROUP BY release_year
        ORDER BY counter DESC
        LIMIT 1
    )
    """
    df_top_year = run_query(sql_top_year)

    sql_top_era = """
    SELECT era 
    FROM (
        SELECT 
            EXTRACT(YEAR FROM TO_DATE(album_release_date, 'YYYY-MM-DD')) AS release_year,
            COUNT(*) AS counter, 
            CASE 
                WHEN EXTRACT(YEAR FROM TO_DATE(album_release_date, 'YYYY-MM-DD')) BETWEEN 2020 AND 2025 THEN '2020s'
                WHEN EXTRACT(YEAR FROM TO_DATE(album_release_date, 'YYYY-MM-DD')) BETWEEN 2010 AND 2019 THEN '2010s'
            END AS era
        FROM "Top_Tracks"
        GROUP BY release_year
        ORDER BY counter DESC
        LIMIT 1
    ) sub;
    """

    # Run the query
    df_top_era = run_query(sql_top_era)

    #Longest listening time
    sql_longest_listening_time="""
     select SUM(duration_mins) as longest_listening_time
     from "Recently_Played"
     where TO_DATE(played_at)=(select TO_DATE(played_at) as played_date
     from "Recently_Played"
     group by TO_DATE(played_at)
     order by COUNT(TO_DATE(played_at)) desc
     limit 1)"""
    
    df_longest_listening_time = run_query(sql_longest_listening_time)

    
    # Add 'mins' to the value
    longest_time_str = f"{df_longest_listening_time.iloc[0]['longest_listening_time']:.1f} mins"


        
    st.metric("Most Active Listening Day", str(df_active_day.iloc[0]["played_date"]))
    st.metric("Longest Listening Time", longest_time_str)
    st.metric("Longest Listening Streak (days)", int(df_longest_streak.iloc[0]["longest_streak"]))
    st.metric("Most Songs From Year", str(df_top_year.iloc[0]["release_year"]))
    st.metric("Top Era", df_top_era.iloc[0]["era"])
   

    


