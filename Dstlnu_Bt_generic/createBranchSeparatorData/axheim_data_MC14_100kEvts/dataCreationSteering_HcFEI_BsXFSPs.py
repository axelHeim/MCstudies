# based on Gianna Mönig's steering file B_generic_apply_MC_Dstl_DXFEI.py she gave me ~May 2021
# altered by Axel Heimeroth Sep 2021

import basf2
#like that no need for basf2. before fcts
from basf2 import *
from modularAnalysis import *
from stdPhotons import stdPhotons 

from variables import variables as v
import vertex as vx
from stdPhotons import stdPhotons 
from stdCharged import stdCharged
from stdPi0s import stdPi0s

import variables.collections as vc


import pdg
#pdg.add_particle("X+", 9000000, 0, 0, 1, 0)
#pdg.add_particle("X0", 9000001, 0, 0, 0, 0)
pdg.add_particle("X", 9000000, 0, 0, 0, 0)

def buildRestOfEvent(targetListName, inputParticleLists, path):
    roeBuilder = basf2.register_module('RestOfEventBuilder')
    roeBuilder.set_name('ROEBuilder_' + targetListName)
    roeBuilder.param('particleList', targetListName)
    roeBuilder.param('particleListsInput', inputParticleLists)
    path.add_module(roeBuilder)


# #############Definition of aliases for the variable names###################################

v.addAlias('sigProb', 'extraInfo(SignalProbability)')
v.addAlias('log10_sigProb', 'log10(extraInfo(SignalProbability))')
v.addAlias('dmID', 'extraInfo(decayModeID)')
v.addAlias('foxWolframR2_maskedNaN', 'ifNANgiveX(foxWolframR2,1)')
v.addAlias('cosThetaBY', 'cosThetaBetweenParticleAndNominalB')
v.addAlias('d1_p_CMSframe', 'useCMSFrame(daughter(1,p))')
v.addAlias('d2_p_CMSframe', 'useCMSFrame(daughter(2,p))')

gamma_variables = ['p', 'pt', 'useCMSFrame(p)', 'useCMSFrame(pt)', 'mcMother(PDG)', 'mcMother(mcMother(PDG))', 'mcMother(mcMother(mcMother(PDG)))',
                    ]

