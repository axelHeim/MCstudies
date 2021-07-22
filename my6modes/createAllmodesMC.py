import basf2 as b2
import generators as ge
import simulation as si
import L1trigger as l1
import reconstruction as re
import mdst
import sys

mode = sys.argv[1]
print("passed mode:", mode)
num_perTree = 100

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
    signaldecfile=b2.find_file('./decfiles/mode{}.dec'.format(mode))
)

# Simulate the detector response
#si.add_simulation(path=main)

# Simulate the L1 trigger
#l1.add_tsim(path=main)

# Reconstruct the objects
#re.add_reconstruction(path=main)

# Create the mDST output file
mdst.add_mdst_output(path=main, filename="./rootfiles/mode{}_{}_events.root".format(mode,num_perTree))

# Process the steering path
b2.process(path=main)

# Finally, print out some statistics about the modules execution
print(b2.statistics)
#del main