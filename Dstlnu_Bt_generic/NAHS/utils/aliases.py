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