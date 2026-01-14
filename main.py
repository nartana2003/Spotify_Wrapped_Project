#Import the necessary libraries
import os
import re
from textwrap import indent
from dotenv import load_dotenv
import json
import requests
from requests import auth, head
from urllib3 import response

# Load environment variables from .env file
load_dotenv()

# Get the client ID and client secret from the .env file
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Load your token
with open('spotify_token.json', 'r') as f:
    token_info = json.load(f)

ACCESS_TOKEN = token_info['access_token']
