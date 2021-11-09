import numpy as np
import pandas as pd


def isBtoDstlnu(s):
    isDecay = 0
    

    # thats the wrong way of doing it, we dont want to know if reco is correct, but if 
    # the event on gen level was D* l nu
    #if ((np.abs(s["lep_mcPDG"]) == 13.0) or (np.abs(s["lep_mcPDG"]) == 11.0)): # lepton is electron or muon
    #    if (np.abs(s["lep_motherPDG"]) == 511.0): # leptons mother is B
    #        if (np.abs(s["dau1_dau0_mcPDG"]) == 413.0): # daughter of B-sig is D*+ 
    #            isDecay = 1


    for i in range(2): # the 2 B's
        #for j in range(2): # not more than 2 B daughters necessary to check for D*lnu
        gen_Bdau_Dst_PDG = f'genUp4S_PDG_{i}_0'
        gen_Bdau_lep_PDG = f'genUp4S_PDG_{i}_1'
        if ((np.abs(s[gen_Bdau_lep_PDG]) == 13.0) or (np.abs(s[gen_Bdau_lep_PDG]) == 11.0)): # daughter 1 of B is lepton 
            if (np.abs(s[gen_Bdau_Dst_PDG]) == 413.0): # daughter 0 of B is D*+ 
                isDecay = 1
                return isDecay



    return isDecay

def whichBisSig(s):
    Bsig_genParticleID = 0

    for i in range(2): # the 2 B's
        #for j in range(2): # not more than 2 B daughters necessary to check for D*lnu
        gen_Bdau_Dst_PDG = f'genUp4S_PDG_{i}_0'
        gen_Bdau_lep_PDG = f'genUp4S_PDG_{i}_1'
        if ((np.abs(s[gen_Bdau_lep_PDG]) == 13.0) or (np.abs(s[gen_Bdau_lep_PDG]) == 11.0)): # daughter 1 of B is lepton 
            if (np.abs(s[gen_Bdau_Dst_PDG]) == 413.0): # daughter 0 of B is D*+ 
                Bsig_genParticleID = s[f'genUp4S_uniqParID_{i}']
                return Bsig_genParticleID  

    return Bsig_genParticleID


def whichBisSig_NAHS(s):
    Bsig_genParticleID = 0

    for i in range(2): # the 2 B's
        #for j in range(2): # not more than 2 B daughters necessary to check for D*lnu
        gen_Bdau_Dst_PDG = f'genUp4S_PDG_{i}_0'
        gen_Bdau_lep_PDG = f'genUp4S_PDG_{i}_1'
        gen_Bdau_nu_PDG = f'genUp4S_PDG_{i}_2'
        if ((np.abs(s[gen_Bdau_lep_PDG]) == 13.0) or (np.abs(s[gen_Bdau_lep_PDG]) == 11.0)): # daughter 1 of B is lepton 
            if ((np.abs(s[gen_Bdau_nu_PDG]) == 14.0) or (np.abs(s[gen_Bdau_nu_PDG]) == 12.0)): # daughter 2 of B is neutrino 
                if (np.abs(s[gen_Bdau_Dst_PDG]) == 413.0): # daughter 0 of B is D*+ 
                    Bsig_genParticleID = s[f'genUp4S_uniqParID_{i}']
                    return Bsig_genParticleID  

    return Bsig_genParticleID


def customMCmatching(s):
    customMC = 0

    
    for i in range(5):
        D_dau_mothPDG = 'D_dau{}_motherPDG'.format(i)
        if (np.isnan(s[D_dau_mothPDG]) == False):# and s[D_dau_mothPDG] != 0.0):
            
            if (np.abs(s[D_dau_mothPDG]) == 421.0): # D0 daughter must have genMotherPDG==421.0 (D0)
                #print("CONTINUE:",s['D_dau0_motherPDG'],s['D_dau1_motherPDG'],s['D_dau2_motherPDG'],s['D_dau3_motherPDG'],s['D_dau4_motherPDG'])
                continue
                
            else:  # if not, customMC => 0
                #if s["dau1_isSignal"]==1: 
                    #print("\n all should show abs=421.0")
                    #print("return:",s['D_dau0_motherPDG'],s['D_dau1_motherPDG'],s['D_dau2_motherPDG'],s['D_dau3_motherPDG'],s['D_dau4_motherPDG'])              
                return customMC
    #print("PASSED! D_dau_motherPDG==421.0 for B-sig isSignal:",s["dau1_isSignal"],"\n")
            
            
    for i in range(5):
        D_dau_GmothPDG = 'D_dau{}_gmotherPDG'.format(i)
        if (np.isnan(s[D_dau_GmothPDG]) == False):# and s[D_dau_GmothPDG] != 0.0):
            if (np.abs(s[D_dau_GmothPDG]) == 413.0): # D0 daughter must have grand-genMotherPDG==413.0 (D*+)
               # print("CONTINUE:",s['D_dau0_gmotherPDG'],s['D_dau1_gmotherPDG'],s['D_dau2_gmotherPDG'],s['D_dau3_gmotherPDG'],s['D_dau4_gmotherPDG'])              
                
                continue
            else:  # if not, customMC => 0
                if s["dau1_isSignal"]==1: 
                    print("\n all should show abs=413.0")
                    print("return:",s['D_dau0_gmotherPDG'],s['D_dau1_gmotherPDG'],s['D_dau2_gmotherPDG'],s['D_dau3_gmotherPDG'],s['D_dau4_gmotherPDG'])              
                return customMC
    #print("PASSED!")
                
    #for i in range(5):
    #    D_dau_GmothID = 'D_dau{}_genGmothID'.format(i)
    #    Dst_genParticleID = 'Dst_genParticleID'
    #    #print("D_dau_GmothID:",s[D_dau_GmothID], "Dst_genParticleID:",s[Dst_genParticleID])
    #    if (np.isnan(s[D_dau_GmothID]) == False):
    #        if ((np.abs(s[D_dau_GmothID]) == 3.0)): # grandmother ID has to be 3.0 = D* (Bsig first daughter)
    #            continue
    #        else:  # if not, customMC => 0
    #            return customMC
            #raise ValueError('what does correct genParticleID mean?')
            #continue
            
            
    
    #print("isBtoDstlnu:",s["isBtoDstlnu"])
    if (((s["isBtoDstlnu"]) == 1)): # last steps, decay has to be BtoDstlnu
        #print("slowPi_motherPDG:",s["slowPi_motherPDG"],"slowPi_mcPDG:",s["slowPi_mcPDG"])
        
        # slow pions mother has to be D*+ (413) and itself has to be a pion (211)
        if ((np.abs(s["slowPi_motherPDG"]) == 413.0) and (np.abs(s["slowPi_mcPDG"]) == 211.0)):
            customMC = 1
       
        elif s["dau1_isSignal"]==1: 
            print("slowPi_motherPDG:",s["slowPi_motherPDG"],"slowPi_mcPDG:",s["slowPi_mcPDG"])
    return customMC

