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
#import fei
#import skim

from basf2 import *
from modularAnalysis import *
from stdPhotons import stdPhotons 

from variables import variables as v
import vertex as vx
from stdPhotons import stdPhotons 
from stdCharged import stdCharged
from stdPi0s import stdPi0s

import variables.collections as vc


import pdg
#pdg.add_particle("X+", 9000000, 0, 0, 1, 0)
#pdg.add_particle("X0", 9000001, 0, 0, 0, 0)
pdg.add_particle("X", 9000000, 0, 0, 0, 0)


def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

#import sys
#sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/createOwnFEIskim/localTry/')
from aliasDict import define_aliases_Xl


path = create_path()

inputMdstList('default', [], path)

v.addAlias('sigProb', 'extraInfo(SignalProbability)')
v.addAlias('log10_sigProb', 'log10(extraInfo(SignalProbability))')
v.addAlias('dmID', 'extraInfo(decayModeID)')
v.addAlias('foxWolframR2_maskedNaN', 'ifNANgiveX(foxWolframR2,1)')
v.addAlias('cosThetaBY', 'cosThetaBetweenParticleAndNominalB')
v.addAlias('d1_p_CMSframe', 'useCMSFrame(daughter(1,p))')
v.addAlias('d2_p_CMSframe', 'useCMSFrame(daughter(2,p))')

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

basf2.conditions.globaltags = ['analysis_tools_release-04']

""" import fei
particles = fei.get_default_channels(baryonic=True)
# You can turn on and off individual parts of the reconstruction without retraining!
# particles = fei.get_default_channels(hadronic=True, semileptonic=True, chargedB=True, neutralB=True)

configuration = fei.config.FeiConfiguration(prefix='FEIv4_2020_MC13_release_04_01_01', training=False, monitor=False)
feistate = fei.get_path(particles, configuration)

path.add_path(feistate.path)
 """
fillParticleList(decayString='pi+:eventShapeForSkims',
                     cut='pt> 0.1', path=path)
fillParticleList(decayString='gamma:eventShapeForSkims',
                     cut='E > 0.1', path=path)

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

#path.add_module('MCMatcherParticles', listName='B0:generic', looseMCMatching=True)


#rankByHighest('B0:generic', 'extraInfo(SignalProbability)', numBest=1,
#              outputVariable='FEIProbabilityRank', path=path)

# #ROE of B_tag reconstructed by FEI

stdCharged('pi','all', path=path)
stdCharged('K','all', path=path)
stdPi0s('eff40_Jan2020', path=path)

fillParticleList("gamma:myMinimumThresholdList", "clusterE > 0.02", path=path)

reconstructDecay('pi0:forX -> gamma:myMinimumThresholdList gamma:myMinimumThresholdList','M > 0.124 and M < 0.140', path=path)

