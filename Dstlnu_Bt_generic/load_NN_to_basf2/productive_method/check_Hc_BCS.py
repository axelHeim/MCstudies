# Now let's import torch and basf2 and try to load our model


import torch

import basf2 as b2

import modularAnalysis as ma
from variables import variables as v
import variables.collections as vc


from stdCharged import stdMostLikely
from stdPhotons import stdPhotons 

import fei
import sys
sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/NAHS/utils')
from aliases import define_aliases_Hc, define_aliases_FSPs, define_aliases_Upsilon4S

import pdg
pdg.add_particle("Hc", 9876555, 0, 0, 0, 0)
pdg.add_particle("X", 9000000, 0, 0, 0, 0)

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictHc= define_aliases_Hc()
add_aliases(AliasDictHc)
AliasDictUps4S= define_aliases_Upsilon4S()
add_aliases(AliasDictUps4S)

from bsm_customModule import bsm_customModule

identifier = str(sys.argv[1])

outpath="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/check_Hc_BCS/1stRun/"


# Do some basic basf2 stuff
path = b2.create_path()
#ma.inputMdst("/nfs/dust/belle2/user/axelheim/mixed_generic_MC14ri_a/mdst_000001_prod00016816_task10020000001.root", path=path)

input_file = str(sys.argv[2])
ma.inputMdst(input_file, path=path)


###################
# event cuts for D*lnu etc and FEI

v.addAlias('foxWolframR2_maskedNaN', 'ifNANgiveX(foxWolframR2,1)')

# continuum suppression event cuts as used by Gianna
ma.fillParticleList(decayString='pi+:eventShapeForSkims',
                        cut='d0<0.5 and -2<z0<2 and pt>0.1', path=path)
ma.fillParticleList(decayString='gamma:eventShapeForSkims',
                        cut='E > 0.1 and 0.296706 < theta < 2.61799', path=path)
v.addAlias('E_ECL_pi', 'totalECLEnergyOfParticlesInList(pi+:eventShapeForSkims)')
v.addAlias('E_ECL_gamma', 'totalECLEnergyOfParticlesInList(gamma:eventShapeForSkims)')
v.addAlias('E_ECL', 'formula(E_ECL_pi+E_ECL_gamma)')


ma.applyEventCuts('nCleanedTracks(abs(z0) < 2.0 and abs(d0) < 0.5 and pt>0.1)>=3', path=path)
ma.applyEventCuts('nCleanedECLClusters(0.296706 < theta < 2.61799 and E>0.2)>=3', path=path)
ma.buildEventKinematics(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'], path=path)
ma.applyEventCuts('visibleEnergyOfEventCMS>4', path=path)
ma.applyEventCuts('2<E_ECL<7', path=path)

ma.buildEventShape(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'],
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
ma.applyEventCuts('foxWolframR2_maskedNaN<0.4 and nTracks>=4', path=path)


### cut for D*lnu
ma.applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] and [[abs_genUp4S_PDG_0_1 == 11.0] or [abs_genUp4S_PDG_0_1 == 13.0]] and [[abs_genUp4S_PDG_0_2 == 12.0] or [abs_genUp4S_PDG_0_2 == 14.0]]] or [[abs_genUp4S_PDG_1_0 == 413.0] and [[abs_genUp4S_PDG_1_1 == 11.0] or [abs_genUp4S_PDG_1_1 == 13.0]] and [[abs_genUp4S_PDG_1_2 == 12.0] or [abs_genUp4S_PDG_1_2 == 14.0]]]]''', path)

ma.cutAndCopyList('pi+:saveForEvtCount',"pi+:eventShapeForSkims",'', path= path)
ma.rankByHighest('pi+:saveForEvtCount', 'px', numBest=1, path=path)
ma.variablesToNtuple('pi+:saveForEvtCount', variables="px", filename=outpath + 'evt_counter_' + identifier + '.root', path=path)


### FEI part
particles = fei.get_default_channels(baryonic=True)


b2.conditions.prepend_globaltag(ma.getAnalysisGlobaltag()) # needed for FEI prefix  FEIv4_2021_MC14_release_05_01_12  ;from: https://questions.belle2.org/question/11130/b2bii-global-tag-error-in-release-05-02-06/
configuration = fei.config.FeiConfiguration(prefix='FEIv4_2021_MC14_release_05_01_12', training=False, monitor=False)
feistate = fei.get_path(particles, configuration)

path.add_path(feistate.path)

# now take best H_c and check if isSignal==1
sigprob_cut = 0.001
ma.cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>{} and 0.139<massDifference(0)<0.16'.format(sigprob_cut), path= path)
ma.cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>{} and 0.139<massDifference(0)<0.16'.format(sigprob_cut), path= path)
ma.cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>{}'.format(sigprob_cut), path= path)
ma.cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>{}'.format(sigprob_cut), path= path)
ma.cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>{}'.format(sigprob_cut), path= path)
ma.cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>{}'.format(sigprob_cut), path= path)
ma.cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>{}'.format(sigprob_cut), path= path)

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
v.addAlias('sigProb', 'extraInfo(SignalProbability)')


for Hc in all_Hcs:
    path.add_module('MCMatcherParticles', listName=f'{Hc_dict[Hc]}:genericsigProb', looseMCMatching=True)

    #ma.applyCuts(f'{Hc_dict[Hc]}:genericsigProb', 'isSignalAcceptMissingNeutrino == 1 and abs(genMotherPDG) == 511.0', path=path)
    ma.variablesToNtuple(f'{Hc_dict[Hc]}:genericsigProb',
                    ["PDG","mcPDG","sigProb","isSignalAcceptMissingNeutrino","genMotherPDG"],
                    filename=outpath + f'{Hc}_' + identifier + '.root',
                    path=path)


sigProbList = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]


# combine lists, should now contain exactly one Hc candidate
ma.combineAllParticles(sigProbList, "Hc:used", cut='', path=path)




ma.variablesToNtuple('Hc:used',
                    ["PDG","mcPDG","sigProb","isSignalAcceptMissingNeutrino","genMotherPDG"]
                   ,
                  filename=outpath + 'Hc_' + identifier + '.root',
                  path=path)





b2.process(path, max_event=70000)

print("**************")

print("THIS IS GONNA CHANGE THE WORLD!!!")

print("**************")

