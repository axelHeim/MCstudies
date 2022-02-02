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


def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictUps4S= define_aliases_Upsilon4S()
add_aliases(AliasDictUps4S)
outvars_Ups4S = list(AliasDictUps4S.keys()) 

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

#outpath="/nfs/dust/belle2/user/axelheim/MC_studies/ROEcleanup/moro/onlineRawData/test/"
outpath="/nfs/dust/belle2/user/axelheim/MC_studies/ROEcleanup/moro/onlineRawData/fullBGseparation/"


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


###### create FSP lists to save them

stdCharged('pi','all', path=path)
stdCharged('K','all', path=path)


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

ma.cutAndCopyList('pi+:slow', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2', path=path)
ma.cutAndCopyList('pi+:sig', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)
ma.cutAndCopyList('K+:sig', 'K+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)



ma.cutAndCopyLists('K+:save', ['K+:forX','K+:sig'], '', path=path)
ma.cutAndCopyLists('pi+:save', ['pi+:forX','pi+:slow'], '', path=path)




ma.cutAndCopyList('pi+:saveForEvtCount',"pi+:eventShapeForSkims",'', path= path)
ma.rankByHighest('pi+:saveForEvtCount', 'px', numBest=1, path=path)
ma.variablesToNtuple('pi+:saveForEvtCount', variables=["px"] + outvars_Ups4S, filename=outpath + 'evt_counter_' + identifier + '.root', path=path)






# delete duplicates in outvars
from collections import OrderedDict
outvars_FSPs = list(OrderedDict.fromkeys(outvars_FSPs))

#roeinputs = ['gamma:forX','pi+:forX','K+:forX','p+:forX', 'e+:cande','mu+:candmu']




# save all FSPs
ma.variablesToNtuple('pi+:save', variables=outvars_FSPs, filename=outpath + 'pions_' + identifier + '.root', path=path)
ma.variablesToNtuple('K+:save', variables=outvars_FSPs, filename=outpath + 'kaons_' + identifier + '.root', path=path)
ma.variablesToNtuple('e+:cande', variables=outvars_FSPs, filename=outpath + 'electrons_' + identifier + '.root', path=path)
ma.variablesToNtuple('mu+:candmu', variables=outvars_FSPs, filename=outpath + 'muons_' + identifier + '.root', path=path)
ma.variablesToNtuple('p+:forX', variables=outvars_FSPs, filename=outpath + 'protons_' + identifier + '.root', path=path)
ma.variablesToNtuple('gamma:forX', variables=outvars_FSPs, filename=outpath + 'gammas_' + identifier + '.root', path=path)




b2.process(path)#, max_event=40000)

print(b2.statistics)


print("**************")
print("THIS IS GONNA CHANGE THE WORLD!!!")
print("**************")