## run with: 
# no source, no conda deactivate


import basf2 as b2

import modularAnalysis as ma
from variables import variables as v
import variables.collections as vc


from stdCharged import stdCharged
from stdPhotons import stdPhotons 
from stdPi0s import stdPi0s


import vertex as vx


import sys
sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/NAHS/utils')
from aliases import define_aliases_Bsig, define_aliases_FSPs, define_aliases_Upsilon4S

import pdg
pdg.add_particle("Hc", 9876555, 0, 0, 0, 0)
pdg.add_particle("X", 9000000, 0, 0, 0, 0)

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictUps4S= define_aliases_Upsilon4S()
add_aliases(AliasDictUps4S)


AliasDictFSPs= define_aliases_FSPs()
print(AliasDictFSPs)
add_aliases(AliasDictFSPs)
outvars_FSPs = list(AliasDictFSPs.keys()) 

outvars_FSPs += ['isSignal', 'uniqueParticleIdentifier','mcErrors','mcPDG','genMotherID','genMotherP',
 'genMotherPDG','charge','dr','dz','clusterReg','clusterE9E21','M','PDG','genParticleID']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs += vc.pid 

nn_vars = ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID",
           "electronID","muonID","protonID"]
outvars_FSPs += nn_vars 


identifier = str(sys.argv[1])

#outpath="/nfs/dust/belle2/user/axelheim/MC_studies/ROEcleanup/caupi/onlineRawData/test/"
outpath="/nfs/dust/belle2/user/axelheim/MC_studies/ROEcleanup/caupi/onlineRawData/Bsig_isSig1/"


path = b2.create_path()

input_file = str(sys.argv[2])
ma.inputMdst(input_file, path=path)


