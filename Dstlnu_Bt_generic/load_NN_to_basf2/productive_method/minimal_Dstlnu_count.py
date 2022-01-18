import basf2 as b2

import modularAnalysis as ma
from variables import variables as v
import variables.collections as vc

import sys
sys.path.insert(1, '/afs/desy.de/user/a/axelheim/private/MC_studies/Dstlnu_Bt_generic/NAHS/utils')
from aliases import define_aliases_Hc, define_aliases_FSPs, define_aliases_Upsilon4S

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

AliasDictUps4S= define_aliases_Upsilon4S()
add_aliases(AliasDictUps4S)
outvars_Ups4S = list(AliasDictUps4S.keys()) 


outpath="/nfs/dust/belle2/user/axelheim/MC_studies/Dstlnu_Bt_generic/appliedNNdata/minimalDstcounter/"


path = b2.create_path()

ma.inputMdst("/pnfs/desy.de/belle/local/belle/MC/release-05-02-00/DB00001330/MC14ri_a/prod00016816/s00/e1003/4S/r00000/mixed/mdst/sub00/mdst_000010_prod00016816_task10020000010.root", path=path)


ma.fillParticleList(decayString='pi+:counter',
                        cut='', path=path)


ma.rankByHighest('pi+:counter', 'px', numBest=1, path=path)
ma.variablesToNtuple('pi+:counter', variables=outvars_Ups4S, filename=outpath + 'evt_counter.root', path=path)



### cut for D*lnu
ma.applyEventCuts('''[[[abs_genUp4S_PDG_0_0 == 413.0] and [[abs_genUp4S_PDG_0_1 == 11.0] or [abs_genUp4S_PDG_0_1 == 13.0]] and [[abs_genUp4S_PDG_0_2 == 12.0] or [abs_genUp4S_PDG_0_2 == 14.0]]] or [[abs_genUp4S_PDG_1_0 == 413.0] and [[abs_genUp4S_PDG_1_1 == 11.0] or [abs_genUp4S_PDG_1_1 == 13.0]] and [[abs_genUp4S_PDG_1_2 == 12.0] or [abs_genUp4S_PDG_1_2 == 14.0]]]]''', path)
ma.variablesToNtuple('pi+:counter', variables=outvars_Ups4S, filename=outpath + 'evt_counter_afterDstlnu_cut.root', path=path)


b2.process(path)#, max_event=200)
print(b2.statistics)


print("**************")
print("THIS IS GONNA CHANGE THE WORLD!!!")
print("**************")