def define_aliases_Bsig():
    alias_dict ={}


    alias_dict['lep_genMotherID'] = 'daughter(1 ,genMotherID)'
    alias_dict['lep_genMotherPDG'] = 'daughter(1 ,genMotherPDG)'
    alias_dict['lep_mcPDG'] = 'daughter(1 ,mcPDG)'
    alias_dict['lep_PDG'] = 'daughter(1 ,PDG)'
    alias_dict['lep_isSignal'] = 'daughter(1 ,isSignal)'
    alias_dict['lep_motherUniqParID'] = 'daughter(1 ,mcMother(uniqueParticleIdentifier))'
    alias_dict['lep_uniqParID'] = 'daughter(1 ,uniqueParticleIdentifier)'
    
    
    alias_dict['Bsig_genMotherID'] = 'genMotherID'
    alias_dict['Bsig_genMotherPDG'] = 'genMotherPDG'
    alias_dict['Bsig_mcPDG'] = 'mcPDG'
    alias_dict['Bsig_PDG'] = 'PDG'
    alias_dict['Bsig_isSignal'] = 'isSignal'
    alias_dict['Bsig_motherUniqParID'] = 'mcMother(uniqueParticleIdentifier)'
    alias_dict['basf2Bsig_uniqParID'] = 'uniqueParticleIdentifier'
    alias_dict['Bsig_genParticleID'] = 'genParticleID'
     
    for i in range(0,2): # B level
        alias_dict[f'genUp4S_uniqParID_{i}'] = f'genUpsilon4S(mcDaughter({i}, uniqueParticleIdentifier))'

        for j in range(0,4): # D* l nu + 1 level
            alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
            alias_dict[f'abs_genUp4S_PDG_{i}_{j}'] = f'abs(genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG))))'
            alias_dict[f'genUp4S_uniqParID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},uniqueParticleIdentifier)))'
            if j == 0:
                for k in range(0,3): # D0 pi +1 level
                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},uniqueParticleIdentifier))))'
                    if k == 0: # D0 daughters
                        for l in range(0,6): 
                            alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},PDG)))))'
                            alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},uniqueParticleIdentifier)))))'
                            if l < 3:
                                for m in range(0,6): 
                                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},PDG))))))'
                                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},uniqueParticleIdentifier))))))'
    
    for i in range(0,2):
          for j in range(0,3):
              alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
              alias_dict[f'genUp4S_mdstIndex_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mdstIndex)))'
              alias_dict[f'genUp4S_genParticleID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},genParticleID)))'
              alias_dict[f'genUp4S_uniqParID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},uniqueParticleIdentifier)))'
              if j == 0:
                for k in range(0,2):
                   alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                   alias_dict[f'genUp4S_mdstIndex_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mdstIndex))))'
                   alias_dict[f'genUp4S_genParticleID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},genParticleID))))'
                   alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},uniqueParticleIdentifier))))'
    
    
    return(alias_dict)


def define_aliases_Upsilon4S():
    alias_dict ={}
