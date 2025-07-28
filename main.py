import sys 
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame, 
    QPushButton,
    QTextEdit
)

from pynput import keyboard
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QTimer
from Capturer import Capture

COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='a')},
    {keyboard.Key.shift, keyboard.KeyCode(char='A')}
    ]
current = set()

class TriggerHandler(QObject):
    trigger_gui = pyqtSignal()

class ScreenRegionSelector(QMainWindow):
    def __init__(self,):
        super().__init__(None)

        self.m_width = 400
        self.m_height = 500

        self.setMinimumSize(self.m_width, self.m_height)

        frame = QFrame()
        frame.setContentsMargins(0,0,0,0)
        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(5,5,5,5)

        #screenshot display
        self.label = QLabel()
        #openai response display
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        #retake screenshot display
        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)

        lay.addWidget(self.label)
        lay.addWidget(self.btn_capture)
        lay.addWidget(self.text)

        self.setCentralWidget(frame)

    def capture(self):
        self.capturer = Capture(self)
        self.capturer.show()
            
def start_keyboard_listener(trigger_handler):
    def on_press(key):     
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.add(key)
            if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
                trigger_handler.trigger_gui.emit()

    def on_release(key):
        if any([key in COMBO for COMBO in COMBINATIONS]):
            current.discard(key)
    
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
            
    app.setStyleSheet("""
    QFrame {
        background-color: #2c2c2c;
        border-radius: 8px;
        padding: 10px;
    }

    QPushButton {
        border-radius: 6px;
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #4e7eff, stop:1 #3a54ff);
        padding: 10px 16px;
        color: #ffffff;
        font-weight: 600;
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 13px;
        border: none;
    }

    QPushButton:hover {
        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #5e5cff, stop:1 #4630ff);
    }

    QTextEdit {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
        font-family: "Consolas", monospace;
        font-size: 12px;
        padding: 8px;
        border-radius: 6px;
    }

    QLabel {
        color: white;
        font-size: 13px;
        padding: 4px;
    }
    """)

        
    trigger_handler = TriggerHandler()
    selector = ScreenRegionSelector()

    trigger_handler.trigger_gui.connect(selector.capture)
    
    start_keyboard_listener(trigger_handler=trigger_handler)

    sys.exit(app.exec_())