fillParticleList('K-:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and kaonID > 0.6 \
and pionID<0.6 and muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
fillParticleList('pi+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and pionID > 0.6 \
and kaonID < 0.6 and electronID < 0.9 and  muonID < 0.9 and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
fillParticleList('e+:cande',"abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and electronID > 0.9 and theta > 0.297 and theta < 2.618", path=path)
fillParticleList('mu+:candmu', "abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and muonID > 0.9 and electronID < 0.9 and theta > 0.297 and theta < 2.618", path=path)

fillParticleList('p+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and protonID > 0.6 and kaonID < 0.6 \
and pionID<0.6 and muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)

cutAndCopyList('gamma:forX', 'gamma:myMinimumThresholdList', "[clusterReg==1 and pt>0.02 and clusterZernikeMVA > 0.35] or [clusterReg==2 and pt>0.03 and clusterZernikeMVA > 0.15] or [clusterReg==3 and pt>0.02 and clusterZernikeMVA > 0.4]", path=path)


roeinputs = ['gamma:forX','pi+:forX','K+:forX','p+:forX', 'e+:cande','mu+:candmu']

# define the mask with hard-coded CS cuts in the ROE mask
# ROEmask tuple: (mask name, track cuts, cluster cuts)

#names = ['B0:generic']

#construct ROE for FEI reconstructed B
#for name in names:
# buildRestOfEvent(name,roeinputs, path=path)
# # append both masks to ROE
# appendROEMask(name, "cleanMask", "dr < 2 and abs(dz) < 4 and pt > 0.2", "[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]", path=path)

 # choose one mask which is applied
 #buildContinuumSuppression(name, 'cleanMask',path=path)



cutAndCopyList('pi+:slow', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2', path=path)
cutAndCopyList('pi+:sig', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)
cutAndCopyList('K+:sig', 'K+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)

# ##Reconstruct Signal side ###

reconstructDecay('D0:kpi -> K-:sig pi+:sig', '1.8 < M < 1.9', dmID=1001, path=path)
reconstructDecay('D0:kpipipi -> K-:sig pi+:sig pi-:sig pi+:sig', '1.8 < M < 1.9',dmID=1003, path=path)
#reconstructDecay('D0:kpipi0 -> K-:sig pi+:sig pi0:loose', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipi0 -> K-:sig pi+:sig pi0:eff40_Jan2020', '1.8 < M < 1.9',dmID=1002, path=path)
#reconstructDecay('D0:kpipipipi0 -> K-:sig pi+:sig pi-:sig pi+:sig pi0:loose', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipipipi0 -> K-:sig pi+:sig pi-:sig pi+:sig pi0:eff40_Jan2020', '1.8 < M < 1.9',dmID=1004, path=path)
copyLists('D0:cand', ['D0:kpi','D0:kpipipi','D0:kpipi0','D0:kpipipipi0'], path=path)
#vx.vertexKFit('D0:cand',0.0, path=path)
path.add_module('MCMatcherParticles', listName='D0:cand', looseMCMatching=True)

reconstructDecay('D*+:kpi -> D0:cand pi+:slow', '0.139<massDifference(0)<0.16', path=path)
#vx.vertexKFit('D*+:kpi',0.0, path=path)

path.add_module('MCMatcherParticles', listName='D*+:kpi', looseMCMatching=True)

reconstructDecay('anti-B0:Dstkpie -> D*+:kpi e-:cande', '', path=path)
reconstructDecay('anti-B0:Dstkpimu -> D*+:kpi mu-:candmu', '', path=path)
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpie')
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpimu')
copyLists('anti-B0:sig', ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu'], path=path)
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
for name in ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu']:
    buildRestOfEvent(name,roeinputs, path=path)
    appendROEMask(name, "cleanMask", roe_mask[0], roe_mask[1], path=path)
    buildContinuumSuppression(name, 'cleanMask',path=path)


AliasDict= define_aliases_Xl()
print(AliasDict)
add_aliases(AliasDict)
tagside_variables = list(AliasDict.keys()) 


cutAndCopyList('anti-B0:sigclean',"anti-B0:sig",'-1.5 < cosThetaBetweenParticleAndNominalB < 1.5 and daughter(0,useCMSFrame(p))<2.4 and daughter(1,useCMSFrame(p))>1.', path= path)

#cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
#cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
#cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>0.001', path= path)
#cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>0.001', path= path)
#cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>0.001', path= path)
#cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>0.001', path= path)
#cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>0.001', path= path)


#reconstruct a pseudo upsilon4s from B_sig and H_c to determine ROE of this
reconstructDecay('Upsilon(4S):Dst0Dstl -> anti-B0:sigclean  anti-D*0:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DstpDstl -> anti-B0:sigclean  D*-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DpDstl -> anti-B0:sigclean  D-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):D0Dstl -> anti-B0:sigclean  anti-D0:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):LcDstl -> anti-B0:sigclean  anti-Lambda_c-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DsDstl -> anti-B0:sigclean  D_s+:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):JpsiDstl -> anti-B0:sigclean  J/psi:genericsigProb','',path=path,allowChargeViolation=True)

parts_BHc_all=['Upsilon(4S):DpDstl', 'Upsilon(4S):LcDstl' ,'Upsilon(4S):DsDstl', 'Upsilon(4S):DstpDstl', 'Upsilon(4S):D0Dstl', 
                'Upsilon(4S):JpsiDstl', 'Upsilon(4S):Dst0Dstl']


path.add_module('MCMatcherParticles', listName='anti-D*0:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D*-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='anti-D0:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='anti-Lambda_c-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D_s+:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='J/psi:genericsigProb', looseMCMatching=True)

name_dict={
    "DstpDstl" : 'D*-',
    "Dst0Dstl" : 'anti-D*0',
    "DpDstl" : 'D-',
    "D0Dstl" : 'anti-D0',
    "LcDstl" : 'anti-Lambda_c-',
    "DsDstl" : 'D_s+',
    "JpsiDstl" : 'J/psi'
}

outlists_DX =[]

for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]

    rankByHighest(part_BHc_all, 'daughter(1,extraInfo(SignalProbability))', numBest=0, allowMultiRank=True,
            outputVariable='FEIProbabilityRank_all', path=path)

    applyCuts(part_BHc_all, 'extraInfo(FEIProbabilityRank_all) == 1', path=path)

    cutAndCopyList(f'{name_dict[parid]}:tag',f"{name_dict[parid]}:genericsigProb",f'IsDaughterOf({part_BHc_all}) == 1', path= path)


    buildRestOfEvent(part_BHc_all,roeinputs,path=path)
    appendROEMask(part_BHc_all, 'CleanROEBtag', roe_mask[0], roe_mask[1], path=path)
    ##construct X from ROE
    fillParticleListFromROE(f'X:tag{parid}','',maskName="CleanROEBtag",sourceParticleListName=part_BHc_all ,path=path)
    ##reconstruct B_tag from X and H_c
    reconstructDecay(f'B0:{parid}DXtag -> {name_dict[parid]}:tag X:tag{parid}','',path=path,allowChargeViolation=True)
    reconstructDecay(f'Upsilon(4S):{parid}DXtag -> B0:{parid}DXtag anti-B0:sigclean','',path=path)
    applyCuts(f'Upsilon(4S):{parid}DXtag', 'abs(daughter(0,deltaE))<0.2', path=path)
    outlists_DX.append(f'Upsilon(4S):{parid}DXtag')


copyLists('Upsilon(4S):DXtag', outlists_DX, path=path)

rankByHighest('Upsilon(4S):DXtag', 'daughter(0,daughter(0, extraInfo(SignalProbability)))', numBest=1,
              outputVariable='FEIProbabilityRank', path=path)

path.add_module('MCMatcherParticles', listName='Upsilon(4S):DXtag', looseMCMatching=True)

buildRestOfEvent('Upsilon(4S):DXtag', roeinputs,  path=path)
appendROEMask('Upsilon(4S):DXtag', "CleanROE", "dr < 2 and abs(dz) < 4 and pt > 0.2", "[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]", path=path)



#only proceed with event if a Y(4S) candidate was found 
applyEventCuts("[countInList(Upsilon(4S):DXtag) > 0]", path)
# don't proceed if Hc is not isSignal == 1 to get rid of millions of unwanted events
applyEventCuts("[countInList(Upsilon(4S):DXtag , daughter(0, daughter(0, isSignalAcceptMissingGamma)) == 1) > 0] ", path)




variablesToNtuple('Upsilon(4S):DXtag',
                  [
                   "m2RecoilSignalSide",
                   "foxWolframR2_maskedNaN",
                   'foxWolframR2',
		   'extraInfo(FEIProbabilityRank)',
                   "nTracks"
                   ]+  tagside_variables,
                  filename='DXtagDstl.root',
                  path=path)


### create and cut lists to only contain the finally used Hc,X,Bsig in order to label to the FSPs with them

HcAll = []
X_All = []
BtagAll = []
for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]
    HcAll.append(f'{name_dict[parid]}:tag')
    X_All.append(f'X:tag{parid}')
    BtagAll.append(f'B0:{parid}DXtag')


cutAndCopyLists('B0:tag_onlyUsedOne', BtagAll, "[isDescendantOfList(Upsilon(4S):DXtag) == 1]", path=path)
cutAndCopyLists('X:XonlyUsedOne', X_All, "[isDescendantOfList(B0:tag_onlyUsedOne) == 1]", path=path)
# cannot combine all Hc's because they are different particles, sigh :/
#cutAndCopyLists('X:HcOnlyUsedOne', HcAll, "[isDaughterOfList(B0:tag_onlyUsedOne) > 0]", path=path)

cutAndCopyList('B0:sig_onlyUsedOne', "anti-B0:sigclean", "[isDescendantOfList(Upsilon(4S):DXtag) == 1]", path=path)


# these three vars indicate binary if to what category a particle got assigned by semi-inclusive Hc+X tagging
v.addAlias('basf2_X', 'isDescendantOfList(X:XonlyUsedOne)')
#v.addAlias('YYY', 'isDescendantOfList("pi0:forX")')
v.addAlias('basf2_used', 'isDescendantOfList(Upsilon(4S):DXtag)')
v.addAlias('basf2_Bsig', 'isDescendantOfList(B0:sig_onlyUsedOne)')


outvars_FSPs = ['basf2_X','basf2_used','basf2_Bsig']
#outvars_FSPs = ['isDescendantOfList(B0:sig_onlyUsedOne)']
#'countInList(X:XonlyUsedOne)','countInList(B0:tag_onlyUsedOne)',
outvars_FSPs += ['isSignal', 'uniqueParticleIdentifier',
 'mcErrors',
 'mcPDG',
 'genMotherID',
 'genMotherP',
 'genMotherPDG']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs.append("charge")
outvars_FSPs.append("dr")
outvars_FSPs.append("dz")
outvars_FSPs.append("clusterReg")
outvars_FSPs.append("clusterE9E21")
outvars_FSPs.append("M")
outvars_FSPs.append("PDG")
outvars_FSPs += vc.pid 


#outvars_FSPs += vc.mc_variables  
for i in range(10): # dont know yet if that's deep enough, 8 seemed okay at first glance
    tmp_var = "genMotherPDG({})".format(i)
    key = "genMothPDG_{}".format(i)
    v.addAlias(key,tmp_var)
    outvars_FSPs.append(key)

""" for i in range(10): 
    tmp_var = "genMotherID({})".format(i)
    key = "genMotherID_{}".format(i)
    v.addAlias(key,tmp_var)
    outvars_FSPs.append(key) 
    
 """

for i in range(10): # dont know yet if that's deep enough, 8 seemed okay at first glance
    start = "mcMother("
    tmp_var = start
    for j in range(i):
        tmp_var += start
    tmp_var += "uniqueParticleIdentifier"
    for j in range(i+1):
        tmp_var += ")"   
    #print(tmp_var)
    key = "mcMother{}_uniqParID".format(i)
    v.addAlias(key,tmp_var)
    outvars_FSPs.append(key)

for name in ["px","py","pz","E"]:
    tmp_var = "useCMSFrame({})".format(name)
    key = "cm{}".format(name)
    v.addAlias(key,tmp_var)
    outvars_FSPs.append(key)

copyLists('pi+:out', ['pi+:forX','pi+:sig','pi+:slow'], path=path)
variablesToNtuple('pi+:out', variables=outvars_FSPs, filename="pions.root", path=path)

copyLists('K+:out', ['K+:forX','K+:sig'], path=path)
variablesToNtuple('K+:out', variables=outvars_FSPs, filename="kaons.root", path=path)

variablesToNtuple('e+:cande', variables=outvars_FSPs, filename="electrons.root", path=path)
variablesToNtuple('mu+:candmu', variables=outvars_FSPs, filename="muons.root", path=path)

outvars_FSPs.append("mcPhotos")
outvars_FSPs.append("goodBelleGamma")
variablesToNtuple('gamma:myMinimumThresholdList', variables=outvars_FSPs, filename="gammas.root", path=path)




process(path, max_event=6000)  
