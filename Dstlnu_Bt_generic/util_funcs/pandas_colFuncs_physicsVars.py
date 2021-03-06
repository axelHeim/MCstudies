import numpy as np
import pandas as pd
import math

def Mbc_Btag(s):
    
    fourVec_tag_cmsX = s["CMSpx_summed_X"] + s["Hc_cmPx"]
    fourVec_tag_cmsY = s["CMSpy_summed_X"] + s["Hc_cmPy"]
    fourVec_tag_cmsZ = s["CMSpz_summed_X"] + s["Hc_cmPz"]
    
    
    sqrt_s = 10.580 # centre-of-mass energy
    Mbc = math.sqrt(abs((sqrt_s/2.0)**2 -  ((fourVec_tag_cmsX)**2 + (fourVec_tag_cmsY)**2 + (fourVec_tag_cmsZ)**2)))
        
    
    
    return Mbc

""" 

'px_summed_bg', 'py_summed_bg', 'pz_summed_bg', 'E_summed_bg',
       'CMSpx_summed_bg', 'CMSpy_summed_bg', 'CMSpz_summed_bg',
       'CMSE_summed_bg', 'px_summed_X', 'py_summed_X', 'pz_summed_X',
       'E_summed_X', 'CMSpx_summed_X', 'CMSpy_summed_X', 'CMSpz_summed_X',
       'CMSE_summed_X', 'px_summed_Bs', 'py_summed_Bs', 'pz_summed_Bs',
       'E_summed_Bs', 'CMSpx_summed_Bs', 'CMSpy_summed_Bs', 'CMSpz_summed_Bs',
       'CMSE_summed_Bs', 'Hc_px', 'Hc_py', 'Hc_pz', 'Hc_E', 'Hc_cmpx',
       'Hc_cmpy', 'Hc_cmpz', 'Hc_cmE'
 """

def MM2recoilSignalSide(s):  # from Giannas thesis p.24
    variables = ["px","py","pz","E"]
    fourVec_sig = []
    fourVec_tag = []
    for i in range(4):
        var = variables[i]
        fourVec_sig.append(s[f'CMS{var}_summed_Bs'])
        fourVec_tag.append(s[f'CMS{var}_summed_X'])
    
    for i in range(3):
        var = variables[i]
        fourVec_tag[i] += s[f'Hc_cm{var}']
    
    
    sqrt_s = 10.580 # centre-of-mass energy
    fourVec_tag[3] = -sqrt_s/2

    vec=[]
    for k in range(4):
        vec.append(-fourVec_tag[k] -fourVec_sig[k])
    
    # E^2 - p^2
    MM2 = (vec[3])**2 - ((vec[0])**2 + (vec[1])**2 + (vec[2])**2)
    
    return MM2




def deltaE(s):
    sqrt_s = 10.580 # centre-of-mass energy
    dE = sqrt_s/2.0 - s["Mbc_Btag"]
    
    return dE
    
    
    
