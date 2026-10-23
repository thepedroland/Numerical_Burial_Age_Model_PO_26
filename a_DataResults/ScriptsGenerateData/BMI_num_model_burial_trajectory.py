import numpy as np
from z_AuxDataScripts.aux_scripts import *
from z_AuxDataScripts.aux_scripts import models_constants as constants

c_p=cosmo_production()

class deposition_trajectories():
    def __init__(self,measured_n10,measured_n26,stn_dev_n10,measured_std_dev_n26):

        self.measured_n10 = measured_n10
        self.measured_n26 = measured_n26
        self.measured_std_dev_n10 = stn_dev_n10
        self.measured_std_dev_n26 = measured_std_dev_n26
        
        self.decay_be = constants.decay_be
        self.decay_al = constants.decay_al

    def setup_model(self,arguments):

        self.profile_depths = []
        self.profile_times= []

        self.n10_series = []
        self.n26_series = []
        self.ratio_series = []

        self.Rc_series = []

        self.initial_n10 = arguments["initial_n10"]
        self.ratio = arguments["initial_ratio"]
        self.burial_depth = arguments["burial_depth"]
        self.sample_id = arguments["sample_id"]
        self.reference_sample = arguments["reference_sample"]
        self.time_burial = arguments["time_burial"]
        self.deposition_rate = np.round(arguments["depo_rate"],10)
        self.final_depth = np.round(arguments["final_depth"], 10)
        self.erosion_rate = np.round(arguments["erosion_rate"], 10)
        self.density = arguments["density"]
        self.time_erosion = np.round(arguments["time_erosion"])

        self.n26 = self.ratio * self.initial_n10
        self.n10 = self.initial_n10

        lines_model = steady_state_model()
        self.lines_between = lines_model.plot_steady_state_model(Rc_value='min', checking_only=True)

    def check_simple_exposure_region(self):
        if not check_simple_exposure_region(self.initial_n10,self.ratio,self.lines_between):
            # print("REJECTED invalid exposure region:",self.n10,self.n26,(self.n26/self.n10))
            return "REJECTED BY EXPOSURE REGION"

        if ((self.deposition_rate*self.time_burial) < self.burial_depth) and (self.time_burial > 0):
            # print(self.depth,self.deposition_rate*self.time_burial)
            # print("Rejecting simulation, invalid deposition rate:",self.deposition_rate)
            return "REJECTED BY DEPOSITION RATE"

        if (self.erosion_rate*self.time_erosion) < (self.burial_depth-self.final_depth):
            # print(self.depth,self.deposition_rate*self.time_burial)
            # print("Rejecting simulation, invalid erosion rate:",self.erosion_rate)
            return "REJECTED BY EROSION RATE"

    def run_model(self):
        self.n10_series.append(self.n10)
        self.n26_series.append(self.n26)

        self.ratio_series.append(self.n26/self.n10)

        dt = 10000

        n_burial = int(round(self.time_burial / dt))
        n_erosion = int(round(self.time_erosion / dt))

        self.sed_accum = (self.deposition_rate) * dt
        self.ero_thickness = (self.erosion_rate) * dt

        if self.reference_sample !="Surface":
            self.current_depth = self.burial_depth
        else:
            self.current_depth = 0  # 0cm initial

        total_t = self.time_burial + self.time_erosion

        self.profile_times = []
        self.profile_depths = []

        for _ in range(n_burial):
            if self.current_depth < self.burial_depth:
                self.current_depth += self.sed_accum
                if self.current_depth > self.burial_depth:
                    self.current_depth = self.burial_depth
            total_t -= dt
            self.profile_times.append(total_t)
            self.profile_depths.append(self.current_depth)

        for _ in range(n_erosion):
            if self.current_depth > self.final_depth:
                self.current_depth -= self.ero_thickness
                if self.current_depth < self.final_depth:
                    self.current_depth = self.final_depth
            total_t -= dt
            self.profile_times.append(total_t)
            self.profile_depths.append(self.current_depth)

        self.data_prod_be, self.data_prod_al,Rc_time = c_p.LSDn_var_production_nuclides(self.profile_times,Rc_value="free",z_cm_list=self.profile_depths)

        for prod_total_al,prod_total_be in zip(self.data_prod_al[0],self.data_prod_be[0]):

            ##Where the concentration changes
            self.n10 = c_p.concentration_nuclide(prod_total_be, dt, self.n10, self.decay_be)
            self.n26 = c_p.concentration_nuclide(prod_total_al, dt, self.n26, self.decay_al)

            self.n10_series.append(self.n10)
            self.n26_series.append(self.n26)

            self.ratio_series.append(self.n26/self.n10)

        x0 = self.measured_n10
        y0 = self.measured_n26 / self.measured_n10

        # 2. Define the 1-sigma uncertainties
        sig_x = self.measured_std_dev_n10
        sig_y = y0 * np.sqrt((self.measured_std_dev_n26 / self.measured_n26) ** 2 +
                             (self.measured_std_dev_n10 / self.measured_n10) ** 2)

        current_x = self.n10_series[-1]
        current_y = self.ratio_series[-1]
        dist_sq = ((current_x - x0) ** 2 / sig_x ** 2) + ((current_y - y0) ** 2 / sig_y ** 2)

        if dist_sq <= 4 and self.time_burial + self.time_erosion >= dt:
            self.solution=True
        else :
            self.solution=False

        results_data_csv = {
            "Solution":self.solution,
            "Deposition rate [cm/year]":self.deposition_rate,
            "Erosion rate [cm/year]":self.erosion_rate,
            "Initial N10":self.initial_n10,
            "Initial ratio":self.ratio,
            "Burial Depth [cm]": self.burial_depth,
            "Final Depth [cm]": self.final_depth,
            "Final 2-Sigma N10": current_x,
            "Final 2-Sigma Ratio": current_y,
            "Burial Time [Ma]": (self.time_burial / 1e6),
            "Erosion Time [Ma]": (self.time_erosion / 1e6),
            "Total Time [Ma]": ((self.time_burial + self.time_erosion) / 1e6),
        }

        trajectory_data_pkl = {
            "N10 series": np.array(self.n10_series),
            "Ratio series": np.array(self.ratio_series),
            "Depth series": np.array(self.profile_depths)
        }
        return results_data_csv, trajectory_data_pkl