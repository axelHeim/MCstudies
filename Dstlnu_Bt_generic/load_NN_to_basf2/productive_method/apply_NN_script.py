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

outpath="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/appliedNNdata/15thRun/"
#outpath="/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/load_NN_to_basf2/productive_method/testOut/"


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
# ma.applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] and [[abs_genUp4S_PDG_0_1 == 11.0] or [abs_genUp4S_PDG_0_1 == 13.0]] and [[abs_genUp4S_PDG_0_2 == 12.0] or [abs_genUp4S_PDG_0_2 == 14.0]]] or [[abs_genUp4S_PDG_1_0 == 413.0] and [[abs_genUp4S_PDG_1_1 == 11.0] or [abs_genUp4S_PDG_1_1 == 13.0]] and [[abs_genUp4S_PDG_1_2 == 12.0] or [abs_genUp4S_PDG_1_2 == 14.0]]]]''', path)

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


for Hc in all_Hcs:
    path.add_module('MCMatcherParticles', listName=f'{Hc_dict[Hc]}:genericsigProb', looseMCMatching=True)

    #ma.applyCuts(f'{Hc_dict[Hc]}:genericsigProb', 'isSignalAcceptMissingNeutrino == 1 and abs(genMotherPDG) == 511.0', path=path)


sigProbList = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]


# only proceed if the lists contain exactly one Hc candidate
#ma.applyEventCuts(f'''[formula(countInList({sigProbList[0]}) + countInList({sigProbList[1]}) + countInList({sigProbList[2]}) + countInList({sigProbList[3]}) + countInList({sigProbList[4]}) + countInList({sigProbList[5]}) + countInList({sigProbList[6]})) == 1]''', path)
# combine lists, should now contain exactly one Hc candidate
ma.combineAllParticles(sigProbList, "Hc:used", cut='', path=path)

ma.rankByHighest("Hc:used", 'extraInfo(SignalProbability)', numBest=1,
              outputVariable='Hc_FEIProbabilityRank', path=path)



# only proceed if the lists contain exactly one Hc candidate
ma.applyEventCuts('[countInList(Hc:used) == 1]', path)


###################






stdMostLikely(path=path)



nn_vars = ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID",
           "electronID","muonID","protonID"]

stdPhotons('all', path=path)
ma.cutAndCopyList('gamma:goodBelleGamma', 'gamma:all', 
        "[[clusterReg == 1 and E > 0.100] or [clusterReg == 2 and E > 0.050] or [clusterReg == 3 and E > 0.150]]", 
        path=path)


fsp_particleLists = ['pi+:mostlikely','K+:mostlikely','e+:mostlikely','mu+:mostlikely','gamma:goodBelleGamma']

for parList in fsp_particleLists:
   ma.variablesToExtraInfo(parList, {"isDescendantOfList(Hc:used)":"Hc_used"}, option=0, path=path)

