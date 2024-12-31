from PyQt5.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
#import serial
from tensile import Tensile, TensileOutput
from random import randint
from time import sleep



class ReaderSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    data
        tuple data point (unit, x, y)
    """

    data = pyqtSignal(TensileOutput)  # <1>


class Reader(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals
    and wrap-up.
    """

    def __init__(self):
        super().__init__()
        
        self.signals = ReaderSignals()
        self.forces = []
        self.r100 = []
        self.ext = []
       # print(setting)
        self.tensile = Tensile()
     #   self.tensile.move_up()

    @pyqtSlot()
    def run(self):

        raw_data = []
        sample_number = 0
     
        self.do = True
        while self.do:
            #temp = []
            #unit = ''
            #raw_data = [1,'N']
            #convert data to float list   
            data = self.tensile.read_data()
            
        
            self.forces.append(data.force)
            self.r100.append(data.r100)
            self.ext.append(data.ext)
            self.signals.data.emit(data)
    

    def close(self):
        self.do = False
        self.tensile.stop()
        self.tensile.close()
        
    
     