def B_ID(s):
    label = 0
    for i in range(10):
        mcMotheri_uniqParID = "mcMother{}_uniqParID".format(i)
        if ((s[mcMotheri_uniqParID]) == 83886082.0):
            label = 83886082   
        elif ((s[mcMotheri_uniqParID]) == 83886081.0):
            label = 83886081   
    return label

def ancestor_below_B(s):
    ancestor=0 # 0: no B ancestor
    # search for B
    for i in range(10):
        genMothPDG_i = "genMothPDG_{}".format(i)
        # if B is found:
        if (np.abs(s[genMothPDG_i]) == 511.0):
            if i == 0:
                ancestor = -1 # -1: particle is directly below B
                return ancestor
            else: # take particle one generation below and return its PDG
                genMotherID_i = "genMotherID_{}".format(i - 1)
                ancestor = s[genMotherID_i]
                return ancestor

    return ancestor


def D0_decay_type(s):
    FSPs = [211.,111.,321.]
    
    # set which B is B-sig
    if s['Bsig_uniqParID'] == 83886081.0:
        i = 0
    elif s['Bsig_uniqParID'] == 83886082.0:
        i = 1

    D0_FSP_ancestors = []
    nonFSPs = []
    
    # check each D0 daughter
    for l in range(0,6): 
        D0_dau = f'genUp4S_PDG_{i}_0_0_{l}'
        
        # skip if nan
        if (np.isnan(s[D0_dau]) == True):
            continue
        
        D0_dau_absPDG = np.abs(s[D0_dau])
        
        # if daughter is gamma, pion, kaon -> save in list
        if D0_dau_absPDG in FSPs:
            D0_FSP_ancestors.append(D0_dau_absPDG)
        else:
            # not more than 3 (actually 2) intermediates possible because 5 final FSPs is max and each intermediate
            # must decay into at least 2 particles
            if l < 3:
                # if the first daughter of the non FSP does not exist it is not an intermediate
                if (np.isnan(s[f'genUp4S_PDG_{i}_0_0_{l}_0']) == True):
                    nonFSPs.append(D0_dau_absPDG)
                # check up to 6 daus of the intermediate
                for m in range(0,6): 
                    D0_grDau = f'genUp4S_PDG_{i}_0_0_{l}_{m}'
                    if (np.isnan(s[D0_grDau]) == True):
                        continue
                    D0_grDau_absPDG = np.abs(s[D0_grDau])
                    if D0_grDau_absPDG in FSPs:
                        D0_FSP_ancestors.append(D0_grDau_absPDG)
                    else:
                        nonFSPs.append(D0_grDau_absPDG)
            # as described above only the first 3 (actually 2) can be intermediates
            else:
                nonFSPs.append(D0_dau_absPDG)
                
    D0_FSP_ancestors.sort(reverse=True)    
    
    if len(nonFSPs) == 0:
        if D0_FSP_ancestors == [321.,211.]:
            D0_decay = "Kpi"
        elif D0_FSP_ancestors == [321.,211.,211.,211.]:
            D0_decay = "Kpipipi"
        elif D0_FSP_ancestors == [321.,211.,111.]:
            D0_decay = "Kpipi0"
        elif D0_FSP_ancestors == [321.,211.,211.,211.,111.]:
            D0_decay = "Kpipipipi0"
        else:
            D0_decay = "notWanted"
    else:
        D0_decay = "notWanted" 
    
    
    #print("event:",s["__event__"])            
    #print("Bsig_uniqParID:",s['Bsig_uniqParID'])            
    #print("D0_FSP_ancestors:",D0_FSP_ancestors)
    #print("len(nonFSPs):",len(nonFSPs))
    #print("D0_decay:",D0_decay)
    #print('\n')
    return D0_decay