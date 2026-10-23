import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from matplotlib.patches import Ellipse
import matplotlib.legend_handler as handler
import os
from z_AuxDataScripts.aux_scripts.forbiden_zone import plot_forbiden_zone
from z_AuxDataScripts.aux_scripts.solution_trajectories import set_trajectories
from z_AuxDataScripts.aux_scripts.misc_functions import load_dataset
from cmcrameri import cm

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.linewidth'] = 0.5

samples_id = ["BV-018","SB-013","SB-011","SB-017"]
density = 1.7
plot_trajectories = False
reference_sample = "Surface"

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
folder_path = os.path.join(main_path, "DataResults")

os.makedirs(main_path+"/Figures/Plots", exist_ok=True)
plots_path = main_path+"/Figures/Plots"

#20 for Figure 3 and 40 for Figure S10
limit = 20 #Ma
x_lim = limit

if x_lim != 20:
    print("Supporting figure")
    samples_id = ["BV-018", "SB-011", "SB-017"]
    fig, axs = plt.subplots(3, 1, figsize=(8, 6),constrained_layout=False)
else:
    fig, axs = plt.subplots(4, 1, figsize=(3,4),constrained_layout=True)

for i, sample_id in enumerate(samples_id):
    print("\u2B95 Plotting sample:", sample_id)
    file_name_csv = os.path.join(folder_path, f"NumSimResults/Results_[{sample_id}]_R{reference_sample}_D{density}.csv")
    try:
        results_run = pd.read_csv(file_name_csv)
        print("\u2B95 Reading data from:", file_name_csv)
    except:
        print("\u274C File not found in",folder_path)

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
    valid_erosion_rates = list(results_run.loc[results_run["Solution"], "Erosion rate [cm/year]"])
    valid_initial_n10 = results_run.loc[results_run["Solution"], 'Initial N10']
    valid_initial_ratio = results_run.loc[results_run["Solution"], "Initial ratio"]

    false_initial_ratio = list(results_run.loc[~results_run["Solution"], "Initial ratio"])
    false_initial_n10 = list(results_run.loc[~results_run["Solution"], 'Initial N10'])
    false_times_solution = list(results_run.loc[~results_run["Solution"], "Total Time [Ma]"])
    false_deposition_rates = list(results_run.loc[~results_run["Solution"], "Deposition rate [cm/year]"])
    false_erosion_rates = list(results_run.loc[~results_run["Solution"], "Erosion rate [cm/year]"])

    sample_color = [214, 61, 153]

    class HandlerEllipse(handler.HandlerPatch):
        def create_artists(self, legend, orig_handle,
                           xdescent, ydescent, width, height, fontsize, trans):
            center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 1 * ydescent
            p = Ellipse(xy=center, width=width * 0.7, height=height, angle=8)
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]

    # --- use the existing subplot axes instead of creating a new figure ---
    axs_flat = axs.flatten()
    ax = axs_flat[i]
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
            edgecolor=tuple(rgb_base + [0.3]), linewidth=0.5,
            label=r"2$\sigma$ Error")

    x_1s = x0 + dx_1s * np.sin(theta)
    y_1s = y0 + dy_1s * np.cos(theta)
    ax.fill(x_1s, y_1s, facecolor=tuple(rgb_base + [0.25]),
            edgecolor=tuple(rgb_base + [1.0]), linewidth=0.5,
            label=r"1$\sigma$ Error")

    # ax.set_ylabel("$^{26}$Al / $^{8}$Be", fontsize=18, fontname="Arial")
    ax.set_xscale("log")
    # ax.set_facecolor("#F7F7F3")
    # ax.tick_params(axis="both", which="major", labelsize=12)

    if x_lim != 20:
        sc = ax.scatter(range_age_valid_final_n10, range_age_valid_final_ratio, s=3, c=range_age_valid_times_solution,
                        cmap=cm.nuuk, edgecolor="black", linewidth=0.05)
        ax.annotate(f"{sample_id[:2]+sample_id[-2:]}", (0.01, 0.95), xycoords="axes fraction",
                    fontweight="bold", fontsize=7, fontname="Arial")
    else:
        # ax.legend(loc="lower right", framealpha=1, fontsize=15, frameon=False,
        #           handler_map={Ellipse: HandlerEllipse()})
        sc = ax.scatter(range_age_valid_final_n10, range_age_valid_final_ratio, s=1, c=range_age_valid_times_solution,
                        cmap=cm.nuuk, edgecolor="black", linewidth=0.01)
        # ax.annotate(f"{sample_id[:2]+sample_id[-2:]}", (0.01, 0.94), xycoords="axes fraction",
        #             fontweight="bold", fontsize=18, fontname="Arial")

    if limit != 20:
        if sample_id == "SB-011":
            ax.set_xlim(3e4, 2e5);
            ax.set_ylim(3.8, 5.2)
        elif sample_id == "SB-017":
            ax.set_xlim(1e4, 9e4);
            ax.set_ylim(3.1, 5.4)
        elif sample_id == "BV-018":
            ax.set_xlim(3e4, 2e5);
            ax.set_ylim(4.7, 6.5)
    else:
        if sample_id == "SB-011":
            ax.set_xlim(3e4, 1e5); ax.set_ylim(3.8, 5.2)
        elif sample_id == "SB-017":
            ax.set_xlim(1e4, 6e4); ax.set_ylim(3.1, 5.4)
        elif sample_id == "SB-013":
            ax.set_xlim(2.5e5, 6e5); ax.set_ylim(4.3, 5.2)
        elif sample_id == "BV-018":
            ax.set_xlim(3e4, 9e4); ax.set_ylim(4.7, 6.5)

    ax.set_box_aspect(0.5)
    ax.set_frame_on(False)
    ax.set_xticks([])  # Removes X ticks & labels
    ax.set_yticks([])

    # Hides major and minor ticks/labels on the x-axis
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False,size=0.1)

    # --- inset histogram anchored to THIS subplot's bounding box, not the whole figure ---

    bins = np.linspace(0, limit, 20)

    if sample_id == "SB-013":
        gap = 0.02
        w = (0.9 - gap) / 2
        hist_ax1 = ax.inset_axes([0, 0, w, 1])
        hist_ax2 = ax.inset_axes([w + gap, 0, w, 1], sharey=hist_ax1)

        for a in (hist_ax1, hist_ax2):
            n, bins, patches = a.hist(range_age_valid_times_solution, bins=6,
                   edgecolor="black", linewidth=0.3)

            norm = plt.Normalize(bins.min(), bins.max())
            cmap = plt.get_cmap(cm.nuuk)

            for bin_val, patch in zip(bins, patches):
                patch.set_facecolor(cmap(norm(bin_val)))

        hist_ax1.set_xlim(0, 1.5)  # adjust to your data
        hist_ax2.set_xlim(1.5, 20)  # adjust to your data

        # clean up the break
        hist_ax1.spines["right"].set_visible(False)
        hist_ax1.spines["left"].set_visible(True)
        hist_ax2.spines["left"].set_visible(False)
        hist_ax1.spines["top"].set_visible(False)
        hist_ax2.spines["top"].set_visible(False)
        hist_ax2.tick_params(left=False,labelleft=False,labelsize=7,width=0.5)
        hist_ax1.tick_params(left=True,labelleft=True,labelsize=7,width=0.5)

        # diagonal break marks
        d = 0.015
        kw = dict(transform=hist_ax1.transAxes, color="k", clip_on=False, lw=0.8)
        hist_ax1.plot((1 - d, 1 + d), (-d, +d), **kw)
        # hist_ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kw)
        kw.update(transform=hist_ax2.transAxes)
        hist_ax2.plot((-d, +d), (-d, +d), **kw)
        # hist_ax2.plot((-d, +d), (1 - d, 1 + d), **kw)

    else:
        hist_ax = ax.inset_axes([0, 0, 0.9, 1])
        n, bins, patches = hist_ax.hist(range_age_valid_times_solution, bins=bins,
                     edgecolor="black", linewidth=0.5)
        hist_ax.set_xlim([0, x_lim])

        norm = plt.Normalize(bins.min(), bins.max())
        cmap = plt.get_cmap(cm.nuuk)

        for bin_val, patch in zip(bins, patches):
            patch.set_facecolor(cmap(norm(bin_val)))

        hist_ax.set_facecolor('None')
        if sample_id == "SB-017":
            hist_ax.set_xlabel(r"Solution Times 2$\sigma$ [Ma]", fontsize=7)
        else:
            hist_ax.set_xlabel("", fontsize=7)
        # hist_ax.set_ylabel("Count", fontsize=8)
        hist_ax.tick_params(axis="both", which="major", labelsize=7,width=0.3)
        from matplotlib.ticker import MaxNLocator
        hist_ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
        hist_ax.yaxis.tick_left()
        hist_ax.yaxis.set_label_position("left")
        hist_ax.spines["top"].set_visible(False)
        hist_ax.spines["right"].set_visible(True)
        hist_ax.spines["left"].set_visible(True)

