import basf2 as b2
import modularAnalysis as ma
import variables.collections as vc
import sys 

mode = sys.argv[1]
print("passed mode:", mode)

nfs_path = "/nfs/dust/belle2/user/axelheim/MC_studies/my6modes"
root_subdir = "wSim_wReco"

events_num_identifier = "_15000_events"
# create path
path = b2.create_path()

# load input ROOT file
ma.inputMdst(environmentType='default',
             filename=b2.find_file(nfs_path + "/rootfiles/" + root_subdir + f"/mode{mode}" + events_num_identifier + ".root"),
             path=path)




ma.fillParticleListsFromMC([('K+:gen', ''),# ('K-:gen', ''),
                    ('pi+:gen', ''),# ('pi-:gen', ''),
                    ('gamma:gen', "")], path=path)
# generate the decay string
#path.add_module('ParticleMCDecayString', listName='J/psi', fileName='hashmap_Jpsi_from_B2A502.root')

#ma.copyLists('Upsilon(4S):all', ['K+:gen','K-:gen','pi+:gen','pi-:gen','gamma:gen'], path=path)


# write out ntuples
var = ['M',
       'x', 'y', 'z'
       ]

ma.matchMCTruth("gamma:gen", path=path)
ma.matchMCTruth("pi+:gen", path=path)
ma.matchMCTruth("K+:gen", path=path)
var +=  vc.kinematics 
var.append("kaonID")
var.append("pionID")
#var +=  "pionID" 

var += vc.mc_truth  
var.append("mcPhotos")
var.append("mcPrimary")
var.append("mcInitial")
var.append("charge")
var.append("uniqueParticleIdentifier")

var += ['genMotherID', 'genMotherPDG']
for i in range(4): # 4 deepest decay tree number of decays
    tmp_var = "genMotherPDG({})".format(i)
    #print(tmp_var)
    var.append(tmp_var)

#ma.combineAllParticles(['K+:gen','K-:gen','pi+:gen','pi-:gen','gamma:gen'], 'all:gen', path=path)
 
#ma.variablesToNtuple('Upsilon(4S):all', variables=var, filename='myFSP_nTuples_mode0.root', path=path)
file_extension = f"_nTuples_mode{mode}" + events_num_identifier + ".root"
print("example path to save data:", nfs_path + '/rootfiles/' + root_subdir + '/gamma' + file_extension)
ma.variablesToNtuple('gamma:gen',
                     variables=var,
                     filename=nfs_path + '/rootfiles/' + root_subdir + '/gamma' + file_extension,
                     path=path)
ma.variablesToNtuple('K+:gen',
                     variables=var,
                     filename=nfs_path + '/rootfiles/' + root_subdir + '/K' + file_extension,
                     path=path)
ma.variablesToNtuple('pi+:gen',
                     variables=var,
                     filename=nfs_path + '/rootfiles/' + root_subdir + '/pi' + file_extension,
                     path=path)
#ma.variablesToNtuple('all:gen',  variables=var, filename='allP_nTuples_mode0.root',  path=path)
# process the events
b2.process(path)

# print out the summary
print(b2.statistics)

