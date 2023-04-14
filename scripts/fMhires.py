import numpy as np
import pynbody 

def calculate(sim_fn):
    s = pynbody.load(sim_fn)
    s.physical_units()

    h = s.halos()
    
    h1 = h[1]

    high_res_mass = min(h[1].d['mass'])
    fMhires = sum(h1.d[h1.d['mass'] == high_res_mass]['mass']) / sum(h1.d['mass'])

    return fMhires
     
