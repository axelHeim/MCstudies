""" 
Steering file to run only the FEI and check if event is B->D*lnu
and subsequently save all FSPs
 """
import basf2
#like that no need for basf2. before fcts
from basf2 import *
from modularAnalysis import *
from stdPhotons import stdPhotons 

from variables import variables as v
import vertex as vx
from stdPhotons import stdPhotons 
from stdCharged import stdCharged
from stdPi0s import stdPi0s

import variables.collections as vc
import fei
import sys

sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/NAHS/utils')
from aliases import define_aliases

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDict= define_aliases()
print(AliasDict)
add_aliases(AliasDict)

#import pdg
#pdg.add_particle("Hc", 9876555, 0, 0, 0, 0)

path = create_path()
inputMdstList('default', [], path)


v.addAlias('foxWolframR2_maskedNaN', 'ifNANgiveX(foxWolframR2,1)')

# continuum suppression event cuts as used by Gianna
fillParticleList(decayString='pi+:eventShapeForSkims',
                        cut='d0<0.5 and -2<z0<2 and pt>0.1', path=path)
fillParticleList(decayString='gamma:eventShapeForSkims',
                        cut='E > 0.1 and 0.296706 < theta < 2.61799', path=path)
v.addAlias('E_ECL_pi', 'totalECLEnergyOfParticlesInList(pi+:eventShapeForSkims)')
v.addAlias('E_ECL_gamma', 'totalECLEnergyOfParticlesInList(gamma:eventShapeForSkims)')
v.addAlias('E_ECL', 'formula(E_ECL_pi+E_ECL_gamma)')


applyEventCuts('nCleanedTracks(abs(z0) < 2.0 and abs(d0) < 0.5 and pt>0.1)>=3', path=path)
applyEventCuts('nCleanedECLClusters(0.296706 < theta < 2.61799 and E>0.2)>=3', path=path)
buildEventKinematics(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'], path=path)
applyEventCuts('visibleEnergyOfEventCMS>4', path=path)
applyEventCuts('2<E_ECL<7', path=path)

buildEventShape(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'],
                       allMoments=False,
                       foxWolfram=True,
                       harmonicMoments=False,
                       cleoCones=False,
                       thrust=False,
                       collisionAxis=False,
                       jets=False,
                       sphericity=False,
                       checkForDuplicates=False,
                       path=path)
applyEventCuts('foxWolframR2_maskedNaN<0.4 and nTracks>=4', path=path)


### cut for D*lnu
           
applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] AND 
                [abs_genUp4S_PDG_0_1 == 11.0] OR [abs_genUp4S_PDG_0_1 == 13.0] AND 
                [abs_genUp4S_PDG_0_2 == 12.0] OR [abs_genUp4S_PDG_0_2 == 14.0]] OR
                [[abs_genUp4S_PDG_1_0 == 413.0] AND 
                [abs_genUp4S_PDG_1_1 == 11.0] OR [abs_genUp4S_PDG_1_1 == 13.0] AND 
                [abs_genUp4S_PDG_1_2 == 12.0] OR [abs_genUp4S_PDG_1_2 == 14.0]]]''', path)

### FEI part
particles = fei.get_default_channels(baryonic=True)


conditions.prepend_globaltag(getAnalysisGlobaltag()) # needed for FEI prefix  FEIv4_2021_MC14_release_05_01_12  ;from: https://questions.belle2.org/question/11130/b2bii-global-tag-error-in-release-05-02-06/
configuration = fei.config.FeiConfiguration(prefix='FEIv4_2021_MC14_release_05_01_12', training=False, monitor=False)
feistate = fei.get_path(particles, configuration)

path.add_path(feistate.path)

# now take best H_c and check if isSignal==1
cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>0.001', path= path)

all_Hcs = ["DstpDstl" ,"Dst0Dstl", "DpDstl","D0Dstl", "LcDstl", "DsDstl","JpsiDstl"]
Hc_dict={
    "DstpDstl" : 'D*-',
    "Dst0Dstl" : 'anti-D*0',
    "DpDstl" : 'D-',
    "D0Dstl" : 'anti-D0',
    "LcDstl" : 'anti-Lambda_c-',
    "DsDstl" : 'D_s+',
    "JpsiDstl" : 'J/psi'
}


for Hc in all_Hcs:
    path.add_module('MCMatcherParticles', listName=f'{Hc_dict[Hc]}:genericsigProb', looseMCMatching=True)

    applyCuts(f'{Hc_dict[Hc]}:genericsigProb', 'isSignalAcceptMissingGamma == 1', path=path)

    variablesToNtuple(f'{Hc_dict[Hc]}:genericsigProb',
                    ['extraInfo(SignalProbability)',
                    'isSignalAcceptMissingGamma',
                    'PDG'],
                    filename=f'{Hc}.root',
                    path=path)

sigProbList = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]


applyEventCuts(f'''[[countInList({sigProbList[0]}) > 0] OR
                [countInList({sigProbList[1]}) > 0] OR
                [countInList({sigProbList[2]}) > 0] OR
                [countInList({sigProbList[3]}) > 0] OR
                [countInList({sigProbList[4]}) > 0] OR
                [countInList({sigProbList[5]}) > 0] OR
                [countInList({sigProbList[6]}) > 0]]''', path)



## cut for D* l nu
## add alias for sigProb
## online cuts
## vars in extra file: Hc + FSPs: CM vars , 4mom 
"[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]"
"""       goodGammaRegion1 = region == 1 && energy > 0.100;
      goodGammaRegion2 = region == 2 && energy > 0.050;
      goodGammaRegion3 = region == 3 && energy > 0.150;
 """


process(path, max_event=500)  
