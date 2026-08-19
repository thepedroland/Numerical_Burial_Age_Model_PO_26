import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


plt.rcParams['font.family'] = 'Arial'

area_ne_contribution = 1047010623.1604749  # m2
area_sw_contribution = 2984669853.4390244  # m2

# Base Guiana sediment supply (100% scenario)
vol_supply_guiana_base = 5 * 500 * 20  # m/yr(rate) * m(width) * m(depth) -> m3/yr

erosion_rates_list = np.linspace(1, 29, 500)   # m/Myr — sediment supply rate scenarios
channel_valley_area = 1107717131.1457663       # m2
depth_list = np.arange(0, 100)                 # m

# The three Guiana-supply scenarios to plot
guiana_supply_fractions = {
    "100%": vol_supply_guiana_base*1,
    "50%": vol_supply_guiana_base*0.5,
    "25%": vol_supply_guiana_base*0.25,
}

output_dir = "/Users/pedro_oliveira/Library/CloudStorage/OneDrive-CityUniversityofNewYork/PhD_LIFE/1_PhD_PAPER_1/images"

for label, fraction in guiana_supply_fractions.items():
    vol_supply_guiana = vol_supply_guiana_base * fraction

    time_to_fill_list = []
    depth_plot_list = []
    erosion_plot_list = []

    for erosion_rate in erosion_rates_list:
        volume_ne_contribution = area_ne_contribution * erosion_rate
        volume_sw_contribution = area_sw_contribution * erosion_rate
        total_flux = volume_ne_contribution + volume_sw_contribution + vol_supply_guiana  # m3/Myr

        for depth in depth_list:
            channel_volume = channel_valley_area * depth
            time_to_fill_list.append(channel_volume / total_flux)
            depth_plot_list.append(depth)
            erosion_plot_list.append(erosion_rate)

    time_to_fill_arr = np.array(time_to_fill_list)
    depth_plot_arr = np.array(depth_plot_list)
    erosion_plot_arr = np.array(erosion_plot_list)

    fig, ax = plt.subplots(figsize=(8, 6))

    sc = ax.scatter(time_to_fill_arr, depth_plot_arr * -1, c=erosion_plot_arr,
                     cmap='viridis', s=10)

    plt.colorbar(sc, ax=ax, label="Erosion rate [m/Myr]")
    ax.set_xlabel("Time to fill [Myr]", fontsize=14, fontweight='bold')
    ax.set_ylabel("Depth of channel valley [m]", fontsize=14, fontweight='bold')
    ax.set_title(f"Guiana sediment supply = {label}", fontsize=13, fontweight='bold')
    ax.set_xticks(np.arange(0, 30, 2))
    ax.tick_params(axis='both', labelsize=12)
    # ax.hlines(-37.5, 0, 30, color='black')

    # --- Small inset graph: Time (x) vs Erosion rate (y), colored by depth ---
    axins = inset_axes(ax, width="30%", height="30%", loc='upper right', borderpad=2)
    sc_in = axins.scatter(time_to_fill_arr, erosion_plot_arr, c=depth_plot_arr,
                           cmap='cividis', s=3)
    axins.set_xlabel("Time [Myr]", fontsize=8)
    axins.set_ylabel("Erosion rate [m/Myr]", fontsize=8)
    axins.tick_params(axis='both', labelsize=7)
    axins.set_title("Depth 0–100 m", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/sediment_calculation_{label.replace('%', 'pct')}.png")
    plt.show()