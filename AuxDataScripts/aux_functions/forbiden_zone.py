import numpy as np
import matplotlib.pyplot as plt
from AuxDataScripts.aux_functions.constant_steady_lines_model import burial_exposure_model

def plot_forbiden_zone(all_initial_c10, all_ratio,ax,sample=None):
    lines_model = burial_exposure_model()
    lines_between = lines_model.plot_steady_state_model(Rc_value='min',checking_only=True)

    black_x, black_y = lines_between[0][0:50000], lines_between[1][0:50000]
    blue_x, blue_y = lines_between[0][50000:100000], lines_between[1][50000:100000]

    ax.plot(black_x, black_y, '.', color='gray', markersize=0.01, label='Constant Exposure')
    ax.plot(blue_x, blue_y, '.', color='gray', markersize=0.01, label='Steady Erosion')
    if not sample:
        ax.annotate("F", (0.009, 1.01), xycoords="axes fraction",
                     fontweight="bold", fontsize=12, fontname="Arial")
    else:
        ax.annotate("H", (0.009, 1.01), xycoords="axes fraction",
                    fontweight="bold", fontsize=12, fontname="Arial")
    ax.set_facecolor = '#FCFCFC"'
    black_order = np.argsort(black_x)

    blue_order = np.argsort(blue_x)
    black_x_sorted, black_y_sorted = np.array(black_x)[black_order], np.array(black_y)[black_order]
    blue_x_sorted, blue_y_sorted = np.array(blue_x)[blue_order], np.array(blue_y)[blue_order]

    inside_x, inside_y = [], []
    outside_x, outside_y = [], []

    for N10, ratio in zip(all_initial_c10, all_ratio):   # loop over your random points, not the linspace ranges
        lower_bound = np.interp(N10, black_x_sorted, black_y_sorted)
        upper_bound = np.interp(N10, blue_x_sorted, blue_y_sorted)

        lo, hi = min(lower_bound, upper_bound), max(lower_bound, upper_bound)

        if lo <= ratio <= hi:
            inside_x.append(N10)
            inside_y.append(ratio)
        elif ratio <= lo:
            inside_x.append(N10)
            inside_y.append(ratio)
        else:
            outside_x.append(N10)
            outside_y.append(ratio)

    ax.scatter(inside_x, inside_y, color="#E6F3F9",label='within bounds',edgecolor='black',linewidth=0.2,s=7)
    ax.scatter(outside_x, outside_y, color='red',label='outside bounds')
    ax.set_xlabel("$^{10}$Be Concentration [at/g]", fontsize=8, fontname="Arial")
    ax.set_ylabel("$^{26}$Al/$^{10}$Be", fontsize=8, fontname="Arial")
    ax.tick_params(axis="both", which="major", labelsize=8)
    ax.set_yticks([4,5,6,7,8])

    ax.set_xlim(1e4, 1e6)
    ax.set_ylim(3.5, 8)
#
# fig,ax = plt.subplots()
#
#
# N10_range = np.linspace(76508.75214, 689006.2439, 20000)
# ratio_range = np.linspace(5.572903084, 7.559285158, 20000)
#
# rng = np.random.default_rng()
# random_N = rng.choice(N10_range, size=5000, replace=False)
# random_ratio = rng.choice(ratio_range, size=5000, replace=False)
#
# plot_forbiden_zone(random_N,random_ratio,ax)
