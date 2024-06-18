import requests
import webbrowser
import json
from urllib.parse import urlencode, urlparse, parse_qs
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

CLIENT_ID = '853fe2d917894e31b39b9c9ebe865d1c'
CLIENT_SECRET = '110ff2eee7bc434888c877bdb4932e33'
REDIRECT_URI = 'http://localhost:8888/callback'
SCOPES = 'user-read-currently-playing'

def get_spotify_token():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    webbrowser.open(auth_url)
    
    # Wait for the redirect to your REDIRECT_URI and get the code from the URL
    # This part should be handled by a web server or manually by the user
    auth_response = input("Paste the URL you were redirected to: ")
    code = parse_qs(urlparse(auth_response).query)['code'][0]
    
    token_url = "https://accounts.spotify.com/api/token"

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

class LyricsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Lyrics App with Spotify Integration')
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Current Track: None")
        layout.addWidget(self.label)
        
        self.button = QPushButton("Get Current Track")
        self.button.clicked.connect(self.show_current_track)
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def show_current_track(self):
        access_token = get_spotify_token()
        track, artist = get_current_playing(access_token)
        if track and artist:
            self.label.setText(f"Current Track: {track} by {artist}")
        else:
            self.label.setText("No track is currently playing")

if __name__ == '__main__':
    app = QApplication([])
    window = LyricsApp()
    window.show()
    app.exec()
