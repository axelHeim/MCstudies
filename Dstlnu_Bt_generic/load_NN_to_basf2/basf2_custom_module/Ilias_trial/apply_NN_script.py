# Now let's import torch and basf2 and try to load our model


import torch

import basf2 as b2

import modularAnalysis as ma

from stdCharged import stdMostLikely
from stdPhotons import stdPhotons 

from bsm_customModule import bsm_customModule

# Do some basic basf2 stuff
path = b2.create_path()
ma.inputMdst("/nfs/dust/belle2/user/axelheim/mixed_generic_MC14ri_a/mdst_000001_prod00016816_task10020000001.root", path=path)
stdMostLikely(path=path)

#print(path)
# Now let's import our model


nn_vars = ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID","electronID","muonID","protonID",
     "x","y","z"]

stdPhotons('all', path=path)
ma.cutAndCopyList('gamma:goodBelleGamma', 'gamma:all', 
        "[[clusterReg == 1 and E > 0.100] or [clusterReg == 2 and E > 0.050] or [clusterReg == 3 and E > 0.150]]", 
        path=path)


fsp_particleLists = ['pi+:mostlikely','K+:mostlikely','e+:mostlikely','mu+:mostlikely','gamma:goodBelleGamma']


import sys
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























b2.process(path, max_event=100)


print("**************")

print("THIS IS GONNA CHANGE THE WORLD!!!")

print("**************")