def define_aliases_Xl():
    alias_dict ={}

    alias_dict['BeamE'] = 'beamE'
    alias_dict['BeamPx'] = 'beamPx'
    alias_dict['BeamPy'] = 'beamPy'
    alias_dict['BeamPz'] = 'beamPz'
    alias_dict['BeamcmsE'] = 'useCMSFrame(beamE)'
    alias_dict['BeamcmsPx'] = 'useCMSFrame(beamPx)'
    alias_dict['BeamcmsPy'] = 'useCMSFrame(beamPy)'
    alias_dict['BeamcmsPz'] = 'useCMSFrame(beamPz)'
    for i in range(0,2):
          alias_dict[f'genUp4S_PDG_{i}'] = f'genUpsilon4S(mcDaughter({i}, PDG))'
          alias_dict[f'genUp4S_charge_{i}'] = f'genUpsilon4S(mcDaughter({i}, charge))'
          alias_dict[f'genUp4S_mdstIndex_{i}'] = f'genUpsilon4S(mcDaughter({i}, mdstIndex))'
          alias_dict[f'genUp4S_genParticleID_{i}'] = f'genUpsilon4S(mcDaughter({i}, genParticleID))'
          alias_dict[f'genUp4S_E_{i}'] = f'genUpsilon4S(mcDaughter({i}, E))'
          alias_dict[f'genUp4S_Px_{i}'] = f'genUpsilon4S(mcDaughter({i}, px))'
          alias_dict[f'genUp4S_Py_{i}'] = f'genUpsilon4S(mcDaughter({i}, py))'
          alias_dict[f'genUp4S_Pz_{i}'] = f'genUpsilon4S(mcDaughter({i}, pz))'
          alias_dict[f'genUp4S_P_{i}'] = f'genUpsilon4S(mcDaughter({i}, p))'
          alias_dict[f'genUp4S_cmE_{i}'] = f'genUpsilon4S(mcDaughter({i}, useCMSFrame(E)))'
          alias_dict[f'genUp4S_cmPx_{i}'] = f'genUpsilon4S(mcDaughter({i}, useCMSFrame(px)))'
          alias_dict[f'genUp4S_cmPy_{i}'] = f'genUpsilon4S(mcDaughter({i}, useCMSFrame(py)))'
          alias_dict[f'genUp4S_cmPz_{i}'] = f'genUpsilon4S(mcDaughter({i}, useCMSFrame(py)))'
          alias_dict[f'genUp4S_cmP_{i}'] = f'genUpsilon4S(mcDaughter({i}, useCMSFrame(p)))'

          for j in range(0,3):
              alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
              alias_dict[f'genUp4S_mdstIndex_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mdstIndex)))'
              alias_dict[f'genUp4S_genParticleID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},genParticleID)))'
              if j == 0:
                for k in range(0,2):
                   alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                   alias_dict[f'genUp4S_mdstIndex_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mdstIndex))))'
                   alias_dict[f'genUp4S_genParticleID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},genParticleID))))'
    for i in range(0,1):
      alias_dict['dau{}_M'.format(i)]= 'daughter({}, M)'.format(i)
      alias_dict['dau{}_chiProb'.format(i)]= 'daughter({}, chiProb)'.format(i)
      alias_dict['dau{}_cmp'.format(i)]= 'useCMSFrame(daughter({}, p))'.format(i)
      alias_dict['dau{}_cmE'.format(i)]= 'useCMSFrame(daughter({}, E))'.format(i)
      alias_dict['dau{}_cmpx'.format(i)]= 'useCMSFrame(daughter({}, px))'.format(i)
      alias_dict['dau{}_cmpy'.format(i)]= 'useCMSFrame(daughter({}, py))'.format(i)
      alias_dict['dau{}_cmpz'.format(i)]= 'useCMSFrame(daughter({}, pz))'.format(i)
      alias_dict['dau{}_cmpt'.format(i)]= 'useCMSFrame(daughter({}, pt))'.format(i)
      alias_dict['dau{}_p'.format(i)]= 'daughter({}, p)'.format(i)
      alias_dict['dau{}_E'.format(i)]= 'daughter({}, E)'.format(i)
      alias_dict['dau{}_px'.format(i)]= 'daughter({}, px)'.format(i)
      alias_dict['dau{}_py'.format(i)]= 'daughter({}, py)'.format(i)
      alias_dict['dau{}_pz'.format(i)]= 'daughter({}, pz)'.format(i)
      alias_dict['dau{}_pt'.format(i)]= 'daughter({}, pt)'.format(i)
      alias_dict['dau{}_mcp'.format(i)]= 'daughter({},mcP)'.format(i)
      alias_dict['dau{}_mcpt'.format(i)]= 'daughter({},mcPT)'.format(i)
      alias_dict['dau{}_dau1_charge'.format(i)]= 'daughter({}, daughter(1, charge))'.format(i)
      alias_dict['dau{}_dau0_motherP'.format(i)]= 'daughter({}, daughter(0, mcMother(p)))'.format(i)
      alias_dict['dau{}_dau0_motherE'.format(i)]= 'daughter({}, daughter(0, mcMother(E)))'.format(i)
      alias_dict['dau{}_dau0_motherPx'.format(i)]= 'daughter({}, daughter(0, mcMother(px)))'.format(i)
      alias_dict['dau{}_dau0_motherPy'.format(i)]= 'daughter({}, daughter(0, mcMother(py)))'.format(i)
      alias_dict['dau{}_dau0_motherPz'.format(i)]= 'daughter({}, daughter(0, mcMother(pz)))'.format(i)
      alias_dict['dau{}_dau0_mothercmsP'.format(i)]= 'daughter({}, daughter(0, mcMother(useCMSFrame(p))))'.format(i)
      alias_dict['dau{}_dau0_mothercmsE'.format(i)]= 'daughter({}, daughter(0, mcMother(useCMSFrame(E))))'.format(i)
      alias_dict['dau{}_dau0_mothercmsPx'.format(i)]= 'daughter({}, daughter(0, mcMother(useCMSFrame(px))))'.format(i)
      alias_dict['dau{}_dau0_mothercmsPy'.format(i)]= 'daughter({}, daughter(0, mcMother(useCMSFrame(py))))'.format(i)
      alias_dict['dau{}_dau0_mothercmsPz'.format(i)]= 'daughter({}, daughter(0, mcMother(useCMSFrame(pz))))'.format(i)
      alias_dict['dau{}_dau0_motherPDG'.format(i)]= 'daughter({}, daughter(0, mcMother(PDG)))'.format(i)
      alias_dict['dau{}_dau0_grandmotherP'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(p))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherE'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(E))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPx'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(px))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPy'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(py))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPz'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(pz))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherP'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(useCMSFrame(p)))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherE'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(useCMSFrame(E)))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPx'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(useCMSFrame(px)))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPy'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(useCMSFrame(py)))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPz'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(useCMSFrame(pz)))))'.format(i)
      alias_dict['dau{}_dau0_grandmotherPDG'.format(i)]= 'daughter({}, daughter(0, mcMother(mcMother(PDG))))'.format(i)
      alias_dict['dau{}_mccmp'.format(i)]= 'daughter({}, useCMSFrame(mcP))'.format(i)
      alias_dict['dau{}_mccmpt'.format(i)]= 'daughter({}, useCMSFrame(mcPT))'.format(i)
      alias_dict['dau{}_decmode'.format(i)]= 'daughter({}, extraInfo(decayModeID))'.format(i)
      alias_dict['dau{}_sigProb'.format(i)]= 'daughter({}, extraInfo(SignalProbability))'.format(i)
      alias_dict['dau{}_dau0_decmode'.format(i)]= 'daughter({}, daughter(0, extraInfo(decayModeID)))'.format(i)
      alias_dict['dau{}_dau0_sigProb'.format(i)]= 'daughter({}, daughter(0,extraInfo(SignalProbability)))'.format(i)
      alias_dict['dau{}_dau0_charge'.format(i)]= 'daughter({}, daughter(0, charge))'.format(i)
      alias_dict['dau{}_dau0_M'.format(i)]= 'daughter({}, daughter(0, M))'.format(i)
      alias_dict['dau{}_dau0_DeltaM'.format(i)] = 'daughter({},daughter(0,massDifference(0)))'.format(i)
      alias_dict['dau{}_dau0_E'.format(i)]= 'daughter({}, daughter(0, E))'.format(i)
      alias_dict['dau{}_dau0_px'.format(i)]= 'daughter({}, daughter(0, px))'.format(i)
      alias_dict['dau{}_dau0_py'.format(i)]= 'daughter({}, daughter(0, py))'.format(i)
      alias_dict['dau{}_dau0_pz'.format(i)]= 'daughter({}, daughter(0, pz))'.format(i)
      alias_dict['dau{}_dau0_PDG'.format(i)]= 'daughter({}, daughter(0, PDG))'.format(i)
      alias_dict['dau{}_dau0_isSignal'.format(i)]= 'daughter({}, daughter(0, isSignal))'.format(i)
      alias_dict['dau{}_dau0_isSignalAcceptMissingGamma'.format(i)]= 'daughter({}, daughter(0, isSignalAcceptMissingGamma))'.format(i)
      alias_dict['dau{}_dau1_M'.format(i)]= 'daughter({}, daughter(1, M))'.format(i)
      alias_dict['dau{}_dau1_E'.format(i)]= 'daughter({}, daughter(1, E))'.format(i)
      alias_dict['dau{}_dau1_px'.format(i)]= 'daughter({}, daughter(1, px))'.format(i)
      alias_dict['dau{}_dau1_py'.format(i)]= 'daughter({}, daughter(1, py))'.format(i)
      alias_dict['dau{}_dau1_pz'.format(i)]= 'daughter({}, daughter(1, pz))'.format(i)
      alias_dict['dau{}_dau1_nDaughters'.format(i)]= 'daughter({}, daughter(1, nDaughters))'.format(i)
      alias_dict['dau{}_dau1_dau0_PDG'.format(i)]= 'daughter({}, daughter(1, daughter(0,PDG)))'.format(i)
      alias_dict['dau{}_dau1_dau1_PDG'.format(i)]= 'daughter({}, daughter(1, daughter(1,PDG)))'.format(i)
      alias_dict['dau{}_dau1_dau2_PDG'.format(i)]= 'daughter({}, daughter(1, daughter(2,PDG)))'.format(i)
      alias_dict['dau{}_dau1_dau3_PDG'.format(i)]= 'daughter({}, daughter(1, daughter(3,PDG)))'.format(i)     
      alias_dict['dau{}_dau2_p'.format(i)]= 'daughter({}, daughter(1, E))'.format(i)
      alias_dict['dau{}_dau2_p'.format(i)]= 'daughter({}, daughter(1, p))'.format(i)
      alias_dict['dau{}_deltaE'.format(i)]= 'daughter({},deltaE)'.format(i)
      alias_dict['dau{}_Mbc'.format(i)]= 'daughter({},Mbc)'.format(i)
      alias_dict['dau{}_FEIRank'.format(i)]= 'daughter({}, extraInfo(FEIProbabilityRank))'.format(i)
      alias_dict['dau{}_isSignal'.format(i)]= 'daughter({},isSignal)'.format(i)
      alias_dict['dau{}_R2'.format(i)]= 'daughter({},R2)'.format(i)
      alias_dict['dau{}_cosTBTO'.format(i)]= 'daughter({},cosTBTO)'.format(i) 
      alias_dict['dau{}_cosThetaBetweenParticleAndNominalB'.format(i)]= 'daughter({},cosThetaBetweenParticleAndNominalB)'.format(i)
      alias_dict['dau{}_PDG'.format(i)]= 'daughter({},PDG)'.format(i)
      alias_dict['dau{}_motherPDG'.format(i)]= 'daughter({},genMotherPDG)'.format(i)
    for i in range(1,2):
      alias_dict['dau{}_Nelectrons'.format(i)]= 'daughter({},nROE_Charged(cleanMask,11))'.format(i)
      alias_dict['dau{}_Nmuons'.format(i)]= 'daughter({},nROE_Charged(cleanMask,13))'.format(i)
      alias_dict['dau{}_Npip'.format(i)]= 'daughter({},nROE_Charged(cleanMask,211))'.format(i)
      alias_dict['dau{}_NKp'.format(i)]= 'daughter({},nROE_Charged(cleanMask,321))'.format(i)
      alias_dict['dau{}_M'.format(i)]= 'daughter({}, M)'.format(i)
      alias_dict['dau{}_cmp'.format(i)]= 'daughter({}, useCMSFrame(p))'.format(i)
      alias_dict['dau{}_cmE'.format(i)]= 'daughter({}, useCMSFrame(E))'.format(i)
      alias_dict['dau{}_cmpx'.format(i)]= 'daughter({}, useCMSFrame(px))'.format(i)
      alias_dict['dau{}_cmpy'.format(i)]= 'daughter({}, useCMSFrame(py))'.format(i)
      alias_dict['dau{}_cmpz'.format(i)]= 'daughter({}, useCMSFrame(pz))'.format(i)
      alias_dict['dau{}_cmpt'.format(i)]= 'daughter({}, useCMSFrame(pt))'.format(i)
      alias_dict['dau{}_theta'.format(i)]= 'daughter({}, theta)'.format(i)
      alias_dict['dau{}_p'.format(i)]= 'daughter({}, p)'.format(i)
      alias_dict['dau{}_E'.format(i)]= 'daughter({}, E)'.format(i)
      alias_dict['dau{}_px'.format(i)]= 'daughter({}, px)'.format(i)
      alias_dict['dau{}_py'.format(i)]= 'daughter({}, py)'.format(i)
      alias_dict['dau{}_pz'.format(i)]= 'daughter({}, pz)'.format(i)
      alias_dict['dau{}_pt'.format(i)]= 'daughter({}, pt)'.format(i)
      alias_dict['dau{}_mcp'.format(i)]= 'daughter({},mcP)'.format(i)
      alias_dict['dau{}_mcpt'.format(i)]= 'daughter({},mcPT)'.format(i)
      alias_dict['dau{}_mccmE'.format(i)]= 'daughter({}, useCMSFrame(mcE))'.format(i)
      alias_dict['dau{}_mccmp'.format(i)]= 'daughter({}, useCMSFrame(mcP))'.format(i)
      alias_dict['dau{}_mccmpx'.format(i)]= 'daughter({}, useCMSFrame(mcPX))'.format(i)
      alias_dict['dau{}_mccmpy'.format(i)]= 'daughter({}, useCMSFrame(mcPY))'.format(i)
      alias_dict['dau{}_mccmpz'.format(i)]= 'daughter({}, useCMSFrame(mcPZ))'.format(i)
      alias_dict['dau{}_mccmpt'.format(i)]= 'daughter({}, useCMSFrame(mcPT))'.format(i)
      alias_dict['dau{}_cosThetaBetweenParticleAndNominalB'.format(i)]= 'daughter({},cosThetaBetweenParticleAndNominalB)'.format(i)
      alias_dict['dau{}_isSignal'.format(i)]= 'daughter({},isSignalAcceptMissingNeutrino)'.format(i)
      alias_dict['dau{}_mcPDG'.format(i)]= 'daughter({},mcPDG)'.format(i)
      alias_dict['dau{}_dau0_mcPDG'.format(i)]= 'daughter({},daughter(0,mcPDG))'.format(i)
      alias_dict['dau{}_dau1_mcPDG'.format(i)]= 'daughter({},daughter(1,mcPDG))'.format(i)
      alias_dict['dau{}_dau0_mothermdstIndex'.format(i)]= 'daughter({},daughter(0,mcMother(mdstIndex)))'.format(i)
      alias_dict['dau{}_dau1_mothermdstIndex'.format(i)]= 'daughter({},daughter(1,mcMother(mdstIndex)))'.format(i)
      alias_dict['dau{}_mdstIndex'.format(i)]= 'daughter({},mdstIndex)'.format(i)
      alias_dict['dau{}_motherPDG'.format(i)]= 'daughter({},genMotherPDG)'.format(i)
    for i in range(1,2):
      alias_dict['lep_mdstIndex'.format(i)]= 'daughter(1, daughter({},mdstIndex))'.format(i)
      alias_dict['lep_PDG'.format(i)]= 'daughter(1, daughter({},PDG))'.format(i)
      alias_dict['lep_theta'.format(i)]= 'daughter(1, daughter({},theta))'.format(i)
      alias_dict['lep_clusterEP']= 'daughter(1,daughter({}, formula(clusterE/p)))'.format(i)
      alias_dict['lep_clusterE']= 'daughter(1,daughter({},clusterE))'.format(i)
      alias_dict['lep_eID']= 'daughter(1,daughter({},electronID))'.format(i)
      alias_dict['lep_muID']= 'daughter(1,daughter({},muonID))'.format(i)
      alias_dict['lep_clusterE9E21']= 'daughter(1,daughter({},clusterE9E21))'.format(i)
      alias_dict['lep_absdz']= 'daughter(1,daughter({},abs(dz)))'.format(i)
      alias_dict['lep_absd0']= 'daughter(1,daughter({},abs(d0)))'.format(i)
      alias_dict['lep_klmLayers']= 'daughter(1,daughter({},klmClusterLayers))'.format(i)
      alias_dict['lep_MatchedKLMClusters']= 'daughter(1,daughter({},nMatchedKLMClusters))'.format(i)
      alias_dict['lep_M']= 'daughter(1,daughter({}, M))'.format(i)
      alias_dict['lep_chiProb']= 'daughter(1,daughter({}, chiProb))'.format(i)
      alias_dict['lep_cmE']= 'daughter(1,daughter({}, useCMSFrame(E)))'.format(i)
      alias_dict['lep_cmp']= 'daughter(1,daughter({}, useCMSFrame(p)))'.format(i)
      alias_dict['lep_cmpx']= 'daughter(1,daughter({}, useCMSFrame(px)))'.format(i)
      alias_dict['lep_cmpy']= 'daughter(1,daughter({}, useCMSFrame(py)))'.format(i)
      alias_dict['lep_cmpz']= 'daughter(1,daughter({}, useCMSFrame(pz)))'.format(i)
      alias_dict['lep_cmpt']= 'daughter(1,daughter({}, useCMSFrame(pt)))'.format(i)
      alias_dict['lep_E']= 'daughter(1,daughter({}, E))'.format(i)
      alias_dict['lep_p']= 'daughter(1,daughter({}, p))'.format(i)
      alias_dict['lep_px']= 'daughter(1,daughter({}, px))'.format(i)
      alias_dict['lep_py']= 'daughter(1,daughter({}, py))'.format(i)
      alias_dict['lep_pz']= 'daughter(1,daughter({}, pz))'.format(i)
      alias_dict['lep_pt']= 'daughter(1,daughter({}, pt))'.format(i)
      alias_dict['lep_mcp']= 'daughter(1,daughter({},mcP))'.format(i)
      alias_dict['lep_mcpt']= 'daughter(1,daughter({},mcPT))'.format(i)
      alias_dict['lep_mccmp']= 'daughter(1,daughter({}, useCMSFrame(mcP)))'.format(i)
      alias_dict['lep_mccmpt']= 'daughter(1,daughter({}, useCMSFrame(mcPT)))'.format(i)
      alias_dict['lep_mcPDG']= 'daughter(1,daughter({},mcPDG))'.format(i)
      alias_dict['lep_genParticleID']= 'daughter(1,daughter({},genParticleID))'.format(i)
      alias_dict['lep_motherPDG']= 'daughter(1,daughter({},genMotherPDG))'.format(i)
      alias_dict['lep_gmotherPDG']= 'daughter(1,daughter({},genMotherPDG(1)))'.format(i)
      alias_dict['lep_genmotherID']= 'daughter(1,daughter({},genMotherID))'.format(i)
      alias_dict['lep_mothermdstIndex']= 'daughter(1,daughter({},mcMother(mdstIndex)))'.format(i)
    
    alias_dict['D_nDaughters'] = 'daughter(1,daughter(0,daughter(0,nDaughters)))'
    alias_dict['D_M'] = 'daughter(1,daughter(0,daughter(0,M)))'
    alias_dict['D_p'] = 'daughter(1,daughter(0,daughter(0,p)))'
    alias_dict['D_pt'] = 'daughter(1,daughter(0,daughter(0,pt)))'
    alias_dict['D_cmp'] = 'daughter(1,daughter(0,daughter(0,useCMSFrame(p))))'
    alias_dict['D_cmpt'] = 'daughter(1,daughter(0,daughter(0,useCMSFrame(pt))))'
    alias_dict['D_isSignal'] = 'daughter(1,daughter(0,daughter(0,isSignal)))'
    alias_dict['Dst_M'] = 'daughter(1,daughter(0,M))'
    alias_dict['Dst_E'] = 'daughter(1,daughter(0,E))'
    alias_dict['Dst_p'] = 'daughter(1,daughter(0,p))'
    alias_dict['Dst_px'] = 'daughter(1,daughter(0,px))'
    alias_dict['Dst_py'] = 'daughter(1,daughter(0,py))'
    alias_dict['Dst_pz'] = 'daughter(1,daughter(0,pz))'
    alias_dict['Dst_pt'] = 'daughter(1,daughter(0,pt))'
    alias_dict['Dst_cmE'] = 'daughter(1,daughter(0,useCMSFrame(E)))'
    alias_dict['Dst_cmp'] = 'daughter(1,daughter(0,useCMSFrame(p)))'
    alias_dict['Dst_cmpx'] = 'daughter(1,daughter(0,useCMSFrame(px)))'
    alias_dict['Dst_cmpy'] = 'daughter(1,daughter(0,useCMSFrame(py)))'
    alias_dict['Dst_cmpz'] = 'daughter(1,daughter(0,useCMSFrame(pz)))'
    alias_dict['Dst_cmpt'] = 'daughter(1,daughter(0,useCMSFrame(pt)))'
    alias_dict['Dst_mccmE'] = 'daughter(1,daughter(0,useCMSFrame(mcE)))'
    alias_dict['Dst_mccmp'] = 'daughter(1,daughter(0,useCMSFrame(mcP)))'
    alias_dict['Dst_mccmpx'] = 'daughter(1,daughter(0,useCMSFrame(mcPX)))'
    alias_dict['Dst_mccmpy'] = 'daughter(1,daughter(0,useCMSFrame(mcPY)))'
    alias_dict['Dst_mccmpz'] = 'daughter(1,daughter(0,useCMSFrame(mcPZ)))'
    alias_dict['Dst_DeltaM'] = 'daughter(1,daughter(0,massDifference(0)))'
    alias_dict['Dst_isSignal'] = 'daughter(1,daughter(0,isSignal))'
    return(alias_dict)

