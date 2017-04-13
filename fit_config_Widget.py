import sys
from PyQt4 import QtGui, QtCore
import ConfigParser
import RFmodels 
import numpy as np
from lmfit import Model


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
        fit_cfg_layout = QtGui.QGridLayout()
        
        function_list = rem_builtins(dir(RFmodels))
        
        self.model_selector = QtGui.QComboBox(self)
        self.model_selector.addItems(function_list)

        self.model_selector.currentIndexChanged.connect(self.find_models)
                
        
        c_label = QtGui.QLabel('C',self)
        r_label = QtGui.QLabel('R',self)
        ra_label = QtGui.QLabel('Ra',self)
        val_lbl = QtGui.QLabel('start val',self)
        min_lbl = QtGui.QLabel('min',self)
        max_lbl = QtGui.QLabel('max',self)
        vary_lbl = QtGui.QLabel('vary?',self)

        c_val_edt = QtGui.QLineEdit(self)   
        c_min_edt = QtGui.QLineEdit(self)
        c_max_edt = QtGui.QLineEdit(self)
        c_vary_chk = QtGui.QCheckBox(self)
        r_val_edt = QtGui.QLineEdit(self)   
        r_min_edt = QtGui.QLineEdit(self)
        r_max_edt = QtGui.QLineEdit(self)  
        r_vary_chk = QtGui.QCheckBox(self)
        ra_val_edt = QtGui.QLineEdit(self)   
        ra_min_edt = QtGui.QLineEdit(self)
        ra_max_edt = QtGui.QLineEdit(self)
        ra_vary_chk = QtGui.QCheckBox(self)
        
        fit_cfg_layout.addWidget(self.model_selector,0,0)
        fit_cfg_layout.addWidget(c_label, 1,0)
        fit_cfg_layout.addWidget(r_label, 2,0)
        fit_cfg_layout.addWidget(ra_label, 3,0)        
        fit_cfg_layout.addWidget(val_lbl, 0,1)
        fit_cfg_layout.addWidget(min_lbl, 0,2)
        fit_cfg_layout.addWidget(max_lbl, 0,3)
        fit_cfg_layout.addWidget(vary_lbl, 0,4)
        fit_cfg_layout.addWidget(c_val_edt, 1,1)
        fit_cfg_layout.addWidget(c_min_edt, 1,2)
        fit_cfg_layout.addWidget(c_max_edt, 1,3)
        fit_cfg_layout.addWidget(c_vary_chk, 1,4)
        fit_cfg_layout.addWidget(r_val_edt, 2,1)
        fit_cfg_layout.addWidget(r_min_edt, 2,2)
        fit_cfg_layout.addWidget(r_max_edt, 2,3)
        fit_cfg_layout.addWidget(r_vary_chk, 2,4)
        fit_cfg_layout.addWidget(ra_val_edt, 3,1)
        fit_cfg_layout.addWidget(ra_min_edt, 3,2)
        fit_cfg_layout.addWidget(ra_max_edt, 3,3)
        fit_cfg_layout.addWidget(ra_vary_chk, 3,4)
        
        
        self.setLayout(fit_cfg_layout)
        self.setGeometry(50, 50, 300, 600)
        self.setWindowTitle('Configure Fit')   
        self.show()
        
    def find_models(self,i):
        cur_mod = Model(getattr(RFmodels,self.model_selector.currentText()))
        self.var_list = cur_mod.param_names
        print self.var_list
        return
        
        
        