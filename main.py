import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
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
        layout.addWidget(self.label)
        search = QLineEdit(self)
        layout.addWidget(search)
        
        button = QPushButton("Click Me", self)
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Hello, World!")

app = QApplication(sys.argv)

window = TransparentWindow()
window.show()

sys.exit(app.exec())