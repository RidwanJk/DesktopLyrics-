import requests
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs

import http.server
import threading
import apikey

CLIENT_ID = apikey.CLIENT_ID
CLIENT_SECRET = apikey.CLIENT_SECRET
REDIRECT_URI = 'http://localhost:8888/callback/'  # Ensure this matches the registered URI
SCOPES = 'user-read-currently-playing'
TOKEN = None

class TokenHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global TOKEN
        query = urlparse(self.path).query
        code = parse_qs(query).get('code')
        if code:
            TOKEN = get_access_token(code[0])
            print("Access Token received:", TOKEN)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'You can close this window now')

def start_server():
    server = http.server.HTTPServer(('localhost', 8888), TokenHandler)
    server.handle_request()

def get_spotify_token():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    webbrowser.open(auth_url)
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    server_thread.join()
    return TOKEN
    
def get_access_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    token_data = response.json()
    return token_data.get('access_token')

def get_current_playing(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    if response.status_code == 200:
        data = response.json()
        track_name = data['item']['name']
        artist_name = data['item']['artists'][0]['name']
        return track_name, artist_name
    return None, None

def saveToken(TOKEN):    
    apikey.TOKEN = TOKEN

