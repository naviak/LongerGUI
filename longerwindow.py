import serial
import time
from longergui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QErrorMessage
import serial_ports as sp
import longer


class LongerWindow(QtWidgets.QMainWindow):
    running1 = False
    running2 = False
    comport1 = None
    comport2 = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.pump1 = None
        self.pump2 = None
        #ui
        self.ui.pushButton.clicked.connect(self.stop1)
        self.ui.pushButton_2.clicked.connect(self.start2)
        self.ui.pushButton_3.clicked.connect(self.start1)
        self.ui.pushButton_4.clicked.connect(self.stop2)
        self.ui.pushButton_5.clicked.connect(self.refresh1)
        self.ui.pushButton_6.clicked.connect(self.refresh2)

        self.ui.listWidget.addItems(sp.serial_ports())
        self.ui.listWidget_2.addItems(sp.serial_ports())
        self.ui.listWidget.itemDoubleClicked.connect(self.changeComPort1)
        self.ui.listWidget_2.itemDoubleClicked.connect(self.changeComPort2)

        self.ui.checkBox.stateChanged.connect(self.set_rotation1)
        self.ui.checkBox_2.stateChanged.connect(self.set_rotation2)

        self.ui.spinBox.valueChanged.connect(self.set_speed1)
        self.ui.spinBox_2.valueChanged.connect(self.set_speed2)

    @pyqtSlot()
    def changeComPort1(self):
        self.comport1 = self.ui.listWidget.currentItem().text()
        self.ui.label_7.setText(self.comport1)
        self.pump1 = longer.Longer(self.comport1)

    @pyqtSlot()
    def changeComPort2(self):
        self.comport2 = self.ui.listWidget_2.currentItem().text()
        self.ui.label_8.setText(self.comport2)
        self.pump2 = longer.Longer(self.comport2)

    @pyqtSlot()
    def start1(self):
        if not self.running1 and self.comport1 is not None:
            try:
                self.running1 = True
                self.pump1.setSettings(state=True)
                self.pump1.printToCom(self.pump1.getWriteMsg())
            except serial.SerialException:
                self.handle_error('could not open port ' + self.comport1)

    @pyqtSlot()
    def stop1(self):
        if self.running1 and self.comport1 is not None:
            try:
                running1 = False
                self.pump1.setSettings(state=False)
                self.pump1.printToCom(self.pump1.getWriteMsg())
            except serial.SerialException:
                self.handle_error('could not open port ' + self.comport1)

    @pyqtSlot()
    def start2(self):
        if not self.running2 and self.comport2 is not None:
            self.running2 = True
            self.pump2.setSettings(state=True)
            try:
                self.pump2.printToCom(self.pump2.getWriteMsg())
            except serial.SerialException:
                self.handle_error('could not open port ' + self.comport2)

    @pyqtSlot()
    def stop2(self):
        if self.running2 and self.comport2 is not None:
            try:
                running2 = False
                self.pump2.setSettings(state=False)
                self.pump2.printToCom(self.pump2.getWriteMsg())
            except serial.SerialException:
                self.handle_error('could not open port ' + self.comport2)

    @pyqtSlot()
    def set_speed1(self):
        tmp = self.ui.spinBox.value()
        if self.pump1 is not None:
            self.pump1.setSettings(tmp)
            self.pump1.printToCom(self.pump1.getWriteMsg())

    @pyqtSlot()
    def set_speed2(self):
        tmp = self.ui.spinBox_2.value()
        if self.pump2 is not None:
            self.pump2.setSettings(tmp)
            self.pump2.printToCom(self.pump2.getWriteMsg())

    @pyqtSlot()
    def set_rotation1(self):
        tmp = self.ui.checkBox.checkState()
        if self.pump1 is not None:
            self.pump1.setSettings(rotation=int(tmp/2))
            self.pump1.printToCom(self.pump1.getWriteMsg())

    @pyqtSlot()
    def set_rotation2(self):
        tmp = self.ui.checkBox_2.checkState()
        if self.pump2 is not None:
            self.pump2.setSettings(rotation=int(tmp/2))
            self.pump2.printToCom(self.pump2.getWriteMsg())

    @pyqtSlot()
    def refresh1(self):
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(sp.serial_ports())

    @pyqtSlot()
    def refresh2(self):
        self.ui.listWidget_2.clear()
        self.ui.listWidget_2.addItems(sp.serial_ports())

    def handle_error(self, error):
        em = QErrorMessage(self)
        em.showMessage(error)