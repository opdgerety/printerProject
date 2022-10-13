from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math

class Move:
    def __init__(self):
        self.hub = PrimeHub()
        self.x= Motor('F')
        self.y=Motor('C')
        self.pen=Motor('A')
        self.end=ForceSensor('D')
        self.fed=ColorSensor('B')

    def calibrate(self):
        self.x.start(-100)
        self.end.wait_until_pressed()
        self.x.stop()
    #18o pcm y vs 90 pcm for x /5
    def moveX(self,x):
        self.x.run_for_degrees(int(x), 50)

    def carridgeReturn(self,y):
        self.calibrate()
        self.y.run_for_degrees(int(y), 50)
    
    def dot(self):
        self.pen.run_for_degrees(20, 50)
        self.pen.run_for_degrees(20, -50)
    
    def feed(self):
        self.y.start(25)
        self.fed.wait_until_color('white')
        self.y.stop()

class Printer:
    def __init__(self,image):
        self.image=image
        self.XLEN=int(4*360)
        self.YLEN=self.XLEN//5
        self.RESX=25
        self.RESY=25
        self.m=Move()
        
    def printAll(self):
        self.m.feed()
        self.m.calibrate()
        for y in range(self.RESY):
            self.xBuffer=0
            self.printRow(y)

    def printRow(self,y):
        for x in range(self.RESX):
            if self.image[y*self.RESX+x]=="1":
                self.m.moveX(self.xBuffer)
                self.m.dot()
            self.xBuffer+=self.XLEN/self.RESX
        self.m.carridgeReturn(self.YLEN/self.RESY)


printer=Printer(list("0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000110000000000000000000000000010000010110000000000001001000000001000000000001000000001000010000000000010010000000000000000000000100000000000000000000000000000001000100000000000000000000001000000000000000000100000000000000000000000000000000000000000000000010000000000000000000000010000000000000000000000000000010000000000000000000010100000000010000000010000000000000010000000000100000000000000000000000010000000000010000000000000100000001100000000000000000101110000000000000000000000000000000000000000000000000000000000000"))
printer.printAll()
