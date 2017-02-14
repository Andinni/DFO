#from __future__ import division
from RFLPA.measurement import measurement
import numpy as np
from glob import glob
import ConfigParser
import multiprocessing
from functools import partial
from time import time,sleep
from lmfit import Model
from RFmodels import dist_rc_ra

import sys

def deembed_single_file(meas_f,thru,dummy):
    '''Deembed a single spectrum
    
    Function must be external to Analyser class, 
    otherwise multiprocessing does not work...    
    '''
    meas = measurement(meas_f)
    de_thru = meas.deembed_thru(thru)
    de_thru.create_y()
    full_de = measurement(from_s=thru.y2s(de_thru.y-dummy.y),
                          parent_meas = meas)
    # Somewhere deep in multiprocessing only iterables can be pickled.
    # Standard workaround is to put result in a list.
    return (full_de,) 

class Analyser(object):
    def __init__(self,dut_path,thru_file,dummy_file,parallelize = True):
        self.par = parallelize
        self.DuT_flist = glob(dut_path+'/*.txt')
        self.thru = measurement(thru_file)
        self.dummy_raw = measurement(dummy_file)
        self.dummy = self.dummy_raw.deembed_thru(self.thru)
        self.dummy.create_y()
        self.dummy.plot_mat_spec(self.dummy.y)
        
        # Define single file de-embedding function with a single argument.
        # ... again related to weird behavior of multiprocessing.
        self.de_single = partial(deembed_single_file, 
                                 thru = self.thru, 
                                 dummy = self.dummy)
                                 
        self.all_de_meas = self.deembed_all_dut(self.DuT_flist)
              
        
    def deembed_all_dut(self,files):
        if self.par:
            N_CPU = multiprocessing.cpu_count()-1
            p = multiprocessing.Pool(N_CPU)
            deembedded_meas = np.array(p.map(self.de_single, files))     
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