import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import matplotlib.pyplot as plt
from support.aux_functions.nuclide_prod_concentration import cosmo_production

class burial_exposure_model:
    def __init__(self):
        pass

    def plot_steady_state_model(self,scaling_method,Rc_value,checking_only=False):
        import matplotlib.pyplot as plt

        c_p = cosmo_production()

        color_fill = [246, 228, 172]

        color_fill= tuple(x / 255.0 for x in color_fill)

        N_be_series = []
        N_al_series = []
        N_be_series_time = []
        N_al_series_time = []

        import numpy as np

        points_per_line = 50000
        many_times = np.concatenate(([0], np.logspace(0, 8, points_per_line - 1)))
        many_erosions = np.concatenate(([0], np.logspace(-2, 8, points_per_line - 1))) /1e4

        for time in many_times:
            N_be = float(c_p.constant_exposure_be(time,scaling_method,Rc_value))
            N_al = float(c_p.constant_exposure_al(time,scaling_method,Rc_value))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            N_al_series_time.append(N_al)
            N_be_series_time.append(N_be)

        plt.fill_between(N_be_series, np.array(N_al_series_time) / np.array(N_be_series_time), 8, color='white', alpha=0.5,linewidth=0)

        plt.xscale('log')

        for er in many_erosions:
            N_be = float(c_p.steady_erosion_be(er))
            N_al = float(c_p.steady_erosion_al(er))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

        if checking_only:
            return N_be_series, np.array(N_al_series) / np.array(N_be_series)

        plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color=color_fill, alpha=0.5, linewidth=0)
        plt.xscale('log')

        line_times = [1e6, 5e5]
        labels = ["1Ma", "0.5Ma"]

        for time, label in zip(line_times, labels):
            N_be_series_line_times = []
            N_al_series_line_times = []

            for er in many_erosions:
                N_be = float(c_p.burial_lines_be(er,time))
                N_al = float(c_p.burial_lines_al(er,time))

                N_be_series_line_times.append(N_be)
                N_al_series_line_times.append(N_al)

            plt.plot(N_be_series_line_times, np.array(N_al_series_line_times) / np.array(N_be_series_line_times),
                     alpha=0.5, color="#F1C49D",
                     label=label,linewidth=0.3)
            plt.xscale('log')
            plt.annotate(labels[0],
                         xy=(7e4, 3.9),
                         xytext=(5, 5),  # The offset distance in points
                         textcoords='offset points',
                         xycoords='data',
                         fontsize=10,backgroundcolor="#FAF4EF",
                         c="#F1C49D")
            plt.annotate(labels[1],
                         xy=(7e4, 5.05),
                         xytext=(5, 5),  # The offset distance in points
                         textcoords='offset points',
                         xycoords='data',c="#F1C49D",
                         fontsize=10,
                         backgroundcolor="#FAF4EF")

###---------###
    def plot_steady_state_model_depth(self,z_cm,color):

        c_p = cosmo_production()

        N_be_series = []
        N_al_series = []
        N_be_series_time = []
        N_al_series_time = []
        N_be_series_erosion = []
        N_al_series_erosion = []

        import numpy as np

        points_per_line = 50000  # example, set your value
        many_times = np.concatenate(([0], np.logspace(0, 8, points_per_line - 1)))
        many_erosions = np.concatenate(([0], np.logspace(-2, 6, points_per_line - 1))) / 1e4

        for time in many_times:
            N_be = float(c_p.constant_exposure_be(time,"mean",z_cm))
            N_al = float(c_p.constant_exposure_al(time,"mean",z_cm))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            N_al_series_time.append(N_al)
            N_be_series_time.append(N_be)

        plt.xscale('log')

        for er in many_erosions:
            N_be = float(c_p.steady_erosion_be(er))
            N_al = float(c_p.steady_erosion_al(er))

            N_be_series_erosion.append(N_be)
            N_al_series_erosion.append(N_al)

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            # plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color="black", alpha=0.5)
            #
        plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color, alpha=0.3, linewidth=0.3,edgecolor="black")
        plt.xscale('log')

        # plt.plot(N_be_series_erosion, np.array(N_al_series_erosion) / np.array(N_be_series_erosion), alpha=0.5, color=color,
        #  label='')

        return N_be_series,N_al_series

    ###-------

    def burial_decay_time(self, measured_N10, measured_N26):
        import numpy as np
        c_p = cosmo_production()
        time=0
        N_be = float(c_p.constant_exposure_be(time, 1.7, "mean", 0))
        N_al = float(c_p.constant_exposure_al(time, 1.7, "mean", 0))

        points_per_line = 50000
        times = np.linspace(1e3, 1e6, 100)
        many_erosions = np.concatenate(([0], np.logspace(-2, 6, points_per_line - 1))) / 1e4

        best_time = None
        best_dist = np.inf

        for time in times:
            N_be_series= []
            N_al_series = []
            for er in many_erosions:
                N_be = float(c_p.burial_lines_be(er, 1.7, time))
                N_al = float(c_p.burial_lines_al(er, 1.7, time))
                N_be_series.append(N_be)
                N_al_series.append(N_al)

            for N_be,N_al in zip(N_be_series,N_al_series):
                dist = np.sqrt((N_be - measured_N10) ** 2 + (N_al - measured_N26) ** 2)
                if dist < best_dist:
                    best_time = time
                    best_dist = dist

        return best_time





