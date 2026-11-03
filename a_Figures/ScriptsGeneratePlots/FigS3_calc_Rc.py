import sys
import os

main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

add_path = os.path.join(main_path,"z_ExtraAnalyzes/Production_Rates_Calculator-main", "src")
sys.path.insert(0, add_path)

import numpy as np
import pmagpy.pmag as pmag
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from mcadam import calc_mcadam_medians

plt.rcParams["font.family"] = "Arial"


class calc_Rc:
    def __init__(self):
        self.time = np.arange(0, 40, 1E-3) #35 million years as the limit
        pass
    def calc_df_paleo(self):
        vals = []
        for j in tqdm(self.time):
            data = ['SA', -2, -58, j]
            pmag.apwp(data, print_results=False)  # change to true if you want to see the output
            vals.append(pmag.apwp(data))

        df = pd.DataFrame(vals)
        df.columns = ['Age', 'Paleolat', 'Dec', 'Inc', 'Pole_lat', 'Pole_Long']
        Paleolat = df['Paleolat']

        self.pl_df = pd.DataFrame(
            [(Paleolat.values.tolist()[n:n + len(self.time)]) for n in range(0, len(Paleolat.values.tolist()), len(self.time))])


    def calc_Rc(self):
        mu_knot = (1.256 * 10 ** -6) * 10 ** 22  # m kg s-2 A-2, permeability of free space.
        c = 299792458  # m/s, speed of light.
        R = 6.378 * 10 ** 6  # m, radius of Earth.
        Rc_list = []
        time_list = []


        """
        This Rc calculation will run the MCADAM pmag dataset only

        """
        mcadam_medians = calc_mcadam_medians(self.time)

        for x in range(len(self.pl_df)):
            for i in range(len(mcadam_medians)):
                Rc_calc = (((mcadam_medians[i] * mu_knot * c) / (16 * np.pi * R ** 2)) * ((np.cos(np.deg2rad(
                    self.pl_df.iloc[x, i]))) ** 4)) / 10 ** 9  # divided by 10^9 to convert [V] to [GV]
                Rc_list.append(Rc_calc)

        Rc = pd.DataFrame([(Rc_list[n:n + len(self.time)]) for n in range(0, len(Rc_list), len(self.time))])
        plt.figure(figsize=(12, 6),facecolor="white",alpha=0.1)
        plt.plot(((np.arange(0,800,1))*50000)/1e6,Rc_list, label="Cutoff Rigidity (Rc) - based on MCADAM",color="gray")
        ax = plt.gca()
        ax.set_facecolor("#FAFAFA")
        plt.xlabel("Age [Ma]",fontsize=26)
        plt.ylabel("Cutoff Rigidity - Rc [GV]",fontsize=26)
        ax.set_xticks(np.arange(0, 41, 5))
        ax.set_yticks(np.arange(4, 15, 2))
        ax.set_xticklabels(ax.get_xticks(), fontsize=22)
        ax.set_yticklabels(ax.get_yticks(), fontsize=22)
        plt.legend(fontsize=20)
        plt.tight_layout()
        print(main_path)
        output_dir = os.path.join(main_path, "z_AuxData_Scripts/data")
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, "Rc_results.csv")
        Rc.to_csv(output_file, index=False)

        print(f"Rc DataFrame saved to {output_file}")

        fig_dir = os.path.join(main_path, "a_Figures","Plots","SupMaterial")
        print(fig_dir)
        os.makedirs(fig_dir, exist_ok=True)

        fig_name = "FigS8_Rc_variation_time"
        fig_file = os.path.join(fig_dir, f"{fig_name}.png")

        plt.savefig(fig_file, dpi=300, bbox_inches="tight")
        plt.show()


if __name__ == "__main__":
    rc = calc_Rc()
    rc.calc_df_paleo()
    rc.calc_Rc()
