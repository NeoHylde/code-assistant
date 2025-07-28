from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QCursor, QMouseEvent, QKeyEvent
from PyQt5.QtCore import Qt, QPoint, QRect, QThread, QTimer
from Analyzer import AnalyzerWorker
from PIL import Image

#resize image, not sure if this helps performance, probably for larger imgs
@staticmethod
def resize_image(image_path, output_path, max_width=1024):
        with Image.open(image_path) as img:
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.ANTIALIAS)
            img.save(output_path)

class Capture(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.main.hide()

        self.setMouseTracking(True)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.15)
        self.showFullScreen()

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()
        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(), rect.y(), rect.width(), rect.height()
        )

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rubber_band.show()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()

            rect = self.rubber_band.geometry()
            self.imgmap = self.imgmap.copy(rect)
            QApplication.restoreOverrideCursor()

            clipboard = QApplication.clipboard()
            clipboard.setPixmap(self.imgmap)

            self.main.label.setPixmap(self.imgmap)
            self.main.show()

            file_name = "img1.png"
            self.imgmap.save(file_name)

            resize_image("img1.png", "img1.png")

            self.main.text.setText("Analyzing image...")

            #start new thread so gui still is displayed while api returns response
            self.thread = QThread()
            self.worker = AnalyzerWorker(file_name)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.handle_result)
            self.worker.error.connect(self.handle_error)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()

            self.close()
    
    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event.key() == Qt.Key_Escape:
            QApplication.restoreOverrideCursor()
            self.main.show()
            self.close()

    def closeEvent(self, event):
        self.releaseKeyboard()
        QApplication.restoreOverrideCursor()
        super().closeEvent(event)
    
    def handle_result(self, result):
        self.main.text.setText(result)
        self.close()

    def handle_error(self, error_msg):
        self.main.text.setText(f"Error: {error_msg}")
        self.close()