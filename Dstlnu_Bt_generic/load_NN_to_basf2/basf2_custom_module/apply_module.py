""" 
Steering file to run only the FEI and check if event is B->D*lnu
and subsequently save all FSPs
 """
from NN_custom_module import BranchSeparatorModule
 
#import basf2
#like that no need for basf2. before fcts
from basf2 import *
from modularAnalysis import *

import basf2 as b2

import modularAnalysis as ma

from variables import variables as v
import vertex as vx
from stdPhotons import stdPhotons 
from stdCharged import stdCharged, stdMostLikely

import variables.collections as vc
import fei
import sys



outpath = "/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/load_NN_to_basf2/basf2_custom_module/test_output/"
### define out variables
sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/NAHS/utils')
from aliases import define_aliases_Hc, define_aliases_FSPs

identifier = str(sys.argv[1])

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictFSPs= define_aliases_FSPs()
print(AliasDictFSPs)
add_aliases(AliasDictFSPs)
outvars_FSPs = list(AliasDictFSPs.keys()) 


outvars_FSPs += ['isSignal', 'uniqueParticleIdentifier','mcErrors','mcPDG','genMotherID','genMotherP',
 'genMotherPDG','charge','dr','dz','clusterReg','clusterE9E21','M','PDG','genParticleID']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs += vc.pid 







AliasDictHc= define_aliases_Hc()
print(AliasDictHc)
add_aliases(AliasDictHc)
Hc_variables = list(AliasDictHc.keys()) 
Hc_variables +=  vc.kinematics 
Hc_variables += ['x','y','z','x_uncertainty','y_uncertainty','z_uncertainty','uniqueParticleIdentifier','genParticleID']




#import pdg
#pdg.add_particle("Hc", 9876555, 0, 0, 0, 0)