sys.path.append('/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
from BranchSeparatorModel import BranchSeparatorModel
# See below why I put this



model_dir="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/saved_models/NAHSA_Gmodes_fixedD0modes/NAHS_allEvts_twoSubs_fixedD0run/NAHSA_no_xyz/256_0_64_0.1_4/"
checkpoint_name = "model_checkpoint_model_perfectSA=0.7674.pt"
specs_output_label = "256_0_64_0.1_4"
num_classes = 3    


specs = specs_output_label.split("_")

bs_model = BranchSeparatorModel(infeatures=len(nn_vars),
            dim_feedforward=int(specs[0]),
            num_classes=num_classes,
            dropout=float(specs[3]),
            nblocks=int(specs[4]))



import torch

checkpoint = torch.load(model_dir +  checkpoint_name, map_location=torch.device('cpu'))
bs_model.load_state_dict(checkpoint)
inference_model=bs_model

customModule = bsm_customModule(fsp_particleLists , nn_vars, inference_model)

path.add_module(customModule)


v.addAlias('NN_prediction', 'extraInfo(NN_prediction)')

AliasDictFSPs= define_aliases_FSPs()
print(AliasDictFSPs)
add_aliases(AliasDictFSPs)
outvars_FSPs = list(AliasDictFSPs.keys()) 
outvars_Ups4S = list(AliasDictUps4S.keys()) 

outvars_FSPs += ['isSignal', 'uniqueParticleIdentifier','mcErrors','mcPDG','genMotherID','genMotherP',
 'genMotherPDG','charge','dr','dz','clusterReg','clusterE9E21','M','PDG','genParticleID']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs += vc.pid 
outvars_FSPs += nn_vars 


outvars_FSPs.append("NN_prediction")





# cut lists accordingly to NN prediction
ma.cutAndCopyList('gamma:pred_bg', 'gamma:goodBelleGamma', "[NN_prediction == 0]", path=path)
ma.cutAndCopyList('gamma:pred_X', 'gamma:goodBelleGamma', "[NN_prediction == 1]", path=path)
ma.cutAndCopyList('gamma:pred_Bsig', 'gamma:goodBelleGamma', "[NN_prediction == 2]", path=path)

ma.cutAndCopyList('pi+:pred_bg', 'pi+:mostlikely', "[NN_prediction == 0]", path=path)
ma.cutAndCopyList('pi+:pred_X', 'pi+:mostlikely', "[NN_prediction == 1]", path=path)
ma.cutAndCopyList('pi+:pred_Bsig', 'pi+:mostlikely', "[NN_prediction == 2]", path=path)

ma.cutAndCopyList('K+:pred_bg', 'K+:mostlikely', "[NN_prediction == 0]", path=path)
ma.cutAndCopyList('K+:pred_X', 'K+:mostlikely', "[NN_prediction == 1]", path=path)
ma.cutAndCopyList('K+:pred_Bsig', 'K+:mostlikely', "[NN_prediction == 2]", path=path)

ma.cutAndCopyList('e+:pred_bg', 'e+:mostlikely', "[NN_prediction == 0]", path=path)
ma.cutAndCopyList('e+:pred_X', 'e+:mostlikely', "[NN_prediction == 1]", path=path)
ma.cutAndCopyList('e+:pred_Bsig', 'e+:mostlikely', "[NN_prediction == 2]", path=path)

ma.cutAndCopyList('mu+:pred_bg', 'mu+:mostlikely', "[NN_prediction == 0]", path=path)
ma.cutAndCopyList('mu+:pred_X', 'mu+:mostlikely', "[NN_prediction == 1]", path=path)
ma.cutAndCopyList('mu+:pred_Bsig', 'mu+:mostlikely', "[NN_prediction == 2]", path=path)


## reconstruct Y(4S) based on NN prediction
# reconstruct D0
#ma.reconstructDecay('pi0:forD0 -> gamma:pred_Bsig gamma:pred_Bsig','M > 0.124 and M < 0.140', path=path)
ma.reconstructDecay('pi0:forD0 -> gamma:pred_Bsig gamma:pred_Bsig','', path=path)

#ma.reconstructDecay('D0:kpi -> K-:pred_Bsig pi+:pred_Bsig', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpi -> K-:pred_Bsig pi+:pred_Bsig',  '', dmID=21001, path=path)

#ma.reconstructDecay('D0:kpipipi -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipipi -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig', '', dmID=21002, path=path)

#ma.reconstructDecay('D0:kpipi0 -> K-:pred_Bsig pi+:pred_Bsig pi0:forD0', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipi0 -> K-:pred_Bsig pi+:pred_Bsig pi0:forD0', '', dmID=21003, path=path)

#ma.reconstructDecay('D0:kpipipipi0 -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig pi0:forD0', '1.8 < M < 1.9', path=path)
ma.reconstructDecay('D0:kpipipipi0 -> K-:pred_Bsig pi+:pred_Bsig pi-:pred_Bsig pi+:pred_Bsig pi0:forD0', '', dmID=21004, path=path)
ma.copyLists('D0:cand', ['D0:kpi','D0:kpipipi','D0:kpipi0','D0:kpipipipi0'], path=path)
path.add_module('MCMatcherParticles', listName='D0:cand', looseMCMatching=True)



roeinputs = ['gamma:pred_X','pi+:pred_X','K+:pred_X','p+:pred_X', 'e+:pred_X','mu+:pred_X']


# reconstruct D*+
#ma.reconstructDecay('D*+:kpi -> D0:cand pi+:pred_Bsig', '0.139<massDifference(0)<0.16', path=path)
ma.reconstructDecay('D*+:kpi -> D0:cand pi+:pred_Bsig', '', path=path)
path.add_module('MCMatcherParticles', listName='D*+:kpi', looseMCMatching=True)


# reconstruct B-sig
ma.reconstructDecay('anti-B0:Dstkpie -> D*+:kpi e-:pred_Bsig', '', path=path)
ma.reconstructDecay('anti-B0:Dstkpimu -> D*+:kpi mu-:pred_Bsig', '', path=path)
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpie')
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpimu')
ma.copyLists('anti-B0:sig', ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu'], path=path)


# maybe necessary, check later:
#ma.cutAndCopyList('anti-B0:sigclean',"anti-B0:sig",'-1.5 < cosThetaBetweenParticleAndNominalB < 1.5 and daughter(0,useCMSFrame(p))<2.4 and daughter(1,useCMSFrame(p))>1.', path= path)

#reconstruct a pseudo upsilon4s from B_sig and H_c to determine ROE of this
""" ma.reconstructDecay('Upsilon(4S):Dst0Dstl -> anti-B0:sigclean  anti-D*0:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):DstpDstl -> anti-B0:sigclean  D*-:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):DpDstl -> anti-B0:sigclean  D-:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):D0Dstl -> anti-B0:sigclean  anti-D0:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):LcDstl -> anti-B0:sigclean  anti-Lambda_c-:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):DsDstl -> anti-B0:sigclean  D_s+:genericsigProb','',path=path,allowChargeViolation=True)
ma.reconstructDecay('Upsilon(4S):JpsiDstl -> anti-B0:sigclean  J/psi:genericsigProb','',path=path,allowChargeViolation=True)
 """
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


X_lists = ["K+:pred_X","pi+:pred_X","mu+:pred_X","e+:pred_X","gamma:pred_X"]
ma.combineAllParticles(X_lists, "X:all", cut='', path=path)

for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]

 
    ##reconstruct B_tag from X and H_c   
    
    ma.reconstructDecay(f'B0:{parid}DXtag -> {name_dict[parid]}:genericsigProb X:all','',path=path,allowChargeViolation=True)
    path.add_module('MCMatcherParticles', listName=f'B0:{parid}DXtag')
    
    ma.reconstructDecay(f'Upsilon(4S):{parid}DXtag -> B0:{parid}DXtag anti-B0:sig','',path=path)
    #ma.applyCuts(f'Upsilon(4S):{parid}DXtag', 'abs(daughter(0,deltaE))<0.2', path=path)
    outlists_DX.append(f'Upsilon(4S):{parid}DXtag')


ma.copyLists('Upsilon(4S):DXtag', outlists_DX, path=path)

""" ma.rankByHighest('Upsilon(4S):DXtag', 'daughter(0,daughter(0, extraInfo(SignalProbability)))', numBest=1,
              outputVariable='FEIProbabilityRank', path=path) """

path.add_module('MCMatcherParticles', listName='Upsilon(4S):DXtag', looseMCMatching=True)


#only proceed with event if a Y(4S) candidate was found 
ma.applyEventCuts("[countInList(Upsilon(4S):DXtag) > 0]", path)


# construct the E_extra of unused gammas in the event
#goodBelleGammas = "[[clusterReg == 1 and E > 0.100] or [clusterReg == 2 and E > 0.050] or [clusterReg == 3 and E > 0.150]]"
ma.buildRestOfEvent('Upsilon(4S):DXtag', inputParticlelists='gamma:goodBelleGamma', path=path)
ma.appendROEMask('Upsilon(4S):DXtag', 'my_mask_gammas', '', '', path=path)
#ma.printROEInfo(mask_names=['my_mask_gammas'], full_print=True, path=path)

v.addAlias('roeE_ofUps4S', 'roeE(my_mask_gammas)')
outvars_Ups4S.append("roeE_ofUps4S")


v.addAlias('E_predicted_bg_gammas', 'totalEnergyOfParticlesInList(gamma:pred_bg)')
outvars_Ups4S.append("E_predicted_bg_gammas")



#v.addAlias('Eextra_ROEofUps4S', 'roeEextra(goodROEGamma)')
#outvars_Ups4S.append("Eextra_ROEofUps4S")


""" 
# second way to construct the E_extra of unused gammas in the event, probably wrong
ma.cutAndCopyList('gamma:notUsed', 'gamma:goodBelleGamma', 
        "[isDescendantOfList(Upsilon(4S):DXtag) == 0]", 
        path=path)
v.addAlias('Eextra_goodBelleGamma', 'totalEnergyOfParticlesInList(gamma:notUsed)')
outvars_Ups4S.append("Eextra_goodBelleGamma")
 """

### create and cut lists to only contain the finally used Hc,X,Bsig in order to label to the FSPs with them

HcAll = []
X_All = []
BtagAll = []
for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]
    HcAll.append(f'{name_dict[parid]}:tag')
    #X_All.append(f'X:tag{parid}')
    BtagAll.append(f'B0:{parid}DXtag')


