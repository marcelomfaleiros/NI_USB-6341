# encoding: utf-8

from usb6341_interface import Ui_MainWindow
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import numpy as np
import time
import keyboard

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import nidaqmx as daqmx
import time

class NiUsb6341(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("NI USB-6341")
        self.setupUi(self)
                
        self.init_pushButton.clicked.connect(self.set_up)
        self.start_pushButton.clicked.connect(self.start_up)
        #self.stop_pushButton.clicked.connect(self.stop)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)
        
    def set_up(self):
        self.rm = visa.ResourceManager()
        self.spex = self.rm.open_resource('GPIB0::2')
        
    def identity(self):        
        pass    
 
    def start_up(self):        
        pass
  
    def run(self):                           
        pass

    def stop(self):
        pass

    def clear(self):
        self.graphicsView.clear()
        
    def exit(self):
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = NiUsb6341()
    tela.show()
    app.exec_()