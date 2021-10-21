def define_aliases_Hc():
    alias_dict ={}
    for i in range(0,2):
        for j in range(0,3):
            alias_dict[f'genUp4S_PDG_{i}_{j}'] = f'genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG)))'
            alias_dict[f'abs_genUp4S_PDG_{i}_{j}'] = f'abs(genUpsilon4S(mcDaughter({i}, mcDaughter({j},PDG))))'

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