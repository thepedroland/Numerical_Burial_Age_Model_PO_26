from AuxDataScripts.aux_functions.constant_steady_lines_model import *
import numpy as np
from matplotlib.patches import Ellipse
import matplotlib.legend_handler as handler
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, LogLocator, NullFormatter
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.patches as patches

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
file_path = main_path + "/support/data/samples_amazon_23_data.csv"

fig_dir = main_path + "/generate_figures/figures"
fig_name = "sec_equi"
mpl.rcParams['font.family'] = 'Arial'

st_model = burial_exposure_model()

class HandlerEllipse(handler.HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        # Create an ellipse centered in the legend handle area
        center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
        p = Ellipse(xy=center, width=width*0.7, height=height,angle=15)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]

samples_list= ["SB-011","SB-017"]

import matplotlib.cm as cm

fig, ax = plt.subplots()
fig.set_size_inches(2, 2)
# Load data once, outside the loop
df_data_samples = pd.read_csv(file_path)
df_data_samples["ratio_c26_c10"] = df_data_samples['n26_measured'] / df_data_samples['n10_measured']

ellipse_handles = []      # for the per-sample ellipse legend
depth_handles = []        # for the per-sample depth/exposure legend

for i, sample_id in enumerate(samples_list):
    print(f"Secular plot for sample: {sample_id}")

    observed_c10 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n10_measured'].item())
    observed_c26 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n26_measured'].item())

    obs_dev_c10 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n10'].values[0]
    obs_dev_c26 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n26'].values[0]

    depth_min_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_min'].values[0]
    depth_max_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_max'].values[0]

    color_sample = ([214, 61, 153])
    rgb_base_sample = [x / 255.0 for x in color_sample]
    color_fill_sample = tuple(rgb_base_sample + [0.05])
    color_edge_sample = tuple(rgb_base_sample + [0.9])

    color_island = ([252, 254, 236],[236, 243, 254])
    rgb_base_island = [x / 255.0 for x in color_island[i]]
    color_fill_island = tuple(rgb_base_island)

    depth_sample = (depth_max_sample + depth_min_sample) / 2
    if sample_id == "SB-011":
        depth_sample = depth_min_sample

    theta = np.linspace(0, 2 * np.pi, 100)
    x0 = observed_c10
    y0 = observed_c26 / observed_c10
    dx_1s = obs_dev_c10
    dy_1s = y0 * np.sqrt(
        (obs_dev_c10 / observed_c10) ** 2
        + (obs_dev_c26 / observed_c26) ** 2
    )

    ## Outer (2-sigma)
    x_2s = x0 + (2 * dx_1s) * np.sin(theta)
    y_2s = y0 + (2 * dy_1s) * np.cos(theta)
    ax.fill(
        x_2s, y_2s,
        facecolor=tuple(color_fill_sample),
        edgecolor=tuple(color_edge_sample), linewidth=0.1,
    )

    ## Inner (1-sigma)
    x_1s = x0 + dx_1s * np.sin(theta)
    y_1s = y0 + dy_1s * np.cos(theta)
    ax.fill(
        x_1s, y_1s,
        facecolor=tuple(color_fill_sample),
        edgecolor=tuple(color_edge_sample),
        linewidth=0.1,
    )

    # ax.annotate(f"{sample_id[0:2]+sample_id[-2:]}\n",((x0 + (2 * dx_1s)),(y0)),alpha=0.8,fontsize=7,fontweight='bold',color=rgb_base_sample)

    st_model.plot_steady_state_model_depth(depth_sample, color="#B3B3B3")

    # Collect legend handles instead of drawing a legend per sample
    h_depth = plt.Rectangle((0, 0), 1, 1, facecolor=color_fill_island, alpha=0.5,
                             edgecolor='black', linestyle='-', linewidth=0.8)
    depth_handles.append(h_depth)

    st_model = burial_exposure_model()

    N_be_series, N_al_series = st_model.plot_steady_state_model_depth(depth_sample, color="#B3B3B3")


####----Axis formatting (done once)----####
ax.set_xlabel(r'$^{10}\mathrm{Be}$ Concentration [at/g] ', fontsize=6)
ax.set_ylabel(r'$^{26}\mathrm{Al}/^{10}\mathrm{Be}$', fontsize=6)
ax.set_facecolor(color="#FAFAFA")
ax.tick_params(width=0.5)

ax.xaxis.set_major_locator(FixedLocator([1e4]))
ax.set_xticklabels(["$10^4$"], fontsize=6, fontname="Arial")
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=12))
ax.xaxis.set_minor_formatter(NullFormatter())

y_ticks = [3, 5, 7]
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.set_yticklabels(["3","5","7"], fontsize=7, fontname="Arial")
#
# ax.legend(handles=depth_handles,loc="lower right",frameon=False,borderaxespad=0.8,handletextpad=0.2,
#     ncol=1, fontsize=10, columnspacing=1)