ma.cutAndCopyLists('B0:tag_onlyUsedOne', BtagAll, "[isDescendantOfList(Upsilon(4S):DXtag) == 1]", path=path)
#ma.cutAndCopyLists('X:XonlyUsedOne', X_All, "[isDescendantOfList(B0:tag_onlyUsedOne) == 1]", path=path)
# cannot combine all Hc's because they are different particles, sigh :/
#cutAndCopyLists('X:HcOnlyUsedOne', HcAll, "[isDaughterOfList(B0:tag_onlyUsedOne) > 0]", path=path)

ma.cutAndCopyList('B0:sig_onlyUsedOne', "anti-B0:sig", "[isDescendantOfList(Upsilon(4S):DXtag) == 1]", path=path)


# these three vars indicate binary if to what category a particle got assigned by semi-inclusive Hc+X tagging
#v.addAlias('YYY', 'isDescendantOfList("pi0:forX")')
v.addAlias('basf2_used', 'isDescendantOfList(Upsilon(4S):DXtag)')
v.addAlias('basf2_Bsig', 'isDescendantOfList(B0:sig_onlyUsedOne)')

v.addAlias('Hc_used', 'extraInfo(Hc_used)')

outvars_FSPs += ['basf2_used','basf2_Bsig','Hc_used']








