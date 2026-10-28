decay_be = 4.99E-7
decay_al = 9.83E-7

be_spallation_SLHL = 4.68 # Code in Balco,2017
B0 = be_spallation_SLHL * 0.61 #LSDn scaling factor calculate from z_AuxDataScripts/aux_functions/mat_codes/calc_spallation_scaling_factor.m

al_spallation_SLHL = 30.28 # Code in Balco,2017
A0 = al_spallation_SLHL * 0.61 #LSDn scaling factor calculated from z_AuxDataScripts/aux_functions/mat_codes/calc_spallation_scaling_factor.m

L0 = 160 #attenuation by spallation - Balco,2017
L1 = 1500 #attenuation by negative muon capture - Balco,2017
L2 = 4200 #attenuation by fast muon- Balco,2017

L = [L0, L1, L2]

density = 1.7 #g/cm^3 - EMBRAPA Solos Database check z_AuxDataScripts/data/SM_profiles_Amazon.html