#uniqueParticleIdentifier uniqParID




    alias_dict['dau1_sigProb'] = 'daughter(1,extraInfo(SignalProbability))'
    
    
    
    
    
    alias_dict['Up4S_isSig'] = 'isSignalAcceptMissingNeutrino'
    #alias_dict['Up4S_isSignalMissingNeutrino'] = 'isSignalAcceptMissingNeutrino'
    alias_dict['BeamE'] = 'beamE'
    alias_dict['BeamPx'] = 'beamPx'
    alias_dict['BeamPy'] = 'beamPy'
    alias_dict['BeamPz'] = 'beamPz'
    alias_dict['BeamcmsE'] = 'useCMSFrame(beamE)'
    alias_dict['BeamcmsPx'] = 'useCMSFrame(beamPx)'
    alias_dict['BeamcmsPy'] = 'useCMSFrame(beamPy)'
    alias_dict['BeamcmsPz'] = 'useCMSFrame(beamPz)'
    for i in range(0,2): # B level
        alias_dict[f'genUp4S_uniqParID_{i}'] = f'genUpsilon4S(mcDaughter({i}, uniqueParticleIdentifier))'

        for j in range(0,4): # D* l nu + 1 level
            alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
            alias_dict[f'abs_genUp4S_PDG_{i}_{j}'] = f'abs(genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG))))'
            alias_dict[f'genUp4S_uniqParID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},uniqueParticleIdentifier)))'
            if j == 0:
                for k in range(0,3): # D0 pi +1 level
                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},uniqueParticleIdentifier))))'
                    if k == 0: # D0 daughters
                        for l in range(0,6): 
                            alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},PDG)))))'
                            alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},uniqueParticleIdentifier)))))'
                            if l < 3:
                                for m in range(0,6): 
                                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},PDG))))))'
                                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},uniqueParticleIdentifier))))))'
 
    
    
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
          alias_dict[f'genUp4S_uniqParID_{i}'] = f'genUpsilon4S(mcDaughter({i}, uniqueParticleIdentifier))'

          for j in range(0,3):
              alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
              alias_dict[f'genUp4S_mdstIndex_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mdstIndex)))'
              alias_dict[f'genUp4S_genParticleID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},genParticleID)))'
              alias_dict[f'genUp4S_uniqParID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},uniqueParticleIdentifier)))'
              if j == 0:
                for k in range(0,2):
                   alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                   alias_dict[f'genUp4S_mdstIndex_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mdstIndex))))'
                   alias_dict[f'genUp4S_genParticleID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},genParticleID))))'
                   alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},uniqueParticleIdentifier))))'
    for i in range(0,1):
      alias_dict['Btag_uniqParID'.format(i)]= 'daughter({}, uniqueParticleIdentifier)'.format(i)
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
      alias_dict['dau{}_isSignal'.format(i)]= 'daughter({},isSignalAcceptMissingNeutrino)'.format(i)
      alias_dict['dau{}_R2'.format(i)]= 'daughter({},R2)'.format(i)
      alias_dict['dau{}_cosTBTO'.format(i)]= 'daughter({},cosTBTO)'.format(i) 
      alias_dict['dau{}_cosThetaBetweenParticleAndNominalB'.format(i)]= 'daughter({},cosThetaBetweenParticleAndNominalB)'.format(i)
      alias_dict['dau{}_PDG'.format(i)]= 'daughter({},PDG)'.format(i)
      alias_dict['dau{}_motherPDG'.format(i)]= 'daughter({},genMotherPDG)'.format(i)
    for i in range(1,2):
      alias_dict['Bsig_uniqParID'.format(i)]= 'daughter({}, uniqueParticleIdentifier)'.format(i)
      #alias_dict['dau{}_Nelectrons'.format(i)]= 'daughter({},nROE_Charged(cleanMask,11))'.format(i)
      #alias_dict['dau{}_Nmuons'.format(i)]= 'daughter({},nROE_Charged(cleanMask,13))'.format(i)
      #alias_dict['dau{}_Npip'.format(i)]= 'daughter({},nROE_Charged(cleanMask,211))'.format(i)
      #alias_dict['dau{}_NKp'.format(i)]= 'daughter({},nROE_Charged(cleanMask,321))'.format(i)
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
      alias_dict['lep_PDG']= 'daughter(1,daughter({},PDG))'.format(i)
      alias_dict['lep_genParticleID']= 'daughter(1,daughter({},genParticleID))'.format(i)
      alias_dict['lep_motherPDG']= 'daughter(1,daughter({},genMotherPDG))'.format(i)
      alias_dict['lep_gmotherPDG']= 'daughter(1,daughter({},genMotherPDG(1)))'.format(i)
      alias_dict['lep_genmotherID']= 'daughter(1,daughter({},genMotherID))'.format(i)
      alias_dict['lep_mothermdstIndex']= 'daughter(1,daughter({},mcMother(mdstIndex)))'.format(i)
      alias_dict['lep_uniqParID']= 'daughter(1,daughter({},uniqueParticleIdentifier))'.format(i)
      alias_dict['lepMother_uniqParID']= 'daughter(1,daughter({},mcMother(uniqueParticleIdentifier)))'.format(i)
    
    for i in range(5):  
      alias_dict['D_dau{}_genGmothID'.format(i)] = 'daughter(1,daughter(0,daughter(0,daughter({}, genMotherID(1)))))'.format(i)
      alias_dict['D_dau{}_motherPDG'.format(i)] = 'daughter(1,daughter(0,daughter(0,daughter({},genMotherPDG))))'.format(i)
      alias_dict['D_dau{}_gmotherPDG'.format(i)] = 'daughter(1,daughter(0,daughter(0,daughter({},genMotherPDG(1)))))'.format(i)
      alias_dict['D_dau{}_mcPDG'.format(i)] = 'daughter(1,daughter(0,daughter(0,daughter({},mcPDG))))'.format(i)
    
    #alias_dict['slowPi_genParticleID'] = 'daughter(1,daughter(0,daughter(1,genParticleID)))'
    alias_dict['slowPi_motherPDG'] = 'daughter(1,daughter(0,daughter(1,genMotherPDG)))'
    #alias_dict['slowPi_gmotherPDG'] = 'daughter(1,daughter(0,daughter(1,genMotherPDG(1))))'
    alias_dict['slowPi_mcPDG'] = 'daughter(1,daughter(0,daughter(1,mcPDG)))'
    alias_dict['Dst_genParticleID'] = 'daughter(1,daughter(0,genParticleID))'

    alias_dict['Hc_isSignalAcceptMissingGamma']= 'daughter(0, daughter(0, isSignalAcceptMissingGamma))'
    alias_dict['Hc_genMotherPDG']= 'daughter(0, daughter(0, genMotherPDG))'
    alias_dict['Hc_mcPDG']= 'daughter(0, daughter(0, mcPDG))'
    alias_dict['Hc_uniqParID']= 'daughter(0, daughter(0, uniqueParticleIdentifier))'
    alias_dict['Hc_genMotherID']= 'daughter(0, daughter(0, genMotherID))'
    alias_dict['Hc_motherUniqParID']= 'daughter(0, daughter(0, mcMother(uniqueParticleIdentifier)))'
      


    alias_dict['D_nDaughters'] = 'daughter(1,daughter(0,daughter(0,nDaughters)))'
    alias_dict['D_M'] = 'daughter(1,daughter(0,daughter(0,M)))'
    alias_dict['D_p'] = 'daughter(1,daughter(0,daughter(0,p)))'
    alias_dict['D_pt'] = 'daughter(1,daughter(0,daughter(0,pt)))'
    alias_dict['D_cmp'] = 'daughter(1,daughter(0,daughter(0,useCMSFrame(p))))'
    alias_dict['D_cmpt'] = 'daughter(1,daughter(0,daughter(0,useCMSFrame(pt))))'
    alias_dict['D_isSignal'] = 'daughter(1,daughter(0,daughter(0,isSignal)))'
    alias_dict['D_uniqParID'] = 'daughter(1,daughter(0,daughter(0,uniqueParticleIdentifier)))'
    alias_dict['D_decayModeID'] = 'daughter(1,daughter(0,daughter(0,extraInfo(decayModeID))))'

    
    alias_dict['Dst_uniqParID'] = 'daughter(1,daughter(0,uniqueParticleIdentifier))'    
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


