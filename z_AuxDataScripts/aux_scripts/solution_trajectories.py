from matplotlib import pyplot as plt
from matplotlib.ticker import FixedLocator
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from z_AuxDataScripts.aux_scripts.constant_steady_lines_model import steady_state_model

class set_trajectories:
    def __init__(self,sample_id,reference_sample,density,folder_path,plots_path):
        self.path_fig = plots_path + f"/solution_trajectories_[{sample_id}]_D{density}.pdf"
        self.pdf = PdfPages(self.path_fig)
        self.fig, self.ax = plt.subplots(dpi=30)  # low dpi = smaller/faster pages
        self.path_pickle = folder_path + f"/NumSimResults/Trajectories_[{sample_id}]_R{reference_sample}_D{density}.pkl"
        self.df = pd.read_pickle(self.path_pickle)

    def plot_trajectories(self,x_2s, y_2s):
        for run, (be_serie, ratio_serie) in enumerate(zip(self.df["N10 series"], self.df["Ratio series"])):
            if run % 5 == 0 :
                self.ax.plot(list(be_serie), list(ratio_serie))
                self.ax.title.set_text(f"Simulation {run}")
                lines_model = steady_state_model()
                lines_between = lines_model.plot_steady_state_model(
                    Rc_value='mean', checking_only=True)

                self.ax.fill(  # <-- FIX: plt.fill -> ax.fill (consistency with 'ax')
                    x_2s, y_2s,
                    linestyle="--",
                    linewidth=0.8,alpha=0.5,
                    label=r"2$\sigma$ Error",
                )

                self.ax.semilogx()
                self.ax.set_facecolor(color="#FAF4EF")
                self.ax.set_xlabel("$^{10}$Be Concentration [at/g]", fontsize=14, fontname="Arial")
                self.ax.set_ylabel("$^{26}$Al/$^{10}$Be", fontsize=14, fontname="Arial")

                x_ticks = [1e4, 1e5, 1e6]
                self.ax.xaxis.set_major_locator(FixedLocator(x_ticks))
                self.ax.set_xticklabels(["$10^4$", "$10^5$", "$10^6$"], fontsize=12, fontname="Arial")

                y_ticks = [2,3, 4, 5, 6, 7]
                self.ax.yaxis.set_major_locator(FixedLocator(y_ticks))
                self.ax.set_yticklabels(["2","3", "4", "5", "6", "7"], fontsize=12, fontname="Arial")

                self.ax.plot(lines_between[0], lines_between[1])
                self.ax.set_xlim(1e4, 1e6)
                self.ax.set_ylim(2, 7.5)

                # --- save this batch's figure as one page in the shared PDF ---
                self.pdf.savefig(self.fig)
                self.ax.clear()  # wipe axes so next batch starts on a clean plot

        self.pdf.close()
