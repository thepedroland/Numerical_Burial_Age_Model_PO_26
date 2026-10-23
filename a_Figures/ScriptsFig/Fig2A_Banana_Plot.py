from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from z_AuxDataScripts.aux_scripts.constant_steady_lines_model import burial_exposure_model
from z_AuxDataScripts.aux_scripts.nuclide_prod_concentration import *
import matplotlib.legend_handler as handler
import matplotlib as mpl
import os
import pandas as pd
from matplotlib.ticker import FixedLocator
import warnings

mpl.rcParams['font.family'] = 'Arial'
warnings.filterwarnings('ignore')
#------SET UP PLOT------#

sigma = "1-sigma"
short_sample_names = True
Rc_value = 'mean' #can be mean, min or max within the 40Myrs
density = 1.7

##------------------------##
print(f"\u25B6Running banana diagram using LSDn_{Rc_value}")

class HandlerEllipse(handler.HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        # Create an ellipse centered in the legend handle area
        center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
        p = Ellipse(xy=center, width=width*0.7, height=height,angle=15)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]

####----IMPORTING DATA----########
main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
file_path = main_path + "/support/data/samples_amazon_23_data.csv"

fig_dir = main_path + "/generate_figures/figures"
fig_name = "Fig2A_banana_plot_diagram"

df_data_samples = pd.read_csv(file_path)

sample_names = df_data_samples['sample_names'].values
n10 = df_data_samples['n10_measured'].values
n26 = df_data_samples['n26_measured'].values
std_dev_n10 = (df_data_samples['std_dev_n10'].values)
std_dev_n26 = (df_data_samples['std_dev_n26'].values)
description_sample = df_data_samples['description'].values
depth_min = df_data_samples['depth_min'].values
depth_max = df_data_samples['depth_max'].values

if short_sample_names == True:
    sample_names =  df_data_samples['simple_names'].values

df_data_samples["ratio_n26_n10"] = n26 / n10
ratio_n26_n10 = df_data_samples['ratio_n26_n10'].values

####----Colors----########
flood = [143, 116, 246]
burial = [214, 61, 153]
surface = [107, 168, 255]
color_fill = [246, 228, 172]

color_ellipse = {
    "flood": tuple([x / 255.0 for x in flood] + [0.05]),
    "burial": tuple([x / 255.0 for x in burial] + [0.05]),
    "surface": tuple([x / 255.0 for x in surface] + [0.05])
}
color_edge = {"flood": tuple([x / 255.0 for x in flood]),
    "burial": tuple([x / 255.0 for x in burial]),
    "surface": tuple([x / 255.0 for x in surface])
              }

##----------PRODUCTION ZONE----##

lines_model = burial_exposure_model()
lines_model.plot_steady_state_model(Rc_value=Rc_value)

#######----PLOTTING----########

h_purple= Ellipse((0,0), 0.2, 0.2,angle=45, facecolor=color_ellipse["flood"], label='Seasonally \nflooded',
                 edgecolor=color_edge["flood"],linewidth=0.5)
h_red = Ellipse((0,0), 0.2, 0.2, facecolor=color_ellipse["burial"], label='Buried',
                edgecolor=color_edge["burial"],linewidth=0.5)
h_blue = Ellipse((0,0), 0.2, 0.2, facecolor=color_ellipse["surface"], label='Permanent \nflow',
                 edgecolor=color_edge["surface"],linewidth=0.5)

text_font_size =  10
font_size_labels = 8

theta = np.linspace(0, 2 * np.pi, 100)

if sigma == "2-sigma":
    std_dev_n10 *= 2
    std_dev_n26 *= 2