"""     # added for BranchSeparator data creation
    variables = ["px","py","pz","E","charge","PDG"] # uniqueParticleIdentifier
    #variables = ["uniqueParticleIdentifier"] #  
    for var in variables:
    
      # for X: all are daughter of X = dau0dau1
      for i in range(30): # root output shows no more than 25 daughters in X
        #continue
        alias_dict['X_dau{}_{}'.format(i,var)]= 'daughter(0,daughter(1,daughter({},{})))'.format(i,var)


      # for Bsig particles: Bsig = dau1
      # for Dst = dau1dau0 , depth of 2 for decay pions and kaons and possible pi0->2gamma
      for i in range(2): # maximum of 2 particles from Dst (D0 and K)
        alias_dict['Dst_dau{}_{}'.format(i,var)]= 'daughter(1,daughter(0,daughter({},{})))'.format(i,var)
        
      for i in range(2): # maximum of 2 gammas from pi0 (only at pos 2 or 4 (counting from 0))
        alias_dict['D0_pi0_2_gamma{}_{}'.format(i,var)]= 'daughter(1,daughter(0,daughter(0,daughter(2,daughter({},{})))))'.format(i,var)
        alias_dict['D0_pi0_4_gamma{}_{}'.format(i,var)]= 'daughter(1,daughter(0,daughter(0,daughter(4,daughter({},{})))))'.format(i,var)
  
      # for lepton = dau1dau1
      alias_dict['lep_{}'.format(var)]= 'daughter(1,daughter(1,{}))'.format(var)
    return(alias_dict)
 """
  



    

