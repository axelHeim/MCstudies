import basf2 as b2
import generators as ge
import simulation as si
import L1trigger as l1
import reconstruction as re
import mdst
import sys

nfs_path = "/nfs/dust/belle2/user/axelheim/MC_studies/my6modes"
root_subdir = "wSim_wReco"
mode = sys.argv[1]
print("passed mode:", mode)
num_perTree = int(sys.argv[2])
print("events to create:", num_perTree)

num_modes = 6

#for mode in range(num_modes):
# Create the steering path
main = b2.Path()

# Define number of events and experiment number
main.add_module('EventInfoSetter', evtNumList=num_perTree, expList=[0])

main.add_module('Progress')

# Generate B0B0bar events
ge.add_evtgen_generator(
    path=main,
    finalstate='signal',
    signaldecfile=b2.find_file('/afs/desy.de/user/a/axelheim/private/MC_studies/my6modes/decfiles/mode{}.dec'.format(mode))
)

# Simulate the detector response
si.add_simulation(path=main)

# Simulate the L1 trigger
l1.add_tsim(path=main)

# Reconstruct the objects
re.add_reconstruction(path=main)

# Create the mDST output file
outpath = nfs_path + "/rootfiles/" + root_subdir + "/mode{}_{}_events.root".format(mode,num_perTree)
print("\n \n \n \n save data to:",outpath)
mdst.add_mdst_output(path=main, filename=outpath)

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)
#del main