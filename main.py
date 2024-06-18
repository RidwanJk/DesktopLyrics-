import sys
import os

from PyQt6.QtCore import Qt
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

    def on_button_click(self):
        if not self.hasclicked:
            self.search.hide()
            self.label.setText("Lyrics for " + self.search.text())
            self.button.setText("Go Back")
            self.hasclicked = True
        else:
            self.search.show()
            self.label.setText("Lyrics App")
            self.button.setText("Search")
            self.hasclicked = False
    
    
        

app = QApplication(sys.argv)

window = TransparentWindow()
window.show()

sys.exit(app.exec())