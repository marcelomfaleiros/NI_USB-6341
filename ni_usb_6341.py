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

class Worker(QThread):
    signal = pyqtSignal(object)
    finished = pyqtSignal()
    position_mm = pyqtSignal(float)

    def move_stage_fs(self, target_delay):                                     
        target_fs = target_delay + self.zero/0.0003             #compute target delay position
        self.smc.move_abs_fs(target_fs)                         #move to target position in fs
        self.current_mm = self.smc.current_position()           #read current stage position          
        self.position_mm.emit(self.current_mm)

    def run(self):
        self.mode = 'measure'

        if self.channel == 'CH1 output':
            channel = 'ch1'
        elif self.channel == 'CH2 output':
            channel = 'ch2'

        intnsity_array = []
        stdrd_array = []
        dlay_array = []
              
        for target_delay in range(self.init_pos, (self.fin_pos + self.step), self.step):
            if keyboard.is_pressed('Escape'):
                break 
            dlay_array.append(target_delay)  
            self.move_stage_fs(target_delay)        
            #lock-in measurement
            y = self.sr830.measure_buffer(channel, self.sampling_time)
            y_mean = y[0]
            y_std = [1]
            #intensity_array.append(lock-in measurement)
            intnsity_array.append(y[0])
            stdrd_array.append(y[1])

            delay_array = np.array(dlay_array)
            intensity_array = np.array(intnsity_array)
            self.point = (delay_array, intensity_array)
             
            self.signal.emit(self.point)

        self.data = delay_array, intensity_array, stdrd_array
    
        self.finished.emit()

class NiUsb6341(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName("NI USB-6341")
        self.setupUi(self)
                
        self.init_pushButton.clicked.connect(self.set_up)
        self.start_pushButton.clicked.connect(self.run)
        #self.stop_pushButton.clicked.connect(self.stop)
        self.clear_pushButton.clicked.connect(self.clear)
        self.exit_pushButton.clicked.connect(self.exit)
        
    def set_up(self):
        #self.rm = visa.ResourceManager()
        #self.spex = self.rm.open_resource('GPIB0::2')
        self.graph_start()

    def graph_start(self):
        self.clear()
        
        #self.wl_array = [i for i in range(200, 1000, 2)]
        #self.emission_array = []
        
        self.graphicsView.showGrid(x=True, y=True, alpha=True)
        self.graphicsView.setLabel("left", "PD signal", units="A.U.")
        self.graphicsView.setLabel("bottom", "Time", units="s")
  
    def run(self):
        #set interface elements as Worker thread elements
        self.thread.channel = self.comboBox.currentText()
        self.thread.move_to = float(self.move_to_lineEdit.text())
        self.thread.delay = int(self.delay_lineEdit.text())
        self.thread.init_pos = int(self.init_pos_lineEdit.text())
        self.thread.fin_pos = int(self.fin_pos_lineEdit.text())
        self.thread.step = int(self.step_lineEdit.text())
        self.thread.sampling_time = float(self.sample_lineEdit.text())
        self.thread.signal.connect(self.plot)
        self.thread.position_mm.connect(self.show_position)
        self.thread.start()
        #disable interface buttons while measurement is running
        self.init_pushButton.setEnabled(False)
        self.one_fs_pushButton.setEnabled(False)
        self.mone_fs_pushButton.setEnabled(False)
        self.five_fs_pushButton.setEnabled(False)
        self.mfive_fs_pushButton.setEnabled(False)
        self.ten_fs_pushButton.setEnabled(False)
        self.mten_fs_pushButton.setEnabled(False)
        self.twenty_fs_pushButton.setEnabled(False)
        self.mtwenty_fs_pushButton.setEnabled(False)
        self.move_to_pushButton.setEnabled(False)
        self.delay_pushButton.setEnabled(False)
        self.freerun_pushButton.setEnabled(False)
        self.start_pushButton.setEnabled(False)
        self.save_pushButton.setEnabled(False)
        self.clear_pushButton.setEnabled(False)
        self.exit_pushButton.setEnabled(True)
        #connect the interface buttons to the Worker thread
        self.thread.finished.connect(lambda: self.init_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.one_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mone_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.five_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mfive_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.ten_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mten_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.twenty_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.mtwenty_fs_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.move_to_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.delay_pushButton.setEnabled(True))        
        self.thread.finished.connect(lambda: self.start_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.freerun_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.save_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.clear_pushButton.setEnabled(True))
        self.thread.finished.connect(lambda: self.exit_pushButton.setEnabled(True))

    def plot(self, point):
        self.graphicsView.plot(point[0], point[1], pen=None, symbol='o', clear=False)
        pg.QtWidgets.QApplication.processEvents()

    def save(self):  
        if self.thread.mode == 'measure':
            raw_data = np.array(self.thread.data)
        elif self.thread.mode == 'free run':
            raw_data = np.array(self.data)
        transposed_raw_data = np.vstack(raw_data)                      
        data = transposed_raw_data.transpose()
        file_spec = qtw.QFileDialog.getSaveFileName()[0]
        np.savetxt(file_spec, data)    

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