outvars_Ups4S.append("mcPDG")
# save Upsilon(4S)
ma.variablesToNtuple('Upsilon(4S):DXtag',
                  [
                   "m2RecoilSignalSide",
                   "foxWolframR2_maskedNaN",
                   'foxWolframR2',
		   'extraInfo(FEIProbabilityRank)',
                   "nTracks"
                   ]+  outvars_Ups4S,
                  filename=outpath + 'Ups4S_NN_predicted_' + identifier + '.root',
                  path=path)






# delete duplicates in outvars
from collections import OrderedDict
outvars_FSPs = list(OrderedDict.fromkeys(outvars_FSPs))

# save FSPs
ma.variablesToNtuple('pi+:mostlikely', variables=outvars_FSPs, filename=outpath + 'pions_' + identifier + '.root', path=path)
ma.variablesToNtuple('K+:mostlikely', variables=outvars_FSPs, filename=outpath + 'kaons_' + identifier + '.root', path=path)
ma.variablesToNtuple('e+:mostlikely', variables=outvars_FSPs, filename=outpath + 'electrons_' + identifier + '.root', path=path)
ma.variablesToNtuple('mu+:mostlikely', variables=outvars_FSPs, filename=outpath + 'muons_' + identifier + '.root', path=path)
ma.variablesToNtuple('gamma:goodBelleGamma', variables=outvars_FSPs, filename=outpath + 'gammas_' + identifier + '.root', path=path)



b2.process(path)#, max_event=200)

print(b2.statistics)


print("**************")

print("THIS IS GONNA CHANGE THE WORLD!!!")

print("**************")

