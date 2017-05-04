#==============================================================================
# Allows parallelized deembedding of data
#==============================================================================
from RFLPA.measurement import measurement
import numpy as np
import ConfigParser
import multiprocessing
from functools import partial
from time import time,sleep
from lmfit import Model
from RFmodels import dist_rc_ra
from PyQt4 import QtCore
import sys


def fit_single_meas(meas,model,freqs):
    '''Fit a single spectrum
    
    Function must be external to Analyser class, 
    otherwise multiprocessing does not work...    
    '''
    xs = freqs
    ys = meas
    model.fit()

    # Somewhere deep in multiprocessing only iterables can be pickled.
    # Standard workaround is to put result in a list.
    return (None, ) 

class Fitter(object):
    def __init__(self, measurement_list, model, parameter='y',element = [0,1],parallelize = True):
        self.parallel = parallelize
        self.parameter = parameter
        self.meas_list = measurement_list
        self.define_fit()
        self.fit_all_meas()
                      
    def define_fit(self):
        self.data2fit = np.array([getattr(m,self.parameter) for m in self.meas_list])
        self.freq = self.meas_list[0].freq
        
    def fit_all_meas(self):
        QtCore.QCoreApplication.processEvents() # Avoids freezing? 
        if self.parallel:
            N_CPU = multiprocessing.cpu_count()-1
            p = multiprocessing.Pool(N_CPU)
            fit_meas = np.array(p.map(self.de_single, files))     
        else:
            deembedded_meas = []
            for f in files:
                deembedded_meas.append(self.de_single(f))
            deembedded_meas = np.array(deembedded_meas)
        deembedded_meas = deembedded_meas[:,0]
        return deembedded_meas
        
    def fit(self,a1,a2):
        #For the moment these are just dummy arguments
        for data in self.all_de_meas:
            data.create_y()
            y12 = data.y[0,1]
            w = data.w
            fit_res = self.fit_single_spec(w,y12,{"a":1})# just dummy dict so far
            data.fit_res = fit_res
 
    def fit_single_spec(self, x,y,fit_dict):
        model = Model(dist_rc_ra)
        fit_res = model.fit(y, w = x, r = 300, c= 1e-12,ra = 100)
        return fit_res
       

if __name__=='__main__':
    config = ConfigParser.RawConfigParser()
    config.read('DFO.cfg')        
    dut_path = config.get('main','dut-dir')
    dummy_file = config.get('main','dummy-dir')
    thru_file = config.get('main','thru-dir') 
    t1 = time()
    ana1 = Analyser(dut_path,thru_file, dummy_file)
    t2 = time()
    ana2 = Analyser(dut_path,thru_file, dummy_file,parallelize=False)
    t3 = time()
    
    print 'Parallelized took {}seconds'.format(t2-t1)
    print 'Serial took {}seconds'.format(t3-t2)