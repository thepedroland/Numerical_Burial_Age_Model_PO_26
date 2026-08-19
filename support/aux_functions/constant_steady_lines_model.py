import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import os
import matlab.engine
from support.aux_functions.nuclide_prod_concentration import cosmo_production

class steady_state_model:
    def __init__(self):
        pass

    def plot_steady_state_model(self,scaling_method,density,Rc_value,checking_only=False):
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
            N_be = float(c_p.constant_exposure_be(time,scaling_method,density,Rc_value))
            N_al = float(c_p.constant_exposure_al(time,scaling_method,density,Rc_value))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            N_al_series_time.append(N_al)
            N_be_series_time.append(N_be)

        # plt.plot(N_be_series, np.array(N_al_series) / np.array(N_be_series), alpha=0.3, color="blue",
        #         label='Constant exposure')
        plt.fill_between(N_be_series, np.array(N_al_series_time) / np.array(N_be_series_time), 8, color='white', alpha=0.5,linewidth=0)

        plt.xscale('log')
        times = [0,1e6]

        for er in many_erosions:
            N_be = float(c_p.steady_erosion_be(er,density))
            N_al = float(c_p.steady_erosion_al(er,density))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

        #
        # plt.plot(N_be_series_erosion, np.array(N_al_series_erosion) / np.array(N_be_series_erosion), alpha=0.8, color="grey",
        #         label='Steady Erosion')
        # Then plot fills below the line with the desired color
        # plt.fill_between(N_be_series_erosion, np.array(N_al_series_erosion) / np.array(N_be_series_erosion), 8, color='lightgreen', alpha=0.4)

        if checking_only:
            return N_be_series, np.array(N_al_series) / np.array(N_be_series)

        plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color=color_fill, alpha=0.5, linewidth=0)
        # plt.plot(N_be_series, np.array(N_al_series) / np.array(N_be_series))
        plt.xscale('log')

        line_times = [1e6, 5e5]
        labels = ["1Ma", "0.5Ma"]

        for time, label in zip(line_times, labels):
            N_be_series_line_times = []
            N_al_series_line_times = []

            for er in many_erosions:
                N_be = float(c_p.burial_lines_be(er,density, time))
                N_al = float(c_p.burial_lines_al(er,density, time))

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
    def plot_steady_state_model_depth(self,density,z_cm,color):

        from support.aux_functions.nuclide_prod_concentration import cosmo_production
        import matplotlib.pyplot as plt

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
            N_be = float(c_p.constant_exposure_be(time,"LSDn",density,"mean",z_cm))
            N_al = float(c_p.constant_exposure_al(time,"LSDn",density,"mean",z_cm))

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            N_al_series_time.append(N_al)
            N_be_series_time.append(N_be)


        # plt.plot(N_be_series, np.array(N_al_series) / np.array(N_be_series), alpha=0.5, color=color,
        #          label='')
        # plt.scatter(N_be_series[-1],np.array(N_al_series[-1]) / np.array(N_be_series[-1]), alpha=0.5, color="black",s=5,marker="o",
        #          label='')

        plt.xscale('log')

        for er in many_erosions:
            N_be = float(c_p.steady_erosion_be(er,density))
            N_al = float(c_p.steady_erosion_al(er,density))

            N_be_series_erosion.append(N_be)
            N_al_series_erosion.append(N_al)

            N_be_series.append(N_be)
            N_al_series.append(N_al)

            # plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color="black", alpha=0.5)
            #
        plt.fill(N_be_series, np.array(N_al_series) / np.array(N_be_series), color, alpha=0.4, linewidth=0)
        plt.xscale('log')

        # plt.plot(N_be_series_erosion, np.array(N_al_series_erosion) / np.array(N_be_series_erosion), alpha=0.5, color=color,
        #  label='')

        return N_be_series,N_al_series

