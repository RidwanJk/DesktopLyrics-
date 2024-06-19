import sys
import os
from bs4 import BeautifulSoup as bs
from torch import Size
from api import get_song_lyrics, extract_lyrics, SaveLyrics
from apikey import api_token
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,    
    QLineEdit,    
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea
)
from Spotify import get_current_playing, get_spotify_token


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
           
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(QSize(600, 800))

        layout = QVBoxLayout()

        # Create a QScrollArea
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)

        # Create a widget to contain the label
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its content widget

        # Use a QVBoxLayout for the scroll widget
        scroll_layout = QVBoxLayout(scroll_widget)

        self.label = QLabel("Lyrics App", scroll_widget)
        scroll_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("QLabel { font-size: 20px; color: White; }")

        self.searchlabel = QLabel("Search for a song", self)
        self.search = QLineEdit(self)
        layout.addWidget(self.searchlabel)        
        layout.addWidget(self.search)
        self.artist_name = QLabel("Artist Optional", self)
        self.artist = QLineEdit(self)
        layout.addWidget(self.artist_name)        
        layout.addWidget(self.artist)
        

        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.hasclicked = False
        self.oldPos = self.pos()  # Store the initial position of the window


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition()  # Update oldPos with the current mouse position
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition() - self.oldPos
            new_x = int(self.x() + delta.x())
            new_y = int(self.y() + delta.y())
            self.move(new_x, new_y)
            self.oldPos = event.globalPosition()
            super().mouseMoveEvent(event)

    def on_button_click(self):
        if not self.hasclicked:
            self.search.hide()
            self.label.setText("Lyrics for " + self.search.text())
            self.button.setText("Go Back")
            self.hasclicked = True
            # Call the function to search and save lyrics
            self.search.text()
            self.artist.text()
            lyrics = get_song_lyrics(self.search.text(), self.artist.text() ,api_token) 
            
            extracted_lyrics = extract_lyrics(lyrics)
            SaveLyrics(extracted_lyrics, f"{self.search.text()}.txt")

            # Decode the file with BeautifulSoup
            file_path = f"{self.search.text()}.txt"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    lyrics_content = file.read()
                    soup = bs(lyrics_content, "html.parser")
                    cleaned_lyrics = soup.get_text(separator="\n")  # Separate lines for better display
                    even_cleaner_lyrics = cleaned_lyrics[1:-1] 
                    self.label.setText(even_cleaner_lyrics)                                        
            else:
                self.label.setText("Error: Lyrics file not found")
        
        else:
            self.search.show()
            self.label.setText("Lyrics App")
            self.button.setText("Search")
            self.hasclicked = False

    def on_button_current_track_click(self):
        access_token = get_spotify_token() 
        if access_token:
            track, artist = get_current_playing(access_token)
            if track and artist:
                self.search.setText(track)
                self.artist.setText(artist)
                
            else:
                self.label.setText("No track is currently playing")
        else:
            self.label.setText("Failed to get access token")


app = QApplication(sys.argv)

window = TransparentWindow()
window.show()

sys.exit(app.exec())