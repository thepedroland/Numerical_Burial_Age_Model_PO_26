import pandas as pd
import matplotlib.pyplot as plt
import os

from matplotlib.ticker import FixedLocator


main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
fig_dir = main_path + "/a_Figures/Plots"

fig_name = "Fig4_MCyork_erosion_rate_relief_graph"

data_file = main_path + "/z_AuxDataScripts/data/TopographicData/corr_topographic_data_ksn_erosion_rf.csv"

remove_samples = []

df_data = pd.read_csv(data_file)
re_index = df_data[df_data["labels"].isin(remove_samples)].index
df_data.drop(re_index, inplace=True)

erosion = df_data["erosion"].values
dev_ero = df_data["unc_erosion"].values

relief_basins_df = pd.read_csv(
    main_path + "/z_AuxDataScripts/data/TopographicData/relief_basins_data.csv",
    header=None
)

relief_data_std_df = pd.read_csv(
    main_path + "/z_AuxDataScripts/data/TopographicData/relief_basins_data_std.csv",
    header=None
)

sorted_erosion_values = df_data.sort_values(by=["code_matlab"], ascending=True).reset_index(drop=True)

corr_erosion_values = sorted_erosion_values["erosion"].values
corr_erosion_values_std = sorted_erosion_values["unc_erosion"].values

relief_values = relief_basins_df.loc[:, 4].values
relief_std_values = relief_data_std_df.loc[:, 4].values

if len(corr_erosion_values) != len(relief_values):
    raise ValueError(
        f"Length mismatch: erosion has {len(corr_erosion_values)} values, "
        f"but relief has {len(relief_values)} values."
    )

fig, (ax1, ax2) = plt.subplots(2, 1,sharex=True,constrained_layout=True)

colors = [
    "#FCDED9" if i in [0, 14] else "#F7FCD9"
    for i in range(len(corr_erosion_values))
]


ax1.errorbar(
    corr_erosion_values,
    relief_values,
    xerr=corr_erosion_values_std,
    yerr=relief_std_values,
    fmt="none",
    ecolor="#2C2C1C",
    zorder=1,
    elinewidth=0.3
)

ax1.scatter(
    corr_erosion_values,
    relief_values,
    c=colors,
    edgecolors="black",
    s=9,
    linewidths=0.3,
    zorder=2
)

ax1.set_facecolor(color="#FAFAFA")
ax1.set_ylabel("Relief [m]", fontsize=8)
ax1.set_box_aspect(0.5)

ax2.set_xlabel("Erosion rate [m/Myr]", fontsize=8)

ax2.set_facecolor(color="#FAFAFA")
ax2.hist(
    erosion,
    bins=13,
    edgecolor="black",
    linewidth=0.3,
    color="#F7FCD9"
)
ax2.set_ylabel("Count", fontsize=8)
ax2.set_box_aspect(0.5)
ax2.yaxis.set_label_position("left")

for axis in ["top", "bottom", "left", "right"]:
    ax1.spines[axis].set_linewidth(0.5)
    ax2.spines[axis].set_linewidth(0.5)

ax2.tick_params(axis="both", width=0.5, labelsize=6)
y_ticks = [1,3,5]
ax2.yaxis.set_major_locator(FixedLocator(y_ticks))
ax2.set_yticklabels(y_ticks)
ax1.tick_params(axis="y", width=0.5, labelsize=6)
ax1.tick_params(axis="x", width=0, labelsize=6)

fig = plt.gcf()
fig.set_size_inches(3.5, 3)

os.makedirs(fig_dir, exist_ok=True)

plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=700)
plt.show()
