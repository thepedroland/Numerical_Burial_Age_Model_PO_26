
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
fig_dir = main_path + "/generate_figures/figures"

fig_name = f"Fig4_MCyork_erosion_rate_relief_graph"

data_file = main_path +  "/support/data/topographic_data_ksn_erosion_rf.csv"

remove_samples = []

df_data = pd.read_csv(data_file)
re_index = df_data[df_data['labels'].isin(remove_samples)].index

df_data.drop(re_index, inplace=True)

erosion = df_data['erosion'].values
dev_ero = df_data['unc_erosion'].values
ksn = df_data['ksn'].values
std_ksn = df_data['std_ksn'].values
relief = df_data['relief'].values
std_relief = df_data['std_relief'].values
labels = df_data["labels"].values
se_ksn = df_data["se_ksn"].values
slope = df_data["slope"].values
se_slope = df_data["de_slope"].values
drainage = df_data["drainage_area"].values

fig,(ax1,ax2) = plt.subplots(1,2)

color = drainage
ax1.errorbar(erosion, relief,xerr=dev_ero,yerr=std_relief,marker='o',
         mec='black', ms=3, mew=0.4,linestyle='None',ecolor="#2C2C1C",zorder=1,elinewidth=0.5,c="#F6F9E7")

ax1.set_facecolor(color="#FAFAFA")
ax1.set_xlabel('Erosion rate [m/Myr]',fontsize=6 )
ax1.set_ylabel('Relief [m/m]',fontsize=6 )
ax1.set_box_aspect(0.5)

ax2.set_facecolor(color="#FAFAFA")
ax2.hist(erosion, bins=15, edgecolor="black", linewidth=0.4,color="#F6F9E7")
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

fig = plt.gcf()
fig.set_size_inches(3.5,2)
plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=700)
plt.show()


