##--Define constants--##

decay_be = 4.99E-7
decay_al = 9.83E-7

be_spallation_SLHL = 4.68
B0 = be_spallation_SLHL * 0.61 #LSDn scaling factor

al_spallation_SLHL = 30.28
A0 = al_spallation_SLHL * 0.61 #LSDn scaling factor

L0 = 160 #attenuation by spallation - balco,2017
L1 = 1500 #attenuation by negative muon capture -   balco,2017
L2 = 4200 #attenuation by fast muon-  balco,2017

L = [L0, L1, L2]

density = int(1.7)