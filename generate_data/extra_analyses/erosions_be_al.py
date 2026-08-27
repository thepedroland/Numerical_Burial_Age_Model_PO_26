import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import numpy as np
import os
from datetime import datetime
from adjustText import adjust_text

file_erosion_csv = "/support/data/results_erosion_all_be_al.csv"

df = pd.read_csv(file_erosion_csv)
df_data = df.dropna()

st_erosion = df_data["st_erosion"].values
lm_erosion = df_data["lm_erosion"].values
lsd_erosion = df_data["lsd_erosion"].values

deviation_st_erosion = df_data["st_in_unc"].values
deviation_lm_erosion = df_data["lm_in_unc"].values
deviation_lsd_erosion = df_data["lsd_in_unc"].values

labels = df_data["sample_name"].values
labels__st = list(dict.fromkeys(labels))
labels__lm = list(dict.fromkeys(labels))
labels__lsd = list(dict.fromkeys(labels))

nuclides = df_data["nuclide"].values

dev_be_data__st_erosion= np.array(deviation_st_erosion[nuclides == "Be-10 (qtz)"])
dev_al_data__st_erosion = np.array(deviation_st_erosion[nuclides == "Al-26 (qtz)"])

dev_be_data__lm_erosion= np.array(deviation_lm_erosion[nuclides == "Be-10 (qtz)"])
dev_al_data__lm_erosion = np.array(deviation_lm_erosion[nuclides == "Al-26 (qtz)"])

dev_be_data__lsd_erosion= np.array(deviation_lsd_erosion[nuclides == "Be-10 (qtz)"])
dev_al_data__lsd_erosion = np.array(deviation_lsd_erosion[nuclides == "Al-26 (qtz)"])

be_data__st_erosion = np.array(st_erosion[nuclides == "Be-10 (qtz)"])
al_data__st_erosion = np.array(st_erosion[nuclides == "Al-26 (qtz)"])

be_data__lm_erosion= np.array(lm_erosion[nuclides == "Be-10 (qtz)"])
al_data__lm_erosion = np.array(lm_erosion[nuclides == "Al-26 (qtz)"])

be_data__lsd_erosion= np.array(lsd_erosion[nuclides == "Be-10 (qtz)"])
al_data__lsd_erosion = np.array(lsd_erosion[nuclides == "Al-26 (qtz)"])

dev_ratio__st_erosion  = (dev_be_data__st_erosion/dev_al_data__st_erosion ) * np.sqrt((dev_be_data__st_erosion  / be_data__st_erosion)**2  + (dev_al_data__st_erosion  / al_data__st_erosion)**2)
dev_ratio__lm_erosion  = (dev_be_data__lm_erosion/dev_al_data__lm_erosion ) * np.sqrt((dev_be_data__lm_erosion  / be_data__lm_erosion)**2  + (dev_al_data__lm_erosion  / al_data__lm_erosion)**2)
dev_ratio__lsd_erosion = (dev_be_data__lsd_erosion/dev_al_data__lsd_erosion ) * np.sqrt((dev_be_data__lsd_erosion / be_data__lsd_erosion)**2 + (dev_al_data__lsd_erosion / al_data__lsd_erosion)**2)


print(dev_ratio__st_erosion)


ratio__st_erosion = be_data__st_erosion/al_data__st_erosion
ratio__lm_erosion = be_data__lm_erosion/al_data__lm_erosion
ratio__lsd_erosion = be_data__lsd_erosion/al_data__lsd_erosion
fig, axes = plt.subplots(2, 3, facecolor='#F5F5F5', figsize=(14, 9), layout='constrained')

# ── Row 1: Histograms ──────────────────────────────────────────────────────────
hist_data   = [ratio__st_erosion, ratio__lm_erosion, ratio__lsd_erosion]
hist_titles = ['St', 'Lm', 'LSDn']
hist_colors = ['#E0F5E7', '#E0F5F1', '#E0EEF5']

for ax, data, title, color in zip(axes[0], hist_data, hist_titles, hist_colors):
    n, bins, patches = ax.hist(
        data,
        bins='auto',
        color=color,
        edgecolor='black',
        linewidth=0.6,
        alpha=0.85,
    )
    ax.set_title(title, fontsize=14, fontweight='semibold')
    ax.set_xlabel("E$_{Be}$/E$_{Al}$", fontsize=12)

    ax.set_ylabel('Count', fontsize=12)
    ax.set_facecolor('white')
    ax.spines[['top', 'right']].set_visible(False)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# ── Row 2: Scatter figures ───────────────────────────────────────────────────────

scatter_x = [be_data__st_erosion, be_data__lm_erosion, be_data__lsd_erosion]
scatter_y = [ratio__st_erosion, ratio__lm_erosion, ratio__lsd_erosion]
deviation = [dev_ratio__st_erosion ,dev_ratio__lm_erosion ,dev_ratio__lsd_erosion ]
scatter_labels = [labels__st, labels__lm, labels__lsd]

for ax, x, y, color,deviation, lbls in zip(axes[1], scatter_x, scatter_y, hist_colors, deviation,scatter_labels):

    # ax.scatter(x, y, color=color, alpha=0.1, edgecolors='white',
    #            linewidths=0.4, s=50)

    ax.errorbar(x, y,xerr=0,yerr=deviation,marker='o',
             mec='black', ms=5, mew=0.2,linestyle='None',ecolor="black",zorder=1,elinewidth=0.9,c="white")

    ax.axhline(y=1.0, color='red', linestyle='-', linewidth=0.5)

    for xi, yi, lbl in zip(x, y, lbls):
        ax.annotate(lbl[-2:], (float(xi), float(yi)),
                    textcoords="offset points",
                    xytext=(-5,10),
                    fontsize=7,
                    color='#333333',
                    fontweight='bold')

    ax.set_xlabel('Erosion Rate [m/Myr]', fontsize=9)
    ax.set_ylabel("E$_{Be}$/E$_{Al}$", fontsize=12)
    ax.set_facecolor('white')
    ax.spines[['top', 'right']].set_visible(False)



fig_name = "Erosion_rates_ratio_graph_hist"
plt.tight_layout()
plt.savefig(f"/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/1_PhD_PAPER_1/images/{fig_name}.png", dpi=700, bbox_inches="tight")

readme_path = os.path.join("/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/1_PhD_PAPER_1/images/README_files"
, f"README_fig_{fig_name}.txt")

# 2. Get metadata
script_path = os.path.abspath(__file__)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. Write the file to that specific path
with open(readme_path, "w") as f:
    f.write(f"# Erosion rates ratio graph&hist\n\n")
    f.write(f"Using data base in {file_erosion_csv}\n\n")
    f.write(f"The figure was generated using code: {script_path}\n")
    f.write(f"Date: {current_time}\n")

print(f"Metadata saved successfully to: {readme_path}")