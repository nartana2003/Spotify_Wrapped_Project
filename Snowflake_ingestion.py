#Import the necessary libraries
import snowflake.connector
from sqlalchemy import create_engine
import pandas as pd 
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

# Create connection
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
)

engine = create_engine(
    f'snowflake://{USER}:{PASSWORD}@{ACCOUNT}/{DATABASE}/{SCHEMA}?warehouse={WAREHOUSE}'
)

# Import your modules/functions
from Recently_played import recently_played_songs
from Top_artists import get_top_50_artists
from Top_songs import get_top_50_tracks
from User_Profile import user_info
import pandas as pd

# --- Top Artists ---
df_top_artists_6m = get_top_50_artists("medium_term", "6_months")
df_top_artists_1y = get_top_50_artists("long_term", "1_year")
df_top_artists = pd.concat([ df_top_artists_6m, df_top_artists_1y], ignore_index=True)


# --- Top Tracks ---
df_top_tracks_1m = get_top_50_tracks("short_term", "1_month")
df_top_tracks_6m = get_top_50_tracks("medium_term", "6_months")
df_top_tracks_1y = get_top_50_tracks("long_term", "1_year")
df_top_tracks = pd.concat([df_top_tracks_1m, df_top_tracks_6m, df_top_tracks_1y], ignore_index=True)

# --- Other dataframes ---
df_recently_played = recently_played_songs()
df_user_info = user_info()


def make_sql_friendly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts list-like columns in a DataFrame into comma-separated strings
    so that the DataFrame can be safely uploaded to SQL/Snowflake.
    """
    df_copy = df.copy()
    
    for col in df_copy.columns:
        # Check if the column contains lists
        if df_copy[col].apply(lambda x: isinstance(x, list)).any():
            df_copy[col] = df_copy[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    
    return df_copy

#Make sure all columns are sql friendly
df_recently_played = make_sql_friendly(df_recently_played)
df_top_artists = make_sql_friendly(df_top_artists)
df_top_tracks = make_sql_friendly(df_top_tracks)
df_user_info = make_sql_friendly(df_user_info)


# --- Push to Snowflake ---
df_recently_played.to_sql("Recently_Played", engine, index=False, if_exists='replace')
print("Recently_Played table uploaded successfully")

df_top_artists.to_sql("Top_Artists", engine, index=False, if_exists='replace')
print("Top_Artists table uploaded successfully")

df_top_tracks.to_sql("Top_Tracks", engine, index=False, if_exists='replace')
print("Top_Tracks table uploaded successfully")

df_user_info.to_sql("User_Profile", engine, index=False, if_exists='replace')
print("User_Profile table uploaded successfully")