def add_aliases(alias_dict={}):
   for key,value in alias_dict.items():
      v.addAlias(key,value)

# ##########################FEI part####################################

def get_tag_side_variables():
    return [
          'nRemainingTracksInEvent',
          'dx', 'dy', 'dz', 'chiProb','E','px','py','pz',
          'mcP','mcPT','mcPX','mcPY','mcPZ','mcPhi','genMotherPDG',
          'mcPDG','isContinuumEvent'
          
    ]
#reset_database()
#use_central_database()
#use_local_database('/gpfs/group/belle2/users/sutclw/fei4/feiv4_2019_MC12_release_03_01_01_phase3/localdb/database.txt',
#                     '/gpfs/group/belle2/users/sutclw/fei4/feiv4_2019_MC12_release_03_01_01_phase3/localdb', True, LogLevel.WARNING)

# input_file = '/home/belle2/gmonig/Test/MC/sub00/mdst_000001_prod00009434_task10020000001.root'

path = create_path()
#basf2.fw.add_module_search_path(".")
#basf2.register_module("EnableMyVariable")
inputMdstList('default', [], path)



fillParticleList(decayString='pi+:eventShapeForSkims',
                        cut='d0<0.5 and -2<z0<2 and pt>0.1', path=path)
fillParticleList(decayString='gamma:eventShapeForSkims',
                        cut='E > 0.1 and 0.296706 < theta < 2.61799', path=path)