### cut for D*lnu
ma.applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] and [[abs_genUp4S_PDG_0_1 == 11.0] or [abs_genUp4S_PDG_0_1 == 13.0]] and [[abs_genUp4S_PDG_0_2 == 12.0] or [abs_genUp4S_PDG_0_2 == 14.0]]] or [[abs_genUp4S_PDG_1_0 == 413.0] and [[abs_genUp4S_PDG_1_1 == 11.0] or [abs_genUp4S_PDG_1_1 == 13.0]] and [[abs_genUp4S_PDG_1_2 == 12.0] or [abs_genUp4S_PDG_1_2 == 14.0]]]]''', path)



###################
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



ma.cutAndCopyList('pi+:saveForEvtCount',"pi+:eventShapeForSkims",'', path= path)
ma.rankByHighest('pi+:saveForEvtCount', 'px', numBest=1, path=path)
ma.variablesToNtuple('pi+:saveForEvtCount', variables="px", filename=outpath + 'evt_counter_' + identifier + '.root', path=path)




##### B-sig reconstruction from Gianna
# reconstruct FSPs
stdCharged('pi','all', path=path)
stdCharged('K','all', path=path)
stdPi0s('eff40_May2020', path=path) # same as Giannas loose list: https://software.belle2.org/sphinx/release-04-02-09/_modules/stdPi0s.html#stdPi0s

#ma.reconstructDecay('pi0:forX -> gamma:all gamma:all','M > 0.124 and M < 0.140', path=path)

ma.fillParticleList('K-:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and kaonID > 0.6 and pionID<0.6 and \
            muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
ma.fillParticleList('pi+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and pionID > 0.6 and kaonID < 0.6 and \
            electronID < 0.9 and  muonID < 0.9 and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
ma.fillParticleList('e+:cande',"abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and \
            electronID > 0.9 and theta > 0.297 and theta < 2.618", path=path)
ma.fillParticleList('mu+:candmu', "abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and \
            muonID > 0.9 and electronID < 0.9 and theta > 0.297 and theta < 2.618", path=path)
ma.fillParticleList('p+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and protonID > 0.6 and kaonID < 0.6 \
            and pionID<0.6 and muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
ma.cutAndCopyList('gamma:forX', 'gamma:all', "[clusterReg==1 and pt>0.02 and clusterZernikeMVA > 0.35] or \
            [clusterReg==2 and pt>0.03 and clusterZernikeMVA > 0.15] or [clusterReg==3 and pt>0.02 and clusterZernikeMVA > 0.4]", path=path)


roeinputs = ['gamma:forX','pi+:forX','K+:forX','p+:forX', 'e+:cande','mu+:candmu']



ma.cutAndCopyList('pi+:slow', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2', path=path)
ma.cutAndCopyList('pi+:sig', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)
ma.cutAndCopyList('K+:sig', 'K+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)

# ##Reconstruct Signal side ###

ma.reconstructDecay('D0:kpi -> K-:sig pi+:sig', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipipi -> K-:sig pi+:sig pi-:sig pi+:sig', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipi0 -> K-:sig pi+:sig pi0:eff40_May2020', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipipipi0 -> K-:sig pi+:sig pi-:sig pi+:sig pi0:eff40_May2020', '1.8 < M < 1.9', path=path)
ma.copyLists('D0:cand', ['D0:kpi','D0:kpipipi','D0:kpipi0','D0:kpipipipi0'], path=path)

path.add_module('MCMatcherParticles', listName='D0:cand', looseMCMatching=True)

ma.reconstructDecay('D*+:kpi -> D0:cand pi+:slow', '0.139<massDifference(0)<0.16', path=path)

path.add_module('MCMatcherParticles', listName='D*+:kpi', looseMCMatching=True)

ma.reconstructDecay('anti-B0:Dstkpie -> D*+:kpi e-:cande', '', path=path)
ma.reconstructDecay('anti-B0:Dstkpimu -> D*+:kpi mu-:candmu', '', path=path)
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpie')
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpimu')
ma.copyLists('anti-B0:sig', ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu'], path=path)


#vx.fitVertex('anti-B0:sig', 0.0, path=path)
vx.treeFit("anti-B0:sig", conf_level=0, path=path)

# BCS for Bsig based on chi squared of vertex fit as described here (3.1) by Chaoyi: https://docs.belle2.org/record/2084/files/BELLE2-CONF-PH-2020-008.pdf
ma.cutAndCopyList('anti-B0:BCS', 'anti-B0:sig', "", path=path)

ma.rankByLowest("anti-B0:BCS", 'abs(chiProb)', numBest=1, outputVariable='chiSq_rank', path=path)
v.addAlias('chiSquare_rank', 'extraInfo(chiSq_rank)')

# cut for Bsig isSig==1
ma.cutAndCopyList('anti-B0:BCS2',"anti-B0:BCS",'[isSignalAcceptMissingNeutrino == 1]', path= path)

# only proceed if the list con tain exactly one Bsig candidate
ma.applyEventCuts('[countInList(anti-B0:BCS2) == 1]', path)




AliasDictBsig= define_aliases_Bsig()
print(AliasDictBsig)
add_aliases(AliasDictBsig)
outvars_Bsig = list(AliasDictBsig.keys()) 




ma.variablesToNtuple('anti-B0:BCS2',
                  ['chiSquare_rank', 'chiProb'] + outvars_Bsig,
                  filename=outpath + 'Bsig_cand_' + identifier + '.root',
                  path=path)





""" 
track_selection=" and ".join(
            [
                "[dr < 2]",
                "[abs(dz) < 4]",
                "[nCDCHits > 0]",
                "[thetaInCDCAcceptance==1]"
            ]
)
ecl_selection="[[[clusterReg==1] and [pt>0.02] and [clusterZernikeMVA > 0.35]] or [[clusterReg==2] and [pt>0.03] and [clusterZernikeMVA > 0.15]] or [[clusterReg==3] and [pt>0.02] and [clusterZernikeMVA > 0.4]]]"
roe_mask = (track_selection, ecl_selection)


ma.appendROEMask('anti-B0:sig', "cleanMask", roe_mask[0], roe_mask[1], path=path)
ma.buildContinuumSuppression('anti-B0:sig', 'cleanMask',path=path)
 """
 
 
v.addAlias('Bsig_used', 'isDescendantOfList(anti-B0:BCS)')

pdg.add_particle("ROE_of_Bsig", 98766789, 0, 0, 0, 0)
ma.combineAllParticles(roeinputs, "ROE_of_Bsig:all", cut='[Bsig_used == 0]', path=path)

outvars_FSPs.append('Bsig_used')

# delete duplicates in outvars
from collections import OrderedDict
outvars_FSPs = list(OrderedDict.fromkeys(outvars_FSPs))

#roeinputs = ['gamma:forX','pi+:forX','K+:forX','p+:forX', 'e+:cande','mu+:candmu']




# save all FSPs
ma.variablesToNtuple('pi+:forX', variables=outvars_FSPs, filename=outpath + 'pions_' + identifier + '.root', path=path)
ma.variablesToNtuple('K+:forX', variables=outvars_FSPs, filename=outpath + 'kaons_' + identifier + '.root', path=path)
ma.variablesToNtuple('e+:cande', variables=outvars_FSPs, filename=outpath + 'electrons_' + identifier + '.root', path=path)
ma.variablesToNtuple('mu+:candmu', variables=outvars_FSPs, filename=outpath + 'muons_' + identifier + '.root', path=path)
ma.variablesToNtuple('p+:forX', variables=outvars_FSPs, filename=outpath + 'protons_' + identifier + '.root', path=path)
ma.variablesToNtuple('gamma:forX', variables=outvars_FSPs, filename=outpath + 'gammas_' + identifier + '.root', path=path)




b2.process(path)#, max_event=40000)

print(b2.statistics)


print("**************")
print("THIS IS GONNA CHANGE THE WORLD!!!")
print("**************")