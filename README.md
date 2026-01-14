🎧 Spotify Wrapped Dashboard (2025)

This project uses the Spotify API to extract a user’s listening history and preferences, similar to Spotify Wrapped. The data is then pushed into a Snowflake database where SQL queries are used to analyze listening patterns. Finally, a Streamlit dashboard presents a personalized, interactive visualization of the user’s top artists, songs, genres, and listening habits.It’s designed to provide a fun, data-driven snapshot of your music taste. 

✨ Features

🎤 1.Top 10 Artists & 🎵 Top 10 Songs: Displays your most listened-to artists and tracks over the past year with images and rankings.

🎼 2.Top Genres: Shows your favorite genres extracted from your top artists.

📊 3.Listening Metrics:

📅(i) Most active listening day
⏱️ (ii)Longest listening time in a single day
🔥(iii) Longest listening streak (days)
🗓️ (iv) Year with the most songs listened to
🕰️(v)Top listening era (e.g., 2010s, 2020s)

💻 Tech Stack

1.Python: For API calls, data processing, and building the dashboard 🐍

2.Spotify API: Extracts user listening data, including tracks, artists, genres, and play history 🎧

3.Snowflake: Stores the Spotify data in a secure cloud data warehouse ❄️

4.SQL: Performs data transformations, aggregations, and analysis 📝

5.Streamlit: Displays the data in a modern, interactive dashboard 📊

🏗 Architecture

1.Data Extraction: Spotify API fetches user listening history (tracks, artists, play times) 🎶

2.Data Storage: Data is pushed into Snowflake for structured storage and easy querying ❄️

3.Data Analysis: SQL queries calculate metrics such as top artists, top songs, top genres, and listening streaks 📝

4.Dashboard Visualization: Streamlit renders the data as a clean, Spotify-style dashboard 🎨
