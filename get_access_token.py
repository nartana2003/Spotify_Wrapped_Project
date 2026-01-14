#Import the necessary libraries
import os
import requests
import json
import webbrowser
from dotenv import load_dotenv
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

# Load environment variables from .env file
load_dotenv()

# Get the client ID and client secret from the .env file
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Set the redirect URI
REDIRECT_URI = "http://127.0.0.1:8888/callback"

# Set the scope
SCOPE = "user-top-read user-read-recently-played user-follow-read user-library-read playlist-read-private"

# Initialize the authorization code
auth_code = None

# Define the callback handler
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Initialize the authorization code
        global auth_code
        # Get the query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful! You can close this window.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress server logs

def get_token_with_server():
    global auth_code
    auth_code=None
    
    # Build authorization URL
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(auth_params)}"
    
    print("Opening browser for authorization...")
    webbrowser.open(auth_url)
    
    # Start local server
    print("Waiting for authorization...")
    server = HTTPServer(('127.0.0.1', 8888), CallbackHandler)
    server.handle_request()  # Handle one request then stop
    
    if auth_code:
        print(f"✓ Authorization code received")
        
        # Exchange for token
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        
        response = requests.post(token_url, data=token_data)
        
        if response.status_code == 200:
            token_info = response.json()
            
            with open('spotify_token.json', 'w') as f:
                json.dump(token_info, f, indent=4)
            
            print("\n✓ Token saved to spotify_token.json")
            print(json.dumps(token_info, indent=2))
        else:
            print(f"Error: {response.text}")
            return None
    return None

def refresh_access_token():
    """Use refresh token to get a new access token"""
    try:
        with open('spotify_token.json', 'r') as f:
            token_info = json.load(f)
        
        if 'refresh_token' not in token_info:
            print("No refresh token found. Re-authorizing...")
            return get_token_with_server()
        
        token_url = "https://accounts.spotify.com/api/token"
        token_data = {
            "grant_type": "refresh_token",
            "refresh_token": token_info['refresh_token'],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        
        response = requests.post(token_url, data=token_data)
        
        if response.status_code == 200:
            new_token_info = response.json()
            # Keep the old refresh_token if not provided in response
            if 'refresh_token' not in new_token_info:
                new_token_info['refresh_token'] = token_info['refresh_token']
            
            with open('spotify_token.json', 'w') as f:
                json.dump(new_token_info, f, indent=4)
            
            print("✓ Access token refreshed")
            return new_token_info
        else:
            print(f"Error refreshing token: {response.text}")
            return get_token_with_server()
    
    except FileNotFoundError:
        print("No token file found. Authorizing...")
        return get_token_with_server()

if __name__ == "__main__":
    # Initial authorization.Checks if there is an existing token, if not it generates it
    if not os.path.exists('spotify_token.json'):
        get_token_with_server()
    
    # Token refresh loop
    while True:
        token_info = refresh_access_token()
        if token_info:
            print(f"Current access token: {token_info['access_token'][:20]}...")
        time.sleep(3500)  # Refresh every ~58 minutes



