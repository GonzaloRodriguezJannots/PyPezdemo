# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 19:56:40 2021

@author: Pc
"""

from PyQt5.QtWidgets import *
from GUI import *
import sys
import numpy as np
import scipy.signal as sig
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        #Acomodo todos los connct por compoennte asi se ve bien en que orden se ejecuta cada función
        
        
        self.pushButton_addpole.clicked.connect(self.add_pole)
        self.pushButton_addpole.clicked.connect(self.igual_zp)
        self.pushButton_addpole.clicked.connect(self.del_zp)
        self.pushButton_addpole.clicked.connect(self.ecuation)
        self.pushButton_addpole.clicked.connect(lambda:self.magnitude_plot())
        self.pushButton_addpole.clicked.connect(lambda:self.phase_plot())
        self.pushButton_addpole.clicked.connect(lambda:self.impulse_plot())        
        self.pushButton_addpole.clicked.connect(lambda:self.zp_plt())
        
        self.pushButton_addzero.clicked.connect(self.add_zero)
        self.pushButton_addzero.clicked.connect(self.igual_zp)
        self.pushButton_addzero.clicked.connect(self.del_zp)
        self.pushButton_addzero.clicked.connect(self.ecuation)
        self.pushButton_addzero.clicked.connect(lambda:self.magnitude_plot())
        self.pushButton_addzero.clicked.connect(lambda:self.phase_plot())
        self.pushButton_addzero.clicked.connect(lambda:self.impulse_plot())
        self.pushButton_addzero.clicked.connect(lambda:self.zp_plt())
        
        self.pushButton_deletepole.clicked.connect(self.delete_pole)
        self.pushButton_deletepole.clicked.connect(self.igual_zp)
        self.pushButton_deletepole.clicked.connect(self.del_zp)
        self.pushButton_deletepole.clicked.connect(self.ecuation)
        self.pushButton_deletepole.clicked.connect(lambda:self.magnitude_plot())
        self.pushButton_deletepole.clicked.connect(lambda:self.phase_plot())
        self.pushButton_deletepole.clicked.connect(lambda:self.impulse_plot())
        self.pushButton_deletepole.clicked.connect(lambda:self.zp_plt())
        
        self.pushButton_deletezero.clicked.connect(self.delete_zero)
        self.pushButton_deletezero.clicked.connect(self.igual_zp)
        self.pushButton_deletezero.clicked.connect(self.del_zp)
        self.pushButton_deletezero.clicked.connect(self.ecuation)
        self.pushButton_deletezero.clicked.connect(lambda:self.magnitude_plot())
        self.pushButton_deletezero.clicked.connect(lambda:self.phase_plot())
        self.pushButton_deletezero.clicked.connect(lambda:self.impulse_plot())
        self.pushButton_deletezero.clicked.connect(lambda:self.zp_plt())
        
        self.pushButton_gain.clicked.connect(self.add_gain)
        self.pushButton_gain.clicked.connect(lambda:self.magnitude_plot())
        self.pushButton_gain.clicked.connect(lambda:self.phase_plot())
        self.pushButton_gain.clicked.connect(lambda:self.impulse_plot())


    #Agrega polos a la lista
    def add_pole(self):
        pole = self.line_pole.text()
        self.listWidget_pole.insertItem(0, str(pole))

    #Elimina un polo de la lista
    def delete_pole(self):
        pole = self.listWidget_pole.selectedItems()
        if len(pole) == 0:
            return
        else: self.listWidget_pole.takeItem(self.listWidget_pole.row(pole[0]))            
 
    #Agrega ceros a la lista
    def add_zero(self):
        zero = self.line_zero.text()
        self.listWidget_zero.insertItem(0, str(zero))

    #Elimina un polo de la lista
    def delete_zero(self):
        zero = self.listWidget_zero.selectedItems()
        if len(zero) == 0:
            return
        else: self.listWidget_zero.takeItem(self.listWidget_zero.row(zero[0]))     

    def igual_zp(self):
        '''Agrega ceros o polos en el (0,0) si hay mas de uno que del otro'''
        zeros = self.get_zeros_list()
        poles = self.get_poles_list()

        
        if len(zeros)>len(poles):
            if len(zeros)-len(poles) == 1:
                self.listWidget_pole.insertItems(0, ['0'])
            else:
                self.listWidget_pole.insertItems(0, str(np.zeros(len(zeros)-len(poles))))
        elif len(zeros)<len(poles):
            if len(poles)-len(zeros) == 1:
                self.listWidget_zero.insertItems(0, ['0'])
            else:
                self.listWidget_zero.insertItems(0, str(np.zeros(len(poles)-len(pzeros))))
               
    #No encontre un método que cree una lista con todos los items de un Widget, por eso cree estas funciones
    def get_poles_list(self):
        ''' Devuelve una lista con todos los polos del WidgetList_pole'''
        itemsTextList =  [str(self.listWidget_pole.item(i).text()) for i in range(self.listWidget_pole.count())]
        return itemsTextList 
    
    def get_zeros_list(self):
        ''' Devuelve una lista con todos los zeros del WidgetList_zero'''
        itemsTextList =  [str(self.listWidget_zero.item(i).text()) for i in range(self.listWidget_zero.count())]
        return itemsTextList 

    def del_zp(self):
        '''Elimina polos y ceros que estén en el mismo lugar'''
        zeros = self.get_zeros_list()
        poles = self.get_poles_list()
        zeros_bis = np.copy(zeros)
        poles_bis = np.copy(poles)
        #Estos for borran items duplciados de cada lista
        for i in zeros:
            if i in poles:
                try:
                    poles.remove(i)
                except: 
                    pass
                
        for i in poles_bis:
            if i in zeros:
                try:
                    zeros.remove(i)
                except:
                    pass
                     
        #Borro todos los items del Widget y vuelvo a poner solo los no repetidos 
        #Debe haber formas mas eficientes de hacer esta parte, pero esta funciona bien por ahora
        
        self.listWidget_zero.clear()
        self.listWidget_pole.clear()
        

        if len(zeros) == 1:
            self.listWidget_zero.insertItems(0, zeros)
        else:    
            self.listWidget_zero.insertItems(0, zeros)
                
        if len(zeros) == 1:
            self.listWidget_pole.insertItems(0, poles)
        else:    
            self.listWidget_pole.insertItems(0, poles)

    def get_complex_zeros(self):
        '''Devuelve la lista de ceros en forma compleja
        Esta función también tiene formas de hacerla mas eficiente'''
        zeros = self.get_zeros_list()
        for i in range(len(zeros)): zeros[i] = complex(zeros[i])
        return zeros
    
    def get_complex_poles(self):
        '''Devuelve la lista de polos en forma compleja
        Esta función también tiene formas de hacerla mas eficiente'''
        poles = self.get_poles_list()
        for i in range(len(poles)): poles[i] = complex(poles[i])
        return poles
    
    def ecuation(self):
        zeros = self.get_complex_zeros()
        poles = self.get_complex_poles()
        
        num, den = sig.zpk2tf(zeros,poles,1)
        
        poly_num = np.poly1d(num, variable='z')
        poly_den = np.poly1d(den, variable='z')
        
        self.label_num.setText(str(poly_num))
        self.label_den.setText(str(poly_den))

    def add_gain(self):
        gain = self.line_gain.text()
        self.label_ec_gain.setText(gain)


#-----------------------------------------------------------------------------#
#                                  PLOTEO                                     # 
#-----------------------------------------------------------------------------#

    def magnitude_plot(self):
        self.magnitudeGraph.clear()
        
        zeros = self.get_complex_zeros()
        poles = self.get_complex_poles()
        gain = float(self.line_gain.text())
        
        w, h = sig.freqz_zpk(zeros,poles,gain)
        
        self.magnitudeGraph.plot(w/np.pi,abs(h),pen='r')
        self.magnitudeGraph.showGrid(x=True,y=True)
        self.magnitudeGraph.setLabel('bottom', 'Frecuencia', units='Pi')        
        
    def phase_plot(self):
        self.phaseGraph.clear()
        
        zeros = self.get_complex_zeros()
        poles = self.get_complex_poles()
        gain = float(self.line_gain.text())
        
        w, h = sig.freqz_zpk(zeros,poles,gain)
        
        self.phaseGraph.plot(w/np.pi,np.angle(h),pen='r')
        self.phaseGraph.showGrid(x=True,y=True)
        self.phaseGraph.setLabel('bottom', 'Frecuencia', units='Pi')
        
    def impulse_plot(self):
        self.impulseGraph.clear()
        
        zeros = self.get_complex_zeros()
        poles = self.get_complex_poles()
        gain = float(self.line_gain.text())
        
        w, h = sig.freqs_zpk(zeros,poles,gain)
        
        self.impulseGraph.addLegend([0,0])
        self.impulseGraph.plot(w,np.real(h),pen='y', name = 'Parte Real')
        self.impulseGraph.plot(w,np.imag(h),pen='b',name = 'Parte Imaginaria')
        self.impulseGraph.showGrid(x=True,y=True)
        self.impulseGraph.setLabel('bottom', 'Time', units='s')



    def zp_plt(self):
        zeros_complex = self.get_complex_zeros()
        poles_complex = self.get_complex_poles()
        
        zeros_re = []
        zeros_im = []
        poles_re = []
        poles_im = []
        
        for i in range(len(zeros_complex)):
            zeros_re = np.append(zeros_re, np.real(zeros_complex[i]))
            zeros_im = np.append(zeros_im, np.imag(zeros_complex[i]))
            poles_re = np.append(poles_re, np.real(poles_complex[i]))
            poles_im = np.append(poles_im, np.imag(poles_complex[i]))
        
        self.polezeroGraph.clear()
        zp_plt = self.polezeroGraph
        
        self.polezeroGraph.showGrid(x=True,y=True)
        circle = pg.QtGui.QGraphicsEllipseItem(-1, -1, 2, 2)
        circle.setPen(pg.mkPen(color='w'))
        zp_plt.addItem(circle)
        
        zeros = pg.ScatterPlotItem(zeros_re,zeros_im)
        zp_plt.addItem(zeros)
        
        poles = pg.ScatterPlotItem(poles_re,poles_im,symbol='x',size=13)
        poles.setPen(pg.mkPen(color='r'))
        zp_plt.addItem(poles)
        













if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()