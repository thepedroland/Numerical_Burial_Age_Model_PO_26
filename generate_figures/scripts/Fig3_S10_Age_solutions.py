import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse
import matplotlib.legend_handler as handler
import os
from support.aux_functions.forbiden_zone import plot_forbiden_zone
from support.aux_functions.solution_trajectories import set_trajectories
from support.aux_functions.misc_functions import load_dataset
from cmcrameri import cm
plt.rcParams['font.family'] = 'Arial'

samples_id = ["BV-018","SB-013","SB-011","SB-017"]
density = 1.7
plot_trajectories = False
reference_sample = "Surface"

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
folder_path = os.path.join(main_path, "generate_data")

os.makedirs(main_path+"/generate_figures/figures", exist_ok=True)
plots_path = main_path+"/generate_figures/figures"

fig, axs = plt.subplots(4, 1, figsize=(9, 20),constrained_layout=True)

limit = 40 #Ma

for i, sample_id in enumerate(samples_id):
    print("Plotting sample:", sample_id)
    file_name_csv = os.path.join(folder_path, f"results_data/Results_[{sample_id}]_R{reference_sample}_D{density}.csv")
    print(file_name_csv)
    try:
        results_run = pd.read_csv(file_name_csv)
    except:
        print("not found")

    st = set_trajectories(sample_id,reference_sample, density, folder_path,plots_path)

    data_amazon = load_dataset(sample_id, reference_sample="Surface")

    valid_final_n10 = results_run.loc[results_run["Solution"], 'Final 2-Sigma N10']
    range_age_valid_final_n10 = results_run.loc[
        (results_run["Solution"]) & (results_run["Total Time [Ma]"] <= limit),
        'Final 2-Sigma N10'
    ].tolist()

    valid_final_ratio = results_run.loc[results_run["Solution"], "Final 2-Sigma Ratio"]
    range_age_valid_final_ratio = results_run.loc[
        (results_run["Solution"]) & (results_run["Total Time [Ma]"] <= limit),
        "Final 2-Sigma Ratio"
    ].tolist()

    valid_times_solution = list(results_run.loc[results_run["Solution"], "Total Time [Ma]"])
    range_age_valid_times_solution = results_run.loc[
        (results_run["Solution"]) & (results_run["Total Time [Ma]"] <= limit),
        "Total Time [Ma]"
    ].tolist()

    valid_deposition_rates = list(results_run.loc[results_run["Solution"], "Deposition rate [cm/year]"])
    valid_initial_n10 = results_run.loc[results_run["Solution"], 'Initial N10']
    valid_initial_ratio = results_run.loc[results_run["Solution"], "Initial ratio"]

    false_initial_ratio = list(results_run.loc[~results_run["Solution"], "Initial ratio"])
    false_initial_n10 = list(results_run.loc[~results_run["Solution"], 'Initial N10'])
    false_times_solution = list(results_run.loc[~results_run["Solution"], "Total Time [Ma]"])
    false_deposition_rates = list(results_run.loc[~results_run["Solution"], "Deposition rate [cm/year]"])

    sample_color = [214, 61, 153]

    class HandlerEllipse(handler.HandlerPatch):
        def create_artists(self, legend, orig_handle,
                           xdescent, ydescent, width, height, fontsize, trans):
            center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 1 * ydescent
            p = Ellipse(xy=center, width=width * 0.7, height=height, angle=10)
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    # --- use the existing subplot axes instead of creating a new figure ---
    ax = axs[i]

    rgb_base = [x / 255.0 for x in sample_color]

    sample_eli = Ellipse((0, 0), 1, 1, angle=45,
                         facecolor=tuple(rgb_base + [0.05]),
                         edgecolor=tuple(rgb_base), linewidth=1.2)
    ax.add_patch(sample_eli)

    x0 = data_amazon.measured_n10
    y0 = data_amazon.measured_n26 / data_amazon.measured_n10
    dx_1s = data_amazon.stn_dev_n10
    dy_1s = y0 * np.sqrt(
        (data_amazon.stn_dev_n10 / data_amazon.measured_n10) ** 2
        + (data_amazon.stn_dev_n26 / data_amazon.measured_n26) ** 2
    )

    theta = np.linspace(0, 2 * np.pi, 100)

    x_2s = x0 + (2 * dx_1s) * np.sin(theta)
    y_2s = y0 + (2 * dy_1s) * np.cos(theta)
    ax.fill(x_2s, y_2s, facecolor=tuple(rgb_base + [0.1]),
            edgecolor=tuple(rgb_base + [0.3]), linestyle="--", linewidth=0.8,
            label=r"2$\sigma$ Error")

    x_1s = x0 + dx_1s * np.sin(theta)
    y_1s = y0 + dy_1s * np.cos(theta)
    ax.fill(x_1s, y_1s, facecolor=tuple(rgb_base + [0.25]),
            edgecolor=tuple(rgb_base + [1.0]), linewidth=1.2,
            label=r"1$\sigma$ Error")
    if sample_id != "SB-017":
        ax.set_xlabel("")
    else:
        ax.set_xlabel("$^{10}$Be Concentration [at/g]", fontsize=18, fontname="Arial")
    ax.set_ylabel("$^{26}$Al / $^{10}$Be", fontsize=18, fontname="Arial")
    ax.set_xscale("log")
    ax.set_facecolor("#F7F7F3")
    ax.tick_params(axis="both", which="major", labelsize=12)
    ax.legend(loc="lower right", framealpha=1, fontsize=15, frameon=False,
              handler_map={Ellipse: HandlerEllipse()})

    if sample_id == "SB-011":
        ax.set_xlim(3e4, 1e5); ax.set_ylim(3.8, 5.2)
    elif sample_id == "SB-017":
        ax.set_xlim(1e4, 6e4); ax.set_ylim(3.1, 5.4)
    elif sample_id == "SB-013":
        ax.set_xlim(2.5e5, 6e5); ax.set_ylim(4.3, 5.2)
    elif sample_id == "BV-018":
        ax.set_xlim(3e4, 9e4); ax.set_ylim(4.7, 6.5)


    ax.set_xticklabels([])
    ax.set_yticklabels([], fontsize=18)

    ax.annotate(f"{sample_id}", (0.01, 0.94), xycoords="axes fraction",
                fontweight="bold", fontsize=18, fontname="Arial")

    sc = ax.scatter(range_age_valid_final_n10, range_age_valid_final_ratio, s=30, c=range_age_valid_times_solution,
                     cmap=cm.acton, edgecolor="black", linewidth=0.1)

    ax.set_box_aspect(0.5)

    # --- inset histogram anchored to THIS subplot's bounding box, not the whole figure ---
    hist_ax = ax.inset_axes([0.4, 0.45, 0.5, 0.4])

    ##cut valid solutions for histograms
    n, bins, patches = hist_ax.hist(range_age_valid_times_solution, bins=10, edgecolor="black", linewidth=0.4)

    norm = plt.Normalize(bins.min(), bins.max())
    cmap = plt.get_cmap(cm.acton)
    for bin_val, patch in zip(bins, patches):
        patch.set_facecolor(cmap(norm(bin_val)))
    if sample_id != "SB-013":
        hist_ax.set_xlim([0,20])
    else:
        hist_ax.set_xlim([0,1])
    hist_ax.set_facecolor("#FAFAFA")
    hist_ax.set_xlabel(r"Solution Times 2$\sigma$ [Ma]", fontsize=10)
    hist_ax.set_ylabel("Count", fontsize=10)
    hist_ax.tick_params(axis="both", which="major", labelsize=10)
    hist_ax.spines["top"].set_visible(False)
    hist_ax.spines["right"].set_visible(False)

fig_name = f"Fig10_Full_Solution_Histograms_D{density}"
fig.savefig(f"{plots_path}/supporting_figures/SVG_{fig_name}.png", dpi=300, bbox_inches="tight")

if plot_trajectories:
    print("Plotting trajectories")
    st.plot_trajectories(x_2s,y_2s)
