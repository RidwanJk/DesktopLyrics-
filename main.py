import sys
import os
from bs4 import BeautifulSoup as bs
from api import get_song_lyrics, extract_lyrics, SaveLyrics
from apikey import api_token

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,    
    QLineEdit,    
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.label = QLabel("Lyrics App", self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.search = QLineEdit(self)
        layout.addWidget(self.search)

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
            lyrics = get_song_lyrics(self.search.text(), api_token)
            extracted_lyrics = extract_lyrics(lyrics)
            SaveLyrics(extracted_lyrics, f"{self.search.text()}.txt")
            
        else:
            self.search.show()
            self.label.setText("Lyrics App")
            self.button.setText("Search")
            self.hasclicked = False


app = QApplication(sys.argv)

window = TransparentWindow()
window.show()

sys.exit(app.exec())