import numpy as np
from lmfit import Model
def dist_rc_ra(w, r, c, ra):
    "Distributed R-C line with access resistance"
    k = np.sqrt(-1.0j*r*c*w)
    tlm = (1j*k/r) * np.tanh(1j*k)
    res = 1.0/(1.0/tlm + ra)
    return res

def lm_dist_rc_ra():
    return Model(dist_rc_ra)
    
    