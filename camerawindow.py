import cv2
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import queue
import threading
from cameragui import *


class CameraException(Exception):
    def __init__(self, message):
        super().__init__(message)


class OwnImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()


class CameraWindow(QtWidgets.QMainWindow):

    camera_port = None
    img_counter = 0
    running = False
    q = queue.Queue()
    frame = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.startButton.clicked.connect(self.start_clicked)

        self.window_width = self.ui.ImgWidget.frameSize().width()
        self.window_height = self.ui.ImgWidget.frameSize().height()
        self.ui.ImgWidget = OwnImageWidget(self.ui.ImgWidget)
        self.capture_thread = threading.Thread(target=self.grab, args=(0, self.q, 640, 480))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.ui.screenshotButton.clicked.connect(self.saveFrame)
        self.timer.start(1)

    def setCamera(self, index=0):
        self.camera_port = index
        self.cam.release()
        #self.cam = cv2.VideoCapture(self.camera_port)

    def saveFrame(self):
        if self.frame is not None:
            img_name = "opencv_frame_{}.png".format(self.img_counter)
            cv2.imwrite(img_name, self.frame)
            print("{} written!".format(img_name))
            self.img_counter += 1

    def grab(self, cam, queu, width, height):
        capture = cv2.VideoCapture(cam)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        while self.running:
            frame = {}
            capture.grab()
            retval, img = capture.retrieve(0)
            frame["img"] = img

            if queu.qsize() < 10:
                queu.put(frame)
            else:
                print(queu.qsize())

    def update_frame(self):
        if not self.q.empty():
            self.ui.startButton.setText('Camera is live')
            frame = self.q.get()
            img = frame["img"]
            self.frame = img

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])
            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)

            self.ui.ImgWidget.setImage(image)

    def closeEvent(self, event):
        self.running = False

    def start_clicked(self):
        self.running = True
        self.capture_thread.start()
        self.ui.startButton.setEnabled(False)
        self.ui.startButton.setText('Starting...')
