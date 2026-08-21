import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import tight_layout
from matplotlib.ticker import FixedLocator
import pandas as pd
from matplotlib.patches import Ellipse
import matplotlib.legend_handler as handler
import os
from datetime import datetime
from support.aux_functions.forbiden_zone import plot_forbiden_zone
from support.aux_functions.solution_trajectories import set_trajectories
from support.aux_functions.misc_functions import load_dataset
from cmcrameri import cm
plt.rcParams['font.family'] = 'Arial'

samples_id = ["BV-018"]
density = 1.7
plot_trajectories = True
reference_sample = "Surface"

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
folder_path = os.path.join(main_path, "generate_data", "python_data_results")

os.makedirs(main_path+"/generate_figures/figures", exist_ok=True)
plots_path = main_path+"/generate_figures/figures"


fig, axs = plt.subplots(4, 1, figsize=(9, 20),constrained_layout=True)

limit = 20 #Ma

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

#
####----EXPLORATION PARAMETERS---------######
    fig2, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(12, 6), constrained_layout=True)

    fig2.set_facecolor("#EBEBEB")
    fig2.suptitle(f"Sample: {sample_id} | Starting from: {reference_sample }\n ρ = {density}", fontsize=18)
    ###Histogram for ages
    all_ages_sampled = []
    all_ages_sampled.extend(false_times_solution)
    all_ages_sampled.extend(valid_times_solution)

    facecolor_axes = "#EBEBEB"
    sampled_color = "#E4CAA0"
    false_color = "#DCE4A0"
    valid_color = "#BAE4A0"

    ax1.set_facecolor(facecolor_axes)
    ax1.hist(all_ages_sampled, bins=20, edgecolor="black", linewidth=0.5, color=sampled_color, label="Sampled ")
    ax1.hist(false_times_solution, bins=20, edgecolor="black", linewidth=0.5, color= false_color, label="No solution")
    ax1.hist(valid_times_solution, bins=20, edgecolor="black", linewidth=0.5, color=valid_color, label="Solution found")

    ax1.set_xlabel(r"Tentative Time [Ma]", fontsize=8)
    ax1.set_ylabel("Count", fontsize=10)
    ax1.tick_params(axis="both", which="major", labelsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ###Histogram for deposition rates

    all_deposition_sampled = []
    all_deposition_sampled.extend(valid_deposition_rates)
    all_deposition_sampled.extend(false_deposition_rates)

    ax2.set_facecolor(facecolor_axes)
    ax2.hist(all_deposition_sampled, bins=30, edgecolor="black", linewidth=0.5, color=sampled_color, label="Sampled")
    ax2.hist(false_deposition_rates,bins=30,edgecolor="black",linewidth=0.5,color=false_color, label="No solution")
    ax2.hist(valid_deposition_rates,bins=30,edgecolor="black",linewidth=0.5,color=valid_color,  label="Solution found")

    ax2.vlines(0.0002,0,100,linewidth=0.7,color="black", linestyle="--", label="Dep rate data")
    ax2.vlines(0.001,0,100,linewidth=0.7,color="black", linestyle="--", label="Dep rate data")

    ax2.set_xlabel(r"Deposition rate [cm/year]", fontsize=8)
    ax2.set_ylabel("Count", fontsize=10)
    ax2.tick_params(axis="both", which="major", labelsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.semilogx()
    ##Histogram for initial n10

    all_initial_n10 = []
    all_initial_n10.extend(valid_initial_n10)
    all_initial_n10.extend(false_initial_n10)

    ax3.set_facecolor(facecolor_axes)
    ax3.hist(all_initial_n10, bins=30, edgecolor="black", linewidth=0.5, color=sampled_color, label="Sampled")
    ax3.hist(false_initial_n10,bins=30,edgecolor="black",linewidth=0.5,color=false_color, label="No solution")
    ax3.hist(valid_initial_n10,bins=30,edgecolor="black",linewidth=0.5,color=valid_color, alpha=0.7, label="Solution found")

    ax3.set_xlabel(r"Initial $^{10}$Be Concentration [atoms/g]", fontsize=10)
    ax3.set_ylabel("Count", fontsize=10)
    ax3.tick_params(axis="both", which="major", labelsize=8)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.legend(fontsize=10)
    ax3.semilogx()
    ##Scatter for deposition and time

    ax4.set_facecolor(facecolor_axes)
    ax4.scatter(valid_deposition_rates,valid_times_solution,linewidth=0.5,edgecolors="black",s=30,c="#EAFAF4")
    ax4.set_xlabel(r"Deposition rate [cm/year]", fontsize=10)
    ax4.set_ylabel("Age [Myr]", fontsize=10)
    ax4.tick_params(axis="both", which="major", labelsize=8)
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.semilogx()

    ##Scatter initial and times
    all_ratio = []
    all_ratio.extend(valid_initial_ratio)
    all_ratio.extend(false_initial_ratio)

    ax5.set_facecolor(facecolor_axes)
    ax5.scatter(valid_initial_n10,valid_times_solution,edgecolors="black",s=30,c="#EAFAF4",linewidth=0.5)
    ax5.set_xlabel(r"Initial $^{10}$Be Concentration [atoms/g]", fontsize=10)
    ax5.set_ylabel("Age [Myr]", fontsize=10)
    ax5.tick_params(axis="both", which="major", labelsize=8)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.semilogx()
    plot_forbiden_zone(all_initial_n10,all_ratio,ax6)

    ###plot info###
    fig_name = f"FigS{i+1}_Parameters_Sampling_[{sample_id}_D_{density}]_"

    fig_dir_2 = os.path.join(plots_path, fig_name)
    print(fig_dir_2)
    fig2.savefig(f"{fig_dir_2}.png", dpi=300, bbox_inches="tight")


fig_name = f"Fig3_Solutions_Profile_Ages_D{density}]"

fig.savefig(f"{plots_path}/{fig_name}.png", dpi=300, bbox_inches="tight")
# fig.savefig(f"{plots_path}/SVG_{fig_name}.svg", format="svg", bbox_inches="tight")

if plot_trajectories:
    print("Plotting trajectories")
    st.plot_trajectories(x_2s,y_2s)
