# Paper 

**Author:** Pedro Oliveira
**GitHub:** [@thepedroland](https://github.com/thepedroland)

The scripts in this repository can be used to reproduce the plots and generate results presented in *[X]*

---
## Overview

The numerical burial model simulates the accumulation of cosmogenic nuclides for buried samples with in depth continuos production.

- **Scaling method:** LSDn
- **Production pathways modeled:**
  - **Spallation**: average scaled from scaling factor CRONUS Calc based on area latitude and altitude
  - **Negative muon capture and fast muons**: calculated as a function of depth and Rc using Balco (2008)
    - **Time-varying cutoff rigidity (Rc)**: calibrated from Mijjum et al. (2025) dataset

- The constants used can be found [here](AuxDataScripts/aux_functions/models_constants.py)
---
## Software/Packages Requirements 
Versions are listed as the ones working when results were generated for this paper. Newer versions might be available, 
however, it is not guaranteed they will work smoothly.

| Package      | Version |
|--------------|---------|
| Python       | 3.13.12 |
| MATLAB       | 2026a   |
| matlabengine | 26.1    |
| numpy        | 2.3.5   |
| pandas       | 2.3.3   |
| torch        | 2.11.0  |
| matplotlib   | 3.10.8  |

---
**Reproduce dataset**

Run MC simulations and generate results using [this script](DataResults/ScriptsData/RUN_num_model_burial_trajectory.py)

**Plots**

Plots can be reproduced using [these scripts](Figures/ScriptsFig)
**Note**: if you want to use the banana plot but for your own data use the structure in 
_Fig2A_Banana_Plot.py_ - you have to calibrate for the production rate of your study area!

---
## References

- Greg Balco, Production rate calculations for cosmic-ray-muon-produced 10Be and 26Al benchmarked against geological calibration data, Quaternary Geochronology, Volume 39,
2017, Pages 150-173, ISSN 1871-1014,https://doi.org/10.1016/j.quageo.2017.02.001. (https://www.sciencedirect.com/science/article/pii/S1871101416301649)

- Mijjum, M., Bristol, K. E., Bono, R. K., Sprain, C. J., Lifton, N., 
& Tremblay, M. M. (2025). A model framework for scaling pre‐quaternary cosmogenic nuclide production rates. Geochemistry, Geophysics, Geosystems, 26,  e2024GC012020. https://doi.org/10.1029/ 2024GC012020
---
## Citation
If you use any part of the scripts in this repository please cite the paper as:
- ...
