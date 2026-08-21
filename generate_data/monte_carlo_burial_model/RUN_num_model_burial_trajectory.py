import warnings
warnings.filterwarnings('ignore', category=SyntaxWarning)
from types import SimpleNamespace

import numpy as np
import pandas as pd
from BMI_num_model_burial_trajectory import deposition_trajectories
import torch
from tqdm import tqdm
import os
from multiprocessing import Pool
from support.aux_functions.misc_functions import load_dataset,save_arguments_to_excel

def init_worker(var_,config):
    global cfg
    global var

    var = var_
    cfg = config
    torch.set_num_threads(1)

rng = np.random.default_rng()

def start_batch_simulation(trial):

    dm = deposition_trajectories(var.measured_n10, var.measured_n26, var.stn_dev_n10, var.stn_dev_n26)

    initial_n10 = np.round(rng.uniform(var.measured_min_n10, var.measured_max_n10),2)
    initial_ratio = np.round(rng.uniform(var.measured_ratio_min_c, var.measured_ratio_max_c),2)
    burial_depth = np.round(rng.uniform(var.burial_depth_min_sample, var.burial_depth_max_sample),1)
    time_burial = np.round(rng.uniform(cfg.time_burial_min, cfg.time_burial_max),0)
    time_erosion = np.round(rng.uniform(cfg.time_erosion_min, cfg.time_erosion_max),0)
    depo_rate = 10 **(rng.uniform(cfg.dep_low.item(), cfg.dep_high.item()))
    erosion_rate = rng.uniform(cfg.ero_low, cfg.ero_high)

    if cfg.sample_id != "BV-018":
        time_erosion = 0
        erosion_rate = 0
        final_depth = burial_depth

    else:
        final_depth = np.round(rng.uniform(var.final_depth_min_sample, var.final_depth_max_sample), 1)

    marker = False
    arguments_to_run = {
        "initial_n10": initial_n10, "initial_ratio": initial_ratio, "burial_depth": burial_depth,"final_depth":final_depth,
        "sample_id": cfg.sample_id,"reference_sample":cfg.reference_sample, "time_burial": time_burial,"time_erosion":time_erosion,
        "depo_rate":  depo_rate, "density": cfg.density,"erosion_rate": erosion_rate
    }

    while not marker:
        dm.setup_model(arguments_to_run)
        check = dm.check_simple_exposure_region()

        if check == "REJECTED BY DEPOSITION RATE":
            depo_rate = 10 **(rng.uniform(cfg.dep_low.item(), cfg.dep_high.item()))
            arguments_to_run["depo_rate"] = depo_rate
        elif check == "REJECTED BY EXPOSURE REGION":
            initial_ratio = rng.uniform(var.measured_ratio_min_c, var.measured_ratio_max_c)
            arguments_to_run["initial_ratio"] = initial_ratio
        elif check == "REJECTED BY EROSION RATE":
            erosion_rate = rng.uniform(cfg.ero_low, cfg.ero_high)
            time_erosion = np.round(rng.uniform(cfg.time_erosion_min, cfg.time_erosion_max), 0)
            arguments_to_run["erosion_rate"] = erosion_rate
            arguments_to_run["time_erosion"] = time_erosion
        else:
            marker = True

    return dm.run_model()
if __name__ == "__main__":

    main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    path_table = os.path.join(main_path, "generate_data", "python_data_results")

    sample_id = "BV-018"
    reference_sample = "Surface" #use Surface when starting from samples at the surface

    ###----MODEL PARAMETERS-----####
    density = 1.7
    n_trials = 10000

    time_burial_min, time_burial_max = 5_000_000, 30_000_000
    time_erosion_min, time_erosion_max = 500_000, 3_000_000

    depo_rate_min, depo_rate_max = 0.0001, 1.0  # cm/yr
    erosion_min, erosion_max = 1e-4,3e-3  # cm/yr

    # log-space bounds, used later for log-uniform sampling
    dep_low, dep_high = torch.log10(torch.tensor(depo_rate_min)), torch.log10(torch.tensor(depo_rate_max))
    # ero_low, ero_high = torch.log10(torch.tensor(erosion_min)), torch.log10(torch.tensor(erosion_max))
    ero_low,ero_high = erosion_min,erosion_max

    print(f"Running {sample_id} starting from {reference_sample} using {density} g/cm3")
    var = load_dataset(sample_id,reference_sample)

    all_results_csv = []
    all_trajectories_pkl = [] #saves trajectory series - n10 and ratio for each timestep

    path_save_csv = os.path.join(path_table, f"results_data/Results_[{sample_id}]_R{reference_sample}_D{density}.csv")
    path_save_pkl = os.path.join(path_table, f"results_data/Trajectories_[{sample_id}]_R{reference_sample}_D{density}.pkl")

    config = SimpleNamespace(
        sample_id=sample_id,reference_sample=reference_sample, density=density,path_table=path_table,
        time_burial_min=time_burial_min, time_burial_max=time_burial_max,
        time_erosion_min=time_erosion_min, time_erosion_max=time_erosion_max,
        dep_low=dep_low, dep_high=dep_high, ero_low=ero_low, ero_high=ero_high,
    )

    save_arguments_to_excel(var, config,path_table)

    with Pool(processes=4,initializer=init_worker, initargs=(var,config,)) as pool:

        for i, result in enumerate(tqdm(pool.imap_unordered(start_batch_simulation, range(n_trials)),desc="Trial runs", total=n_trials,unit="simulations",leave=False)):

            all_results_csv.append(result[0])
            all_trajectories_pkl.append(result[1])

            if (i + 1) % 10 == 0 or (i + 1) == n_trials:
                    pd.DataFrame(all_results_csv).to_csv(path_save_csv, index=False)
                    df_valid = pd.DataFrame(all_results_csv)
                    valid_count = (df_valid["Solution"] == True).sum()
                    pd.DataFrame(all_trajectories_pkl).to_pickle(path_save_pkl)
                    print("Valid solutions:",valid_count)
