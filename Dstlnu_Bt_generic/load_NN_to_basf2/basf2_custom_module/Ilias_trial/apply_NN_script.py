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
from aliases import define_aliases_Hc, define_aliases_FSPs

import pdg
pdg.add_particle("Hc", 9876555, 0, 0, 0, 0)


def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictHc= define_aliases_Hc()
#print(AliasDictHc)
add_aliases(AliasDictHc)

from bsm_customModule import bsm_customModule

# Do some basic basf2 stuff
path = b2.create_path()
ma.inputMdst("/nfs/dust/belle2/user/axelheim/mixed_generic_MC14ri_a/mdst_000001_prod00016816_task10020000001.root", path=path)

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

### FEI part
particles = fei.get_default_channels(baryonic=True)


b2.conditions.prepend_globaltag(ma.getAnalysisGlobaltag()) # needed for FEI prefix  FEIv4_2021_MC14_release_05_01_12  ;from: https://questions.belle2.org/question/11130/b2bii-global-tag-error-in-release-05-02-06/
configuration = fei.config.FeiConfiguration(prefix='FEIv4_2021_MC14_release_05_01_12', training=False, monitor=False)
feistate = fei.get_path(particles, configuration)

path.add_path(feistate.path)

# now take best H_c and check if isSignal==1
ma.cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
ma.cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
ma.cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>0.001', path= path)
ma.cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>0.001', path= path)
ma.cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>0.001', path= path)
ma.cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>0.001', path= path)
ma.cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>0.001', path= path)

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

    ma.applyCuts(f'{Hc_dict[Hc]}:genericsigProb', 'isSignalAcceptMissingGamma == 1 and abs(genMotherPDG) == 511.0', path=path)

    """ variablesToNtuple(f'{Hc_dict[Hc]}:genericsigProb',
                    ['extraInfo(SignalProbability)',
                    'isSignalAcceptMissingGamma',
                    'PDG'] + Hc_variables,
                    filename=outpath + f'{Hc}_' + identifier + '.root',
                    path=path)
    """
sigProbList = [f'{Hc_dict[Hc]}:genericsigProb' for Hc in all_Hcs]


# only proceed if the lists contain exactly one Hc candidate
ma.applyEventCuts(f'''[formula(countInList({sigProbList[0]}) + countInList({sigProbList[1]}) + countInList({sigProbList[2]}) + countInList({sigProbList[3]}) + countInList({sigProbList[4]}) + countInList({sigProbList[5]}) + countInList({sigProbList[6]})) == 1]''', path)
# combine lists, should now contain exactly one Hc candidate
ma.combineAllParticles(sigProbList, "Hc:used", cut='', path=path)



###################






stdMostLikely(path=path)



nn_vars = ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID","electronID","muonID","protonID",
     "x","y","z"]

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



model_dir="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/saved_models/NAHSA_Gmodes_fixedD0modes/NAHS_allEvts_twoSubs_fixedD0run/NAHSA_allExtras/256_0_64_0.1_4/"
checkpoint_name = "model_checkpoint_model_perfectSA=0.7651.pt"
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


outvars_FSPs += ['isSignal', 'uniqueParticleIdentifier','mcErrors','mcPDG','genMotherID','genMotherP',
 'genMotherPDG','charge','dr','dz','clusterReg','clusterE9E21','M','PDG','genParticleID']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs += vc.pid 


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















# save FSPs
identifier = str(sys.argv[1])
outpath="/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/load_NN_to_basf2/basf2_custom_module/Ilias_trial/testOut"
variablesToNtuple('pi+:mostlikely', variables=outvars_FSPs, filename=outpath + 'pions_' + identifier + '.root', path=path)
variablesToNtuple('K+:mostlikely', variables=outvars_FSPs, filename=outpath + 'kaons_' + identifier + '.root', path=path)
variablesToNtuple('e+:mostlikely', variables=outvars_FSPs, filename=outpath + 'electrons_' + identifier + '.root', path=path)
variablesToNtuple('mu+:mostlikely', variables=outvars_FSPs, filename=outpath + 'muons_' + identifier + '.root', path=path)
variablesToNtuple('gamma:goodBelleGamma', variables=outvars_FSPs, filename=outpath + 'gammas_' + identifier + '.root', path=path)



b2.process(path, max_event=1000)


print("**************")

print("THIS IS GONNA CHANGE THE WORLD!!!")

print("**************")

