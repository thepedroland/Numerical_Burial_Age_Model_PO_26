
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
fig_dir = main_path + "/Figures/Plots"

fig_name = f"Fig4_MCyork_erosion_rate_relief_graph"

data_file = main_path +  "/AuxDataScripts/data/TopographicData/corr_topographic_data_ksn_erosion_rf.csv"

remove_samples = []

df_data = pd.read_csv(data_file)
re_index = df_data[df_data['labels'].isin(remove_samples)].index

df_data.drop(re_index, inplace=True)

erosion = df_data['erosion'].values
dev_ero = df_data['unc_erosion'].values
ksn = df_data['ksn'].values
std_ksn = df_data['std_ksn'].values
labels = df_data["labels"].values
se_ksn = df_data["se_ksn"].values
slope = df_data["slope"].values
se_slope = df_data["de_slope"].values
drainage = df_data["drainage_area"].values

relief_basins_df = pd.read_csv("/01_AuxDataScripts/data/TopographicData/relief_basins_data.csv", header=None)
relief_data_std_df = pd.read_csv("/01_AuxDataScripts/data/TopographicData/relief_basins_data_std.csv", header=None)

# Convert to numpy arrays (flatten if multiple columns exist)

sorted_erosion_values = df_data.sort_values(by=["code_matlab"], ascending=True)
corr_erosion_values = sorted_erosion_values["erosion"].values
corr_erosion_values_std = sorted_erosion_values['unc_erosion'].values

fig,(ax1,ax2) = plt.subplots(1,2)

color = drainage
ax1.errorbar(corr_erosion_values, relief_basins_df.loc[:,4],xerr=corr_erosion_values_std,yerr=relief_data_std_df.loc[:,4],marker='o',
         mec='black', ms=3, mew=0.3,linestyle='None',ecolor="#2C2C1C",zorder=1,elinewidth=0.3,c="#FFF2E5")

ax1.set_facecolor(color="#FAFAFA")
ax1.set_xlabel('Erosion rate [m/Myr]',fontsize=6 )
ax1.set_ylabel('Relief [m/m] radius: 3000m',fontsize=6 )
ax1.set_box_aspect(0.5)

ax2.set_facecolor(color="#FAFAFA")
ax2.hist(erosion, bins='fd', edgecolor="black", linewidth=0.3,color="#FFF2E5")
ax2.set_xlabel('Erosion rate [m/Myr]',fontsize=6 )
ax2.set_ylabel('Count',fontsize=6 )
ax2.set_box_aspect(0.5)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")

for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(0.5)
    ax2.spines[axis].set_linewidth(0.5)

ax2.tick_params(axis='both', width=0.5, labelsize=6)
ax1.tick_params(axis='both', width=0.5, labelsize=6)
plt.subplots_adjust(wspace=0.05)
fig = plt.gcf()
fig.set_size_inches(3.5,2)

plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=700)
plt.show()


