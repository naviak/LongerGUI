import cv2


class CameraException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CameraWindow:
    camera_port = None
    img_counter = 0
    frame = None

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def setCamera(self, index=0):
        self.camera_port = index
        self.cam.release()
        self.cam = cv2.VideoCapture(self.camera_port)

    def saveFrame(self):
        img_name = "opencv_frame_{}.png".format(self.img_counter)
        cv2.imwrite(img_name, self.frame)
        print("{} written!".format(img_name))
        self.img_counter += 1

    def loop(self):
        ret, self.frame = self.cam.read()
        if not ret:
            raise CameraException("failed to grab frame")
        cv2.imshow("test", self.frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing camera")
            return 0
        elif k % 256 == 32:
            # SPACE pressed
            self.saveFrame()