#
####----EXPLORATION PARAMETERS-SUPPORTING MATERIAL---------######
    if sample_id == "BV-018":
        fig2, axes = plt.subplots(2, 4, figsize=(14, 5), constrained_layout=True)
        ax1, ax2, ax3, ax4 = axes[0]
        ax5, ax6, ax7, ax8 = axes[1]
    else:
        fig2, axes = plt.subplots(2, 3, figsize=(12, 6), constrained_layout=True)
        ax1, ax2, ax3 = axes[0]
        ax4, ax5, ax6 = axes[1]
    fig2.set_facecolor("#FCFCFC")
    fig2.suptitle(f"Sample {sample_id[:2]+sample_id[-2:]} | ρ = {density} g/cm$^{3}$", fontsize=12, x=0.01, ha='left')
    ###Histogram for ages
    all_ages_sampled = []
    all_ages_sampled.extend([valid_times_solution])
    all_ages_sampled.extend([false_times_solution])

    facecolor_axes = "#FCFCFC"
    false_color = "#F6E6F9"
    valid_color = "#F3F9E6"
    sampled_color = "#E6E9F9"

    ax1.set_facecolor(facecolor_axes)
    n,bins,patches = ax1.hist(all_ages_sampled, bins='fd', edgecolor="black", linewidth=0.3, color=[valid_color,false_color],stacked=True)
    ax1.annotate("A", (0.009, 0.99), xycoords="axes fraction",
                fontweight="bold", fontsize=12, fontname="Arial")

    ax1.set_xlabel(r"Tentative Burial Time [Ma]", fontsize=8)
    ax1.set_ylabel("Count", fontsize=8)
    ax1.tick_params(axis="both", which="major", labelsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ###Histogram for deposition rates

    all_deposition_sampled = []
    all_deposition_sampled.extend([valid_deposition_rates])
    all_deposition_sampled.extend([false_deposition_rates])
    ax2.set_facecolor(facecolor_axes)

    n,bins,patches =  ax2.hist(all_deposition_sampled, bins='fd', edgecolor="black", linewidth=0.3, color=[valid_color,false_color],stacked=True,label=["Valid solution","False solution"])
    ax2.vlines(0.0002,0,len(false_deposition_rates)/2,linewidth=0.7,color="black", linestyle="--", label="")
    ax2.vlines(0.001,0,len(false_deposition_rates)/2,linewidth=0.7,color="black", linestyle="--", label="Measured Erosion Rate")
    ax2.legend(fontsize=8)
    ax2.annotate("B", (0.009, 0.99), xycoords="axes fraction",
                 fontweight="bold", fontsize=12, fontname="Arial")
    ax2.set_xlabel(r"Deposition rate [cm/year]", fontsize=8)
    ax2.set_ylabel("Count", fontsize=8)
    ax2.tick_params(axis="both", which="major", labelsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_xscale("log")    ##Histogram for initial n10

    all_initial_n10 = []
    all_initial_n10_forbid = []
    all_initial_n10.extend([valid_initial_n10])
    all_initial_n10.extend([false_initial_n10])
    all_initial_n10_forbid.extend(valid_initial_n10)
    all_initial_n10_forbid.extend(false_initial_n10)

    ax3.set_facecolor(facecolor_axes)
    n,bins,patches = ax3.hist(all_initial_n10, bins='fd', edgecolor="black", linewidth=0.3, color=[valid_color,false_color],stacked=True)
    ax3.annotate("C", (0.009, 0.99), xycoords="axes fraction",
                 fontweight="bold", fontsize=12, fontname="Arial")
    ax3.set_xlabel(r"Initial $^{10}$Be Concentration [atoms/g]", fontsize=8)
    ax3.set_ylabel("Count", fontsize=8)
    ax3.tick_params(axis="both", which="major", labelsize=8)
    ax3.tick_params(axis="both", which="minor", labelsize=6)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.set_xscale("log")    ##Scatter for deposition and time

    ax4.set_facecolor(facecolor_axes)
    ax4.scatter(valid_deposition_rates,valid_times_solution,linewidth=0.4,edgecolors="black",s=20,c="#E6F3F9")
    ax4.set_xlabel(r"Deposition rate [cm/year]", fontsize=8)
    ax4.set_ylabel("Age [Myr]", fontsize=8)
    ax4.tick_params(axis="both", which="major", labelsize=8)

    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.set_xscale("log")
    ax4.annotate("D", (0.009, 0.99), xycoords="axes fraction",
                 fontweight="bold", fontsize=12, fontname="Arial")

    ##Scatter initial and times
    all_ratio = []
    all_ratio.extend(valid_initial_ratio)
    all_ratio.extend(false_initial_ratio)

    ax5.set_facecolor(facecolor_axes)
    ax5.scatter(valid_initial_n10,valid_times_solution,edgecolors="black",s=20,c="#E6F3F9",linewidth=0.4)
    ax5.set_xlabel(r"Initial $^{8}$Be Concentration [atoms/g]", fontsize=8)
    ax5.set_ylabel("Age [Myr]", fontsize=8)
    ax5.tick_params(axis="both", which="major", labelsize=8)
    ax5.tick_params(axis="both", which="minor", labelsize=6)
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.set_xscale("log")
    ax5.annotate("E", (0.009, 0.99), xycoords="axes fraction",
                 fontweight="bold", fontsize=12, fontname="Arial")
    if sample_id == "BV-018":
        ax6.set_facecolor(facecolor_axes)
        ax6.scatter(valid_erosion_rates, valid_times_solution, edgecolors="black", s=20, c="#E6F3F9", linewidth=0.4)
        ax6.set_xlabel(r"Erosion rates [cm/year]", fontsize=8)
        ax6.set_ylabel("Age [Myr]", fontsize=8)
        ax6.tick_params(axis="both", which="major", labelsize=8)
        ax6.spines["top"].set_visible(False)
        ax6.spines["right"].set_visible(False)
        ax6.set_xscale("log")
        ax6.annotate("F", (0.009, 0.99), xycoords="axes fraction",
                     fontweight="bold", fontsize=12, fontname="Arial")

        all_erosion_sampled = []
        all_erosion_sampled.extend([valid_erosion_rates])
        all_erosion_sampled.extend([false_erosion_rates])


        ax7.set_facecolor(facecolor_axes)
        ax7.hist(all_erosion_sampled, bins=10, edgecolor="black", linewidth=0.3,color=[valid_color,false_color],stacked=True,
                 label="Sampled")
        ax7.vlines(0.0002, 0, 1500, linewidth=0.7, color="black", linestyle="--", label="Dep rate data")
        ax7.vlines(0.003, 0, 1500, linewidth=0.7, color="black", linestyle="--", label="Dep rate data")
        ax7.set_xlabel(r"Erosion rate [cm/year]", fontsize=8)
        ax7.set_ylabel("Count", fontsize=8)
        ax7.tick_params(axis="both", which="major", labelsize=8)
        ax7.spines["top"].set_visible(False)
        ax7.spines["right"].set_visible(False)
        ax7.set_xscale("log")
        ax7.set_xlim(1e-4,1e-2)
        ax7.annotate("G", (0.009, 0.99), xycoords="axes fraction",
                     fontweight="bold", fontsize=12, fontname="Arial")
        ax7.tick_params(axis="both", which="minor", labelsize=6)
        plot_forbiden_zone(all_initial_n10_forbid,all_ratio,ax8,"18")
    else:
        plot_forbiden_zone(all_initial_n10_forbid, all_ratio, ax6)

    ###plot info###
    fig_name_2 = f"FigS{i+2}_Parameters_Sampling_{sample_id}_D_{density}"

    fig_dir_2 = f"{plots_path}/SupMaterial/{fig_name_2}"
    fig2.savefig(f"{fig_dir_2}.png", dpi=300)
    print(" \u2705 Plots available in", fig_dir_2,"\n")

fig_name = f"Fig3_Solutions_Profile_Ages_D{density}"

if x_lim != 20:
    fig_name_3 = f"/supporting_figures/FigS6_Full_Solutions_Profile_Ages_D{density}"
    fig.savefig(f"{plots_path}/{fig_name_3}.png", dpi=300)
else:
    fig.tight_layout()
    fig.savefig(f"{plots_path}/{fig_name}.png", dpi=300)
    fig.savefig(f"{plots_path}/SVG/SVG_{fig_name}.svg", format="svg")


if plot_trajectories:
    print("Plotting trajectories")
    st.plot_trajectories(x_2s,y_2s)
