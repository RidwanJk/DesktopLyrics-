import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.label = QLabel("Welcome to PyQt", self)
        layout.addWidget(self.label)

        button = QPushButton("Click Me", self)
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Hello, World!")

app = QApplication(sys.argv)

window = TransparentWindow()
window.show()

sys.exit(app.exec_())
