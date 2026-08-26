import numpy as np
import pandas as pd
from types import SimpleNamespace
import os
from datetime import datetime

def load_dataset(sample_id=None,reference_sample=None):
    try:
        main_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        file_path = os.path.join(main_path,"data", "samples_amazon_23_data.csv")
        df_data_samples = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Sample dataset not found. Please check the path for file: 'samples_amazon_23_data.csv'")

    df_data_samples = pd.read_csv(file_path)
    all_sample_names = df_data_samples['sample_names'].values
    all_n10 = df_data_samples['n10_measured'].values
    all_n26 = df_data_samples['n26_measured'].values
    all_std_dev_n10 = df_data_samples['std_dev_n10'].values
    all_std_dev_n26 = df_data_samples['std_dev_n26'].values
    all_depth_min = df_data_samples['depth_min'].values
    all_depth_max = df_data_samples['depth_max'].values
    all_description_sample = df_data_samples['description'].values

    df_data_samples["ratio_n26_n10"] = all_n26 / all_n10
    ratio_n26_n10 = df_data_samples['ratio_n26_n10'].values

    if sample_id is None:
        return all_sample_names, all_n10, all_n26,all_description_sample

    measured_n10 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n10_measured'].item())
    measured_n26 = float(df_data_samples[df_data_samples['sample_names'] == sample_id]['n26_measured'].item())

    stn_dev_n10 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n10'].values[0]
    stn_dev_n26 = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['std_dev_n26'].values[0]



    if reference_sample != "Surface":
        burial_depth_min_sample = (df_data_samples.loc[df_data_samples['sample_names'] == reference_sample]['depth_min'].values[0])-5
        burial_depth_max_sample = (df_data_samples.loc[df_data_samples['sample_names'] == reference_sample]['depth_max'].values[0])+5
        final_depth_min_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_min'].values[0]
        final_depth_max_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_max'].values[0]
        measured_min_n10 = float(df_data_samples[df_data_samples['sample_names'] == reference_sample]['n10_measured'].item()) - df_data_samples.loc[df_data_samples['sample_names'] == reference_sample]['std_dev_n10'].values[0]
        measured_max_n10 = float(df_data_samples[df_data_samples['sample_names'] == reference_sample]['n10_measured'].item()) + df_data_samples.loc[df_data_samples['sample_names'] == reference_sample]['std_dev_n10'].values[0]

        ratio_ref_idx = df_data_samples.index.get_loc(
            df_data_samples[df_data_samples['sample_names'] == reference_sample].index[0]
        )
        ratio_ref = ratio_n26_n10[ratio_ref_idx]
        y_err = (ratio_ref) * \
                    (np.sqrt((all_std_dev_n26[ratio_ref_idx] / all_n26[ratio_ref_idx]) ** 2
                             + (all_std_dev_n10[ratio_ref_idx] / all_n10[ratio_ref_idx]) ** 2))
        measured_ratio_min_c = ratio_ref - y_err
        measured_ratio_max_c = ratio_ref + y_err

    else:

        measured_min_n10_idx = np.argmin(np.where(all_description_sample != 'burial', all_n10, np.inf))
        measured_min_n10 = all_n10[measured_min_n10_idx] - all_std_dev_n10[measured_min_n10_idx]
        measured_max_n10_idx = np.argmax(np.where(all_description_sample != 'burial', all_n10, -np.inf))
        measured_max_n10 = all_n10[measured_max_n10_idx] + all_std_dev_n10[measured_max_n10_idx]
        burial_depth_min_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_min'].values[0]
        burial_depth_max_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_max'].values[0]
        final_depth_min_sample = burial_depth_min_sample
        final_depth_max_sample = burial_depth_max_sample

        if sample_id == "BV-018":
            burial_depth_min_sample = 3000
            burial_depth_max_sample = 5000

            final_depth_min_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_min'].values[0] #only for bv018
            final_depth_max_sample = df_data_samples.loc[df_data_samples['sample_names'] == sample_id]['depth_max'].values[0]

        ratio_min_idx = np.argmin(np.where(all_description_sample != 'burial', ratio_n26_n10, np.inf))
        ratio_min = ratio_n26_n10[ratio_min_idx]
        y_err_min = (ratio_n26_n10[ratio_min_idx]) * \
                    (np.sqrt((all_std_dev_n26[ratio_min_idx] / all_n26[ratio_min_idx]) ** 2
                             + (all_std_dev_n10[ratio_min_idx] / all_n10[ratio_min_idx]) ** 2))
        measured_ratio_min_c = ratio_min - y_err_min

        ratio_max_idx = np.argmax(np.where(all_description_sample != 'burial', ratio_n26_n10, -np.inf))
        ratio_max = ratio_n26_n10[ratio_max_idx]

        y_err_max = (ratio_n26_n10[ratio_max_idx]) * \
                    (np.sqrt((all_std_dev_n10[ratio_max_idx] / all_n10[ratio_max_idx]) ** 2
                             + (all_std_dev_n10[ratio_max_idx] / all_n10[ratio_max_idx]) ** 2))
        measured_ratio_max_c = ratio_max - y_err_max

    return SimpleNamespace(**locals())

