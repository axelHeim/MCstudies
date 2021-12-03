# default modules loaded into memory
import sys
#sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
sys.path.append('/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
from BranchSeparatorModel import BranchSeparatorModel
# See below why I put this



model_dir="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/saved_models/NAHSA_Gmodes_fixedD0modes/NAHS_allEvts_twoSubs_fixedD0run/NAHSA_allExtras/256_0_64_0.1_4/"
checkpoint_name = "model_checkpoint_model_perfectSA=0.7651.pt"
specs_output_label = "256_0_64_0.1_4"
num_classes = 3    


specs = specs_output_label.split("_")

bs_model = BranchSeparatorModel(infeatures=18,
            dim_feedforward=int(specs[0]),
            num_classes=num_classes,
            dropout=float(specs[3]),
            nblocks=int(specs[4]))



import torch

checkpoint = torch.load(model_dir +  checkpoint_name, map_location=torch.device('cpu'))
bs_model.load_state_dict(checkpoint)


from torch import nn

test_data=torch.Tensor([[[ 8.52624997e-002, -1.76634550e-001,  2.17837214e-001,
          3.24657362e-001,  1.39570385e-001,  1.00000000e+000,
          8.47053059e-003,  2.52304104e-003, -1.00000000e+000,
         -1.00000000e+000,  5.14801467e-001,  6.69100016e-015,
          1.69642081e-009,  4.85198531e-001,  6.67966173e-027,
         -2.62540281e-002, -1.26729673e-002,  3.36747505e-002]],

       [[-4.21467632e-001,  6.08630925e-002,  1.00266188e-001,
          4.59208539e-001,  1.39570385e-001, -1.00000000e+000,
          5.95115122e-003,  1.60831086e-002,  2.00000000e+000,
          8.01757812e-001,  7.35996084e-001,  9.35060078e-019,
          1.64411012e-008,  2.64003899e-001,  5.14646598e-035,
          5.34804305e-004,  3.70343821e-003, -6.14014221e-003]],

       [[-2.21213996e-001,  4.18315083e-002,  2.11667642e-001,
          5.82413658e-001,  4.93676990e-001,  1.00000000e+000,
          1.32755574e-001,  7.03318153e-002, -1.00000000e+000,
         -1.00000000e+000,  1.83683880e-179,  1.00000000e+000,
          3.39871675e-113,  1.77875211e-207,  3.78418873e-015,
         -2.32943129e-002, -1.23185329e-001,  1.10448878e-002]],

       [[-1.61094218e-001, -5.89269400e-001,  1.43344805e-001,
          7.98407463e-001,  4.93676990e-001, -1.00000000e+000,
          5.80004820e-003,  2.16620372e-002,  2.00000000e+000,
          9.73632812e-001,  1.02505596e-020,  1.00000000e+000,
          3.38268539e-015,  3.55930689e-022,  2.89123620e-014,
         -4.52525951e-002,  1.23711359e-002,  1.24159576e-002]],

       [[ 1.28370857e+000, -7.94306159e-001,  7.78692603e-001,
          1.69858541e+000,  5.10998943e-004,  1.00000000e+000,
          2.79031373e-004,  1.78544847e-002,  2.00000000e+000,
          9.86328125e-001,  4.60170411e-018,  1.67046105e-030,
          1.00000000e+000,  3.06926177e-030,  9.33629360e-053,
         -6.08767522e-003, -9.83852427e-003,  3.44012715e-002]],

       [[ 6.43501878e-002, -1.68076321e-001,  1.25532430e-002,
          2.09073841e-001,  1.05658367e-001,  1.00000000e+000,
          3.10604196e-003,  2.20797573e-002, -1.00000000e+000,
         -1.00000000e+000,  1.49436667e-001,  5.46903384e-017,
          1.26742243e-002,  8.37889108e-001,  1.76993423e-019,
         -3.50176319e-002, -1.34069538e-002,  1.44342761e-002]],

       [[-6.62728492e-003,  4.66204673e-001, -3.14343482e-001,
          5.72159273e-001,  1.05658367e-001, -1.00000000e+000,
          1.61317521e-005,  2.09044128e-002, -1.00000000e+000,
         -1.00000000e+000,  4.87873089e-001,  2.86532700e-006,
          6.88332357e-004,  5.11435713e-001,  1.33373334e-022,
         -4.97629493e-002, -7.07400148e-004,  2.28436738e-002]],

       [[-3.47084962e-002,  8.64448324e-002, -6.74179643e-002,
          1.56161011e-001,  1.05658367e-001, -1.00000000e+000,
          3.08859487e-002,  9.22007467e-003, -1.00000000e+000,
         -1.00000000e+000,  4.01460152e-001,  1.43272745e-011,
          2.39252415e-003,  5.96147324e-001,  6.07779252e-013,
         -6.58167303e-002, -2.64260992e-002,  2.40849517e-002]],

       [[ 7.47699499e-001,  9.21548188e-001,  5.17629921e-001,
          1.29900348e+000,  1.05658367e-001, -1.00000000e+000,
          8.05140925e-004,  1.92971971e-002,  2.00000000e+000,
          1.00000000e+000,  9.72565064e-019,  4.68047834e-029,
          5.12559861e-074,  1.00000000e+000,  3.44842840e-038,
         -3.90938558e-002,  3.17188613e-002,  1.72799770e-002]],

       [[-4.24641222e-002, -4.35361080e-003,  1.04259953e-001,
          1.12660079e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  1.00000000e+000,
          1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[ 6.06684433e-003, -1.07734792e-001,  1.60325989e-001,
          1.93256345e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          9.73632812e-001, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[-8.65274891e-002,  1.73254162e-001, -1.38521731e-001,
          2.38101409e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[-2.56192267e-001,  1.25176698e-001, -2.18457893e-001,
          3.59204029e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          9.92187500e-001, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]]])

#print("bs_model output: \n",bs_model(test_data))
#print(dir())




scripted_model = torch.jit.trace(bs_model, example_inputs=test_data)

#print(scripted_model)

# Loop over the parameters for the normal model and the scripted one

# That's just for us to verify that the model is actually the same

for (param, s_param) in zip(bs_model.parameters(), scripted_model.parameters()):

    if (param != s_param).all():

        raise ValueError("Model and scripted model deviate")

#print("**************")

#print("Model == scripted_model")

#print("**************")


# Save it

torch.jit.save(scripted_model, "bs_model_jit.pt")


# Now let's clean the script from all the import and objects we have

#print(dir())

for element in dir():

    if element[0:2] != "__":

        del globals()[element]

del element

# Check now: We are in the initial state.

#print(dir())


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

inference_model = torch.jit.load("bs_model_jit.pt")

#print("**************")



#print("**************")

#print(inference_model)

# and mimic some application now:
test_data=torch.Tensor([[[ 8.52624997e-002, -1.76634550e-001,  2.17837214e-001,
          3.24657362e-001,  1.39570385e-001,  1.00000000e+000,
          8.47053059e-003,  2.52304104e-003, -1.00000000e+000,
         -1.00000000e+000,  5.14801467e-001,  6.69100016e-015,
          1.69642081e-009,  4.85198531e-001,  6.67966173e-027,
         -2.62540281e-002, -1.26729673e-002,  3.36747505e-002]],

       [[-4.21467632e-001,  6.08630925e-002,  1.00266188e-001,
          4.59208539e-001,  1.39570385e-001, -1.00000000e+000,
          5.95115122e-003,  1.60831086e-002,  2.00000000e+000,
          8.01757812e-001,  7.35996084e-001,  9.35060078e-019,
          1.64411012e-008,  2.64003899e-001,  5.14646598e-035,
          5.34804305e-004,  3.70343821e-003, -6.14014221e-003]],

       [[-2.21213996e-001,  4.18315083e-002,  2.11667642e-001,
          5.82413658e-001,  4.93676990e-001,  1.00000000e+000,
          1.32755574e-001,  7.03318153e-002, -1.00000000e+000,
         -1.00000000e+000,  1.83683880e-179,  1.00000000e+000,
          3.39871675e-113,  1.77875211e-207,  3.78418873e-015,
         -2.32943129e-002, -1.23185329e-001,  1.10448878e-002]],

       [[-1.61094218e-001, -5.89269400e-001,  1.43344805e-001,
          7.98407463e-001,  4.93676990e-001, -1.00000000e+000,
          5.80004820e-003,  2.16620372e-002,  2.00000000e+000,
          9.73632812e-001,  1.02505596e-020,  1.00000000e+000,
          3.38268539e-015,  3.55930689e-022,  2.89123620e-014,
         -4.52525951e-002,  1.23711359e-002,  1.24159576e-002]],

       [[ 1.28370857e+000, -7.94306159e-001,  7.78692603e-001,
          1.69858541e+000,  5.10998943e-004,  1.00000000e+000,
          2.79031373e-004,  1.78544847e-002,  2.00000000e+000,
          9.86328125e-001,  4.60170411e-018,  1.67046105e-030,
          1.00000000e+000,  3.06926177e-030,  9.33629360e-053,
         -6.08767522e-003, -9.83852427e-003,  3.44012715e-002]],

       [[ 6.43501878e-002, -1.68076321e-001,  1.25532430e-002,
          2.09073841e-001,  1.05658367e-001,  1.00000000e+000,
          3.10604196e-003,  2.20797573e-002, -1.00000000e+000,
         -1.00000000e+000,  1.49436667e-001,  5.46903384e-017,
          1.26742243e-002,  8.37889108e-001,  1.76993423e-019,
         -3.50176319e-002, -1.34069538e-002,  1.44342761e-002]],

       [[-6.62728492e-003,  4.66204673e-001, -3.14343482e-001,
          5.72159273e-001,  1.05658367e-001, -1.00000000e+000,
          1.61317521e-005,  2.09044128e-002, -1.00000000e+000,
         -1.00000000e+000,  4.87873089e-001,  2.86532700e-006,
          6.88332357e-004,  5.11435713e-001,  1.33373334e-022,
         -4.97629493e-002, -7.07400148e-004,  2.28436738e-002]],

       [[-3.47084962e-002,  8.64448324e-002, -6.74179643e-002,
          1.56161011e-001,  1.05658367e-001, -1.00000000e+000,
          3.08859487e-002,  9.22007467e-003, -1.00000000e+000,
         -1.00000000e+000,  4.01460152e-001,  1.43272745e-011,
          2.39252415e-003,  5.96147324e-001,  6.07779252e-013,
         -6.58167303e-002, -2.64260992e-002,  2.40849517e-002]],

       [[ 7.47699499e-001,  9.21548188e-001,  5.17629921e-001,
          1.29900348e+000,  1.05658367e-001, -1.00000000e+000,
          8.05140925e-004,  1.92971971e-002,  2.00000000e+000,
          1.00000000e+000,  9.72565064e-019,  4.68047834e-029,
          5.12559861e-074,  1.00000000e+000,  3.44842840e-038,
         -3.90938558e-002,  3.17188613e-002,  1.72799770e-002]],

       [[-4.24641222e-002, -4.35361080e-003,  1.04259953e-001,
          1.12660079e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  1.00000000e+000,
          1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[ 6.06684433e-003, -1.07734792e-001,  1.60325989e-001,
          1.93256345e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          9.73632812e-001, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[-8.65274891e-002,  1.73254162e-001, -1.38521731e-001,
          2.38101409e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]],

       [[-2.56192267e-001,  1.25176698e-001, -2.18457893e-001,
          3.59204029e-001,  0.00000000e+000,  0.00000000e+000,
          1.18686603e-009,  2.23517418e-010,  2.00000000e+000,
          9.92187500e-001, -1.00000000e+000, -1.00000000e+000,
         -1.00000000e+000, -1.00000000e+000, -1.00000000e+000,
         -5.00000007e-002,  1.70000009e-002, -9.99999978e-003]]])
#print(inference_model(test_data))


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

bs_model = BranchSeparatorModel(infeatures=18,
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

b2.process(path, max_event=1000)


print("**************")

print("THIS IS GONNA CHANGE THE WORLD!!!")

print("**************")
