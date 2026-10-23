
%%Calculating the scalling factor for samples in the Amazon
% Considering only spallation 


lat = -2.25 ;%decimal degress
z = 11 ;
pressure = stdatm(z);
Fsp = 1; %only for spallation

scaling_factor = stone2000(lat,pressure, Fsp);