def save_arguments_to_excel(var, config, output_dir=".", include_keys=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/results_data/used_parameters_{config.sample_id}_R{config.reference_sample}_D{config.density}.xlsx"

    def to_dict(obj):
        if isinstance(obj, dict):
            return obj
        return vars(obj)

    var_dict = to_dict(var)
    config_dict = to_dict(config)

    merged = {**var_dict, **config_dict}

    # Keep only the keys you want
    include_keys = include_keys or [
        "sample_id",
        "reference_sample",
        "measured_n10",
        "measured_n26",
        "stn_dev_n10",
        "stn_dev_n26",
        "burial_depth_min_sample",
        "burial_depth_max_sample",
        "final_depth_min_sample",
        "final_depth_max_sample",
        "measured_all_min_n10",
        "measured_all_max_n10",
        "measured_all_ratio_min_c",
        "measured_all_ratio_max_c",
        "density",
        "time_burial_min",
        "time_burial_max",
        "time_erosion_min",
        "time_erosion_max",
        "dep_low",
        "dep_high",
        "ero_low",
        "ero_high",
    ]

    merged = {k: v for k, v in merged.items() if k in include_keys}

    # Map raw parameter names to nicer display labels
    nice_names = {
        "sample_id": "Sample ID",
        "reference_sample": "Starting point",
        "measured_n10": "Measured N10",
        "measured_n26": "Measured N26",
        "stn_dev_n10": "N10 Std. Dev.",
        "stn_dev_n26": "N26 Std. Dev.",
        "burial_depth_min_sample": "Burial Depth Min (Sample)",
        "burial_depth_max_sample": "Burial Depth Max (Sample)",
        "final_depth_min_sample": "Final Depth Min (Sample)",
        "final_depth_max_sample": "Final Depth Max (Sample)",
        "measured_all_min_n10": "Measured N10 Min (All)",
        "measured_all_max_n10": "Measured N10 Max (All)",
        "measured_all_ratio_min_c": "Measured Ratio Min (C)",
        "measured_all_ratio_max_c": "Measured Ratio Max (C)",
        "density": "Density",
        "time_burial_min": "Burial Time Min",
        "time_burial_max": "Burial Time Max",
        "time_erosion_min": "Erosion Time Min",
        "time_erosion_max": "Erosion Time Max",
        "dep_low": "Deposition Rate Low",
        "dep_high": "Deposition Rate High",
        "ero_low": "Erosion Rate Low",
        "ero_high": "Erosion Rate High",
    }

    # Units for each raw parameter (edit to match your actual units)
    units = {
        "sample_id": "",
        "reference_sample": "",
        "measured_n10": "atoms/g",
        "measured_n26": "atoms/g",
        "stn_dev_n10": "atoms/g",
        "stn_dev_n26": "atoms/g",
        "burial_depth_min_sample": "cm",
        "burial_depth_max_sample": "cm",
        "final_depth_min_sample": "cm",
        "final_depth_max_sample": "cm",
        "measured_all_min_n10": "atoms/g",
        "measured_all_max_n10": "atoms/g",
        "measured_all_ratio_min_c": "",
        "measured_all_ratio_max_c": "",
        "density": "g/cm³",
        "time_burial_min": "yr",
        "time_burial_max": "yr",
        "time_erosion_min": "yr",
        "time_erosion_max": "yr",
        "dep_low": "cm/yr",
        "dep_high": "cm/yr",
        "ero_low": "cm/yr",
        "ero_high": "cm/yr",
    }

    # One row per parameter instead of one column per parameter
    df = pd.DataFrame(list(merged.items()), columns=["Parameter", "Value"])
    df["Unit"] = df["Parameter"].map(units).fillna("")
    df["Parameter"] = df["Parameter"].map(nice_names).fillna(df["Parameter"])
    df = df[["Parameter", "Value", "Unit"]]
    df.to_excel(filename, index=False, sheet_name="Parameters")

    print(f"Saved parameters to: {filename}")
    return filename