ax.set_box_aspect(1)
ax.set_ylim(3,8.5)
ax.set_xlim(9e1, 2e5)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)

fig_name = "Fig2B_secular_equilibrium_sb11_sb17"
plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=300, bbox_inches="tight")
plt.savefig(f"{fig_dir}/SVG/SVG_{fig_name}.svg", format="svg", bbox_inches="tight")

plt.show()

####---the exact same but for the sample bv018

fig, ax = plt.subplots()
fig.set_size_inches(2, 2)
# Load data once, outside the loop
df_data_samples = pd.read_csv(file_path)
df_data_samples["ratio_c26_c10"] = df_data_samples['n26_measured'] / df_data_samples['n10_measured']

ellipse_handles = []      # for the per-sample ellipse legend
depth_handles = []        # for the per-sample depth/exposure legend

sample_id = "BV-018"

print(f"Secular plot for sample: {sample_id[:2]+sample_id[-2:]}")

observed_c10 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n10_measured'].item())
observed_c26 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n26_measured'].item())

obs_dev_c10 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n10'].values[0]
obs_dev_c26 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n26'].values[0]

color_sample = ([214, 61, 153])
rgb_base_sample = [x / 255.0 for x in color_sample]
color_fill_sample = tuple(rgb_base_sample + [0.05])
color_edge_sample = tuple(rgb_base_sample + [0.9])

color_island = ([252, 254, 236],[236, 243, 254])
rgb_base_island = [x / 255.0 for x in color_island[i]]
color_fill_island = tuple(rgb_base_island)

depth_sample = 700

theta = np.linspace(0, 2 * np.pi, 100)
x0 = observed_c10
y0 = observed_c26 / observed_c10
dx_1s = obs_dev_c10
dy_1s = y0 * np.sqrt(
    (obs_dev_c10 / observed_c10) ** 2
    + (obs_dev_c26 / observed_c26) ** 2
)

## Outer (2-sigma)
x_2s = x0 + (2 * dx_1s) * np.sin(theta)
y_2s = y0 + (2 * dy_1s) * np.cos(theta)
ax.fill(
    x_2s, y_2s,
    facecolor=tuple(color_fill_sample),
    edgecolor=tuple(color_edge_sample), linewidth=0.1,
)

## Inner (1-sigma)
x_1s = x0 + dx_1s * np.sin(theta)
y_1s = y0 + dy_1s * np.cos(theta)
ax.fill(
    x_1s, y_1s,
    facecolor=tuple(color_fill_sample),
    edgecolor=tuple(color_edge_sample),
    linewidth=0.1,
)

# ax.annotate(f"{sample_id[0:2]+sample_id[-2:]}\n",((x0 - (2 * dx_1s)+1e4),(y0)-1),alpha=0.8,fontsize=7,fontweight='bold',color=rgb_base_sample,ha='left')

st_model.plot_steady_state_model_depth(depth_sample, color="#B3B3B3")

# Collect legend handles instead of drawing a legend per sample
h_depth = plt.Rectangle((0, 0), 1, 1, facecolor=color_fill_island, alpha=0.5,
                         label=f"Depth = {depth_sample/1e2:.0f}m",
                         edgecolor='black', linestyle='-', linewidth=0.8)
depth_handles.append(h_depth)

####----Axis formatting (done once)----####
ax.set_xlabel(r'$^{10}\mathrm{Be}$ Concentration [at/g] ', fontsize=7)
ax.set_ylabel(r'$^{26}\mathrm{Al}/^{10}\mathrm{Be}$', fontsize=7)
ax.set_facecolor(color="#FAFAFA")

ax.xaxis.set_major_locator(FixedLocator([1e4]))
ax.set_xticklabels(["$10^4$"], fontsize=7, fontname="Arial")
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=12))
ax.xaxis.set_minor_formatter(NullFormatter())

y_ticks = [3, 5, 7]
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.set_yticklabels(["3","5","7"], fontsize=7, fontname="Arial")
#
# ax.legend(handles=depth_handles,loc="lower right",frameon=False,borderaxespad=0.8,handletextpad=0.2,
#     ncol=1, fontsize=10, columnspacing=1)

for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)

ax.annotate(f"{sample_id[0:2]+sample_id[-2:]}\n",((x0 + (2 * dx_1s)),(y0-1)),alpha=0.8,fontsize=7,fontweight='bold',color=rgb_base_sample)

ax.set_box_aspect(1)
ax.set_ylim(4,8.5)
ax.set_xlim(5e3, 2e5)
ax.tick_params(axis='both', width=0.5, labelsize=6)

fig_name = "FigS5_secular_equilibrium_sb18"
plt.savefig(f"{fig_dir}/supporting_figures/{fig_name}.png", dpi=300, bbox_inches="tight")
plt.show()