import sys
import ROOT
import functions

ROOT.DisableImplicitMT()

def get_list_of_stable_particles_from_decay(idx, mc_particles, daughters):

    ret = []

    if idx < 0 or idx >= len(mc_particles):
        return ret

    db = mc_particles[idx].daughters_begin
    de = mc_particles[idx].daughters_end

    if db != de: # particle is unstable                                                                                                                  
        for id_ in range(db, de):
            idaughter = daughters[id_].index;
            rr = get_list_of_stable_particles_from_decay(idaughter, mc_particles, daughters)
            ret += rr
    else: # particle is stable                                                                                                                           
        ret.append(idx)
        return ret

    return ret

def get_list_of_particles_from_decay(idx, mc_particles, daughters):

    ret = []

    if idx < 0 or idx >= len(mc_particles):
        return ret

    db = mc_particles[idx].daughters_begin
    de = mc_particles[idx].daughters_end

    if db == de: # particle is stable                                                                                                                    
        return ret

    for idaughter in range(db, de):
        ret.append(daughters[idaughter].index)

    return ret

def run_analysis(dIn):
    ch = ROOT.TChain("events")
    for f in functions.findROOTFiles(dIn):
        ch.Add(f)

    for iEv in range(0, ch.GetEntries()):
        ch.GetEntry(iEv)
        print(f"************* {iEv}")

        mc_particles = getattr(ch, "Particle")
        parents = getattr(ch, "Particle#0")
        daughters = getattr(ch, "Particle#1")

        mc_particles_stable = []
        for k in range(len(mc_particles)):
            if mc_particles[k].generatorStatus == 1:
                mc_particles_stable.append(mc_particles[k])

        print(len(reco_particles), len(mc_particles), len(mc_particles_stable))

        ## example: get the Higgs daughters
        higgs_idx = -1
        for iP, mc_p in enumerate(mc_particles): # This part gets the index of the Higgs                                                                 
            if mc_p.PDG != 25:
                continue
            higgs_idx = iP
            break

        # Done(Lines 76-81): find the Z boson resulting from the Higgs
        
        Z_from_Higgs = -1
        
        for k in range(mc_particles[higgs_idx].daughters_begin, mc_particles[higgs_idx].daughters_end): 
            if mc_particles[enumerate(mc_particles[k])].PDG == 23:
                print("Found Z boson")
                Z_from_Higgs = mc_particles[mc_particles[k].subentry]
        print(Z_from_Higgs)
                
                
        # Done(Lines 84-87): find the decay products of the Z resulting from the Higgs
        
        Higgs_Decay_Products = []
        
        for k in range(mc_particles[Z_from_Higgs].daughters_begin, mc_particles[Z_from_Higgs].daughters_end):
            Higgs_Decay_Products.append(enumerate(mc_particles[mc_particles[k]]))
            print("made it here")
        print(Higgs_Decay_Products)

        # Done(Lines 93-97): show that you have successfully found the decay product of the Higgs
        
        Energy_sum = 0.0
        
        #h = ROOT.TH1F()
        #g = ROOT.TH1F()
        
        for decay_product in Higgs_Decay_Products:
            #h.Fill(<mass of supposed Z particle>)
            #g.Fill(<energy of supposed Z particle>)
            Energy_sum = Energy_sum + decay_product.E
            return Energy_sum == Z_from_Higgs.E
        print(Energy_sum)
            
        #c1 = ROOT.TCanvas()
        #h.Draw()
        #c1.SaveAs('some_file_name_1.png')
        #c2 = ROOT.TCanvas()
        #g.Draw()
        #c2.SaveAs('some_file_name_2.png')
            
            
        

if __name__ == "__main__":
    sample = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_qqH_HZa_ecm240/" # TODO                                                 
    # TODO: Also, instead of opening a single sample, open ALL samples needed for your analysis                                                          
    run_analysis(sample)
