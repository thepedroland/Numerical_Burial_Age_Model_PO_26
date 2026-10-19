function out = integrand_mufast_LSD(t,c)

% Computes integrand for fast muon production using P_mu_total.m.
%
% out = integrand_muneg(t,c)
%
% t is the variable of integration (time)
% c is a structure with other needed data, including
%  c.ee erosion rate (g/cm2/yr)
%  c.l decay const(/yr)
%  c.z sample depth (g/cm2)
%  c.h atmospheric pressure (hPa)
%
% specifically, computes beta(z + ee*t) * phi(z + ee*t) * Ebar(z + ee.*t).^alpha * exp(-lt). 

thisz = c.z + c.ee.*t;

mc.Natoms = 1;
mc.sigma190 = 1;
mc.k_neg = 1;
mc.mfluxRef = c.mfluxRef;

m = P_mu_totalLSD(thisz,c.h,c.Rc,c.Sphi,mc,'yes');

out = m.Beta .* m.phi .* (m.Ebar.^1) .* exp(-c.l.*t);