for i,sample in enumerate(sample_names):
    x_be = n10[sample_names == sample] + std_dev_n10[sample_names == sample] * np.sin(theta)
    y_val = ratio_n26_n10[sample_names == sample]
    y_err = (ratio_n26_n10[sample_names == sample]) *\
    (np.sqrt((std_dev_n10[sample_names == sample] / n10[sample_names == sample]) ** 2
             + (std_dev_n26[sample_names == sample] / n26[sample_names == sample]) ** 2))
    y_ratio = y_val + y_err * np.cos(theta)

    plt.fill(x_be, y_ratio, facecolor=color_ellipse[description_sample[i]],
             edgecolor=color_edge[description_sample[i]], linewidth=0.5)

    plt.scatter(n10[i],ratio_n26_n10[i], color=color_edge[description_sample[i]],marker="o",s=0.1)


    ax=plt.gca()

    if sample == "BE-002" or sample == "BE02":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 13000),
                 ratio_n26_n10[sample_names == sample] + 0.1,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='right', va='bottom')
    elif sample == "RI-046" or sample == "RI46":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 10000),
                 ratio_n26_n10[sample_names == sample] - 0.05,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='right', va='bottom')
    elif sample == "IP-038" or sample == "IP38":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample])),
                 ratio_n26_n10[sample_names == sample] - 0.15,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "RA-051" or sample == "RA51":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample])),
                 ratio_n26_n10[sample_names == sample] + 0.15,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "RA-050" or sample == "RA50":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 10000),
                 ratio_n26_n10[sample_names == sample] + 0.17,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "PE-053" or sample == "PE53":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample])),
                 ratio_n26_n10[sample_names == sample] - 0.25,
                 str(sample_names[sample_names == sample][0])[-2:],
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "PP-036" or sample == "PP36":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 10000),
                 ratio_n26_n10[sample_names == sample] - 0.05,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='right', va='bottom')
    elif sample == "IC-035" or sample == "IC35":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) + 1000),
                 ratio_n26_n10[sample_names == sample] + 0.05,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "RI-048" or sample == "RI48":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 10000),
                 ratio_n26_n10[sample_names == sample] - 0.05,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='right', va='bottom')
    elif sample == "RV-054" or sample == "RV54":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 20000),
                 ratio_n26_n10[sample_names == sample],
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='left', va='bottom')
    elif sample == "RC-044" or sample == "RC44":
        plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) - 20000),
                 ratio_n26_n10[sample_names == sample] - 0.05,
                 str(sample_names[sample_names == sample][0][-2:]),
                 fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                 ha='right', va='bottom')
    else:
        if sample in ["SB11", "SB17"]:
            x = float((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) + (
                    (n10[sample_names == sample]) + (std_dev_n10[sample_names == sample])) / 100))
            y = float(ratio_n26_n10[sample_names == sample] - 0.1)
            col = color_edge[description_sample[sample_names == sample][0]]
            core_text = f"Core\n{float(depth_min[sample_names == sample]) / 100:.0f}m - {float(depth_max[sample_names == sample]) / 100:.0f}m"
            plt.text(x, y, str(sample_names[sample_names == sample][0]) + "\n\n",
                     fontsize=font_size_labels, fontweight='bold', color=col,
                     ha='left', va='bottom')
            plt.text(x, y, "\n\n" + core_text,
                     fontsize=font_size_labels, fontweight='normal', color=col,
                     ha='left', va='bottom')

        elif sample == "SB13":
            x = float((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) + (
                    (n10[sample_names == sample]) + (std_dev_n10[sample_names == sample])) / 100))
            y = float(ratio_n26_n10[sample_names == sample] - 0.1)
            col = color_edge[description_sample[sample_names == sample][0]]
            core_text = f"Core\n{float(depth_min[sample_names == sample]) / 100:.0f}m - {float(depth_max[sample_names == sample]) / 100:.0f}m"
            plt.text(x, y, str(sample_names[sample_names == sample][0]) + "\n\n",
                     fontsize=font_size_labels, fontweight='bold', color=col,
                     ha='left', va='bottom')
            plt.text(x, y, "\n\n\n\n" + core_text,
                     fontsize=font_size_labels, fontweight='normal', color=col,
                     ha='left', va='bottom')

        elif sample == "BV18":
            x = float((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) + (
                    (n10[sample_names == sample]) + (std_dev_n10[sample_names == sample])) / 100))
            y = float(ratio_n26_n10[sample_names == sample] - 0.1)
            col = color_edge[description_sample[sample_names == sample][0]]
            plt.text(x, y, str(sample_names[sample_names == sample][0]) + "\n",
                     fontsize=font_size_labels, fontweight='bold', color=col,
                     ha='left', va='bottom')
            plt.text(x, y, "\nTerrace face",
                     fontsize=font_size_labels, fontweight='normal', color=col,
                     ha='left', va='bottom')
        else:
            plt.text((n10[sample_names == sample]) + ((std_dev_n10[sample_names == sample]) + (
                        (n10[sample_names == sample]) + (std_dev_n10[sample_names == sample])) / 100),
                     ratio_n26_n10[sample_names == sample] - 0.05,
                     str(sample_names[sample_names == sample][0][-2:]),
                     fontsize=font_size_labels, fontweight='bold', color=color_edge[description_sample[sample_names == sample][0]],
                     ha='left', va='bottom')


