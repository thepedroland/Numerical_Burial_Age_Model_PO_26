#----Import modules----#
import math
import numpy as np
import matlab.engine
import os
from support.aux_functions import models_constants as constants

## Calculation of nuclide production and concentration over time
class cosmo_production:

    def __init__(self):
        for key, value in vars(constants).items():
            setattr(self, key, value)

        path_add = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"aux_functions","mat_codes")
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(path_add)

    def _to_flat_list(self,x):
        if isinstance(x, (int, float)):
            return [float(x)]
        return np.array(x, dtype=float).flatten().tolist()

    def LSDn_var_production_nuclides(self, time_list, Rc_value, z_cm_list):

        z_gcm2_list = []
        p_al_spa_list = []
        p_be_spa_list = []

        for z_cm in z_cm_list:
            # Sample depth in g/cm^2
            print(self.density)
            z_gcm2_list.append(z_cm * self.density)  # assuming z is in cm

            # Al and Be production by spallation
            p_al_spa_list.append(self.A0 * math.exp(-z_cm * self.density / self.L0))
            p_be_spa_list.append(self.B0 * math.exp(-z_cm * self.density / self.L0))

        # Be production by muons
        P_neg_muons_be, P_fast_muons_be = self.eng.LSDn_calc_muon_prod(
            matlab.double(time_list), matlab.double(z_gcm2_list),
            str('be'), str(Rc_value), nargout=2
        )
        P_neg_muons_be_list = self._to_flat_list(P_neg_muons_be)
        P_fast_muons_be_list = self._to_flat_list(P_fast_muons_be)

        # Al production by muons
        P_neg_muons_al, P_fast_muons_al = self.eng.LSDn_calc_muon_prod(
            matlab.double(time_list), matlab.double(z_gcm2_list),
            str('al'), str(Rc_value), nargout=2
        )
        P_neg_muons_al_list = self._to_flat_list(P_neg_muons_al)
        P_fast_muons_al_list = self._to_flat_list(P_fast_muons_al)

        # Elementwise totals (NOT list concatenation)
        prod_total_be_list = [
            n + f + s for n, f, s in zip(P_neg_muons_be_list, P_fast_muons_be_list, p_be_spa_list)
        ]
        prod_total_al_list = [
            n + f + s for n, f, s in zip(P_neg_muons_al_list, P_fast_muons_al_list, p_al_spa_list)
        ]

        return ((prod_total_be_list, p_be_spa_list, P_neg_muons_be_list, P_fast_muons_be_list),
                (prod_total_al_list, p_al_spa_list, P_neg_muons_al_list, P_fast_muons_al_list), 0)

    # Calculate nuclide concentration
    def concentration_nuclide(self, prod_total: float, dt: float, N_initial: float, decay: float) -> float:
        initial_n_decay = N_initial * np.exp(-dt * decay)
        prod_and_prod_decay = (prod_total / decay) * (1 - np.exp(-dt * decay))

        # N_initial in at/g, prod_total in at/yr/g, time in yr, tau in yr
        final_concentration = initial_n_decay + prod_and_prod_decay

        return final_concentration

    ##--Functions to calcute exposure zones
    def constant_exposure_be(self,time,Rc_value='free',z_cm=0.0):
        if time == 0:
            self.data_prod_0_be,_,Rc = self.LSDn_var_production_nuclides([0],Rc_value=Rc_value,z_cm_list=[z_cm])

        prod_be_list = [self.data_prod_0_be[1],self.data_prod_0_be[2],self.data_prod_0_be[3]]
        prod_be = 0.0
        for prod_rate in prod_be_list:
            result_be = ((prod_rate[0]) / self.decay_be) * (1- (math.exp(-time * self.decay_be)))
            # prod_rate in at/yr/g, decay_be in yr^-1, result_be in at/g
            prod_be += result_be

        return prod_be

    def constant_exposure_al(self, time,Rc_value='free',z_cm=0.0):
        if time == 0:
            _, self.data_prod_0_al,Rc = self.LSDn_var_production_nuclides([0],Rc_value=Rc_value,z_cm_list=[z_cm])

        prod_al_list = [self.data_prod_0_al[1], self.data_prod_0_al[2],self.data_prod_0_al[3]]
        prod_al = 0.0
        for prod_rate in prod_al_list:
            result_al = (prod_rate[0] / self.decay_al) *  (1-(math.exp(-time * self.decay_al)))
            # prod_rate in at/yr/g, decay_be in yr^-1, result_be in at/g
            prod_al += result_al
        return  prod_al

    def steady_erosion_be(self,erosion):
        
        prod_be_list = [self.data_prod_0_be[1], self.data_prod_0_be[2],self.data_prod_0_be[3]]
        prod_be = 0.0

        for prod_rate,attenuation_length in zip(prod_be_list,self.L):
            effective_lambda = (erosion * self.density / attenuation_length) + self.decay_be
            result_be = (prod_rate[0] / effective_lambda) #dunai book,93
            prod_be += result_be

        return prod_be

    def steady_erosion_al(self, erosion):
        prod_al_list = [self.data_prod_0_al[1], self.data_prod_0_al[2],self.data_prod_0_al[3]]
        prod_al = 0.0

        for prod_rate, attenuation_length in zip(prod_al_list, self.L):
            effective_lambda = (erosion * self.density / attenuation_length) + self.decay_al
            result_al = (prod_rate[0] / effective_lambda)
            prod_al += result_al

        return prod_al

    def burial_lines_be(self,erosion,time):
        prod_be_list = [self.data_prod_0_be[1], self.data_prod_0_be[2],self.data_prod_0_be[3]]

        prod_be = 0.0

        for prod_rate,attenuation_length in zip(prod_be_list,self.L):
            effective_lambda = (erosion * self.density / attenuation_length) + self.decay_be
            result_be = (prod_rate[0] / effective_lambda) *  (math.exp(-time * self.decay_be))
            prod_be += result_be

        return prod_be

    def burial_lines_al(self, erosion,time):

        prod_al_list = [self.data_prod_0_al[1], self.data_prod_0_al[2],self.data_prod_0_al[3]]
        prod_al = 0.0

        for prod_rate, attenuation_length in zip(prod_al_list, self.L):

            effective_lambda = (erosion * self.density / attenuation_length) + self.decay_al
            result_al = (prod_rate[0] / effective_lambda) *  (math.exp(-time * self.decay_al))
            prod_al += result_al

        return prod_al
