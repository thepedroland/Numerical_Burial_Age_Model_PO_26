function out = integrand_muneg_LSD(t,c)

% Computes integrand for negative muon production using P_mu_totalLSD.m.
%
% out = integrand_muneg(t,c)
%
% t is the variable of integration (time)
% c is a structure with other needed data, including
%  c.ee erosion rate (g/cm2/yr)
%  c.l decay const(/yr)
%  c.z sample depth (g/cm2)
%  c.h atmospheric pressure (hPa)
%  c.Rc cutoff rigidity (GV)
%  c.Sphi solar modulation const
%
% specifically, computes Rmu-(z + ee*t)exp(-lt). 

thisz = c.z + c.ee.*t;

mc.Natoms = 1;
mc.sigma190 = 1;
mc.k_neg = 1;
mc.mfluxRef = c.mfluxRef;

m = P_mu_totalLSD(thisz,c.h,c.Rc,c.Sphi,mc,'yes');

out = m.R .* exp(-c.l.*t);



