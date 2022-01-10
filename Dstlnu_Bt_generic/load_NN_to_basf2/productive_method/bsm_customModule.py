#import sys
#sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
#sys.path.append('/afs/desy.de/user/a/axelheim/private/baumbauen/notebooks/')
#from BranchSeparatorModel import BranchSeparatorModel

import basf2 as b2
from ROOT import Belle2
from variables import variables as vm
import numpy as np

import torch 




class bsm_customModule(b2.Module):
    ''' Save given features of given particles lists '''

    def __init__(
        self,
        particle_lists,
        features,
        model
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
        self.model = model

    def initialize(self):
        print("features:",self.features)
        print("initialize func")
        self.eventinfo = Belle2.PyStoreObj('EventMetaData')

        

        #print("self.model:",self.model)



    def event(self):
        ''' Run every event '''
        print("\n start of event")
        self.model.eval()
        evt_num = self.eventinfo.getEvent()
        print("evt_num:", evt_num)
        

        
          
        
        
        

        # IMPORTANT: The ArrayIndex is 0-based.
        
        tmp_par_vars = []
        
        for p_list_name in self.particle_lists:

            # Get the particle list (note this is a regular Particle list, not MCParticle)
            p_list = Belle2.PyStoreObj(p_list_name)


            for particle in p_list.obj():
                #particle.addExtraInfo("NN_prediction", 25) 	
                
                Hc_used = particle.getExtraInfo("Hc_used")
                
                if Hc_used == 1.0:
                    continue
                #print("Hc_used:",Hc_used)
                readOut_features = [vm.evaluate(f, particle) for f in self.features]
                tmp_par_vars.append(readOut_features)
                

                #print("readOut_features:",readOut_features)
                

        NN_input_features = np.array([np.array(xi) for xi in tmp_par_vars])
        
        # impute the nan values with -1. (check if that's logical for all values if input vars get changed)
        NN_input_features= np.nan_to_num(NN_input_features, copy=False, nan=-1.0)
        
        #print("NN_input_features.shape:",NN_input_features.shape)
        shape = NN_input_features.shape
        NN_input_features = NN_input_features.reshape(shape[0], 1, shape[1])
        
        #print("NN_input_features.shape:",NN_input_features.shape)
        NN_input_features = torch.Tensor(NN_input_features)
        
        #print("NN_input_features.shape:",NN_input_features.shape)
        #print("")
        
        
        # shuffle the order of the input particles
        r=torch.randperm(shape[0])
        #print("r:",r)
        
        shuffled_input=NN_input_features[r, :, :]
        
        # pad the input if num_particles < pad_dim
        pad_dim = 22
        num_particles = NN_input_features.shape[0]
        pad_input = (num_particles < pad_dim)
        #print("shuffled_input.shape:",shuffled_input.shape)
        
        # padd_array is needed if padding is done, but needs to be initialized outside of the if clause
        N = pad_dim 
        K = pad_dim - num_particles # K zeros, N-K ones
        padd_array = np.array([0] * K + [1] * (N-K))
        np.random.shuffle(padd_array)
        #print(padd_array)
        
        
        #print("pad_input:",pad_input)
        if pad_input:
            #print("in pad_input:   num_particles:", num_particles)
            

            torch.set_printoptions(threshold=10_000)        
            #print("shuffled_input:",shuffled_input) # prints the whole tensor




            input_padded = torch.ones(pad_dim, 1, shape[1]) * 0.

            particle_counter = 0
            for i in range(pad_dim):
                do_pad = padd_array[i]
                if do_pad == 1:    
                    #print(i)
                    #print(x[particle_counter,:,:])
                    input_padded[i,:,:] = shuffled_input[particle_counter,:,:]
                    particle_counter += 1
                    
            #print(input_padded)
            shuffled_input = input_padded
        
        
        #print("shuffled_input.shape:",shuffled_input.shape)
        #print("shuffled_input:",shuffled_input) # prints the whole tensor
        

        # pass input into the NN
        SA_pred = self.model(shuffled_input)

        
        
        
        probs = torch.softmax(SA_pred, dim=1)  # (N, C, d1)
        winners = probs.argmax(dim=1)
        #print("winners.shape:",winners.shape)
        #print("winners:",winners)
         
        # unpad winners if pad_input
        if pad_input:
            winners_unpadded = torch.empty(1, num_particles)
            particle_counter = 0
            for i in range(pad_dim):
                do_pad = padd_array[i]
                if do_pad == 1:  
                    winners_unpadded[0, particle_counter] = winners[0, i]
                    particle_counter += 1
                    
            #print(winners_unpadded)

            winners=winners_unpadded
        
        #print("winners.shape:",winners.shape)
        #print("winners:",winners)
        
        
        particle_i=0
        for p_list_name in self.particle_lists:
            # Get the particle list (note this is a regular Particle list, not MCParticle)
            p_list = Belle2.PyStoreObj(p_list_name)            

            for particle in p_list.obj():
                Hc_used = particle.getExtraInfo("Hc_used")
                if Hc_used == 1.0:
                    continue
                #print("Hc_used at addExtraInfo:",Hc_used)
                
                index_Shuffreversed = (r == particle_i).nonzero(as_tuple=True)[0].item()
                #print("particle_i:",particle_i,"index_Shuffreversed:",index_Shuffreversed)
                
                particle.addExtraInfo("NN_prediction", winners[0,index_Shuffreversed].item()) 
                
                
                #print("winners[0,particle_i]:", winners[0,particle_i].item())

                particle_i += 1
        print("end of event")
          
                
                           
                           
              
                           
                           
                           
                           
                           
    def terminate(self):
        pass
        # delete network etc here