v.addAlias('E_ECL_pi', 'totalECLEnergyOfParticlesInList(pi+:eventShapeForSkims)')
v.addAlias('E_ECL_gamma', 'totalECLEnergyOfParticlesInList(gamma:eventShapeForSkims)')
v.addAlias('E_ECL', 'formula(E_ECL_pi+E_ECL_gamma)')

applyEventCuts('nCleanedTracks(abs(z0) < 2.0 and abs(d0) < 0.5 and pt>0.1)>=3', path=path)
applyEventCuts('nCleanedECLClusters(0.296706 < theta < 2.61799 and E>0.2)>=3', path=path)
buildEventKinematics(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'], path=path)
applyEventCuts('visibleEnergyOfEventCMS>4', path=path)
applyEventCuts('2<E_ECL<7', path=path)

buildEventShape(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'],
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

applyEventCuts('foxWolframR2_maskedNaN<0.4 and nTracks>=4', path=path)

basf2.conditions.globaltags = ['analysis_tools_release-04']

import fei
particles = fei.get_default_channels(baryonic=True)
# You can turn on and off individual parts of the reconstruction without retraining!
# particles = fei.get_default_channels(hadronic=True, semileptonic=True, chargedB=True, neutralB=True)

configuration = fei.config.FeiConfiguration(prefix='FEIv4_2020_MC13_release_04_01_01', training=False, monitor=False)
feistate = fei.get_path(particles, configuration)

path.add_path(feistate.path)

fillParticleList(decayString='pi+:eventShapeForSkims',
                     cut='pt> 0.1', path=path)
fillParticleList(decayString='gamma:eventShapeForSkims',
                     cut='E > 0.1', path=path)

buildEventShape(inputListNames=['pi+:eventShapeForSkims', 'gamma:eventShapeForSkims'],
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

path.add_module('MCMatcherParticles', listName='B0:generic', looseMCMatching=True)


rankByHighest('B0:generic', 'extraInfo(SignalProbability)', numBest=1,
              outputVariable='FEIProbabilityRank', path=path)

# #ROE of B_tag reconstructed by FEI

stdCharged('pi','all', path=path)
stdCharged('K','all', path=path)
stdPi0s('eff40_Jan2020', path=path)

fillParticleList("gamma:myMinimumThresholdList", "clusterE > 0.02", path=path)

reconstructDecay('pi0:forX -> gamma:myMinimumThresholdList gamma:myMinimumThresholdList','M > 0.124 and M < 0.140', path=path)

fillParticleList('K-:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and kaonID > 0.6 \
and pionID<0.6 and muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
fillParticleList('pi+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and pionID > 0.6 \
and kaonID < 0.6 and electronID < 0.9 and  muonID < 0.9 and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)
fillParticleList('e+:cande',"abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and electronID > 0.9 and theta > 0.297 and theta < 2.618", path=path)
fillParticleList('mu+:candmu', "abs(d0) < 0.5 and abs(dz) < 2 and pt > 0.3 and useCMSFrame(p)>1 and muonID > 0.9 and electronID < 0.9 and theta > 0.297 and theta < 2.618", path=path)

fillParticleList('p+:forX',"dr < 2 and abs(dz) < 4 and pt > 0.3 and protonID > 0.6 and kaonID < 0.6 \
and pionID<0.6 and muonID < 0.9 and electronID < 0.9  and theta > 0.297 and theta < 2.618 and nCDCHits > 0 and thetaInCDCAcceptance==1", path=path)

cutAndCopyList('gamma:forX', 'gamma:myMinimumThresholdList', "[clusterReg==1 and pt>0.02 and clusterZernikeMVA > 0.35] or [clusterReg==2 and pt>0.03 and clusterZernikeMVA > 0.15] or [clusterReg==3 and pt>0.02 and clusterZernikeMVA > 0.4]", path=path)


roeinputs = ['gamma:forX','pi+:forX','K+:forX','p+:forX', 'e+:cande','mu+:candmu']

# define the mask with hard-coded CS cuts in the ROE mask
# ROEmask tuple: (mask name, track cuts, cluster cuts)

names = ['B0:generic']

#construct ROE for FEI reconstructed B
for name in names:
 buildRestOfEvent(name,roeinputs, path=path)
 # append both masks to ROE
 appendROEMask(name, "cleanMask", "dr < 2 and abs(dz) < 4 and pt > 0.2", "[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]", path=path)

 # choose one mask which is applied
 buildContinuumSuppression(name, 'cleanMask',path=path)



cutAndCopyList('pi+:slow', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2', path=path)
cutAndCopyList('pi+:sig', 'pi+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)
cutAndCopyList('K+:sig', 'K+:all', 'abs(d0) < 0.5 and abs(z0) < 2 and thetaInCDCAcceptance and nCDCHits>0', path=path)

# ##Reconstruct Signal side ###

reconstructDecay('D0:kpi -> K-:sig pi+:sig', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipipi -> K-:sig pi+:sig pi-:sig pi+:sig', '1.8 < M < 1.9', path=path)
#reconstructDecay('D0:kpipi0 -> K-:sig pi+:sig pi0:loose', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipi0 -> K-:sig pi+:sig pi0:eff40_Jan2020', '1.8 < M < 1.9', path=path)
#reconstructDecay('D0:kpipipipi0 -> K-:sig pi+:sig pi-:sig pi+:sig pi0:loose', '1.8 < M < 1.9', path=path)
reconstructDecay('D0:kpipipipi0 -> K-:sig pi+:sig pi-:sig pi+:sig pi0:eff40_Jan2020', '1.8 < M < 1.9', path=path)
copyLists('D0:cand', ['D0:kpi','D0:kpipipi','D0:kpipi0','D0:kpipipipi0'], path=path)
#vx.vertexKFit('D0:cand',0.0, path=path)
path.add_module('MCMatcherParticles', listName='D0:cand', looseMCMatching=True)

reconstructDecay('D*+:kpi -> D0:cand pi+:slow', '0.139<massDifference(0)<0.16', path=path)
#vx.vertexKFit('D*+:kpi',0.0, path=path)

path.add_module('MCMatcherParticles', listName='D*+:kpi', looseMCMatching=True)

reconstructDecay('anti-B0:Dstkpie -> D*+:kpi e-:cande', '', path=path)
reconstructDecay('anti-B0:Dstkpimu -> D*+:kpi mu-:candmu', '', path=path)
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpie')
path.add_module('MCMatcherParticles', listName='anti-B0:Dstkpimu')
copyLists('anti-B0:sig', ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu'], path=path)
track_selection=" and ".join(
            [
                "[dr < 2]",
                "[abs(dz) < 4]",
                "[nCDCHits > 0]",
                "[thetaInCDCAcceptance==1]"
            ]
)
ecl_selection="[[[clusterReg==1] and [pt>0.02] and [clusterZernikeMVA > 0.35]] or [[clusterReg==2] and [pt>0.03] and [clusterZernikeMVA > 0.15]] or [[clusterReg==3] and [pt>0.02] and [clusterZernikeMVA > 0.4]]]"
roe_mask = (track_selection, ecl_selection)
for name in ['anti-B0:Dstkpie', 'anti-B0:Dstkpimu']:
    buildRestOfEvent(name,roeinputs, path=path)
    appendROEMask(name, "cleanMask", roe_mask[0], roe_mask[1], path=path)
    buildContinuumSuppression(name, 'cleanMask',path=path)


AliasDict= define_aliases_Xl()
print(AliasDict)
add_aliases(AliasDict)
tagside_variables = list(AliasDict.keys()) 

""" #reconstruct Upsilon4s of B_sig and FEI B_tag
reconstructDecay('Upsilon(4S):UpDste -> B0:generic anti-B0:Dstkpie ','',path=path)
reconstructDecay('Upsilon(4S):UpDstmu -> B0:generic anti-B0:Dstkpimu','',path=path)
names = ['Upsilon(4S):UpDste','Upsilon(4S):UpDstmu']
copyLists('Upsilon(4S):UpDstl', names, path=path)

buildRestOfEvent('Upsilon(4S):UpDstl', roeinputs,  path=path)
appendROEMask('Upsilon(4S):UpDstl', "CleanROE", "dr < 2 and abs(dz) < 4 and pt > 0.2", "[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]", path=path)
rankByHighest('Upsilon(4S):UpDstl', 'daughter(1,useCMSFrame(p))', numBest=1,
              outputVariable='p_best', path=path)





variablesToNtuple('Upsilon(4S):UpDstl',
                  [
                   "m2RecoilSignalSide",
                   "foxWolframR2_maskedNaN",
                   'foxWolframR2',
                   "nTracks"
                   ] +  tagside_variables,
                  filename='B0tagDstl.root',
                  path=path)
 """
cutAndCopyList('anti-B0:sigclean',"anti-B0:sig",'-1.5 < cosThetaBetweenParticleAndNominalB < 1.5 and daughter(0,useCMSFrame(p))<2.4 and daughter(1,useCMSFrame(p))>1.', path= path)

cutAndCopyList('anti-D*0:genericsigProb',"anti-D*0:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
cutAndCopyList('D*-:genericsigProb',"D*-:generic",'extraInfo(SignalProbability)>0.001 and 0.139<massDifference(0)<0.16', path= path)
cutAndCopyList('D-:genericsigProb',"D-:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('anti-D0:genericsigProb',"anti-D0:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('anti-Lambda_c-:genericsigProb',"anti-Lambda_c-:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('D_s+:genericsigProb',"D_s+:generic",'extraInfo(SignalProbability)>0.001', path= path)
cutAndCopyList('J/psi:genericsigProb',"J/psi:generic",'extraInfo(SignalProbability)>0.001', path= path)


#reconstruct a pseudo upsilon4s from B_sig and H_c to determine ROE of this
reconstructDecay('Upsilon(4S):Dst0Dstl -> anti-B0:sigclean  anti-D*0:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DstpDstl -> anti-B0:sigclean  D*-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DpDstl -> anti-B0:sigclean  D-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):D0Dstl -> anti-B0:sigclean  anti-D0:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):LcDstl -> anti-B0:sigclean  anti-Lambda_c-:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):DsDstl -> anti-B0:sigclean  D_s+:genericsigProb','',path=path,allowChargeViolation=True)
reconstructDecay('Upsilon(4S):JpsiDstl -> anti-B0:sigclean  J/psi:genericsigProb','',path=path,allowChargeViolation=True)

parts_BHc_all=['Upsilon(4S):DpDstl', 'Upsilon(4S):LcDstl' ,'Upsilon(4S):DsDstl', 'Upsilon(4S):DstpDstl', 'Upsilon(4S):D0Dstl', 
                'Upsilon(4S):JpsiDstl', 'Upsilon(4S):Dst0Dstl']


path.add_module('MCMatcherParticles', listName='anti-D*0:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D*-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='anti-D0:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='anti-Lambda_c-:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='D_s+:genericsigProb', looseMCMatching=True)
path.add_module('MCMatcherParticles', listName='J/psi:genericsigProb', looseMCMatching=True)

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

for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]

    rankByHighest(part_BHc_all, 'daughter(1,extraInfo(SignalProbability))', numBest=0, allowMultiRank=True,
            outputVariable='FEIProbabilityRank_all', path=path)

    applyCuts(part_BHc_all, 'extraInfo(FEIProbabilityRank_all) == 1', path=path)

    cutAndCopyList(f'{name_dict[parid]}:tag',f"{name_dict[parid]}:genericsigProb",f'IsDaughterOf({part_BHc_all}) == 1', path= path)


    buildRestOfEvent(part_BHc_all,roeinputs,path=path)
    appendROEMask(part_BHc_all, 'CleanROEBtag', roe_mask[0], roe_mask[1], path=path)
    ##construct X from ROE
    fillParticleListFromROE(f'X:tag{parid}','',maskName="CleanROEBtag",sourceParticleListName=part_BHc_all ,path=path)
    ##reconstruct B_tag from X and H_c
    reconstructDecay(f'B0:{parid}DXtag -> {name_dict[parid]}:tag X:tag{parid}','',path=path,allowChargeViolation=True)
    reconstructDecay(f'Upsilon(4S):{parid}DXtag -> B0:{parid}DXtag anti-B0:sigclean','',path=path)
    applyCuts(f'Upsilon(4S):{parid}DXtag', 'abs(daughter(0,deltaE))<0.2', path=path)
    outlists_DX.append(f'Upsilon(4S):{parid}DXtag')


copyLists('Upsilon(4S):DXtag', outlists_DX, path=path)

rankByHighest('Upsilon(4S):DXtag', 'daughter(0,daughter(0, extraInfo(SignalProbability)))', numBest=1,
              outputVariable='FEIProbabilityRank', path=path)

path.add_module('MCMatcherParticles', listName='Upsilon(4S):DXtag', looseMCMatching=True)

buildRestOfEvent('Upsilon(4S):DXtag', roeinputs,  path=path)
appendROEMask('Upsilon(4S):DXtag', "CleanROE", "dr < 2 and abs(dz) < 4 and pt > 0.2", "[[clusterReg == 1 and E > 0.10] or [clusterReg == 2 and E > 0.09] or [clusterReg == 3 and E > 0.16]]", path=path)



#only proceed with event if a Y(4S) candidate was found 
applyEventCuts("[countInList(Upsilon(4S):DXtag) > 0]", path)



variablesToNtuple('Upsilon(4S):DXtag',
                  [
                   "m2RecoilSignalSide",
                   "foxWolframR2_maskedNaN",
                   'foxWolframR2',
		   'extraInfo(FEIProbabilityRank)',
                   "nTracks"
                   ]+  tagside_variables,
                  filename='DXtagDstl.root',
                  path=path)


### create and cut lists to only contain the finally used Hc,X,Bsig in order to label to the FSPs with them

HcAll = []
X_All = []
BtagAll = []
for part_BHc_all in parts_BHc_all:
    parid = part_BHc_all[12:]
    HcAll.append(f'{name_dict[parid]}:tag')
    X_All.append(f'X:tag{parid}')
    BtagAll.append(f'B0:{parid}DXtag')


cutAndCopyLists('B0:tag_onlyUsedOne', BtagAll, "[isDaughterOfList(Upsilon(4S):DXtag) > 0]", path=path)
cutAndCopyLists('X:XonlyUsedOne', X_All, "[isDaughterOfList(B0:tag_onlyUsedOne) > 0]", path=path)
# cannot combine all Hc's because they are different particles, sigh :/
#cutAndCopyLists('X:HcOnlyUsedOne', HcAll, "[isDaughterOfList(B0:tag_onlyUsedOne) > 0]", path=path)

cutAndCopyList('B0:sig_onlyUsedOne', "anti-B0:sigclean", "[isDaughterOfList(Upsilon(4S):DXtag) > 0]", path=path)


# these three vars indicate binary if to what category a particle got assigned by semi-inclusive Hc+X tagging
v.addAlias('basf2_X', 'isDescendantOfList(X:XonlyUsedOne)')
#v.addAlias('YYY', 'isDescendantOfList("pi0:forX")')
v.addAlias('basf2_used', 'isDescendantOfList(Upsilon(4S):DXtag)')
v.addAlias('basf2_Bsig', 'isDescendantOfList(B0:sig_onlyUsedOne)')


outvars_FSPs = ['basf2_X','basf2_used','basf2_Bsig']
#outvars_FSPs = ['isDescendantOfList(B0:sig_onlyUsedOne)']
#'countInList(X:XonlyUsedOne)','countInList(B0:tag_onlyUsedOne)',
outvars_FSPs += ['isSignal',
 'mcErrors',
 'mcPDG',
 'genMotherID',
 'genMotherP',
 'genMotherPDG']
outvars_FSPs +=  vc.kinematics 
outvars_FSPs.append("kaonID")
outvars_FSPs.append("pionID")
#outvars_FSPs += vc.mc_truth  
#outvars_FSPs += vc.mc_variables  
for i in range(10): # dont know yet if that's deep enough, 8 seemed okay at first glance
    tmp_var = "genMotherPDG({})".format(i)
    key = "genMothPDG_{}".format(i)
    v.addAlias(key,tmp_var)
    outvars_FSPs.append(key)

outvars_FSPs.append("PDG")

copyLists('pi+:out', ['pi+:forX','pi+:sig','pi+:slow'], path=path)
variablesToNtuple('pi+:out', variables=outvars_FSPs, filename="pions.root", path=path)

copyLists('K+:out', ['K+:forX','K+:sig'], path=path)
variablesToNtuple('K+:out', variables=outvars_FSPs, filename="kaons.root", path=path)

variablesToNtuple('gamma:myMinimumThresholdList', variables=outvars_FSPs, filename="gammas.root", path=path)
variablesToNtuple('e+:cande', variables=outvars_FSPs, filename="electrons.root", path=path)
variablesToNtuple('mu+:candmu', variables=outvars_FSPs, filename="muons.root", path=path)




process(path, max_event=100)
