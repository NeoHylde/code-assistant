import sys 
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame, 
    QPushButton,
    QTextEdit,
)

from pynput import keyboard
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QTimer
from Capturer import Capture
import mouse

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
        self.setWindowTitle("CodeSnip")

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
        
        # steal focus work around, setfocuspolicy, setfocus etc was not working
        mouse.click('right')
            
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
        background-color: #0d1117;
        border-radius: 6px;
        padding: 10px;
    }

    QPushButton {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: 600;
        font-family: "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 13px;
        color: #c9d1d9;
    }

    QPushButton:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }

    QPushButton:pressed {
        background-color: #161b22;
        border-color: #6e7681;
    }

    QTextEdit {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        font-family: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
        font-size: 13px;
        padding: 8px;
        border-radius: 6px;
    }

    QLabel {
        color: #c9d1d9;
        font-size: 13px;
        padding: 4px;
    }
    """)



        
    trigger_handler = TriggerHandler()
    selector = ScreenRegionSelector()

    trigger_handler.trigger_gui.connect(selector.capture)
    
    start_keyboard_listener(trigger_handler=trigger_handler)

    sys.exit(app.exec_())