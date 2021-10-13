import basf2
#like that no need for basf2. before fcts
from basf2 import *
from modularAnalysis import *
#from stdPhotons import stdPhotons 

#from variables import variables as v
#import vertex as vx
#from stdPhotons import stdPhotons 
#from stdCharged import stdCharged
#from stdPi0s import stdPi0s

#import variables.collections as vc
import fei
import skim

from glob import glob

from skim.fei import BaseFEISkim 


#from skim.systematics import SystematicDstar
""" 
class mySkim(BaseFEISkim):
    def __init__(self, particles):
        FEIChannelArgs = particles
   """
  
#@_FEI_skim_header(["B0", "B+"])
class ah_skim(BaseFEISkim):
    __description__ = "skim as done in Gianna's script"

    FEIChannelArgs = {
        "neutralB": True,
        "chargedB": True,
        "hadronic": True,
        "semileptonic": True,
        "KLong": False,
        "baryonic": True,
        "removeSLD": False
    }

#B_extra_cut=None, hadronic=True, semileptonic=True, KLong=False, baryonic=True, chargedB=True, neutralB=True, convertedFromBelle=False, specific=False, removeSLD=False

    def build_lists(self, path):
        ma.cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
        ma.cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
        ma.cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>0.001', path= path)
        ma.cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>0.001', path= path)
        ma.cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>0.001', path= path)
        ma.cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>0.001', path= path)
        ma.cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>0.001', path= path)
        
        HcLists = ['anti-D*0:genericsigProb', 'D*-:genericsigProb', 'D-:genericsigProb', 
            'anti-D0:genericsigProb', 'anti-Lambda_c-:genericsigProb', 'D_s+:genericsigProb', 
            'J/psi:genericsigProb']

        self.SkimLists = HcLists

path = create_path()

inputMdstList('default', [], path)

particles = fei.get_default_channels(baryonic=True)

#######important:
#fei_precuts(path)





#configuration = fei.config.FeiConfiguration(prefix='FEIv4_2020_MC13_release_04_01_01', training=False, monitor=False)
#feistate = fei.get_path(particles, configuration)

#path.add_path(feistate.path)
#FEIChannelArgs=particles ,
myFEI_skim = ah_skim(OutputFileName="ah_skim.udst")

myFEI_skim(path)
print(myFEI_skim.SkimLists)
print(myFEI_skim.fei_precuts)


process(path, max_event=100)  
