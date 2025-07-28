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

        self.label = QLabel()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
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
            
    app.setStyleSheet("""QFrame {
                        background-color: #3f3f3f;
                    }
                      
                    QPushButton {
                        border-radius: 5px;
                        background-color: rgb(60, 90, 255);
                        padding: 10px;
                        color: white;
                        font-weight: bold;
                        font-family: Arial;
                        font-size: 12px;
                    }
                    
                    QPushButton::hover {
                        background-color: rgb(60, 20, 255);
                    }""")
        
    trigger_handler = TriggerHandler()
    selector = ScreenRegionSelector()

    trigger_handler.trigger_gui.connect(selector.capture)
    
    start_keyboard_listener(trigger_handler=trigger_handler)

    sys.exit(app.exec_())