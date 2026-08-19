import numpy as np
import pmagpy.pmag as pmag
import pandas as pd
import sys
import os
from tqdm import tqdm
import mcadam
import matplotlib.pyplot as plt

main_path = os.path.dirname(os.path.realpath(__file__))
add_path = os.path.join(main_path, "support", "../Production_Rates_Calculator-main", "src")
sys.path.insert(0, add_path)

class calc_Rc:
    def __init__(self):
        self.time = np.arange(0, 35, 1E-3) #35 million years as the limit
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
        mcadam_medians = mcadam.calc_mcadam_medians(self.time)

        for x in range(len(self.pl_df)):
            for i in range(len(mcadam_medians)):
                Rc_calc = (((mcadam_medians[i] * mu_knot * c) / (16 * np.pi * R ** 2)) * ((np.cos(np.deg2rad(
                    self.pl_df.iloc[x, i]))) ** 4)) / 10 ** 9  # divided by 10^9 to convert [V] to [GV]
                Rc_list.append(Rc_calc)

        Rc = pd.DataFrame([(Rc_list[n:n + len(self.time)]) for n in range(0, len(Rc_list), len(self.time))])
        plt.figure(figsize=(10, 6),facecolor="white",alpha=0.1)
        plt.plot(((np.arange(0,700,1))*50000)/1e6,Rc_list, label="Rc-MCADAM")
        ax = plt.gca()
        ax.set_facecolor("#EAFAF4")
        plt.xlabel("Age (Ma)",fontsize=16)
        plt.ylabel("Rc (GV)",fontsize=16)
        ax.set_xticklabels(ax.get_xticks(), fontsize=14)
        ax.set_yticklabels(ax.get_yticks(), fontsize=14)
        plt.legend()
        plt.tight_layout()
        # Save Rc DataFrame to CSV file
        # output_dir = "/Users/pedro_oliveira/Documents/Projects_PhD/deposition_models/support"
        # os.makedirs(output_dir, exist_ok=True)
        # output_file = os.path.join(output_dir, "Rc_results.csv")
        # Rc.to_csv(output_file, index=False)
        # print(f"Rc DataFrame saved to {output_file}")
        #
        # fig_dir ="/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/1_PhD_PAPER_1/images"
        # fig_name = f"Rc_variation_time"
        # plt.savefig(f"{fig_dir}/{fig_name}.png", dpi=300, bbox_inches="tight")
        # plt.show()


if __name__ == "__main__":
    rc = calc_Rc()
    rc.calc_df_paleo()
    rc.calc_Rc()
