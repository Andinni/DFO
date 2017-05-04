import sys
from PyQt4 import QtGui, QtCore
import ConfigParser
import RFmodels 
import numpy as np
from lmfit import Model
import time

def rem_builtins(module):
    here = np.array(module)
    mask = np.array(["__" not in x for x in here])
    here = here[mask]
    mask = np.array(["np" not in x for x in here])
    here = here[mask]
    mask = np.array(["Model" not in x for x in here])
    here = here[mask]
    return here


class CfgWidget(QtGui.QWidget):
    def __init__(self):
        super(CfgWidget,self).__init__()
        self.initUI()
        
    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.config = ConfigParser.RawConfigParser()
        self.config.read('DFO.cfg')
        
        self.fit_cfg_layout = QtGui.QVBoxLayout(self)
        
        self.function_list = rem_builtins(dir(RFmodels))
        
        self.model_selector = QtGui.QComboBox(self)
        self.model_selector.addItems(self.function_list)
        self.create_stacked_Wdg()  
        self.stacked_Wdg.setCurrentIndex(0)
        self.save_btn = QtGui.QPushButton(self)
        self.save_btn.setText('Save!')

        self.fit_cfg_layout.addWidget(self.model_selector)
        self.fit_cfg_layout.addWidget(self.stacked_Wdg)
        self.fit_cfg_layout.addWidget(self.save_btn)
        self.setLayout(self.fit_cfg_layout)
        self.model_selector.currentIndexChanged.connect(self.change_stackedWdg_index)                
        
        self.save_btn.clicked.connect(self.save2cfg)
        
        self.setGeometry(50, 50, 300, 600)
        self.setWindowTitle('Configure Fit')   
        self.show()
        
    def create_stacked_Wdg(self):
        self.stacked_Wdg = QtGui.QStackedWidget(self)
        for fun in self.function_list:
            mod = Model(getattr(RFmodels,fun))
            var_list = mod.param_names
            new_widget = QtGui.QWidget(self)
            new_layout = QtGui.QGridLayout()
            for i, var in enumerate(var_list):
                label = QtGui.QLabel(var,self)
                val_edt = QtGui.QLineEdit(self)   
                min_edt = QtGui.QLineEdit(self)
                max_edt = QtGui.QLineEdit(self)
                vary_chk = QtGui.QCheckBox(self)
                
                new_layout.addWidget(label, i,0)
                new_layout.addWidget(val_edt, i,1)
                new_layout.addWidget(min_edt, i,2)
                new_layout.addWidget(max_edt, i,3)
                new_layout.addWidget(vary_chk, i,4)
                
            new_widget.setLayout(new_layout)
            self.stacked_Wdg.addWidget(new_widget)

    def change_stackedWdg_index(self):
        self.stacked_Wdg.setCurrentIndex(self.model_selector.currentIndex())


    def save2cfg(self):
        sel_mod = self.model_selector.currentText()
        cur_layout = self.stacked_Wdg.currentWidget().layout()
        items = (cur_layout.itemAt(i) for i in range(cur_layout.count())) 
        if 'fit' in self.config.sections():
            self.config.remove_section('fit')
        
        self.config.add_section('fit')
        
        self.config.set('fit', 'model', str(sel_mod))
        mod = Model(getattr(RFmodels,sel_mod))
        var_list = mod.param_names
        self.config.set('fit','vars','\t'.join(var_list))
        
        for i,w in enumerate(items):
            if i%5==0:
                to_write = []
            elif i%5==4:
                to_write.append(str(w.widget().isChecked()))
            else:
                to_write.append(w.widget().text())
            self.config.set('fit',var_list[i//5],'\t'.join(to_write))

        with open('DFO.cfg', 'wb') as configfile:
            self.config.write(configfile)
            
        print "save was clicked"
