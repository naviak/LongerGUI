import serial


class Longer:
    def __init__(self, comport):
        self.lenstr = 0x06
        self.pdu = None
        self.rotation = 0x01
        self.fbspeed = 0x00
        self.sbspeed = 0x10
        self.tspeed = 0x00
        self.addr = 0x01
        self.fc = None
        self.flag = 0xe9
        self.pduprefix = {'W': 0x57, 'R': 0x52, 'J': 0x4A, 'I': 0x49, 'D': 0x44}
        self.fstate = 0x00
        self.port = serial.Serial(comport, baudrate=1200, parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE)
        self.pdu_ = None

    def setSettings(self, speed=None, rotation: bool = None, state: bool = None):
        if speed is not None:
            tmp = speed * 10
            self.fbspeed = (tmp >> 8) & 0xff
            self.sbspeed = tmp & 0xff
        if state is not None:
            self.fstate = state
        if rotation is not None:
            self.rotation = rotation
        if self.sbspeed == 0xe8:
            self.pdu_ = [self.pduprefix['W'], self.pduprefix['J'],
                         self.fbspeed, self.sbspeed, self.tspeed, self.fstate, self.rotation]
        elif self.sbspeed == 0xe9:
            self.pdu_ = [self.pduprefix['W'], self.pduprefix['J'],
                         self.fbspeed, 0xe8, 0x01, self.fstate, self.rotation]
        else:
            self.pdu_ = [self.pduprefix['W'], self.pduprefix['J'],
                         self.fbspeed, self.sbspeed, self.fstate, self.rotation]

    def getfcstr(self):
        tmp = self.lenstr ^ self.addr
        res = 0
        for i in self.pdu_:
            res ^= i
        return hex(tmp ^ res)[2:] if tmp ^ res > 0xf else '0' + hex(tmp ^ res)[2:]

    def getWriteMsg(self):
        resstr = ''.join([hex(i)[2:] if i > 0xf else '0' + hex(i)[2:] for i in self.pdu_])
        return bytearray.fromhex(hex(self.flag)[2:] + '0' + hex(self.addr)[2:] + '0' + hex(self.lenstr)[2:]
                                 + resstr + self.getfcstr())

    def printToCom(self, msg):
        self.port.write(msg)