path = ma.create_path()
inputMdstList([], path)


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
applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] and [[abs_genUp4S_PDG_0_1 == 11.0] or [abs_genUp4S_PDG_0_1 == 13.0]] and [[abs_genUp4S_PDG_0_2 == 12.0] or [abs_genUp4S_PDG_0_2 == 14.0]]] or [[abs_genUp4S_PDG_1_0 == 413.0] and [[abs_genUp4S_PDG_1_1 == 11.0] or [abs_genUp4S_PDG_1_1 == 13.0]] and [[abs_genUp4S_PDG_1_2 == 12.0] or [abs_genUp4S_PDG_1_2 == 14.0]]]]''', path)

### FEI part
particles = fei.get_default_channels(baryonic=True)


b2.conditions.prepend_globaltag(getAnalysisGlobaltag()) # needed for FEI prefix  FEIv4_2021_MC14_release_05_01_12  ;from: https://questions.belle2.org/question/11130/b2bii-global-tag-error-in-release-05-02-06/
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

    applyCuts(f'{Hc_dict[Hc]}:genericsigProb', 'isSignalAcceptMissingGamma == 1 and abs(genMotherPDG) == 511.0', path=path)

    """ variablesToNtuple(f'{Hc_dict[Hc]}:genericsigProb',
                    ['extraInfo(SignalProbability)',
                    'isSignalAcceptMissingGamma',
                    'PDG'] + Hc_variables,
                    filename=outpath + f'{Hc}_' + identifier + '.root',
                    path=path)
    """
sigProbList = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]


# only proceed if one of the lists contains a isSignalAcceptMissingGamma == 1
applyEventCuts(f'''[[countInList({sigProbList[0]}) > 0] or [countInList({sigProbList[1]}) > 0] or [countInList({sigProbList[2]}) > 0] or [countInList({sigProbList[3]}) > 0] or [countInList({sigProbList[4]}) > 0] or [countInList({sigProbList[5]}) > 0] or [countInList({sigProbList[6]}) > 0]]''', path)



## online cuts
## vars in extra file: Hc + FSPs: CM vars , 4mom 

"""       goodGammaRegion1 = region == 1 && energy > 0.100;
      goodGammaRegion2 = region == 2 && energy > 0.050;
      goodGammaRegion3 = region == 3 && energy > 0.150;
 """

stdMostLikely(path=path)
#stdCharged('pi','mostlikely', path=path)
#stdCharged('K','mostlikely', path=path)
#stdCharged('e','mostlikely', path=path)
#stdCharged('mu','mostlikely', path=path)

stdPhotons('all', path=path)
cutAndCopyList('gamma:goodBelleGamma', 'gamma:all', 
        "[[clusterReg == 1 and E > 0.100] or [clusterReg == 2 and E > 0.050] or [clusterReg == 3 and E > 0.150]]", 
        path=path)


#Hc_particleLists = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]
fsp_particleLists = ['pi+:mostlikely','K+:mostlikely','e+:mostlikely','mu+:mostlikely','gamma:goodBelleGamma']

#allParticleLists=Hc_particleLists+FSP_particleLists

nn_vars = ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID","electronID","muonID","protonID",
     "x","y","z"]

branch_separator_module = BranchSeparatorModule(
    particle_lists=fsp_particleLists,
    features=nn_vars,
    model_dir="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/saved_models/NAHSA_Gmodes_fixedD0modes/NAHS_allEvts_twoSubs_fixedD0run/NAHSA_allExtras/256_0_64_0.1_4",
    checkpoint_name = "model_checkpoint_model_perfectSA=0.7651.pt",
    specs_output_label = "256_0_64_0.1_4",
    num_classes = 3    
)
path.add_module(branch_separator_module)

v.addAlias('NN_prediction', 'extraInfo(NN_prediction)')
outvars_FSPs.append("NN_prediction")

""" 
label = 0 # background, cause not related to MC Particles
label = 2 # Bsig
label = 1 #X
 """
"""  
# cut lists accordingly to NN prediction
cutAndCopyList('gamma:pred_bg', 'gamma:goodBelleGamma', "[NN_prediction == 0]", path=path)
cutAndCopyList('gamma:pred_X', 'gamma:goodBelleGamma', "[NN_prediction == 1]", path=path)
cutAndCopyList('gamma:pred_Bsig', 'gamma:goodBelleGamma', "[NN_prediction == 2]", path=path)

cutAndCopyList('pi+:pred_bg', 'pi+:mostlikely', "[NN_prediction == 0]", path=path)
cutAndCopyList('pi+:pred_X', 'pi+:mostlikely', "[NN_prediction == 1]", path=path)
cutAndCopyList('pi+:pred_Bsig', 'pi+:mostlikely', "[NN_prediction == 2]", path=path)

cutAndCopyList('K+:pred_bg', 'K+:mostlikely', "[NN_prediction == 0]", path=path)
cutAndCopyList('K+:pred_X', 'K+:mostlikely', "[NN_prediction == 1]", path=path)
cutAndCopyList('K+:pred_Bsig', 'K+:mostlikely', "[NN_prediction == 2]", path=path)

cutAndCopyList('e+:pred_bg', 'e+:mostlikely', "[NN_prediction == 0]", path=path)
cutAndCopyList('e+:pred_X', 'e+:mostlikely', "[NN_prediction == 1]", path=path)
cutAndCopyList('e+:pred_Bsig', 'e+:mostlikely', "[NN_prediction == 2]", path=path)

cutAndCopyList('mu+:pred_bg', 'mu+:mostlikely', "[NN_prediction == 0]", path=path)
cutAndCopyList('mu+:pred_X', 'mu+:mostlikely', "[NN_prediction == 1]", path=path)
cutAndCopyList('mu+:pred_Bsig', 'mu+:mostlikely', "[NN_prediction == 2]", path=path)

# reconstruct D0
reconstructDecay('pi0:forD0 -> gamma:pred_Bsig gamma:pred_Bsig','M > 0.124 and M < 0.140', path=path)

reconstructDecay('D0:kpi -> K-:pred_Bsig pi+:pred_Bsig', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipipi -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipi0 -> K-:pred_Bsig pi+:pred_Bsig pi0:forD0', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipipipi0 -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig pi0:forD0', '1.8 < M < 1.9', path=path)
copyLists('D0:cand', ['D0:kpi','D0:kpipipi','D0:kpipi0','D0:kpipipipi0'], path=path)
path.add_module('MCMatcherParticles', listName='D0:cand', looseMCMatching=True)



roeinputs = ['gamma:pred_X','pi+:pred_X','K+:pred_X','p+:pred_X', 'e+:pred_X','mu+:pred_X']


# reconstruct D*+
reconstructDecay('D*+:kpi -> D0:cand pi+:pred_Bsig', '0.139<massDifference(0)<0.16', path=path)
path.add_module('MCMatcherParticles', listName='D*+:kpi', looseMCMatching=True)


# reconstruct B-sig
reconstructDecay('anti-B0:Dstkpie -> D*+:kpi e-:pred_Bsig', '', path=path)
reconstructDecay('anti-B0:Dstkpimu -> D*+:kpi mu-:pred_Bsig', '', path=path)
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpie')
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpimu')
copyLists('anti-B0:sig', ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu'], path=path)


# maybe necessary, check later:
#cutAndCopyList('anti-B0:sigclean',"anti-B0:sig",'-1.5 < cosThetaBetweenParticleAndNominalB < 1.5 and daughter(0,useCMSFrame(p))<2.4 and daughter(1,useCMSFrame(p))>1.', path= path)

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
 """



variablesToNtuple('pi+:mostlikely', variables=outvars_FSPs, filename=outpath + 'pions_' + identifier + '.root', path=path)
variablesToNtuple('K+:mostlikely', variables=outvars_FSPs, filename=outpath + 'kaons_' + identifier + '.root', path=path)
variablesToNtuple('e+:mostlikely', variables=outvars_FSPs, filename=outpath + 'electrons_' + identifier + '.root', path=path)
variablesToNtuple('mu+:mostlikely', variables=outvars_FSPs, filename=outpath + 'muons_' + identifier + '.root', path=path)
variablesToNtuple('gamma:goodBelleGamma', variables=outvars_FSPs, filename=outpath + 'gammas_' + identifier + '.root', path=path)



""" 

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

 """
process(path, max_event=400)  
