import pandas as pd
import os
import matplotlib.pyplot as plt

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(root_path)
folder_path = root_path + "/a_DataResults/NumSimResults"
print(folder_path)

colors = {"BV-018":"#71E0CE","SB-013":"#9671E0","SB-011":"#E07184","SB-017":"#BBE071"}


fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5),constrained_layout=False)

fig.set_facecolor("#FCFCFC")
for sample_id in ["BV-018","SB-013","SB-011","SB-017"]:
    file_name_csv = os.path.join(folder_path, f"Results_[{sample_id}]_RSurface_D1.7.csv")
    results_run = pd.read_csv(file_name_csv)
    valid_times_solution = list(results_run.loc[results_run["Solution"], "Total Time [Ma]"])
    valid_deposition_rates = list(results_run.loc[results_run["Solution"], "Deposition rate [cm/year]"])

    ax1.hist(valid_deposition_rates, bins='fd', label=sample_id,histtype='step', fill = False,edgecolor=colors[sample_id])
ax1.annotate("A", (0.01, 0.95), xycoords="axes fraction",weight="bold", fontsize=16, fontname="Arial")
ax1.legend(frameon=False,fontsize=10,loc="upper right",ncol=1)
ax1.set_xscale("log")
ax1.set_xlabel("Deposition rate [cm/year]",fontsize=14,fontname="Arial")
ax1.set_ylabel("Count",fontsize=14,fontname="Arial")
import numpy as np
bins = np.linspace(0, 20, 20)

for sample_id in ["BV-018","SB-011","SB-017"]:
    file_name_csv = os.path.join(folder_path, f"Results_[{sample_id}]_RSurface_D1.7.csv")
    results_run = pd.read_csv(file_name_csv)
    valid_times_solution = list(results_run.loc[results_run["Solution"], "Total Time [Ma]"])
    valid_deposition_rates = list(results_run.loc[results_run["Solution"], "Deposition rate [cm/year]"])
    plot_age = []
    for depo, age in zip(valid_deposition_rates, valid_times_solution):
        if (depo > 0.00097) & (depo < 0.89):
            plot_age.append(age)
    ax2.hist(plot_age,bins=bins, label=sample_id,histtype='step', color=colors[sample_id])
    ax2.hist(valid_times_solution, bins=bins, label=sample_id, histtype='step', color=colors[sample_id],linestyle="--")
    ax2.legend(frameon=False,fontsize=10,loc="upper right",ncol=1)

ax2.annotate("B", (0.01, 0.951), xycoords="axes fraction",weight="bold", fontsize=16, fontname="Arial")
ax2.set_xlabel("Age [Myr]",fontsize=14,fontname="Arial")
ax2.set_ylabel("",fontsize=14,fontname="Arial")
plt.show()


plots_path = os.path.join(root_path,"a_Figures/Plots/SupMaterial")
fig_dir = f"{plots_path}/FigSX_Depo_analysis"
fig.savefig(f"{fig_dir}.png", dpi=300)
