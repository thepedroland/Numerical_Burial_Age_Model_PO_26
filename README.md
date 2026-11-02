<p style="line-height: 150%;">
<strong>Author:</strong> Pedro Oliveira<br>
<strong>GitHub:</strong> <a href="https://github.com/thepedroland">@thepedroland</a>

The content in this repository can be used to reproduce the plots and generate results presented in *[X]*

---
## Overview

The numerical burial model simulates the accumulation of cosmogenic nuclides for buried samples with in depth with continous production.

- **Scaling method:** LSDn
- **Production pathways modeled:**
  - **Spallation**: average scaled from scaling factor CRONUS Calc based on area latitude and altitude
  - **Negative muon capture and fast muons**: calculated as a function of depth and Rc using Balco (2008)
    - **Time-varying cutoff rigidity (Rc)**: calibrated from Mijjum et al. (2025) dataset

- The constants used can be found [here](z_AuxData_Scripts/aux_pyScripts/models_constants.py)
---
## Model Flowchart

```mermaid
flowchart LR
    RUN("RUN_num_model_burial_trajectory.py") --> INPUTS

    subgraph INPUTS ["Inputs"]
        subgraph NotChecked ["Not checked"]
          A("Initial <sup>10</sup>Be")
          TB("Total Burial Time")
          BD("Burial Depth")
          end

        subgraph Checked ["Checked"]
          FD("Final depth")
          DR("Dep. rate")
          R("Initial <sup>26</sup>Al/<sup>10</sup>Be")
          end
    end
    
    NotChecked --> B
    
    V{"INPUTS Validation"}
    V -->|Good| B
    V -->|Not good| Checked
    Checked -->|Try| V

    B("CRN accumulation \n & decay") --> E
    B("CRN accumulation \n & decay") --> |Total burial time| B

    E{"Final \n <sup>26</sup>Al/<sup>10</sup>Be and <sup>10</sup>Be<br/>within 2σ ?"}

    E -->|True| STORE
    E -->|False| STORE

    STORE[("NumSimResults/Results")]

    style RUN fill:#FAFAFA,stroke:#2E5C8A,color:#black
    style A fill:#FFEFDB,stroke:#181A00,color:#black
    style INPUTS fill: #FAF4EF,stroke:#B3B3B3,color:#black
    style Checked fill: #FAF4E0,stroke:#181A00,color:#black
    style TB fill:#FFEFDB,stroke:#181A00,color:#black
    style BD fill:#FFEFDB,stroke:#181A00,color:#black
    style FD fill:#FFEFDB,stroke:#181A00,color:#black
    style DR fill:#FFEFDB,stroke:#181A00,color:#black
    style R fill:#FFEFDB,stroke:#181A00,color:#black
    style B fill:#F3C4E0,stroke:#black,color:#black
    style STORE fill:#E9DDFD,stroke:#7D3C98,color:#BLACK
    style INPUTS rx:10px,ry:10px
    style NotChecked rx:10px,ry:10px,fill:#FAF4ES,stroke:#181A00,color:#black
    style Checked rx:10px,ry:10px
```
## Repository structure (to be updated)
````
numerical_MC_Burial_Ages_PO/
├── a_DataResults/
│ ├── ScriptsGenerateData/ 
│ │ ├── RUN_num_model_burial_trajectory.py #Main script to run simulations
│ │ └── BMI_num_model_burial_trajectory.py #Setup script to run simulations
│ └── NumSimResults/ # Numerical model output files
├── a_Figures/
│ ├── ScriptsGeneratePlots/ # Scripts used to reproduce paper figures
│ │ ├── Fig2A_Banana_Plot.py
│ │ ├── Fig2B_S5_Sec_equilibrium.py
│ │ ├── Fig3_S2toS6_Age_solutions.py
│ │ ├── Fig4_york_regression_erosion_rate_ksn_graph.py
│ │ └── FigS3_calc_Rc.py
│ └── Plots/ 
├── z_AuxData_Scripts/
│ ├── aux_pyScripts/
│ │ ├── models_constants.py # Model constants and production parameters
│ │ ├── nuclide_prod_concentration.py # Nuclide production and concentration functions - equations
│ │ ├── solution_trajectories.py # Solution trajectories plot
│ │ └── misc_functions.py # Miscellaneous functions
│ ├── aux_MatlabScripts/ #Auxiliary Matlab scripts
│ │   └── LSDn_CRN_Burial_Model.m # LSDn model production function - muons calculation
│ ├── data/ # Input and auxiliary datasets
│ └── Tables_SM/ # Excel format tables in the SupportingMateril section of the paper
├── README.md # Repository documentation
└── .gitignore # Files ignored by Git
````

---
## Software/Packages Requirements 
Versions are listed as the ones working when results were generated for this paper. Newer versions might be available, 
however, it is not guaranteed they will work smoothly.

| Package   | Version |
|-----------|---------|
| `Python ` | 3.13.12 |
| ` MATLAB ` | 2026a   |
| ` matlabengine` | 26.1    |
| `numpy`   | 2.3.5   |
| `pandas`  | 2.3.3   |
| `torch`   | 2.11.0  |
| `matplotlib` | 3.10.8  |

Note: topographic datasets were generated using MATLAB 2025a, with [TopoToolbox (v2.5)](https://github.com/wschwanghart/topotoolbox)

---
## Usage

<p style="line-height: 150%;">
<strong>Reproduce dataset:</strong> Run MC simulations and generate results using <a href="a_DataResults/ScriptsGenerateData/RUN_num_model_burial_trajectory.py">this script</a><br>
<strong>Plots</strong> Plots can be reproduced using <a href="a_Figures/ScriptsGeneratePlots">these scripts</a>

**Note**: if you want to use the banana plot but for your own data use the script in 
[_Fig2A_Banana_Plot.py_](a_Figures/ScriptsGeneratePlots/Fig2A_Banana_Plot.py) - you have to calibrate for the production rate of your study area!

---
## References

- Greg Balco, Production rate calculations for cosmic-ray-muon-produced 10Be and 26Al benchmarked against geological calibration data, Quaternary Geochronology, Volume 39,
2017, Pages 150-173, ISSN 1871-1014,https://doi.org/10.1016/j.quageo.2017.02.001. (https://www.sciencedirect.com/science/article/pii/S1871101416301649)

- Mijjum, M., Bristol, K. E., Bono, R. K., Sprain, C. J., Lifton, N., 
& Tremblay, M. M. (2025). A model framework for scaling pre‐quaternary cosmogenic nuclide production rates. Geochemistry, Geophysics, Geosystems, 26,  e2024GC012020. https://doi.org/10.1029/ 2024GC012020

- Schwanghart, W., Scherler, D. (2014): TopoToolbox 2 – MATLAB-based software for topographic analysis and modeling in Earth surface sciences. Earth Surface Dynamics, 2, 1-7. DOI: 10.5194/esurf-2-1-2014

---
## Citation
If you use any part of the scripts in this repository please cite the paper as:
- ...
