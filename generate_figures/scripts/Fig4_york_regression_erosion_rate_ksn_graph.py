
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matlab.engine
import os

main_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
fig_dir = main_path + "/generate_figures/figures"


eng = matlab.engine.start_matlab()
mat_file_path = main_path + "/support/aux_functions/mat_codes"
eng.addpath(mat_file_path)

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

coeff_relief,n_relief,MSWD_relief,MSWD_std_relief,coeff_err_relief,x_plot_relief,y_plot_relief = eng.MC_York(matlab.double(0),matlab.double(erosion),
                                    matlab.double(relief),matlab.double(dev_ero),matlab.double(std_relief),
                                    nargout=7)

fig,ax = plt.subplots()
x_plot_relief = np.array(x_plot_relief[0][1:]).reshape(-1)
y_plot_relief = np.array(y_plot_relief[0][1:]).reshape(-1)
ax.plot(x_plot_relief, y_plot_relief, color="#BFBF9B", linewidth=1.5)

# Add slope (mn) and MSWD text to the Ksn plot
ax.text(0.8, 0.9, r"SPIM $\it{n}$: "+f"{n_relief:.2f}\nMSWD: {MSWD_relief:.2f}",
         transform=ax.transAxes, fontsize=8, bbox=dict(facecolor="white", alpha=0.7))

color = drainage
# ax.scatter(erosion, ksn,c=color,s=10,zorder=2)
ax.errorbar(erosion, relief,xerr=dev_ero,yerr=std_relief,marker='o',
         mec='black', ms=5, mew=0.6,linestyle='None',ecolor="#2C2C1C",zorder=1,elinewidth=0.9,c="white")

ax.set_facecolor(color="#FAFAFA")
ax.set_xlabel('Erosion rate [m/Myr]',fontsize=10)
ax.set_ylabel('Relief [m/m]',fontsize=10)
ax.set_box_aspect(0.5)

fig = plt.gcf()
fig.set_size_inches(3.5,2.3)
plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=700, bbox_inches="tight")
plt.show()
