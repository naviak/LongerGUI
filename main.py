import sys
from PyQt5.QtWidgets import QApplication
from camerawindow import CameraWindow, CameraException
from longerwindow import LongerWindow
from PyQt5.QtCore import QThread, pyqtSignal


class CameraThread(QThread):
    def __init__(self, camera: CameraWindow):
        super().__init__()
        self.camera = camera

    def run(self):
        while True:
            if (self.camera.loop()) == 0:
                self.camera.__del__()
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)

    longerWindow = LongerWindow()
    longerWindow.show()

    cameraWindow = CameraWindow()
    cameraThread = CameraThread(cameraWindow)
    cameraThread.run()

    sys.exit(app.exec_())

