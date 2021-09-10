import sys
from PyQt5.QtWidgets import QApplication
from camerawindow import CameraWindow, CameraException
from longerwindow import LongerWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    longerWindow = LongerWindow()
    longerWindow.show()

    cameraWindow = CameraWindow()
    cameraWindow.show()

    sys.exit(app.exec_())