ax.set_xscale("log")
ax.set_facecolor(color="#FAF4EF")
ax.set_xlabel("$^{10}$Be Concentration [at/g]", fontsize=text_font_size,fontname="Arial")
ax.set_ylabel("$^{26}$Al/$^{10}$Be", fontsize=text_font_size,fontname="Arial")
# x_ticks = [1e4, 1e5, 1e6]
# ax.xaxis.set_major_locator(FixedLocator(x_ticks))
# # Format them as scientific notation or however you prefer
# ax.set_xticklabels(["$10^4$", "$10^5$", "$10^6$"], fontsize=12, fontname="Arial")

# --- Fix Y-Axis (Linear Scale) ---
# This solves your original request: Only 3, 4, 5, 6 showing
y_ticks = [3, 4, 5, 6,7]
ax.yaxis.set_major_locator(FixedLocator(y_ticks))
ax.set_yticklabels(["3", "4", "5", "6","7"], fontsize=text_font_size, fontname="Arial")

# Set limits AFTER setting ticks to ensure they don't get overridden
ax.set_xlim(1e4, 1e6)
ax.set_ylim(3.5, 8)

leg_eli = ax.legend(handles=[h_blue,h_purple,h_red],
          handler_map={Ellipse: HandlerEllipse()},ncols=2,columnspacing=0.2,
          loc='upper left',
         facecolor= "#FAF4EF",
        framealpha = 1,
                    edgecolor="#FAF4EF",
          frameon=False,
          fontsize=8,
          labelcolor=[color_edge["surface"],color_edge["flood"],color_edge["burial"]],
          handleheight=2,  # Makes the area tall enough for an ellipse
          handlelength=1,bbox_to_anchor=(0.05, 0.8, 1, 0.2),
          handletextpad=0.1,
          borderaxespad=0.2)
ax.add_artist(leg_eli)
plt.legend(
    handles=[plt.Rectangle((0, 0), 0.2, 0.2, facecolor="#FAF4EF", label="Complex exposure/Burial zone", edgecolor='black', linestyle='-',linewidth=0.1),
             plt.Rectangle((0, 0), 0.2, 0.2, facecolor=tuple([x / 255.0 for x in color_fill]), alpha=0.5,linewidth=0.1,
                           label="Simple exposure", edgecolor='black', linestyle='-')],
    bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",borderaxespad=-0.5, ncol=2, fontsize=8,handletextpad=0.3,
    frameon=False,columnspacing=1)

# plt.annotate(f"{sigma}",(9e5,7.5))
fig = plt.gcf()
fig.set_size_inches(4,4.2)

plt.savefig(f"{fig_dir}/{fig_name}_{scaling_method}_{Rc_value}.png", dpi=300, bbox_inches="tight")
plt.savefig(f"{fig_dir}/SVG/SVG_{fig_name}.svg", format="svg", bbox_inches="tight")

plt.show()
plt.close()

