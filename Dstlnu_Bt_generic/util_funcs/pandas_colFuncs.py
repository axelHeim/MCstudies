import numpy as np
import pandas as pd


def isBtoDstlnu(s):
    isDecay = 0
    

    # thats the wrong way of doing it, we dont want to know if reco is correct, but if 
    # the event on gen level was D* l nu
    #if ((np.abs(s["lep_mcPDG"]) == 13.0) or (np.abs(s["lep_mcPDG"]) == 11.0)): # lepton is electron or muon
    #    if (np.abs(s["lep_motherPDG"]) == 511.0): # leptons mother is B
    #        if (np.abs(s["dau1_dau0_mcPDG"]) == 413.0): # daughter of B-sig is D*+ 
    #            isDecay = 1


    

    return isDecay