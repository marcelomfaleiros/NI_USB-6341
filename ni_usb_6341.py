# encoding: utf-8

from usb6341_interface import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets as qtw
import nidaqmx as daq
import numpy as np
import time
import keyboard

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

class Worker(QThread):
    signal_point = pyqtSignal(object)
    signal_data = pyqtSignal(object)
    finished = pyqtSignal()

    def run(self):    
        intnsity_array = []
        dlay_array = []
        x = 0

        #task = daq.Task() 
        #task.ai_channels.add_ai_voltage_chan(self.channel)
              
        while True:
            if keyboard.is_pressed('Escape'):
                break      
            #measurement
            #y = task.read()
            x += 1 
            y = np.random.rand()
            
            #intensity_array.append(lock-in measurement)
            dlay_array.append(x)
            intnsity_array.append(y)
            
            delay_array = np.array(dlay_array)
            intensity_array = np.array(intnsity_array)
            self.point = (delay_array, intensity_array)
             
            self.signal_point.emit(self.point)
            self.signal_data.emit(self.point)
    
        self.finished.emit()

class NiUsb6341(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("NI USB-6341")
        self.setupUi(self)

        self.thread = Worker()
                
        self.init_pushButton.clicked.connect(self.start_up)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)
        self.ai0_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai1_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai2_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai3_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai4_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai5_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai6_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        self.ai7_pushButton.clicked.connect(lambda: self.run("Dev1/ai0"))
        '''self.pfi0_pushButton.clicked.connect()
        self.pfi1_pushButton.clicked.connect()
        self.pfi2_pushButton.clicked.connect()
        self.pfi3_pushButton.clicked.connect()
        self.pfi4_pushButton.clicked.connect()
        self.pfi5_pushButton.clicked.connect()
        self.pfi6_pushButton.clicked.connect()
        self.pfi7_pushButton.clicked.connect()'''          

    def start_up(self):
        self.thread.task = daq.Task() 

        self.file = qtw.QFileDialog.getSaveFileName()[0]

        self.clear()
        
        x = []
        y = []
        
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "PMT signal", units="A.U.")
        self.graphicsView.setLabel("bottom", "Time", units="s")

        self.graphicsView.plot(x, y)
  
    def run(self, channel=str):
        self.thread.task.ai_channels.add_ai_voltage_chan(channel)
        #set interface elements as Worker thread elements
        self.thread.signal_point.connect(self.plot)
        self.thread.signal_data.connect(self.save)
        self.thread.start()
        #disable interface buttons while measurement is running
        self.ai0_pushButton.setEnabled(False)
        self.ai1_pushButton.setEnabled(False)
        self.ai2_pushButton.setEnabled(False)
        self.ai3_pushButton.setEnabled(False)
        self.ai4_pushButton.setEnabled(False)
        self.ai5_pushButton.setEnabled(False)
        self.ai6_pushButton.setEnabled(False)
        self.ai7_pushButton.setEnabled(False)
        self.pfi0_pushButton.setEnabled(False)
        self.pfi1_pushButton.setEnabled(False)
        self.pfi2_pushButton.setEnabled(False)
        self.pfi3_pushButton.setEnabled(False)
        self.pfi4_pushButton.setEnabled(False)
        self.pfi5_pushButton.setEnabled(False)
        self.pfi6_pushButton.setEnabled(False)
        self.pfi7_pushButton.setEnabled(False)
        self.init_pushButton.setEnabled(False)
        self.clear_pushButton.setEnabled(False)
        self.exit_pushButton.setEnabled(True)
        #enable interface buttons when measurement stop
        self.thread.finished.connect(lambda: self.ai0_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai1_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai2_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai3_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai4_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai5_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai6_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ai7_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi0_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi1_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi2_pushButton.setEnabled(True))   
        self.thread.finished.connect(lambda: self.pfi3_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi4_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi5_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi6_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.pfi7_pushButton.setEnabled(True))     
        self.thread.finished.connect(lambda: self.start_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.init_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.clear_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.exit_pushButton.setEnabled(True))

    def plot(self, point):
        self.graphicsView.plot(point[0], point[1], pen=None, symbol='o', clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self, point):  
        raw_data = np.array(point)
        transposed_raw_data = np.vstack(raw_data)                      
        data = transposed_raw_data.transpose()
        
        np.savetxt(self.file, data)    

    def clear(self):
        self.graphicsView.clear()
        
    def exit(self):
        self.close()

if __name__ == '__main__':
    app = qtw.QApplication([])
    tela = NiUsb6341()
    tela.show()
    app.exec_()