def define_aliases_Hc():
    alias_dict ={}
    for i in range(0,2): # B level
        alias_dict[f'genUp4S_uniqParID_{i}'] = f'genUpsilon4S(mcDaughter({i}, uniqueParticleIdentifier))'

        for j in range(0,4): # D* l nu + 1 level
            alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
            alias_dict[f'abs_genUp4S_PDG_{i}_{j}'] = f'abs(genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG))))'
            alias_dict[f'genUp4S_uniqParID_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},uniqueParticleIdentifier)))'
            if j == 0:
                for k in range(0,3): # D0 pi +1 level
                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},PDG))))'
                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},uniqueParticleIdentifier))))'
                    if k == 0: # D0 daughters
                        for l in range(0,6): 
                            alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},PDG)))))'
                            alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},uniqueParticleIdentifier)))))'
                            if l < 3:
                                for m in range(0,6): 
                                    alias_dict[f'genUp4S_PDG_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},PDG))))))'
                                    alias_dict[f'genUp4S_uniqParID_{i}_{j}_{k}_{l}_{m}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},mcDaughter({k},mcDaughter({l},mcDaughter({m},uniqueParticleIdentifier))))))'
                                
    alias_dict['BeamE'] = 'beamE'
    alias_dict['BeamPx'] = 'beamPx'
    alias_dict['BeamPy'] = 'beamPy'
    alias_dict['BeamPz'] = 'beamPz'
    alias_dict['BeamcmsE'] = 'useCMSFrame(beamE)'
    alias_dict['BeamcmsPx'] = 'useCMSFrame(beamPx)'
    alias_dict['BeamcmsPy'] = 'useCMSFrame(beamPy)'
    alias_dict['BeamcmsPz'] = 'useCMSFrame(beamPz)'


    for i in range(1): # dont know yet if that's deep enough, 8 seemed okay at first glance
        tmp_var = "genMotherPDG({})".format(i)
        key = "genMothPDG_{}".format(i)
        alias_dict[key] = tmp_var


    for i in range(1): # dont know yet if that's deep enough, 8 seemed okay at first glance
        start = "mcMother("
        tmp_var = start
        for j in range(i):
            tmp_var += start
        tmp_var += "uniqueParticleIdentifier"
        for j in range(i+1):
            tmp_var += ")"   
        key = "mcMother{}_uniqParID".format(i)
        alias_dict[key] = tmp_var

    for name in ["px","py","pz","E"]:
        tmp_var = "useCMSFrame({})".format(name)
        key = "cm{}".format(name)        
        alias_dict[key] = tmp_var


        
    return alias_dict

def define_aliases_FSPs():
    alias_dict ={}

    for i in range(10): # dont know yet if that's deep enough, 8 seemed okay at first glance
        tmp_var = "genMotherPDG({})".format(i)
        key = "genMothPDG_{}".format(i)
        alias_dict[key] = tmp_var

        
    for i in range(10): 
        tmp_var = "genMotherID({})".format(i)
        key = "genMotherID_{}".format(i)
        alias_dict[key] = tmp_var


    for i in range(10): # dont know yet if that's deep enough, 8 seemed okay at first glance
        start = "mcMother("
        tmp_var = start
        for j in range(i):
            tmp_var += start
        tmp_var += "uniqueParticleIdentifier"
        for j in range(i+1):
            tmp_var += ")"   
        key = "mcMother{}_uniqParID".format(i)
        alias_dict[key] = tmp_var

    for name in ["px","py","pz","E"]:
        tmp_var = "useCMSFrame({})".format(name)
        key = "cm{}".format(name)        
        alias_dict[key] = tmp_var


    
    return alias_dict