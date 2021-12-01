import basf2 as b2
from ROOT import Belle2
from variables import variables as vm
import numpy as np

import torch 


import sys
sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
from BranchSeparatorModel import BranchSeparatorModel

class BranchSeparatorModule(b2.Module):
    ''' Save given features of given particles lists '''

    def __init__(
        self,
        particle_lists,
        features,
        model_dir,
        checkpoint_name,
        specs_output_label,
        num_classes
    ):
        ''' Class Constructor.
        Args:
            particle_lists (list): Name of particle lists to save features of
            features (list): List of features to save for each particle
            b_parent_var (str): Name of variable used to flag ancestor B meson and split particles
            output_file (str): Path to output file to save
        '''
        super().__init__()
        print("__init__")
        self.particle_lists = particle_lists
        self.features = features
        self.model_dir = model_dir
        self.checkpoint_name = checkpoint_name
        self.specs_output_label = specs_output_label
        self.num_classes = num_classes

    def initialize(self):
        print("features:",self.features)
        print("initialize func")
        
        print("load model from:", self.model_dir)

        

        specs = self.specs_output_label.split("_")
  
        print("num_classes:",self.num_classes)
        # load the model from checkpoint
        """ 
        self.model = BranchSeparatorModel(infeatures=len(self.features),
            dim_feedforward=int(specs[0]),
            num_classes=num_classes,
            dropout=float(specs[3]),
            nblocks=int(specs[4]))


        checkpoint = torch.load(model_dir / checkpoint_name)
        self.model.load_state_dict(checkpoint)

        self.model.eval()
         """
        
        



    def event(self):
        ''' Run every event '''
        #
        
        

        
          
        
        
        

        # IMPORTANT: The ArrayIndex is 0-based.
        
        tmp_par_vars = []
        
        for p_list_name in self.particle_lists:

            # Get the particle list (note this is a regular Particle list, not MCParticle)
            p_list = Belle2.PyStoreObj(p_list_name)


            

            for particle in p_list.obj():
                
                #print("particle.getInfo():",particle.getInfo())

                
                
                # Get the B parent index, set to -1 if particle has no MC match
                #particle.addExtraInfo("NN_prediction", 25) 	
                
                
                readOut_features = [vm.evaluate(f, particle) for f in self.features]
                tmp_par_vars.append(readOut_features)
                
                
                """     for feature in self.features:
                    print("feature:",feature)
                    
                    
                    if feature in ["px","py","pz","E","M","charge","dr","dz","clusterReg","clusterE9E21","pionID","kaonID","electronID","muonID","protonID","x","y","z"]:
                        funcName=feature    
                        tmp_par_vars.append(varFuncDict[funcName](particle)) 
                        
                        print("funcName:",funcName)
                        print("tmp_par_vars[-1]:",tmp_par_vars[-1])
                    else:
                        funcName="extraInfo"    
                        tmp_par_vars.append(varFuncDict[funcName](particle,feature)) 
                        
                        print("funcName:",funcName)
                        print("tmp_par_vars[-1]:",tmp_par_vars[-1])
                        
                    
                    print(" \n ") """
                    
                #print("readOut_features:",readOut_features)
                
        import numpy as np

        NN_input_features = np.array([np.array(xi) for xi in tmp_par_vars])
        
        # impute the nan values with -1. (check if that's logical for all values if input vars get changed)
        NN_input_features= np.nan_to_num(NN_input_features, copy=False, nan=-1.0)
        
        """ 
        SA_pred = self.model(NN_input_features)

        probs = torch.softmax(SA_pred, dim=1)  # (N, C, d1)
        winners = probs.argmax(dim=1)
         
        num_particles = NN_input_features.shape[0]
        particle_i=0
        for p_list_name in self.particle_lists:
            # Get the particle list (note this is a regular Particle list, not MCParticle)
            p_list = Belle2.PyStoreObj(p_list_name)            

            for particle in p_list.obj():
                particle.addExtraInfo("NN_prediction", winners[0,particle_i]) 

                particle_i += 1
                
        """
        #print("NN_input_features.shape:",NN_input_features.shape)
        #print("NN_input_features:",NN_input_features)
                    
                
                           
                           
              
                           
                           
                           
                           
                           
    def terminate(self):
        pass
        # delete network etc here
        
        
        
"""         
        def px(particle):
            return particle.getPx()
        def py(particle):
            return particle.getPy()
        def pz(particle):
            return particle.getPz()
        def E(particle):
            return particle.getEnergy()
        def mass(particle):
            return particle.getMass()
        def charge(particle):
            return particle.getCharge()
        def clusterE9E21(particle):
            cluster = particle.getECLCluster()
            
            if cluster is not None:
                E9E21 = cluster.getE9oE21()                
            else :
                E9E21 = -1.                
            return E9E21
        
        def extraInfo(particle,var):
            return particle.getExtraInfo(var)
        varFuncDict = {
            "px": px,
            "py": py,
            "pz": pz,
            "E": E,
            "M": mass,
            "charge": charge,
            "clusterE9E21": clusterE9E21,
            "extraInfo": extraInfo,
        }
 """