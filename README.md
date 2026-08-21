# Paper 

**Author:** Pedro Oliveira
**GitHub:** [@thepedroland](https://github.com/thepedroland)

This repository has the numerical burial age model and 
can be used to generate results presented in the paper *[X]*
---
## Overview

This repository simulates the accumulation of cosmogenic nuclides over time for buried samples.
It couples cosmogenic nuclide production by spalattion, negative muon capture and fast muon throughout the 
entire depth

- **Scaling method:** LSDn
- **Production pathways modeled:**
  - **Spallation**: average scaled from scaling factor CRONUS Calc based on area latitude and altitude
  - **Negative muon capture and fast muons**: calculated as a function of depth and Rc using Balco (2017)
    - **Time-varying cutoff rigidity (Rc): calibrated from Mijjum et al. (2025)
      - Rc variation from 0-35Myr saved in /support/data/Rc_results.csv
- Used constants can be found in support/aux_functions/models_constants.py
---
## Software/ Package Requirements 
Versions are listed as the ones working when results were generated for this paper. Newer versions might be available, 
however, it is not guaranteed they will work smoothly.

| Package      | Version |
|--------------|---------|
| Python       | 3.13.12 |
| MATLAB       | 26A     |
| matlabengine | 26.1    |
| numpy        | 2.3.5   |
| pandas       | 2.3.3   |
| torch        | 2.11.0  |
| matplotlib   | 3.10.8  |

---
## Workflow

To reproduce the figures use and data use:

***Reproduce dataset**
Run MC simulations and generate results using:
Run _RUN_num_model_burial_trajectory.py_ 
 - Files pattern
  ..."_[Sample ID]_R[Starting reference]_D[density]..."

***Plot figures**
Figures can be plotted using _generate_figures/scripts_
Note: if you want to use this banana plot but for your own data use the structure in 
_Fig2A_Banana_Plot.py_ - you have to calibrate for the production rate of your study area!

Cosmogenic nuclide data and model parameters used in this work can be found as 
excel files in _**generate_figures/tables**_

## References

- Greg Balco, Production rate calculations for cosmic-ray-muon-produced 10Be and 26Al benchmarked against geological calibration data, Quaternary Geochronology, Volume 39,
2017, Pages 150-173, ISSN 1871-1014,https://doi.org/10.1016/j.quageo.2017.02.001. (https://www.sciencedirect.com/science/article/pii/S1871101416301649)

- Mijjum, M., Bristol, K. E., Bono, R. K., Sprain, C. J., Lifton, N., 
& Tremblay, M. M. (2025). A model framework for scaling pre‐quaternary cosmogenic nuclide production rates. Geochemistry, Geophysics, Geosystems, 26,  e2024GC012020. https://doi.org/10.1029/ 2024GC012020

## Citation
If you use any part of the scripts in this repository please cite:
- ...
